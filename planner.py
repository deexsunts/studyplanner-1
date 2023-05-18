import json
import os
from datetime import datetime, timedelta
from clearterminal import clear_terminal

data = []

def load_data():
    global data
    try:
        with open('endeavors.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_data(data):
    with open('endeavors.json', 'w') as f:
        json.dump(data, f, indent=4)

def show_endeavors():
    clear_terminal()
    data = load_data()
    print()
    tags = set(endeavor['tag'] for endeavor in data)
    total_endeavors = sum(1 for endeavor in data if endeavor['done'])  # Count the number of completed endeavors
    progress_bar_length = 20
    progress_bar_fill = '█'
    
    for tag in sorted(tags):
        print(f"#{tag}")
        endeavors = sorted(filter(lambda e: e['tag'] == tag, data), key=lambda e: e['index'])
        
        for i, endeavor in enumerate(endeavors):
            done = '[x]' if endeavor['done'] else '[ ]'
            print(f" {str(endeavor['index']).rjust(2)}) {done.ljust(3)} {endeavor['name']}")
        
        tag_endeavors = [endeavor for endeavor in endeavors if endeavor['done']]
        tag_progress = len(tag_endeavors) / len(endeavors)
        progress_bar_fill_count = int(tag_progress * progress_bar_length)
        progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
        print(f"\nProgress: {progress_bar} {int(tag_progress * 100)}%\n")
    
    input("\npress any key to continue...")
    clear_terminal()



def showsmall():
    clear_terminal()
    data = load_data()
    tags = set(endeavor['tag'] for endeavor in data)
    for tag in sorted(tags):
        print(f"#{tag}")
        endeavors = sorted(filter(lambda e: e['tag'] == tag, data), key=lambda e: e['index'])
        for i, endeavor in enumerate(endeavors):
            done = '[x]' if endeavor['done'] else '[ ]'
            print(f"({endeavor['index']}) {done} {endeavor['name']}")

def add_endeavor():
    clear_terminal()
    data = load_data()
    name = input("Name of endeavor: ")
    tag = input("Tag of endeavor: ")
    index = len(data)
    data.append({'index': index, 'name': name, 'tag': tag, 'done': False})
    save_data(data)
    print("Endeavor added successfully.")
    clear_terminal()

def remove_endeavor():
    clear_terminal()
    showsmall()
    data = load_data()
    index = int(input("\nIndex of endeavor to remove: "))
    data = [endeavor for endeavor in data if endeavor['index'] != index]
    for i, endeavor in enumerate(data):
        endeavor['index'] = i
    save_data(data)
    clear_terminal()
    print("Endeavor removed successfully.\n")

def toggle_done():
    clear_terminal()
    showsmall()
    data = load_data()
    index = int(input("Index of endeavor to toggle: "))
    for endeavor in data:
        if endeavor['index'] == index:
            endeavor['done'] = not endeavor['done']
            save_data(data)
            clear_terminal()
            print("Endeavor toggled successfully.\n")
            return
    clear_terminal()
    print("Endeavor not found.\n")

def check_date():
    data = load_data()
    if not os.path.isfile("todaysdate2.json"):
        with open("todaysdate2.json", "w") as f:
            json.dump(datetime.now().strftime("%d-%m-%Y"), f)

    with open("todaysdate2.json", "r") as f:
        saved_date = json.load(f)
    today_date = datetime.now().strftime("%d-%m-%Y")
    if saved_date != today_date:
        for endeavor in data:
            endeavor["done"] = False
        save_data(data)
        print("All endeavors have been marked as undone due to a new day.\n")
    else:
        pass

def save_today_date():
    today_date = datetime.now().strftime("%d-%m-%Y")
    with open("todaysdate2.json", "w") as f:
        json.dump(today_date, f)


def print_menu():
    print("\n||Transformative Endeavor||\n\nMenu:")
    print("a. Add endeavor")
    print("s. Show endeavors")
    print("r. Remove endeavor")
    print("m. Toggle endeavor as done")
    print("q. Quit")

def main():
    clear_terminal()
    check_date()
    save_today_date()
    while True:
        print_menu()
        choice = input("\nEnter choice: ")
        if choice == 's':
            show_endeavors()
        elif choice == 'a':
            add_endeavor()
        elif choice == 'r':
            remove_endeavor()
        elif choice == 'm':
            toggle_done()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()
            print("Invalid choice. Try again.\n")

if __name__ == '__main__':
    main()