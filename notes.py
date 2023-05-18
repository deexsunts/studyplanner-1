import json
import os
import PyPDF2
import daycalculator
import datetime
from clearterminal import clear_terminal

# Initialize an empty list to hold the notes
notes = []

# Load the notes data from a JSON file
def load_notes():
    global notes
    try:
        with open('notes.json', 'r') as f:
            notes = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty one
        save_notes()

# Save the notes data to a JSON file
def save_notes():
    with open('notes.json', 'w') as f:
        json.dump(notes, f)

# Remove a note from the list
def remove_note():
    print_notes()
    index = int(input("\n\nEnter index of note to remove: "))
    try:
        del notes[index]
        clear_terminal()
        print("note removed successfully.")
    except IndexError:
        print("Invalid index.")

# Add a new note to the list
def add_note():
    name = input("\n\nEnter note name: ")
    pages = int(input("Enter number of pages: "))
    active = input("Active or Deactive? (A/D): ").upper() == "A"  # Added active status
    note = {"name": name, "pages": pages, "pages_read": 0, "active": active}  # Added active key
    notes.append(note)
    save_notes()  # Save the updated list of notes to the JSON file
    clear_terminal()
    print("Note added successfully.")

def show_on_hold_notes():
    clear_terminal()
    on_hold_notes = [note for note in notes if not note.get('active', True)]  # Get on-hold notes

    if not on_hold_notes:
        clear_terminal()
        print("No notes are currently on hold.\n")
        return

    print("\n\nIndex\tName\t\t\t      Pages\t\t Status")
    for i, note in enumerate(on_hold_notes):
        print(f"{i}\t{note['name'].ljust(30)}{note['pages']}\t\t On Hold")

    index = int(input("\n\nEnter index of note to modify: "))
    try:
        note = on_hold_notes[index]
        print("Selected note:", note["name"])
        print("Current status: On Hold")
        activate = input("Activate this note? (Y/N): ").upper() == "Y"
        note["active"] = activate
        clear_terminal()
        clear_terminal()
        print("Note status modified successfully.\n")
    except IndexError:
        clear_terminal()
        print("Invalid index.")



# Display a list of all the notes
def print_notes():
    print("\n\nIndex\tName\t\t\t      Pages\t\t Progress")
    total_pages = sum(note['pages'] for note in notes if note.get('active', True))  # Calculate total pages only for active notes
    total_pages_read = sum(note.get('pages_read', 0) for note in notes if note.get('active', True))  # Calculate total pages read only for active notes
    progress_bar_length = 20
    progress_bar_fill = '█'

    for i, note in enumerate(notes):
        if note.get('active', True):  # Only display active notes
            pages_read = note.get('pages_read', 0)
            progress = int(pages_read * 100 / total_pages) if total_pages != 0 else 0
            print(f"{i}\t{note['name'].ljust(30)}{note['pages']}\t\t   {progress}%")

    progress_bar_fill_count = int(total_pages_read / total_pages * progress_bar_length)
    progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
    print(f"\nProgress: {progress_bar} {int(total_pages_read / total_pages * 100)}%")

# Show notes divided into a time interval t
def show_notes_by_time_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages read only for active notes
    total_pages_left = sum([note["pages"] - note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages left only for active notes
    pages_per_week = total_pages_left / (t / 7)
    pages_per_day = total_pages_left / t
    pages_per_hour = total_pages_left / (t * int(daycalculator.sum_values) / 7)
    pages_per_today = pages_per_hour * daycalculator.todayhours

    print(f"\n\n{'='*30}\n{' '*2}NOTES BY TIME INTERVAL\n{'='*30}\n")
    print(f"Time interval: {t} days")
    print(f"Total pages: {sum([note['pages'] for note in notes if note.get('active', True)])}")  # Calculate total pages only for active notes
    print(f"Total pages read: {total_pages_read}")
    print(f"Total pages left: {total_pages_left}")
    print(f"Pages per week: {pages_per_week:.2f}")
    print(f"Pages per day: {pages_per_day:.2f}")
    print(f"Pages per hour: {pages_per_hour:.2f}")
    print(f"Pages per today: {pages_per_today:.2f}\n\n")

    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages per week':<20} {'Pages per day':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            pages_read = note.get("pages_read", 0)
            pages_left = note["pages"] - pages_read
            pages_per_week = pages_left / (t / 7)
            pages_per_day = pages_left / t
            print(
                f"{note['name']:<30} {pages_read:<15} {pages_left:<15} {pages_per_week:<20.2f} {pages_per_day:<20.2f}")
    input("\n\nPress any key to continue...")
    clear_terminal()

def modify_note():
    print_notes()
    index = int(input("\n\nEnter index of note to modify: "))
    try:
        note = notes[index]
        print("Selected note:", note["name"])
        print("Current number of pages:", note["pages"])
        print("Active status:", "Active" if note.get("active", True) else "Inactive")
        pages = input("Enter number of pages to add or remove: ")
        if pages != "":
            note["pages"] += int(pages)
        else:
            pass
        active = input("Activate or Deactivate? (A/D): ").upper() == "A"
        note["active"] = active
        clear_terminal()
        print("Note modified successfully.")
    except IndexError:
        print("Invalid index.")


# Update the number of pages read for a note
def update_pages_read():
    clear_terminal()
    print("List of notes:")
    for i, note in enumerate(notes):
        print(f"{i}: {note['name']} - {note['pages']} pages")
    index = int(input("\n\nEnter the index of the note you want to update: "))
    pages_read = int(input("Enter the number of pages read: "))
    if 0 <= index < len(notes):
        notes[index]["pages_read"] += pages_read
        save_notes()
        clear_terminal()
        print("Pages read updated successfully.")
    else:
        clear_terminal()
        print("Invalid index.")

# Save PDF notes from a directory to a JSON file
def save_pdf_notes(directory):
    global notes
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: directory does not exist.")
        return
    # Find PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    # Add each PDF note to the notes list
    for i, pdf_file in enumerate(pdf_files):
        with open(os.path.join(directory, pdf_file), 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            note_name = os.path.splitext(pdf_file)[0]
            note_pages = pdf_reader.getNumPages()
            note = {'name': note_name, 'pages': note_pages}
            notes.append(note)
    # Save the notes to a JSON file
    save_notes()
    print(f"{len(pdf_files)} PDF notes saved successfully.")



# Clear the list of notes
def flush_notes():
    confirm = input("Are you sure you want to delete all notes? (y/n) ")
    if confirm.lower() == "y":
        global notes
        notes = []
        print("notes flushed successfully. remember to save!")
        clear_terminal()
        print("\nAll notes removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

# Load the notes data from the file at program start
load_notes()
clear_terminal()

# Main menu loop
def main():
    while True:
        print("\n||currently working notes||\n\nMenu:")
        print("a. Add note")
        print("u. Update page")
        print("s. Show notes")        
        print("d. show time interval")
        print("h. Change Status")
        print("v. save notes")
        print("f. Flush notes")
        print("m. Modify note")
        print("r. Remove note")
        print("y. import notes from directory.")
        print("q. Quit")
        choice = input("\nEnter choice: ")

        if choice == "a":
            clear_terminal()
            add_note()
            save_notes()
        elif choice == "r":
            clear_terminal()
            remove_note()
            save_notes()
        elif choice == "m":
            clear_terminal()
            modify_note()
            save_notes()
        elif choice == "s":
            clear_terminal()
            print_notes()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == "f":
            clear_terminal()
            flush_notes()
        elif choice == "u":
            update_pages_read()
        elif choice == "d":
            clear_terminal()
            show_notes_by_time_interval()
        elif choice == "v":
            clear_terminal()
            save_notes()
        elif choice == "h":
            show_on_hold_notes()
            save_notes()
        elif choice == "y":
            directory = input("Enter directory path: ")
            save_pdf_notes(directory)
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")

t = int(daycalculator.days)
pages_per_hour = sum([note["pages"] for note in notes]) / (t*int(daycalculator.sum_values)/7)
pages_per_today = pages_per_hour * daycalculator.todayhours

if __name__ == '__main__':
    main()