import json
import os
import calendly
import datetime

start_date = input("Enter min date (YYYY-MM-DD): ")
end_date = input("Enter max date: (YYYY-MM-DD): ")

start_date = datetime.date.fromisoformat(start_date)
end_date = datetime.date.fromisoformat(end_date)
delta = datetime.timedelta(days=7)

data = {}
while(start_date <= end_date):
    week_number = start_date.isocalendar()[1]
    active_events = calendly.get_active_events(
        calendly.get_events(start_date, start_date + delta))

    weekly_events = []
    for event in active_events:
        event_data = calendly.get_event_data(event)

        weekly_events.append({
            "lesson": event_data[0],
            "duration": event_data[1],
            "reason": event_data[2],
            "date": event_data[3]
        })

    data[week_number] = weekly_events

    start_date += delta

path = os.getcwd() + "/output"

if not os.path.exists(path):
    os.mkdir(path)

with open('output/class_data.json', 'w') as outfile:
    json.dump(data, outfile)
