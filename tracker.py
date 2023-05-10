import json
import datetime
import os
from clearterminal import clear_terminal

# Load data from JSON file
try:
    with open("study_tracker.json", "r") as f:
        study_data = json.load(f)
except FileNotFoundError:
    study_data = {}

# Define function to save data to JSON file
def save_data():
    with open("study_tracker.json", "w") as f:
        json.dump(study_data, f)

# Define function to add a new study
def add_study():
    subject = input("Enter the subject you studied: ")
    time_spent = input("Enter the time you spent studying (in minutes): ")
    date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%d-%m-%Y")

    if date not in study_data:
        study_data[date] = []

    study_data[date].append({"subject": subject, "time_spent": time_spent})
    print("Study added successfully.\n")
    input("\npress any key to continue...")

# Define function to browse studies on a particular day
def browse_day():
    clear_terminal()
    date = input("Enter the date you want to browse (today/%d-%m-%Y/-n): ")

    if date == 'today':
        date = datetime.datetime.now().strftime('%d-%m-%Y')
    elif date.startswith('-'):
        days = int(date[1:])
        date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%d-%m-%Y')
    else:
        try:
            date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%d-%m-%Y')
        except ValueError:
            clear_terminal()
            print("Invalid date format. Try again.\n")
            input("\npress any key to continue...")
            return

    if date in study_data:
        clear_terminal()
        print(f"Studies on {date}:")
        for study in study_data[date]:
            print(f"- Subject: {study['subject']}, Time spent: {study['time_spent']} minutes")
        print("")
        input("\npress any key to continue...")
    else:
        clear_terminal()
        print("No studies found for that date.\n")
        input("\npress any key to continue...")

# Define function to remove a day's studies
def remove_day():
    clear_terminal()
    date = input("Enter the date you want to remove (D-M-YY): ")

    if date in study_data:
        del study_data[date]
        clear_terminal()
        print(f"Studies on {date} removed successfully.\n")
    else:
        clear_terminal()
        print("No studies found for that date.\n")

# Define function to flush all data
def flush_all():
    clear_terminal()
    confirm = input("Are you sure you want to delete all data? (y/n) ")
    if confirm.lower() == "y":
        study_data.clear()
        clear_terminal()
        print("All data deleted successfully.\n")
        input("\npress any key to continue...")
    else:
        clear_terminal()
        print("Data deletion cancelled.\n")
        input("\npress any key to continue...")

# Define function to show list of dates
def show_dates():
    clear_terminal()
    dates = sorted(study_data.keys())
    if len(dates) > 0:
        print("\nList of dates:")
        for i, date in enumerate(dates):
            print(f"{i+1}. {date}")
        input("\npress any key to continue...")
    else:
        clear_terminal()
        print("\nNo dates found.\n")
        input("\npress any key to continue...")

# Define function to view statistics
def view_statistics():
    clear_terminal()
    total_time = 0
    subject_time = {}

    # Iterate over each study in study_data
    for studies in study_data.values():
        for study in studies:
            subject = study["subject"]
            time_spent = int(study["time_spent"])

            # Update total time spent studying
            total_time += time_spent

            # Update subject time dictionary
            if subject in subject_time:
                subject_time[subject] += time_spent
            else:
                subject_time[subject] = time_spent

    # Calculate average time spent studying per day
    num_days = len(study_data)
    avg_time = total_time / num_days if num_days > 0 else 0

    # Print statistics
    print(f"\n\nTotal time spent studying: {total_time} minutes")
    print(f"Average time spent studying per day: {avg_time:.2f} minutes")
    if subject_time:
        max_subject = max(subject_time, key=subject_time.get)
        print(f"Subject studied the most: {max_subject} ({subject_time[max_subject]} minutes)")
    input("\n\npress any key to continue...")
    clear_terminal()

def ex():
    print()

# Define menu options
menu = {
    "a": {"text": "Add a study", "action": add_study},
    "b": {"text": "Browse studies on a particular day", "action": browse_day},
    "r": {"text": "Remove studies on a particular day", "action": remove_day},
    "s": {"text": "Show list of dates", "action": show_dates},
    "t": {"text": "View statistics", "action": view_statistics},
    "f": {"text": "Flush all data", "action": flush_all},
    "q": {"text": "Save and exit program", "action": ex}
}

# Define function to display menu
def main():
    while True:
        clear_terminal()
        print("\n||study plan/tracker||\n\nMenu:")
        for key, value in menu.items():
            print(f"{key}. {value['text']}")
        choice = input("\nEnter your choice: ")

        if choice in menu:
            menu[choice]["action"]()
            if choice != "q":
                save_data()
            elif choice == "q":
                clear_terminal()
                break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()