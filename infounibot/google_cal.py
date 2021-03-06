# coding=utf-8
from __future__ import print_function
import calendar
import datetime, time
import hashlib
import pytz
import dateutil.parser
import httplib2
import json
from googleapiclient import discovery
from collections import namedtuple
import os

from infounibot.google_api import get_credentials


class CalendarReader(object):
    def __init__(self, avoid_caching=False):
        self.events = []

        self.MAX_CACHE_TIME = 3600  # One hour

        # Genero il percorso del file
        home_dir = os.path.expanduser('~')
        self.cache_path = os.path.join(home_dir, 'events.txt')

        self.avoid_caching = avoid_caching

    def has_events(self):
        """
        If there are events it returns True.
        """
        return len(self.events) > 0

    def save_events_to_cache(self):
        timestamp = int(time.time())
        output = {
            "timestamp": timestamp,
            "events": map(lambda x: x.get_event_dict(), self.events)
        }
        # Save the file
        with open(self.cache_path, "w") as f:
            json.dump(output, f)

    def load_events_from_cache(self):
        # Open the file
        try:
            with open(self.cache_path, "r") as f:
                json_input = json.load(f)
                json_events = json_input["events"]
                self.events = map(lambda x: CalendarEvent.from_dict(x), json_events)
                return json_input["timestamp"]
        except IOError as e:
            print(e)
            return 0

    def reset_event_cache(self):
        # Delete cache file
        os.remove(self.cache_path)

    def load_events(self):
        now = int(time.time())
        cache_timestamp = self.load_events_from_cache()

        # Check if should request from google api
        if self.avoid_caching or (now - cache_timestamp) > self.MAX_CACHE_TIME:
            self.request_events()
            print("Loaded from Google API.")
        else:
            print("Loaded from cache.")

    def request_events(self):
        # Get the credentials and login into google
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # Get the upcoming events
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        eventsResult = service.events().list(
            calendarId='bdd6543s67uo8ojq7nds3r0a14@group.calendar.google.com', timeMin=now, maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        output = []

        for event in events:
            # Get the event fields
            name = event.get('summary')
            place = event.get('location')
            description = event.get('description')
            event_id = event.get('id')

            # Convert the start date to an int timestamp
            start_string = event.get('start')['dateTime']
            start = -1  # If there was an error, this remains to -1
            if start_string:
                start = calendar.timegm(dateutil.parser.parse(start_string).timetuple())

            # Convert the end date to an int timestamp
            end_string = event.get('end')['dateTime']
            end = -1  # If there was an error, this remains to -1
            if end_string:
                end = calendar.timegm(dateutil.parser.parse(end_string).timetuple())

            # Create the calendar event
            calendar_event = CalendarEvent(name=name, place=place, start=start,
                                           end=end, description=description,
                                           id=event_id)

            # Add the event to the final list
            output.append(calendar_event)

        # Sort the events in a chronological order
        output.sort(key=lambda x: x.start)

        self.events = output

        # Save the events to cache
        self.save_events_to_cache()

    def get_upcoming_events(self, remaining_time=86400, min_difference=0):
        """
        Return a list of the events that will occur within the specified amount of seconds.
        :param remaining_time: the amount of seconds
        :param min_difference: minimum amount of seconds
        :return: a list of CalendarEvent
        """
        output = []
        now_timestamp = datetime.datetime.now()

        for event in self.events:
            # Calculate the amount of seconds that remain until the event
            difference = (event.get_start_date() - now_timestamp).total_seconds()

            # If this is true, the event will be added
            should_add = True

            # If the difference is more than the remaining time, don't add to the list
            if difference > remaining_time:
                should_add = False

            # If a min difference has been specified, exclude the events nearer than that
            if min_difference > 0 and difference < min_difference:
                should_add = False

            # Add to the list
            if should_add:
                output.append(event)

        return output

    def get_tomorrow_events(self):
        """
        Get the events of tomorrow
        """
        output = []
        now = datetime.datetime.utcnow()
        today = (now.year-1)*365 + now.timetuple().tm_yday

        for event in self.events:
            event_date = event.get_start_date()
            event_day = (event_date.year-1)*365 + event_date.timetuple().tm_yday

            # If this is true, the event will be added
            should_add = True

            if (today+1) != event_day:
                should_add = False

            # Add to the list
            if should_add:
                output.append(event)

        return output

    def get_today_events(self):
        """
        Get the today
        """
        output = []
        now = datetime.datetime.utcnow()
        today = (now.year - 1) * 365 + now.timetuple().tm_yday

        for event in self.events:
            event_date = event.get_start_date()
            event_day = (event_date.year - 1) * 365 + event_date.timetuple().tm_yday

            # If this is true, the event will be added
            should_add = True

            if today != event_day:
                should_add = False

            # Add to the list
            if should_add:
                output.append(event)

        return output

    def get_week_events(self):
        """
        Get the events within 7 days
        """
        return self.get_upcoming_events(remaining_time=86400*7)

    def get_tomorrow_message(self):
        """
        Return a formatted message with the tomorrow events
        and the message ID
        """
        upcoming_events = self.get_tomorrow_events()

        if len(upcoming_events) == 0:
            return "Nessun evento per domani.", None

        event_hash = self.calculate_events_hash(upcoming_events)

        messages = []

        for event in upcoming_events:
            message = event.message()
            messages.append(message)

        return '\n\n'.join(messages), event_hash

    def get_tomorrow_full_message(self):
        """
        Return the message with a bit of header
        """
        message, event_id = self.get_tomorrow_message()
        final_message = """
Domani avrai queste lezioni:

{lezioni}

Spero di essere stato utile 😎
        """.format(lezioni=message)
        return final_message, event_id

    def get_today_message(self):
        """
        Return a formatted message with the today events
        and the message ID
        """
        upcoming_events = self.get_today_events()

        if len(upcoming_events) == 0:
            return "Nessun evento per oggi.", None

        event_hash = self.calculate_events_hash(upcoming_events)

        messages = []

        for event in upcoming_events:
            message = event.message()
            messages.append(message)

        return '\n\n'.join(messages), event_hash

    def get_today_full_message(self):
            """
            Return the message with a bit of header
            """
            message, event_id = self.get_today_message()
            final_message = """
Oggi ti rimangono queste lezioni:

{lezioni}

PS: è un pò tardi per chiederlo 😂
            """.format(lezioni=message)
            return final_message, event_id

    @staticmethod
    def calculate_events_hash(events):
        ids = map(lambda x: x.id, events)
        total_id = "".join(ids)
        m = hashlib.md5()
        m.update(total_id.encode('utf-8'))
        return m.hexdigest()


class CalendarEvent(namedtuple("Event", ["name", "place", "start", "end", "description", "id"])):
    def message(self):
        event_time = CalendarEvent.get_formatted_time(self.get_start_date(), self.get_end_date())

        return "*{name}*\n_{event_time}_\n{place}{description}".format(name=self.name,
                                                                           place=self.if_present(self.place),
                                                                           event_time=event_time,
                                                                           description=self.if_present(self.description))

    def get_start_date(self):
        if self.start > 0:
            date = datetime.datetime.utcfromtimestamp(self.start)
            return date
        else:
            return None

    def get_end_date(self):
        if self.end > 0:
            date = datetime.datetime.utcfromtimestamp(self.end)
            return date
        else:
            return None

    def get_event_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start": self.start,
            "end": self.end,
            "description": self.description,
            "id": self.id
        }

    @staticmethod
    def from_dict(dict):
        return CalendarEvent(name=dict['name'], place=dict['place'], start=dict['start'],
                             end=dict['end'], description=dict['description'],
                             id=dict['id'])

    @staticmethod
    def get_formatted_time(start_date, end_date):
        if not start_date or not end_date:
            return ""
        else:
            return "{start_hour} - {end_hour}".format(start_hour=start_date.strftime("%H:%M"),
                                                      end_hour=end_date.strftime("%H:%M"),
                                                      )

    @staticmethod
    def if_present(string):
        if string is None:
            return ""
        else:
            return "\n" + string
