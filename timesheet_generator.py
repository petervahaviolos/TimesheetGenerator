from datetime import timedelta
import pandas as pd
import json
import os
import calendly


def generate_timesheet(active_events: list, rate: float, hst: float) -> None:
    timesheet = pd.DataFrame(
        calendly.create_dataframe_data(active_events, rate, hst),
        columns=[
            'What you worked on',
            'How much time it took',
            'Why you worked on it, how did it help CreationCamp move toward our goals?',
            'Date'
        ]
    )
    timesheet.to_csv('output/timesheet.csv', index=False)


if __name__ == '__main__':
    RATE = 0
    HST = 0

    if not os.path.exists("user.json"):
        print("First time setup")
        RATE = float(input("Enter hourly rate: "))
        HST = 0.13 if input("Include 13% HST? (yes/no): ") == "yes" else 0
        print("")
        with open("user.json", 'w') as f:
            json.dump({
                "rate": RATE,
                "hst": HST
            }, f)
    else:
        with open("user.json") as f:
            user_data = json.load(f)

        RATE = user_data["rate"]
        HST = user_data["hst"]

    start_date = input("Enter min date (YYYY-MM-DD): ")
    end_date = input("Enter max date: (YYYY-MM-DD): ")
    end_date += timedelta(days=1)
    events = calendly.get_events(start_date, end_date)
    active_events = calendly.get_active_events(events)

    path = os.getcwd() + "/output"

    if not os.path.exists(path):
        os.mkdir(path)

    generate_timesheet(active_events, RATE, HST)
    print("Timesheet generated successfully")
