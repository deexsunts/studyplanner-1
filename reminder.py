import json
import datetime
from clearterminal import clear_terminal

REMINDER_FILE = "reminders.json"

def load_reminders():
    try: 
        with open(REMINDER_FILE, 'r') as f:
            reminders = [json.loads(reminder) for reminder in f.readlines()]
    except FileNotFoundError:
        reminders = []
        save_reminders(reminders)
    return reminders


def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        for reminder in reminders:
            json.dump(reminder, f)
            f.write("\n")

def update_reminder_index():
    reminders = load_reminders()
    for i, reminder in enumerate(reminders):
        reminder['index'] = i + 1
    save_reminders(reminders)

def add_reminder():
    update_reminder_index()
    study_name = input("Enter study name: ")
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    reminder_dates = [(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=12)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=22)).strftime("%d-%m-%Y")]
    reminders = load_reminders()
    index = len(reminders) + 1
    reminder = {
        "index": index,
        "study_name": study_name,
        "current_date": current_date,
        "reminder_dates": reminder_dates
    }
    reminders.append(reminder)
    save_reminders(reminders)
    clear_terminal()
    print("Reminder added successfully!")

def remove_reminder():
    clear_terminal()
    update_reminder_index()
    reminders = load_reminders()
    print("Reminders:\n")
    for reminder in reminders:
        print(f"{reminder['index']}. {reminder['study_name']}")
    index = input("Enter index of the study to remove: ")
    index = int(index)
    reminders = [reminder for reminder in reminders if reminder['index'] != index]
    save_reminders(reminders)
    print("Reminder removed successfully!")

def flush_reminders():
    confirm = input("Are you sure you want to delete all reminders? (y/n) ")
    if confirm.lower() == "y":
        with open(REMINDER_FILE, 'w') as f:
            f.write("")
        clear_terminal()
        print("\nAll reminders removed successfully!")
    else:
        clear_terminal()
        print("cancelled.\n")

def show_reminders():
    update_reminder_index()
    reminders = load_reminders()
    if len(reminders) == 0:
        print("\n\nreminders empty.")
    today = datetime.date.today()
    date_groups = {}
    for reminder in reminders:
        for date_str in reminder['reminder_dates']:
            date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
            if date < today:
                date_group_key = date_str
            elif date == today:
                date_group_key = 'Today'
            else:
                days_left = (date - today).days
                date_group_key = f"{days_left} day{'s' if days_left > 1 else ''} left"
            if date not in date_groups:
                date_groups[date] = []
            date_groups[date].append((reminder['index'], reminder['study_name']))
    sorted_dates = sorted(date_groups.keys())
    for date in sorted_dates:
        date_group_key = date.strftime('%d-%m-%Y')
        if date < today:
            date_group_header = date_group_key
        elif date == today:
            date_group_header = 'Today'
        else:
            days_left = (date - today).days
            date_group_header = f"{days_left} day{'s' if days_left > 1 else ''} left"
        print(f"\nDate: {date_group_header}")
        reminders = date_groups[date]
        for reminder in reminders:
            print(f"{reminder[0]}. {reminder[1]}")
        

def modify_reminder():
    update_reminder_index()
    reminders = load_reminders()
    print("Reminders:\n")
    for reminder in reminders:
        print(f"{reminder['index']}. {reminder['study_name']} - {reminder['reminder_dates']}")
    index = input("Enter index of the study to modify: ")
    index = int(index)
    for reminder in reminders:
        if reminder['index'] == index:
            pages = input("Enter number of pages to add (use negative number to remove pages): ")
            pages = int(pages)
            reminder['pages'] += pages
    save_reminders(reminders)
    print("Reminder modified successfully!")

clear_terminal()

def main():
    while True:
        print("\n||spaced repetition||\n\nMenu:")
        print("a. Add reminder")
        print("r. Remove reminder")
        print("f. Flush reminders")
        print("s. Show reminders")
        print("v. Save reminders to file")
        print("l. Load reminders from file")
        print("q. Quit")
        choice = input("\nEnter your choice: ")
        if choice == 'a':
            clear_terminal()
            add_reminder()
        elif choice == 'r':
            clear_terminal()
            remove_reminder()
        elif choice == 'f':
            clear_terminal()
            flush_reminders()
        elif choice == 's':
            clear_terminal()
            show_reminders()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'v':
            clear_terminal()
            reminders = load_reminders()
            save_reminders(reminders)
        elif choice == 'l':
            clear_terminal()
            reminders = load_reminders()
            print(f"{len(reminders)} reminders loaded from file")
        elif choice == 'q':
            clear_terminal()
            break
        else:
            print("Invalid choice, please try again")

if __name__ == '__main__':
    main()
