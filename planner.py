import json
import datetime
import os
from clearterminal import clear_terminal
import gym
import books
# Get today's date
today = datetime.date.today()+datetime.timedelta(0)
todayex = gym.current()

# Load saved tasks from JSON file if it exists
saved_data = {}
if os.path.isfile(f"{today}.json"):
    with open(f"{today}.json", "r") as file:
        saved_data = json.load(file)
        tasks = saved_data.get("tasks", [])
else:
    # Initialize the tasks for each day
    tasks = [
        {"name": "# Productivity", "done": True},
        {"name": "today's study date", "done": False},
        {"name": "today's tasks", "done": False},
        {"name": "today's books", "done": False},
        {"name": "today's notes", "done": False},
        {"name": "today's day plan", "done": False},
        {"name": "today's videos", "done": False},
        {"name": "today's reviews", "done": False},
        {"name": "tomorrow's study planning", "done": False},
        {"name": "# Personal", "done": True},
        {"name": "language learning", "done": False},
        {"name": todayex, "done": False},
        {"name": "instrument", "done": False}
    ]
    # Save the initial tasks to the JSON file
    with open(f"{today}.json", "w") as file:
        json.dump({"date": str(today), "tasks": tasks}, file, indent=4)
    print(f"New tasks file created: {today}.json")

    # Save the updated tasks to the JSON file
    with open(f"{today}.json", "w") as file:
        json.dump({"date": str(today), "tasks": tasks}, file, indent=4)
    print(f"Tasks file updated: {today}.json")

# Show all tasks
def show_all_tasks():
    counter = 1
    for task in tasks:
        if task['name'].startswith('#'):
            print(f"\t{task['name'].capitalize()}")
        else:
            status = "[x]" if task["done"] else "[ ]"
            print(f"\t{status} {task['name'].capitalize()}")
            counter += 1
    print("")

# Tick a task as done
def tick_task():
    try:
        index = int(input("Enter the index of the task to tick as done: "))
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            print(f"{tasks[index]['name'].capitalize()} is now done!")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid index.")

# Save tasks to JSON file
def save_tasks():
    with open(f"{today}.json", "w") as file:
        json.dump({"date": str(today), "tasks": tasks}, file, indent=4)
    print("Tasks saved.")

# Show today's tracker
def show_today_tracker():
    print("\n\nToday's tracker:\n")
    show_all_tasks()

# Menu loop
def main():
    print("\n\n\n||planner menu||")
    while True:
        choice = input("\n\nEnter s to show today's tracker, t to tick a task as done, q to quit: ")
        if choice == "s":
            clear_terminal()
            show_today_tracker()
        elif choice == "t":
            tick_task()
        elif choice == "q":
            save_tasks()
            clear_terminal()
            break
        else:
            print("Invalid choice.")

# Save tasks if any are done
if any(task["done"] for task in tasks):
    save_tasks()

# Congratulate the user if all tasks are done
if all(task["done"] for task in tasks):
    print("Good job! L3333")

if __name__ == '__main__':
    main()
