import datetime
import httplib2
from googleapiclient import discovery
from collections import namedtuple

from infounibot.google_api import get_credentials


class CalendarReader(object):
    def __init__(self):
        pass

    def load_events(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='bdd6543s67uo8ojq7nds3r0a14@group.calendar.google.com', timeMin=now, maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        output = []

        for event in events:
            name = event.get('summary')
            place = event.get('location')
            start = event.get('start')['dateTime']
            end = event.get('end')['dateTime']
            description = event.get('description')
            calendar_event = CalendarEvent(name=name, place=place, start=start,
                                           end=end, description=description)
            output.append(calendar_event)

        return output


class CalendarEvent(namedtuple("Event", ["name", "place", "start", "end", "description"])):
    def message(self):
        return self.name