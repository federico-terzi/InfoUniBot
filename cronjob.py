from infounibot.google_cal import CalendarReader

calendar = CalendarReader()

print(calendar.load_events())