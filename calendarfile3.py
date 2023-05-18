import json
from datetime import datetime, timedelta
from clearterminal import clear_terminal

# Function to flush the database
def flush_database():
    clear_terminal()
    confirmation = input("Are you sure you want to flush the calendar database? (yes/no): ")
    if confirmation.lower() == "yes":
        with open('calendar.json', 'w') as file:
            file.write("{}")
        clear_terminal()
        print("Calendar database flushed successfully!")
    else:
        print("Database flushing aborted.")

# Function to load calendar data from JSON file
def load_calendar():
    try:
        with open('calendar.json', 'r') as file:
            calendar_data = json.load(file)
    except FileNotFoundError:
        calendar_data = {}
    return calendar_data

# Function to save calendar data to JSON file
def save_calendar(calendar_data):
    with open('calendar.json', 'w') as file:
        json.dump(calendar_data, file)

# Function to add an event
def add_event():
    clear_terminal()
    name = input("\nEnter event: ")
    while True:
        event_date = input("Enter date (today/tomorrow/+n/DD-MM-YY): ")
        if event_date == 'today':
            start = datetime.now().strftime('%d-%m-%Y')
            break
        elif event_date == 'tomorrow':
            start = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
            break
        elif event_date.startswith('+'):
            days = int(event_date[1:])
            start = (datetime.now() + timedelta(days=days)).strftime('%d-%m-%Y')
            break
        else:
            try:
                start = datetime.strptime(event_date, '%d-%m-%Y').strftime('%d-%m-%Y')
                break
            except ValueError:
                print("Invalid date format. Try again.")

    calendar_data = load_calendar()
    if start in calendar_data:
        calendar_data[start].append(name)  # Add the event to the existing date key
    else:
        calendar_data[start] = [name]  # Create a new date key and add the event
    save_calendar(calendar_data)
    clear_terminal()
    print("Event added successfully!")

# Function to remove an event
def remove_event():
    calendar_data = load_calendar()
    sorted_dates = sorted(calendar_data.keys(), key=lambda x: datetime.strptime(x.split('_')[0], '%d-%m-%Y'))
    clear_terminal()
    print("\nSelect an event to remove:")
    for i, date in enumerate(sorted_dates):
        events = calendar_data[date]
        for j, event in enumerate(events):
            print(f"{i + 1}.{j + 1} {date}: {event}")
    while True:
        try:
            choice = input("Enter the event number (e.g., 1.2): ")
            date_choice, event_choice = map(int, choice.split('.'))
            if 1 <= date_choice <= len(sorted_dates) and 1 <= event_choice <= len(calendar_data[sorted_dates[date_choice - 1]]):
                break
            else:
                print("Invalid choice. Try again.")
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")

    selected_date = sorted_dates[date_choice - 1]
    selected_event = calendar_data[selected_date][event_choice - 1]
    print(f"\nRemoving event '{selected_event}' on {selected_date}")
    calendar_data[selected_date].remove(selected_event)
    if not calendar_data[selected_date]:
        del calendar_data[selected_date]
    save_calendar(calendar_data)
    clear_terminal()
    print("Event removed successfully!")

# Function to display the calendar
def display_calendar(start_date):
    clear_terminal()
    calendar_data = load_calendar()

    current_month = datetime.strptime(start_date, '%d-%m-%Y').strftime('%B')  # Track current month

    while True:
        current_date = datetime.strptime(start_date, '%d-%m-%Y')

        # Determine the day of the week for the current date
        current_weekday = current_date.weekday()
        days_offset = (current_weekday - 5) % 7  # Calculate the number of days to Saturday
        current_date -= timedelta(days=days_offset)

        week_dates = []
        for _ in range(4):
            week_dates_row = []
            for _ in range(7):
                week_dates_row.append(current_date.strftime('%d-%m-%Y'))
                current_date += timedelta(days=1)
            week_dates.append(week_dates_row)

        today = datetime.now().strftime('%d-%m-%Y')  # Get today's date
        today_week_number = datetime.strptime(today, '%d-%m-%Y').isocalendar()[1]  # Get the week number for today's date

        print("\n-------------------------")
        if current_month == current_date.strftime('%B'):
            print(f"{'':<6} {current_month}")  # Print both months
        else:
            print(f"{'':<6} {current_month}-{current_date.strftime('%B')}")  # Print both months
        print("-------------------------")
        print("  +----------+----------+----------+----------+----------+----------+----------+")
        print("  | Saturday | Sunday   | Monday   | Tuesday  | Wednesday| Thursday | Friday   |")
        print("  +----------+----------+----------+----------+----------+----------+----------+")

        for week in week_dates:
            rows = [""] * 4
            for date in week:
                day = datetime.strptime(date, '%d-%m-%Y').strftime('%d')
                events_on_date = calendar_data.get(date, [])  # Get events for the current date

                event_strings = [f"{event}" for event in events_on_date]
                events_str = "\n".join(event_strings)
                
                date_display = f"{day}{'*' if date == today else ''}"  # Add a star if it's today's date
                rows[0] += "| " + date_display.center(8) + " "
                rows[1] += "+----------"
                rows[2] += "| " + events_str.center(8) + " "
                rows[3] += "+----------"
            
            # Add empty spaces at the start of each row
            rows = ["  " + row for row in rows]

            for i, row in enumerate(rows):
                if i % 2 == 0:
                    print(row + "|")
                else:
                    print(row + "+")

        print(f"today's Week of the year: {today_week_number}")
        direction = input("\nEnter direction to change week (l/r) or 'q' to quit: ")
        if direction == 'q':
            clear_terminal()
            break
        elif direction == 'l':
            clear_terminal()
            start_date = switch_weeks(start_date, -4)
            current_month = datetime.strptime(start_date, '%d-%m-%Y').strftime('%B')  # Update current month
        elif direction == 'r':
            clear_terminal()
            start_date = switch_weeks(start_date, 4)
            current_month = datetime.strptime(start_date, '%d-%m-%Y').strftime('%B')  # Update current month
        else:
            clear_terminal()
            print("Invalid direction.")
            break


def switch_weeks(current_date, weeks_offset):
    current_date = datetime.strptime(current_date, '%d-%m-%Y')
    new_date = current_date + timedelta(weeks=weeks_offset)
    return new_date.strftime('%d-%m-%Y')


def remove_passed_events():
    calendar_data = load_calendar()

    current_date = datetime.now().strftime('%d-%m-%Y')
    updated_events = {}

    for date, events in calendar_data.items():
        if date.split('_')[0] >= current_date:
            updated_events[date] = events

    save_calendar(updated_events)


def show_closest_events():
    clear_terminal()
    calendar_data = load_calendar()
    events = []

    for date, event_list in calendar_data.items():
        for event in event_list:
            events.append({
                'start': date,
                'summary': event
            })

    current_date = datetime.now().strftime('%d-%m-%Y')

    # Get the events closest to today
    closest_events = []
    for event in events:
        event_date = event['start'].split('_')[0]
        if event_date >= current_date:
            closest_events.append((event_date, event['summary']))
            if len(closest_events) >= 5:
                break

    if closest_events:
        closest_events = sorted(closest_events, key=lambda x: x[0])
        print("Closest Events:")
        for event in closest_events[:5]:
            event_date = datetime.strptime(event[0], '%d-%m-%Y')
            days_left = (event_date - datetime.now()).days + 1
            if days_left == 0:
                print(f"- {event[1]}\t\t(today)")
            else:
                print(f"- {event[1]}\t\t({days_left} days left)")
        input("Press Enter to continue...")
    else:
        print("No upcoming events found.")
        input("\nPress Enter to continue...")
        clear_terminal()


# Main menu
def main():
    clear_terminal()
    remove_passed_events()
    current_date = datetime.now().strftime('%d-%m-%Y')
    while True:
        print("\n||Calendar||\n\nMenu:")
        print("a. Add Event")
        print("r. Remove Event")
        print("s. Show Calendar")
        print("c. Show close events")
        print("f. Flush Calendar")
        print("q. Exit")
        choice = input("\nEnter your choice: ")

        if choice == 'a':
            add_event()
        elif choice == 'r':
            remove_event()
        elif choice == 's':
            display_calendar(current_date)
        elif choice == 'f':
            flush_database()
        elif choice == 'c':
            show_closest_events()
            clear_terminal()
            clear_terminal()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()
            print("Invalid choice. Try again.")

# Start the program
if __name__ == '__main__':
    main()
