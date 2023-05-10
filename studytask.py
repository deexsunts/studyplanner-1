import json
import math
import os
from datetime import datetime, timedelta
from clearterminal import clear_terminal

studies = []

def save_data():
    with open("studytracker.json", "w") as f:
        json.dump(studies, f)
    #print("\nData saved successfully!\n")

def load_data():
    global studies
    try:
        with open("studytracker.json", "r") as f:
            studies = json.load(f)
    except FileNotFoundError:
        studies = []
        save_data()
        print("No saved data found. A new data file has been created.")


def update_study_indexes():
    global studies
    num_studies = len(studies)
    if num_studies == 0:
        pass
    else:
        for i in range(num_studies):
            studies[i]['index'] = i+1


def add_study():
    name = input("\n\nEnter study name: ")
    desc = input("Enter study description: ")
    multiplier = float(input("Enter study multiplier: "))
    index = len(studies) + 1
    studies.append({"index": index, "name": name, "desc": desc, "days": 0, "multiplier": multiplier, "selected": 0, "done": 0})
    print("Study added successfully!")

def remove_study():
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        print("\n\nList of studies:")
        for study in studies:
            print(f"{study['index']}. {study['name']}")
        index = int(input("Enter study index to remove: "))
        for study in studies:
            if study["index"] == index:
                studies.remove(study)
                print(f"{study['name']} removed successfully.")
                return
        print(f"Study with index {index} not found.")

def reset_study_index():
    if len(studies) == 0:
        pass
    else:
        n = len(studies)
        for i in range(n):
            studies[i]["index"] = i + 1

def list_studies():
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        print(f"\n{'Index':<6}{'Name':<39}{'Days':<20}{'Multiplier':<20}{'Done':<10}{'selected':<10}")
        print("----------------------------------------------------------------------------------------------------------")
        for study in studies:
            print(f"{study['index']:<6}{study['name']:<39}{study['days']:<20}{str(study['multiplier']):<20}{study['done']:<12}{study['selected']:<13}")
    input("\npress any key to continue......")
    clear_terminal()

def save_task_days():
    task_days= input("enter task days: ")
    with open("taskdays.json", "w") as f:
        json.dump(task_days, f)
    print("\nTask days saved successfully!\n")

def change_study_multiplier():
    global studies
    print("\n\nList of studies:")
    for study in studies:
        print(f"{study['index']}. {study['name']}: {study['multiplier']}")
    index = int(input("Enter study index to modify: "))
    multiplier = float(input("Enter new multiplier for study: "))
    studies[index - 1]['multiplier'] = multiplier
    save_data()
    clear_terminal()
    print(f"Multiplier for study '{studies[index - 1]['name']}' updated to {multiplier}")


def load_task_days():
    global task_days
    try:
        with open("taskdays.json", "r") as f:
            task_days = json.load(f)
        #print("Task days loaded successfully!")
    except FileNotFoundError:
        print("No saved task days found.")
    except json.JSONDecodeError:
        print("Invalid JSON format in saved task days file.")

task_days = 0
load_task_days()

def assign_days_to_studies():
    global studies
    num_studies = len(studies)
    if num_studies == 0:
        print("No studies added yet.")
    else:
        total_multiplier = sum([study['multiplier'] for study in studies])
        if total_multiplier == 0:
            print("No multipliers set yet. Please set multipliers before assigning days.")
            return
        days_per_study = round(int(task_days) / total_multiplier, 2)
        for study in studies:
            study_days = days_per_study * study['multiplier']
            study['days'] = round(study_days, 2)
        print(f"Assigned {days_per_study} days to each study.")


def flush_studies():
    confirm = input("Are you sure you want to delete all studies? (y/n) ")
    if confirm.lower() == "y":
        global studies
        studies = []
        clear_terminal()
        print("\nAll studies removed successfully. remember to save")
    else:
        clear_terminal()
        print("cancelled.\n")

def adjust_study_days():
    if len(studies) < 2:
        print("At least two studies are required to perform this operation.")
        return

    # List all studies
    print("\nList of studies:")
    for i, study in enumerate(studies):
        print(f"{i+1}. {study['name']}\t - days: {study['days']}")

    # Ask for first study to add days to
    while True:
        first_choice = input("Enter the number of the study you want to add days to: ")
        if not first_choice.isdigit() or int(first_choice) < 1 or int(first_choice) > len(studies):
            print("Invalid choice. Please enter a valid study number.")
        else:
            first_choice = int(first_choice)
            break

    # Ask for second study to remove days from
    while True:
        second_choice = input("Enter the number of the study you want to remove days from: ")
        if not second_choice.isdigit() or int(second_choice) < 1 or int(second_choice) > len(studies) or second_choice == first_choice:
            print("Invalid choice. Please enter a valid study number that is different from the first choice.")
        else:
            second_choice = int(second_choice)
            break

    # Ask for the number of days to transfer
    while True:
        days = input("Enter the number of days to transfer: ")
        if not days.isdigit():
            print("Invalid input. Please enter a positive integer.")
        else:
            days = int(days)
            break

    # Update the days of the two studies
    studies[first_choice-1]["days"] += days
    studies[second_choice-1]["days"] -= days

    print(f"{days} days were transferred from {studies[second_choice-1]['name']} to {studies[first_choice-1]['name']}.")

def mark_selected():
    print("\nList of studies:")
    for i, study in enumerate(studies):
        print(f"{i+1}. {study['name']}")
    
    selected = input("\nEnter the number of the study you want to mark as selected: ")
    selected_index = int(selected) - 1
    
    if selected_index < 0 or selected_index >= len(studies):
        print("Invalid selection.")
        return
    
    for study in studies:
        study['selected'] = 0
    studies[selected_index]['selected'] = 1
    clear_terminal()
    save_data()
    print(f"{studies[selected_index]['name']} marked as selected.")

def save_today_date():
    today_date = (datetime.now() - timedelta(days=0)).strftime("%d-%m-%Y")
    with open("todaysdate.json", "w") as f:
        json.dump(today_date, f)
    #print("Today's date saved successfully!")

def check_date():
    if not os.path.isfile("todaysdate.json"):
        with open("todaysdate.json", "w") as f:
            json.dump(datetime.now().strftime("%d-%m-%Y"), f)

    with open("todaysdate.json", "r") as f:
        saved_date = json.load(f)
    today_date = datetime.now().strftime("%d-%m-%Y")
    if saved_date != today_date:
        for study in studies:
            if study["selected"] == 1:
                study["days"] -= 1
        save_data()
        print("One day has been removed from the selected Study.")
    else:
        #print("Today's date is already saved.")
        pass


def mark_subject_done():
    if len(studies) == 0:
        print("No Study added yet.")
        return
    
    print("Select a Study to mark as done:")
    
    try:
        print("\n\nList of studies:")
        for study in studies:
            print(f"{study['index']}. {study['name']}: {study['desc']}")
        index = int(input("Enter study index to set as done: "))
        clear_terminal()
        subject = next((subject for subject in studies if subject["index"] == index), None)
        if subject:
            subject["done"] = 1
            print(f"{subject['name']} marked as done.")
            print("Congrats!!! 🎉🎉🎉🎉")
            save_data()
        else:
            print(f"Study with index {index} not found.")
    except ValueError:
        print("Invalid input. Please enter a valid index.")

def display_study_chart():
    global studies

    # Find the selected study
    selected_study = None
    for study in studies:
        if study['selected'] == 1:
            selected_study = study
            break

    # Display the chart
    print("+" + "-" * 78 + "+")
    print("|{:<78}|".format("{}".format(selected_study['name']).center(77)))
    print("|{:<78}|".format("{} Days left".format(selected_study['days']).center(77)))
    print("|{:<78}|".format(datetime.today().strftime("%d-%m-%Y").center(77)))
    print("+" + "-" * 78 + "+")
    print("|{:<78}|".format("Study Description".center(77)))
    desc = selected_study['desc']
    desc_lines = [desc[i:i+75].ljust(75) for i in range(0, len(desc), 75)]
    for line in desc_lines:
        print("|{:<78}|".format(line))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("+" + "-" * 78 + "+")
    print("\n")

def main():
    clear_terminal()
    load_data()
    load_task_days()
    check_date()
    save_today_date()
    while True:
        update_study_indexes()
        print("\n||study planner||\n\nMenu:")
        print("a. Add study")
        print("s. Show current study")
        print("l. list studies")
        print("o. set deadline date and reset studies")
        print("d. adjust a study")
        print("m. mark a study as on-going")
        print("t. change a study's multiplier")
        print("c. mark a study as done")
        print("v. Save data")
        print("r. Remove study")
        print("f. Flush studies")
        print("b. Load data")
        print("q. Quit")
        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_study()
            reset_study_index()
            save_data()
        elif choice == "r":
            clear_terminal()
            remove_study()
            reset_study_index()
            save_data()
        elif choice == "o":
            clear_terminal()
            save_task_days()
            load_task_days()
            assign_days_to_studies()
            save_data()
        elif choice == "f":
            clear_terminal()
            flush_studies()
        elif choice == "v":
            clear_terminal()
            save_data()
        elif choice == "s":
            clear_terminal()
            display_study_chart()
        elif choice == "l":
            clear_terminal()
            list_studies()
        elif choice == "t":
            clear_terminal()
            change_study_multiplier()
        elif choice == "c":
            clear_terminal()
            mark_subject_done()
        elif choice == "d":
            clear_terminal()
            adjust_study_days()
            save_data()
        elif choice == "b":
            clear_terminal()
            load_data()
        elif choice == "m":
            clear_terminal()
            mark_selected()
            save_data()
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")
            clear_terminal()


if __name__ == '__main__':
    main()