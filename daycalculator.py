import json
import datetime as dt

hours = {
    "Saturday": 12,
    "Sunday":  9,
                    #2-9
    "Monday": 9,
                     #4-9 -2
    "Tuesday": 6,
                     #6-17 +1 at uni
    "Wednesday": 11,
                     #4-9
    "Thursday":12,
    "Friday": 12
}

sum_values = sum([v for v in hours.values() if isinstance(v, int)])

def save_date_to_json():
    # prompt user for date
    while True:
        date = input("Enter the date (today/tomorrow/+n/DD-MM-YY): ")
        if date == "today":
            start = dt.datetime.now().strftime("%Y,%m,%d")
            break
        elif date == "tomorrow":
            start = (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y,%m,%d")
            break
        elif date.startswith("+"):
            days = int(date[1:])
            start = (dt.datetime.now() + dt.timedelta(days=days)).strftime("%Y,%m,%d")
            break
        else:
            try:
                start = dt.datetime.strptime(date, "%d-%m-%Y").strftime("%Y,%m,%d")
                break
            except ValueError:
                print("Invalid date format. Try again.")

    # create dictionary to store date
    data = {"date": start}

    # serialize dictionary to JSON and write to file
    with open("date.json", "w") as f:
        json.dump(data, f)


def read_date_from_json():
    try:
        # read data from JSON file
        with open("date.json", "r") as f:
            data = json.load(f)
        # extract date from data dictionary
        date_str = data["date"]
        date = dt.datetime.strptime(date_str, "%Y,%m,%d").date()
        return date
    except FileNotFoundError:
        # if file does not exist, prompt user for date and save to file
        save_date_to_json()

# def read_date_from_json():
#     try:
#         # read JSON data from file
#         with open("date.json", "r") as f:
#             data = json.load(f)
#             return dt.datetime.strptime(data["date"], "%d-%m-%Y").date()
#     except FileNotFoundError:
#         # if file does not exist, save target date to file
#         save_date_to_json()
#         return target_date
# start = target_date.strftime("%d-%m-%Y")

# deadline semester 8
target_date = read_date_from_json()
date = dt.date.today()
delta = target_date - date
days = delta.days

today = dt.datetime.today()
today1 = today + dt.timedelta(days=0)
today_index = today1.weekday()
weektoday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][today_index]
todayhours = hours[weektoday]


now = dt.datetime.now()
end_of_day = now.replace(hour=22, minute=0, second=0, microsecond=0)
time_left = end_of_day - now

total_seconds = int(time_left.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60