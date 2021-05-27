import requests
import os
from datetime import datetime
from enum import Enum

if not os.path.exists("token.txt"):
    print("Error: token.txt not found, creating now. Place Calendly API key in file.")
    open("token.txt", 'w').close()
    input()
    raise SystemExit

if os.stat("token.txt").st_size == 0:
    print("Error: token.txt is empty. Place Calendly API key in file.")
    input()
    raise SystemExit

BASE_URL = 'https://api.calendly.com'

TOKEN = open('token.txt', 'r').read()
USER = requests.get(f"{BASE_URL}/users/me",
                    headers={'authorization': f"Bearer {TOKEN}"}).json()
USER_URI = USER['resource']['uri']


class Status(Enum):
    ACTIVE = 'active'
    CANCELED = 'canceled'


class SortType(Enum):
    ASCDENDING = 'asc'
    DESCENDING = 'desc'


def get_events(start_date: str, end_date: str, sort_type=SortType.ASCDENDING) -> list:
    '''
    Returns list of Calendly events of uri from start_date to end_date in sort_type order
    '''
    sort = f"start_time:{sort_type.value}"

    params = {
        "user": USER_URI,
        "sort": sort,
        "min_start_time": start_date,
        "max_start_time": end_date,
        "count": 100
    }

    events = requests.get(
        f"{BASE_URL}/scheduled_events",
        params=params,
        headers={'authorization': f"Bearer {TOKEN}"}
    ).json()

    return events['collection']


def get_datetime_from_calendly_str(date: str) -> datetime:
    '''
    Returns datetime of Calendly date
    '''
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date


def get_active_events(events: list) -> list:
    '''
    Returns list of Calendly events where the "status" keys value is marked as "active"
    '''
    active_events = []

    for event in events:
        if event['status'] == Status.ACTIVE.value:
            active_events.append(event)

    return active_events


def get_event_data(event: list) -> list:
    lesson = event['name']

    start_time = get_datetime_from_calendly_str(event['start_time'])
    end_time = get_datetime_from_calendly_str(event['end_time'])
    duration = round((end_time - start_time).total_seconds() / 60 / 60, 2)

    reason = "Taught Students" if lesson != 'Professional Development' else "Taught Teachers"
    lesson_date = start_time.date().isoformat()
    return [lesson, duration, reason, lesson_date]


def create_dataframe_data(active_events: list, rate, hst) -> list:
    '''
    Returns list of all active_events in "lesson, duration, reason, lesson_date"
    with hours, subtotal, HST rate and total in a format for the pandas dataframe
    '''
    data = []
    for event in active_events:
        data.append(get_event_data(event))

    num_of_events = len(active_events)

    data.append([""])
    data.append(["Hours", f"=SUM(B2:B{num_of_events+1})"])
    data.append(["Subtotal", f"=MULTIPLY(B{num_of_events+3}, {rate})"])
    data.append(["HST", f"=MULTIPLY(B{num_of_events+4}, {hst})"])
    data.append([""])
    data.append(["TOTAL: ", f"=SUM(B{num_of_events+4}, B{num_of_events+5})"])

    return data
