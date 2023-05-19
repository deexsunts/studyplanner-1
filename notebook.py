import json
from clearterminal import clear_terminal

# Constants for JSON file names
GOALS_FILE = "goals.json"
CURRENT_NOTES_FILE = "currentnotes.json"
WW_FILE = "ww.json"
WR_FILE = "wr.json"

# Load JSON data from files
def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Save JSON data to files
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Display menu options
def display_menu():
    clear_terminal()
    print("\n||The Notebook||\n\nMenu:")
    print("g. Goals")
    print("n. Current Notes")
    print("r. Rules")
    print("w. Wants and Fun")
    print("q. Exit")

# Add a new item to the JSON file
def add_item(file_name, item):
    clear_terminal()
    data = load_data(file_name)
    data.append(item)
    save_data(file_name, data)
    print("Item added successfully.\n")

# Remove an item from the JSON file
def remove_item(file_name, index):
    clear_terminal()
    data = load_data(file_name)
    if index < len(data):
        del data[index]
        save_data(file_name, data)
        clear_terminal()
        print("Item removed successfully.")
    else:
        print("Invalid index.")

# Update the index of an item in the JSON file
def update_index(file_name, current_index, new_index):
    data = load_data(file_name)
    if current_index < len(data) and new_index <= len(data):
        item = data.pop(current_index)
        data.insert(new_index, item)
        save_data(file_name, data)
        print("Index updated successfully.")
    else:
        print("Invalid index.")

# Check and update indexes in a JSON file
def update_indexes(file_name):
    data = load_data(file_name)
    updated_data = []
    for i, item in enumerate(data):
        updated_data.append(item)
        if i != item["index"]:
            item["index"] = i
    save_data(file_name, updated_data)

# Show the contents of a JSON file
def show_contents(file_name):
    data = load_data(file_name)
    print("\nTITLE")
    print("--------------------")
    for item in data:
        print(f"{item['index']}\t{item['item']}")

# Main program loop
def main():
    while True:
        display_menu()
        option = input("\n Enter your choice: ")

        if option == "q":
            clear_terminal()
            break

        elif option == "g":
            clear_terminal()
            goals_data = load_data(GOALS_FILE)
            while True:
                update_indexes(GOALS_FILE)
                print("\n||Goals||\n\nMenu:")
                print("a. Add Goal")
                print("r. Remove Goal")
                print("u. Update Index")
                print("s. Show Contents")
                print("q. Back to Main Menu")
                sub_option = input("\n Enter your choice: ")

                if sub_option == "q":
                    clear_terminal()
                    break

                elif sub_option == "a":
                    clear_terminal()
                    goal = input("Enter the goal: ")
                    add_item(GOALS_FILE, {"item": goal, "index": len(goals_data)})
                    clear_terminal()

                elif sub_option == "r":
                    clear_terminal()
                    show_contents(GOALS_FILE)
                    print("\n\n")
                    goal_index = int(input("Enter the index of the goal to remove: "))
                    remove_item(GOALS_FILE, goal_index)
                    clear_terminal()

                elif sub_option == "u":
                    clear_terminal()
                    show_contents(GOALS_FILE)
                    current_index = int(input("Enter the current index of the goal: "))
                    new_index = int(input("Enter the new index for the goal: "))
                    update_index(GOALS_FILE, current_index, new_index)
                    clear_terminal()

                elif sub_option == "s":
                    clear_terminal()
                    show_contents(GOALS_FILE)
                    input("\n\npress any key to continue..")
                    clear_terminal()

        elif option == "n":
            clear_terminal()
            current_notes_data = load_data(CURRENT_NOTES_FILE)
            while True:
                update_indexes(CURRENT_NOTES_FILE)
                print("\n||Current Notes||\n\nMenu:")
                print("a. Add Current Note")
                print("r. Remove Current Note")
                print("u. Update Index")
                print("s. Show Contents")
                print("q. Back to Main Menu")
                sub_option = input("\n Enter your choice: ")

                if sub_option == "q":
                    clear_terminal()
                    break

                elif sub_option == "a":
                    clear_terminal()
                    note = input("Enter the current note: ")
                    add_item(CURRENT_NOTES_FILE, {"item": note, "index": len(current_notes_data)})
                    clear_terminal()

                elif sub_option == "r":
                    clear_terminal()
                    show_contents(CURRENT_NOTES_FILE)
                    print("\n\n")
                    note_index = int(input("Enter the index of the current note to remove: "))
                    remove_item(CURRENT_NOTES_FILE, note_index)
                    clear_terminal()

                elif sub_option == "u":
                    clear_terminal()
                    show_contents(CURRENT_NOTES_FILE)
                    current_index = int(input("Enter the current index of the current note: "))
                    new_index = int(input("Enter the new index for the current note: "))
                    update_index(CURRENT_NOTES_FILE, current_index, new_index)
                    clear_terminal()

                elif sub_option == "s":
                    clear_terminal()
                    show_contents(CURRENT_NOTES_FILE)
                    input("\n\npress any key to continue..")
                    clear_terminal()

        elif option == "r":
            clear_terminal()
            ww_data = load_data(WR_FILE)
            while True:
                update_indexes(WR_FILE)
                print("\n||Rules||\n\nMenu:")
                print("a. Add Rule")
                print("r. Remove Rule")
                print("u. Update Index")
                print("s. Show Contents")
                print("q. Back to Main Menu")
                sub_option = input("\n Enter your choice: ")

                if sub_option == "q":
                    clear_terminal()
                    break

                elif sub_option == "a":
                    clear_terminal()
                    rule = input("Enter the rule: ")
                    add_item(WR_FILE, {"item": rule, "index": len(ww_data)})
                    clear_terminal()

                elif sub_option == "r":
                    clear_terminal()
                    show_contents(WR_FILE)
                    rule_index = int(input("\n\nEnter the index of the rule to remove: "))
                    remove_item(WR_FILE, rule_index)
                    clear_terminal()

                elif sub_option == "u":
                    clear_terminal()
                    show_contents(WR_FILE)
                    current_index = int(input("Enter the current index of the rule: "))
                    new_index = int(input("Enter the new index for the rule: "))
                    update_index(WR_FILE, current_index, new_index)
                    clear_terminal()

                elif sub_option == "s":
                    clear_terminal()
                    show_contents(WR_FILE)
                    input("\n\npress any key to continue..")
                    clear_terminal()

        elif option == "w":
            clear_terminal()
            wants_fun_data = load_data(WW_FILE)
            while True:
                update_indexes(WW_FILE)
                print("\n||Wants and Fun||\n\nMenu:")
                print("a. Add Want or Fun")
                print("r. Remove Want or Fun")
                print("u. Update Index")
                print("s. Show Contents")
                print("q. Back to Main Menu")
                sub_option = input("\n Enter your choice: ")

                if sub_option == "q":
                    clear_terminal()
                    break

                elif sub_option == "a":
                    clear_terminal()
                    want_fun = input("Enter the want or fun item: ")
                    add_item(WW_FILE, {"item": want_fun, "index": len(wants_fun_data)})
                    clear_terminal()

                elif sub_option == "r":
                    clear_terminal()
                    show_contents(WW_FILE)
                    want_fun_index = int(input("\n\nEnter the index of the want or fun item to remove: "))
                    remove_item(WW_FILE, want_fun_index)
                    clear_terminal()

                elif sub_option == "u":
                    clear_terminal()
                    show_contents(WW_FILE)
                    current_index = int(input("Enter the current index of the want or fun item: "))
                    new_index = int(input("Enter the new index for the want or fun item: "))
                    update_index(WW_FILE, current_index, new_index)
                    clear_terminal()

                elif sub_option == "s":
                    clear_terminal()
                    show_contents(WW_FILE)
                    input("\n\npress any key to continue..")
                    clear_terminal()

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
