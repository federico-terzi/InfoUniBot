from __future__ import print_function
import datetime, time
import dateutil.parser
import httplib2
from googleapiclient import discovery
from collections import namedtuple

from infounibot.google_api import get_credentials


class CalendarReader(object):
    def __init__(self):
        self.events = []

    def has_events(self):
        """
        If there are events it returns True.
        """
        return len(self.events) > 0

    def load_events(self):
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

            # Convert the start date to an int timestamp
            start_string = event.get('start')['dateTime']
            start = -1  # If there was an error, this remains to -1
            if start_string:
                start = time.mktime(dateutil.parser.parse(start_string).timetuple())

            # Convert the end date to an int timestamp
            end_string = event.get('end')['dateTime']
            end = -1  # If there was an error, this remains to -1
            if end_string:
                end = time.mktime(dateutil.parser.parse(end_string).timetuple())

            # Create the calendar event
            calendar_event = CalendarEvent(name=name, place=place, start=start,
                                           end=end, description=description)

            # Add the event to the final list
            output.append(calendar_event)

        self.events = output

    def get_upcoming_events(self, remaining_time=86400):
        """
        Return a list of the events that will occur within the specified amount of seconds.
        :param remaining_time: the amount of seconds
        :return: a list of CalendarEvent
        """
        output = []
        now_timestamp = time.mktime(datetime.datetime.now().timetuple())

        for event in self.events:
            # Calculate the amount of seconds that remain until the event
            difference = event.start - now_timestamp

            # If the difference is less than the remaining time, add to the list
            if difference < remaining_time:
                output.append(event)

        return output




class CalendarEvent(namedtuple("Event", ["name", "place", "start", "end", "description"])):
    def message(self):
        return "{name}\n{place}\n{description}".format(name=self.name, place=self.place,
                                                       description=self.description)