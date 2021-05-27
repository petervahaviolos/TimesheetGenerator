import json
import os


def total_number_of_classes(data: list) -> float:
    num_of_classes = 0.0
    for week in data:
        num_of_classes += len(data[week])
    return num_of_classes


def total_time(data: list) -> float:
    time = 0.0
    for week in data:
        for lesson in data[week]:
            time += float(lesson['duration'])
    return round(time, 2)


def total_pay(data: list, rate: float) -> float:
    return total_time(data) * rate


def total_pay_with_hst(data: list, rate: float) -> float:
    total = total_pay(data, rate)
    return total + total * 0.13


def average_classes_week(data: list) -> float:
    return total_number_of_classes(data) / len(data)


def average_time_week(data: list) -> float:
    return round(total_time(data) / len(data))


def average_pay_week(data: list, rate: float) -> float:
    return total_pay(data, rate) / len(data)


def average_classes_day(data: list) -> float:
    return average_classes_week(data) / 5.0


def average_time_day(data: list) -> float:
    return average_time_week(data) / 5.0


def average_pay_day(data: list, rate: float) -> float:
    return average_pay_week(data, rate) / 5.0


def average_classes_year(data: list) -> float:
    return average_classes_week(data) * 52


def average_time_year(data: list) -> float:
    return average_time_week(data) * 52


def average_pay_year(data: list, rate: float) -> float:
    return average_pay_week(data, rate) * 52


def data_to_json(data: list, rate: float) -> str:
    json_data = {
        "totals": {
            "classes": total_number_of_classes(data),
            "hours": total_time(data),
            "pay": total_pay(data, rate)
        },
        "weekly_averages": {
            "classes": average_classes_week(data),
            "hours": average_time_week(data),
            "pay": average_pay_week(data, rate)
        },
        "daily_averages": {
            "classes": average_classes_day(data),
            "hours:": average_classes_week(data),
            "pay": average_pay_day(data, rate)
        },
        "yearly_averages": {
            "classes": average_classes_year(data),
            "hours": average_classes_year(data),
            "pay": average_pay_year(data, rate)
        }
    }

    return json_data


if __name__ == '__main__':
    path = os.getcwd() + "/output"
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(path + '/class_data.json'):
        print("Error: Can't find class_data.json, run the Class Data Generator first.")
    else:
        rate = float(input('Enter hourly rate: '))

        with open('output\class_data.json') as f:
            data = json.load(f)

        with open('output\stats.json', 'w') as f:
            json.dump(data_to_json(data, rate), f)

        print("Stats successfully created")
