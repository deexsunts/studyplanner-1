import json
from datetime import datetime, timedelta
from clearterminal import clear_terminal

tasks = []

def load_data():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
        print("Data loaded successfully!\n")
    except FileNotFoundError:
        print("No saved data found.\n")

def update_task_indexes():
    global tasks
    n = len(tasks)

    tasks.sort(key=lambda task: {
        'Haven\'t studied': 0,
        'Studying right now': 1,
        'Study accomplished': 2
    }[task['status']])

    for i in range(n):
        tasks[i]['index'] = i + 1



def save_data():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)
    print("Data saved successfully!\n")

def change_index():
    clear_terminal()
    if len(tasks) == 0:
        print("No tasks added yet.")
        return
    print("List of Tasks:")
    for task in tasks:
        print(f"{task['index']}. {task['name']}")
    old_index = int(input("Enter the old index of the task: "))
    new_index = int(input("Enter the new index for the task: "))
    for task in tasks:
        if task["index"] == new_index:
            task["index"] = old_index
        elif task["index"] == old_index:
            task["index"] = new_index
    print("Index changed successfully!\n")

def add_task():
    update_task_indexes()
    task_index = len(tasks)
    task_name = input("Enter task name: ")
    task_deadline = input("Enter task's deadline (use 'today' or '+n' for relative dates, or 'dd-mm-yyyy' for absolute date): ")
    if task_deadline.lower() == 'today':
        deadline_date = datetime.now().date()
    elif task_deadline.startswith('+'):
        days_offset = int(task_deadline[1:])
        deadline_date = (datetime.now() + timedelta(days=days_offset)).date()
    else:
        deadline_date = datetime.strptime(task_deadline, '%d-%m-%Y').date()
    deadline_str = deadline_date.strftime('%d-%m-%Y')
    tasks.append({"index": task_index, "name": task_name, "deadline": deadline_str, "status": "Haven't studied"})
    print("Task added successfully!")
    save_data()
    show_tasks()

def remove_task():
    clear_terminal()
    update_task_indexes()
    if len(tasks) == 0:
        print("No tasks added yet.")
    else:
        print("List of tasks:")
        for task in tasks:
            print(f"{task['index']}. {task['name']} - Status: {task['status']}")
        task_index = int(input("Enter task index to remove: "))
        for task in tasks:
            if task["index"] == task_index:
                tasks.remove(task)
                print(f"{task['name']} removed successfully.")
                return
        print(f"task with index {task_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_tasks()

def move_task():
    clear_terminal()
    update_task_indexes()
    pending_tasks = [task for task in tasks if task['status'] != "Study accomplished"]

    if len(pending_tasks) == 0:
        print("No pending tasks.")
    else:
        print("List of pending tasks:")
        for task in pending_tasks:
            print(f"{task['index']}. {task['name']} - Status: {task['status']}")
        task_index = int(input("Enter the index of the task to move: "))

        for task in pending_tasks:
            if task["index"] == task_index:
                current_status = task['status']
                if current_status == "Haven't studied":
                    task['status'] = "Studying right now"
                elif current_status == "Studying right now":
                    task['status'] = "Study accomplished"
                else:
                    print(f"{task['name']} is already marked as accomplished.")
                save_data()
                clear_terminal()
                show_tasks()
                return

        print(f"Task with index {task_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_tasks()

def update_task():
    clear_terminal()
    update_task_indexes()
    if len(tasks) == 0:
        print("No tasks added yet.")
    else:
        print("List of tasks:")
        for task in tasks:
            print(f"{task['index']}. {task['name']} - Status: {task['status']}")
        task_index = int(input("Enter task index to update: "))
        for task in tasks:
            if task["index"] == task_index:
                new_name = input("Enter new name for task: ")
                task['name'] = new_name
                return
        print(f"task with index {task_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_tasks()

def show_tasks():
    update_task_indexes()
    if len(tasks) == 0:
        clear_terminal()
        print("No tasks added yet.\n\n")
    else:
        clear_terminal()
        print("Kanban Board:\n")
        print("{:<5} {:<30} {:<20} {:<15}".format("Index", "Task Name", "Status", "Deadline"))
        print("-" * 75)
        count = {"haven't studied": 0, "studying right now": 0, "study accomplished": 0}
        board = {"haven't studied": [], "studying right now": [], "study accomplished": []}
        for task in tasks:
            count[task["status"].lower()] += 1
            board[task["status"].lower()].append(task)

        # sort tasks based on due date
        for status in board.keys():
            board[status] = sorted(board[status], key=lambda x: datetime.strptime(x['deadline'], '%d-%m-%Y'))

        if count["study accomplished"] > -1:
            accomplished_indexes = [s["index"] for s in board["study accomplished"]]
            board_length = count["study accomplished"]
            if count["haven't studied"] > board_length:
                start = 0
                end = count["haven't studied"]
            else:
                start = 0
                end = count["haven't studied"]
            for i in range(start, end):
                task = board["haven't studied"][i]
                deadline = task["deadline"]
                deadline_datetime = datetime.strptime(deadline, "%d-%m-%Y")
                today = datetime.today()
                if deadline_datetime.date() == today.date():
                    deadline_formatted = "today"
                elif deadline_datetime.date() < today.date():
                    deadline_formatted = "overdue"
                else:
                    days_left = (deadline_datetime - today).days+1
                    deadline_formatted = f"{days_left} day{'s' if days_left != 1 else ''} left"
                print("{:<5} {:<30} {:<20} {:<15}".format(task["index"], task["name"], task["status"], deadline_formatted))
            start = count["haven't studied"] + board_length - count["studying right now"]
            end = len(board["haven't studied"])
            print("-" * 75)
            for task in board["studying right now"]:
                deadline = task["deadline"]
                try:
                    deadline_datetime = datetime.strptime(deadline, "%d-%m-%Y")
                    today = datetime.today()
                    if deadline_datetime.date() == today.date():
                        deadline_formatted = "today"
                    elif deadline_datetime.date() < today.date():
                        deadline_formatted = "overdue"
                    else:
                        days_left = (deadline_datetime - today).days+1
                        deadline_formatted = f"{days_left} day{'s' if days_left != 1 else ''} left"
                except ValueError:
                    deadline_formatted = deadline
                print("{:<5} {:<30} {:<20} {:<15}".format(task["index"], task["name"], task["status"], deadline_formatted))
            print("-" * 75)
        accomplished_tasks = sorted(board["study accomplished"], key=lambda x: datetime.strptime(x["deadline"], "%d-%m-%Y"), reverse=True)[:5]
        for task in accomplished_tasks:
            deadline = task["deadline"]
            deadline_datetime = datetime.strptime(deadline, "%d-%m-%Y")
            deadline_formatted = deadline_datetime.strftime("%d-%m-%Y")
            print("{:<5} {:<30}".format(task["index"], task["name"]))
    input("\n\nPress any key to continue...")
    clear_terminal()


def flush_tasks():
    global tasks
    confirm = input("Are you sure you want to delete all studies? (y/n) ")
    if confirm.lower() == "y":
        tasks = []
        clear_terminal()
        save_data()
        print("\nAll studies removed successfully. remember to save")
    else:
        clear_terminal()
        print("cancelled.\n")

def summarize_tasks():
    with open('tasks.json') as f:
        tasks = json.load(f)

    not_studied = []
    studying = []
    studied = []

    for task in tasks:
        if task['status'] == "Haven't studied":
            not_studied.append(task)
        elif task['status'] == 'Studying right now':
            studying.append(task)
        elif task['status'] == 'Study accomplished':
            studied.append(task)

    print(f"\nHaven't Studied ({len(not_studied)} tasks):")
    if len(not_studied) > 10:
        for task in not_studied[:5]:
            print(f"- {task['index']}. {task['name']}")
        print("...")
        for task in not_studied[-5:]:
            print(f"- {task['index']}. {task['name']}")
    else:
        for task in not_studied:
            print(f"- {task['index']}. {task['name']}")

    print(f"\nStudying ({len(studying)} tasks):")
    for task in studying:
        print(f"- {task['index']}. {task['name']}")

    print(f"\nStudy Accomplished ({len(studied)} tasks):")
    for task in studied:
        print(f"- {task['index']}. {task['name']}")

def change_due_date():
    clear_terminal()
    if len(tasks) == 0:
        print("No tasks added yet.")
        return

    print("List of Tasks:")
    for task in tasks:
        if task['status'] != "Study accomplished":
            print(f"{task['index']}. {task['name']} - Deadline: {task['deadline']}")

    task_index = int(input("Enter the index of the task to change the due date: "))
    for task in tasks:
        if task["index"] == task_index:
            new_due_date = input("Enter new due date (use 'today' or '+n' for relative dates, or 'dd-mm-yyyy' for absolute date): ")
            if new_due_date.lower() == 'today':
                deadline_date = datetime.now().date()
            elif new_due_date.startswith('+'):
                days_offset = int(new_due_date[1:])
                deadline_date = (datetime.now() + timedelta(days=days_offset)).date()
            else:
                deadline_date = datetime.strptime(new_due_date, '%d-%m-%Y').date()
            deadline_str = deadline_date.strftime('%d-%m-%Y')
            task['deadline'] = deadline_str
            print(f"Due date for {task['name']} changed successfully to {task['deadline']}!\n")
            save_data()
            return
    print(f"Task with index {task_index} not found.")

def remove_completed_studies():
    clear_terminal()
    if len(tasks) == 0:
        print("No tasks added yet.\n")
        return
    
    removed_count = 0
    tasks_copy = tasks.copy()  # Create a copy to avoid modifying the list during iteration
    
    for task in tasks_copy:
        if task['status'] == "Study accomplished":
            tasks.remove(task)
            removed_count += 1
    
    if removed_count > 0:
        print(f"{removed_count} completed studies removed successfully.\n")
        update_task_indexes()  # Update the task indexes after removal
        save_data()
    else:
        clear_terminal()
        print("No completed studies found.\n")


def main():
    load_data()
    update_task_indexes()
    save_data()
    clear_terminal()
    while True:
        print("\n||Study tasks||\n\nMenu:")
        print("\na. Add task")
        print("m.  Move task")
        print("u.  Update task")
        print("s.  Show tasks")
        print("r.  Remove task")
        print("ss. summarize")
        print("c.  Change index")
        print("cc. Change due date")
        print("rr. remove completed tasks")
        print("v.  Save data")
        print("l.  Load data")
        print("f.  flush data")
        print("q.  Quit")
        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_task()
            clear_terminal()
        elif choice == "m":
            clear_terminal()
            move_task()
            save_data()
            clear_terminal()
        elif choice == "u":
            clear_terminal()
            update_task()
            save_data()
            clear_terminal()
        elif choice == "rr":
            clear_terminal()
            remove_completed_studies()
        elif choice == "s":
            clear_terminal()
            show_tasks()
            clear_terminal()
        elif choice == "r":
            clear_terminal()
            remove_task()
            save_data()
            clear_terminal()
        elif choice == "c":
            clear_terminal()
            change_index()
            save_data()
            clear_terminal()
        elif choice == "v":
            clear_terminal()
            save_data()
            clear_terminal()
        elif choice == "f":
            clear_terminal()
            flush_tasks()
            clear_terminal()
        elif choice == "l":
            clear_terminal()
            load_data()
            clear_terminal()
        elif choice == "cc":
            change_due_date()
            load_data()
            clear_terminal()
        elif choice == "ss":
            clear_terminal()
            print("Kanban Board:")
            summarize_tasks()
            input("\n press any key to continue...")
            clear_terminal()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()
            print("Invalid choice.")


if __name__ == '__main__':
    main()