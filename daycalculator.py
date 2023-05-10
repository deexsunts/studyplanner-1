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

# deadline semester 8
target_date = dt.date(2023, 6, 21)
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