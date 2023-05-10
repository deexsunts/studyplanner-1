import json
from datetime import datetime, timedelta
from clearterminal import clear_terminal

subjects = []

def load_data():
    global subjects
    try:
        with open("subjects.json", "r") as f:
            subjects = json.load(f)
        print("Data loaded successfully!\n")
    except FileNotFoundError:
        print("No saved data found.\n")


def update_subject_indexes():
    global subjects
    n = len(subjects)
    for i in range(n):
        subjects[i]['index'] = i + 1

def save_data():
    with open("subjects.json", "w") as f:
        json.dump(subjects, f)
    print("Data saved successfully!\n")

def change_index():
    clear_terminal()
    if len(subjects) == 0:
        print("No subjects added yet.")
        return
    print("List of subjects:")
    for subject in subjects:
        print(f"{subject['index']}. {subject['name']}")
    old_index = int(input("Enter the old index of the subject: "))
    new_index = int(input("Enter the new index for the subject: "))
    for subject in subjects:
        if subject["index"] == new_index:
            subject["index"] = old_index
        elif subject["index"] == old_index:
            subject["index"] = new_index
    print("Index changed successfully!\n")

def add_subject():
    update_subject_indexes()
    subject_index = len(subjects)
    subject_name = input("Enter subject name: ")
    subjects.append({"index": subject_index, "name": subject_name, "status": "Haven't studied"})
    print("Subject added successfully!")
    show_subjects()

def remove_subject():
    clear_terminal()
    update_subject_indexes()
    if len(subjects) == 0:
        print("No subjects added yet.")
    else:
        print("List of subjects:")
        for subject in subjects:
            print(f"{subject['index']}. {subject['name']} - Status: {subject['status']}")
        subject_index = int(input("Enter subject index to remove: "))
        for subject in subjects:
            if subject["index"] == subject_index:
                subjects.remove(subject)
                print(f"{subject['name']} removed successfully.")
                return
        print(f"Subject with index {subject_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_subjects()

def move_subject():
    clear_terminal()
    update_subject_indexes()
    if len(subjects) == 0:
        print("No subjects added yet.")
    else:
        print("List of subjects:")
        for subject in subjects:
            print(f"{subject['index']}. {subject['name']} - Status: {subject['status']}")
        subject_index = int(input("Enter subject index to move: "))
        for subject in subjects:
            if subject["index"] == subject_index:
                current_status = subject['status']
                if current_status == "Haven't studied":
                    subject['status'] = "Studying right now"
                elif current_status == "Studying right now":
                    subject['status'] = "Study accomplished"
                else:
                    print(f"{subject['name']} already accomplished.")
                return
        print(f"Subject with index {subject_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_subjects()

def update_subject():
    clear_terminal()
    update_subject_indexes()
    if len(subjects) == 0:
        print("No subjects added yet.")
    else:
        print("List of subjects:")
        for subject in subjects:
            print(f"{subject['index']}. {subject['name']} - Status: {subject['status']}")
        subject_index = int(input("Enter subject index to update: "))
        for subject in subjects:
            if subject["index"] == subject_index:
                new_name = input("Enter new name for subject: ")
                subject['name'] = new_name
                return
        print(f"Subject with index {subject_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_subjects()

def show_subjects():
    update_subject_indexes()
    if len(subjects) == 0:
        clear_terminal()
        print("No subjects added yet.\n\n")
    else:
        clear_terminal()
        print("Kanban Board:\n")
        print("{:<5} {:<30} {:<20}".format("Index", "Subject Name", "Status"))
        print("-" * 60)
        count = {"haven't studied": 0, "studying right now": 0, "study accomplished": 0}
        board = {"haven't studied": [], "studying right now": [], "study accomplished": []}
        for subject in subjects:
            count[subject["status"].lower()] += 1
            board[subject["status"].lower()].append(subject)
        if count["study accomplished"] > 0:
            accomplished_indexes = [s["index"] for s in board["study accomplished"]]
            board_length = count["study accomplished"]
            if count["haven't studied"] > board_length:
                start = 0
                end = board_length
            else:
                start = 0
                end = count["haven't studied"]
            for i in range(start, end):
                subject = board["haven't studied"][i]
                print("{:<5} {:<30} {:<20}".format(subject["index"], subject["name"], subject["status"]))
            print("{:<5} {:<30} {:<20}".format("...", "", ""))
            start = count["haven't studied"] + board_length - count["studying right now"]
            end = len(board["haven't studied"])
            for i in range(start, end):
                subject = board["haven't studied"][i]
                print("{:<5} {:<30} {:<20}".format(subject["index"], subject["name"], subject["status"]))
            print("-" * 60)
            for subject in board["studying right now"]:
                print("{:<5} {:<30} {:<20}".format(subject["index"], subject["name"], subject["status"]))
            print("-" * 60)
            for subject in board["study accomplished"]:
                print("{:<5} {:<30} {:<20}".format(subject["index"], subject["name"], subject["status"]))
        else:
            for subject in subjects:
                print("{:<5} {:<30} {:<20}".format(subject["index"], subject["name"], subject["status"]))
        input("\n\npress any key to continue......")
        clear_terminal()

def summarize_subjects():
    with open('subjects.json') as f:
        subjects = json.load(f)

    not_studied = []
    studying = []
    studied = []

    for subject in subjects:
        if subject['status'] == "Haven't studied":
            not_studied.append(subject)
        elif subject['status'] == 'Studying right now':
            studying.append(subject)
        elif subject['status'] == 'Study accomplished':
            studied.append(subject)

    print(f"\nHaven't Studied ({len(not_studied)} subjects):")
    if len(not_studied) > 10:
        for subject in not_studied[:5]:
            print(f"- {subject['index']}. {subject['name']}")
        print("...")
        for subject in not_studied[-5:]:
            print(f"- {subject['index']}. {subject['name']}")
    else:
        for subject in not_studied:
            print(f"- {subject['index']}. {subject['name']}")

    print(f"\nStudying ({len(studying)} subjects):")
    for subject in studying:
        print(f"- {subject['index']}. {subject['name']}")

    print(f"\nStudy Accomplished ({len(studied)} subjects):")
    for subject in studied:
        print(f"- {subject['index']}. {subject['name']}")



def main():
    while True:
        load_data()
        clear_terminal()
        print("\n||Study Subjects||\n\nMenu:")
        print("\na. Add subject")
        print("m. Move subject")
        print("u. Update subject")
        print("s. Show subjects")
        print("r. Remove subject")
        print("ss. summarize")
        print("c. Change index")
        print("v. Save data")
        print("l. Load data")
        print("q. Quit")
        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_subject()
            save_data()
        elif choice == "m":
            clear_terminal()
            move_subject()
            save_data()
        elif choice == "u":
            clear_terminal()
            update_subject()
            save_data()
        elif choice == "s":
            clear_terminal()
            show_subjects()
        elif choice == "r":
            clear_terminal()
            remove_subject()
            save_data()
        elif choice == "c":
            clear_terminal()
            change_index()
            save_data()
        elif choice == "v":
            clear_terminal()
            save_data()
        elif choice == "l":
            clear_terminal()
            load_data()
        elif choice == "ss":
            clear_terminal()
            print("Kanban Board:")
            summarize_subjects()
            input("\n press any key to continue...")
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()