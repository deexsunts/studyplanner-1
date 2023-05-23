import json
import math
import os
from datetime import datetime, timedelta
from clearterminal import clear_terminal

studies = []

def add_study():
    clear_terminal()
    name = input("\n\nEnter study name: ")
    while True:
        study_date = input ("Enter starting date (today/tomorrow/+n/DD-MM-YY): ")
        if study_date == 'today':
            start = datetime.now().strftime('%d-%m-%Y')
            break
        elif study_date == 'tomorrow':
            start = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
            break
        elif study_date.startswith('+'):
            days = int(study_date[1:])
            start = (datetime.now() + timedelta(days=days)).strftime('%d-%m-%Y')
            break
        else:
            try:
                start = datetime.strptime(study_date, '%d-%m-%Y').strftime('%d-%m-%Y')
                break
            except ValueError:
                print("Invalid date format. Try again.")

    amount = int(input("Enter amount of work (p): "))
    days = int(input("Enter number of days to finish: "))

    #number_summable = input("Is the number sum-able? (Y/N): ")
    #number = 1 if number_summable.lower() == "y" else 0
    number=1
    hour_estimate = int(input("Enter the hour estimate for the study: "))

    index = len(studies) + 1
    studies.append({"index": index, "name": name, "amount": amount, "datestart": start, "days": days, "number": number, "hour_estimate": hour_estimate})
    clear_terminal()
    print("Study added successfully!")

def list_studies():
    clear_terminal()
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        print(f"\n{'Index':<8}{'Name':<20}{'Amount':<10}{'Start Date':<15}{'Days':<10}{'Number':<10}{'Hour Estimate':<15}")
        for study in studies:
            print(f"{study['index']:<8}{study['name']:<20}{study['amount']:<10}{study['datestart']:<15}{study['days']:<10}{study['number']:<10}{study['hour_estimate']:<15}")
    input("\npress any key to continue......")
    clear_terminal()

def show_studies():
    clear_terminal()
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        # Find the maximum date among all the studies
        max_date = max([datetime.strptime(s["datestart"], '%d-%m-%Y') + timedelta(days=s["days"]) for s in studies])

        # Calculate the number of days between today and the maximum date
        max_days = (max_date.date() - datetime.today().date()).days

        # Create a list of lists to store the studies for each day
        study_days = [[] for _ in range(max_days+10)]

        # Create a dictionary to store the sum of study amounts for each day with a study with number=1
        sum_days = {}

        # Populate the list of study days and the dictionary of sum days
        for study in studies:
            amount_per_day = round(study["amount"] / study["days"], 2)
            start_day = datetime.strptime(study["datestart"], '%d-%m-%Y').date()
            for i in range(study["days"]):
                day = start_day + timedelta(days=i)
                if start_day <= day < start_day + timedelta(days=study["days"]):
                    index = (day - datetime.today().date()).days
                    study_entry = (study["name"], amount_per_day)
                    study_days[index].append(study_entry)
                    if study["number"] == 1:
                        if index in sum_days:
                            sum_days[index] += amount_per_day
                        else:
                            sum_days[index] = amount_per_day

        # Print the study days and the sum of study amounts for days with number=1
        for i in range(max_days):
            date = datetime.today().date() + timedelta(days=i)
            if date > max_date.date():
                break
            label = ""
            if date == datetime.today().date():
                label = "today"
            elif date < datetime.today().date():
                label = "passed"
            else:
                label = date.strftime('%d-%m-%Y')
            print(f"date: {label}")
            for study in study_days[i]:
                amount_per_day = study[1]
                hour_estimate = [s["hour_estimate"] for s in studies if s["name"] == study[0] and s["number"] == 1][0]
                print(f"{study[0]} ({amount_per_day} per day)")
            print(f"- total workload: {sum_days[i]}")
            hour_estimate = sum([s["hour_estimate"] / s["days"] for s in studies if s["number"] == 1])
            print(f"- total hour estimate: {hour_estimate:.2f}")
            # print("{%.2f}".format(hour_estimate))
            # print("%.2f" % hour_estimate)
            print()
        input("\npress any key to continue......")
        clear_terminal()

def show_date():
    clear_terminal()
    if len(studies) == 0:
        clear_terminal()
        print("No studies added yet.\n")
        return

    date = input("Enter date (today/tomorrow/+n/DD-MM-YY): ")
    try:
        selected_date = datetime.strptime(date, '%d-%m-%Y').date()
    except ValueError:
        if date == 'today':
            selected_date = datetime.today().date()
        elif date == 'tomorrow':
            selected_date = (datetime.today() + timedelta(days=1)).date()
        elif date.startswith('+'):
            days = int(date[1:])
            selected_date = (datetime.today() + timedelta(days=days)).date()
        else:
            print("Invalid date format.")
            input("\npress any key to continue......")
            clear_terminal()
            return

    # Create a list to store the studies for the selected date
    study_date = []

    # Populate the list of study date
    for study in studies:
        amount_per_day = round(study["amount"] / study["days"], 2)
        start_day = datetime.strptime(study["datestart"], '%d-%m-%Y').date()
        for i in range(study["days"]):
            day = start_day + timedelta(days=i)
            if day == selected_date and study["number"] == 1:
                hour_estimate = study["hour_estimate"] / study["days"]
                study_date.append((study["name"], amount_per_day, hour_estimate))

    # Print the study date
    if not study_date:
        print("No studies for the selected date.")
        input("\npress any key to continue......")
        clear_terminal()
    else:
        print()
        print(selected_date.strftime('%d-%m-%Y') + ":")
        for study in study_date:
            print(f"{study[0]} ({study[1]} per day - Hour: {study[2]})")
        input("\npress any key to continue......")
        clear_terminal()


def modify_study():
    clear_terminal()
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        print("\n\nList of studies:")
        for study in studies:
            print(f"{study['index']}. {study['name']}")
        index = int(input("Enter study index to modify: "))
        for study in studies:
            if study["index"] == index:
                print(f"You selected study '{study['name']}' with amount of work '{study['amount']}' and number of days '{study['days']}' and starting date '{study['datestart']}'")
                while True:
                    amount = input("Enter amount of work to add or reduce (or 'q' to quit): ")
                    if amount == 'q':
                        break
                    try:
                        amount = int(amount)
                        study["amount"] += amount
                        print(f"Amount of work updated to '{study['amount']}'")
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                        continue
                    days = input("Enter number of days to add or reduce (or 'q' to quit): ")
                    if days == 'q':
                        break
                    try:
                        days = int(days)
                        study["days"] += days
                        print(f"Number of days updated to '{study['days']}'")
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                        continue
                    datestart = input("Enter starting date (today/tomorrow/+n/DD-MM-YY) or 'q' to quit: ")
                    if datestart == 'q':
                        break
                    try:
                        if datestart == 'today':
                            start = datetime.now().strftime('%d-%m-%Y')
                        elif datestart == 'tomorrow':
                            start = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
                        elif datestart.startswith('+'):
                            days = int(datestart[1:])
                            start = (datetime.now() + timedelta(days=days)).strftime('%d-%m-%Y')
                        else:
                            start = datetime.strptime(datestart, '%d-%m-%Y').strftime('%d-%m-%Y')
                        study["datestart"] = start
                        print(f"Starting date updated to '{study['datestart']}'")
                    except ValueError:
                        print("Invalid date format. Try again.")
                        continue
                    hour_estimate = input("Enter hour estimate (or 'q' to quit): ")
                    if hour_estimate == 'q':
                        break
                    try:
                        hour_estimate = int(hour_estimate)
                        study["hour_estimate"] = hour_estimate
                        print(f"Hour estimate updated to '{study['hour_estimate']}'")
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                        continue
                clear_terminal()
                print("\nStudy modified successfully.\n")
                return
        clear_terminal()
        print(f"Study with index {index} not found.")


def remove_study():
    clear_terminal()
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        clear_terminal()
        print("\n\nList of studies:")
        for study in studies:
            print(f"{study['index']}. {study['name']}")
        index = int(input("Enter study index to remove: "))
        for study in studies:
            if study["index"] == index:
                studies.remove(study)
                clear_terminal()
                print(f"{study['name']} removed successfully.")
                return

# def delay_study():
#     if len(studies) == 0:
#         print("No studies added yet.")
#     else:
#         print("\n\nList of studies:")
#         for study in studies:
#             print(f"{study['index']}. {study['name']} (delayed by {study.get('delayed', 0)} days)")
#         index = int(input("Enter study index to delay: "))
#         for study in studies:
#             if study["index"] == index:
#                 print(f"You selected study '{study['name']}' with amount of work '{study['amount']}' and number of days '{study['days']}'")
#                 delay_days = int(input("Enter number of days to delay: "))
#                 study["delayed"] = delay_days
#                 print(f"Study '{study['name']}' has been delayed by {delay_days} days.")
#                 return
#         print(f"Study with index {index} not found.")

def flush_studies():
    clear_terminal()
    confirm = input("Are you sure you want to delete all studies? (y/n) ")
    if confirm.lower() == "y":
        global studies
        studies = []
        clear_terminal()
        save_data()
        print("\nAll studies removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

def save_data():
    with open("studies.json", "w") as f:
        json.dump(studies, f)
    print("\nData saved successfully!\n")

def load_data():
    global studies
    try:
        with open("studies.json", "r") as f:
            studies = json.load(f)
        print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found.")

# def check_start_date():
#     today = datetime.now().date()

#     for study in studies:
#         study_start = datetime.strptime(study['datestart'], '%d-%m-%Y').date()

#         if today > study_start:
#             difference = (today - study_start).days
#             study['days'] -= difference
#             study['datestart'] = today.strftime('%d-%m-%Y')
#     save_data()

load_data()

def main():
    #check_start_date()
    clear_terminal()
    while True:
        print("\n||day planner||\n\nMenu:")
        print("a. Add study")
        print("r. Remove study")
        print("m. Modify study")
        print("f. Flush studies")
        print("s. Show studies")
        print("d. Show Study by day")
        print("l. list studies")
        print("v. Save data")
        print("b. Load data")
        print("q. Quit")
        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_study()
            save_data()
        elif choice == "r":
            clear_terminal()
            remove_study()
            save_data()
        elif choice == "m":
            clear_terminal()
            modify_study()
            save_data()
        elif choice == "f":
            clear_terminal()
            flush_studies()
        elif choice == "s":
            clear_terminal()
            show_studies()
        elif choice == "d":
            print()
            show_date()
        elif choice == "v":
            clear_terminal()
            save_data()
        elif choice == "l":
            clear_terminal()
            list_studies()
        elif choice == "b":
            clear_terminal()
            load_data()
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()