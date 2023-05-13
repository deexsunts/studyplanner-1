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

# Add a new note to the list
def add_note():
    name = input("\n\nEnter note name: ")
    pages = int(input("Enter number of pages: "))
    note = {"name": name, "pages": pages, "pages_read": 0} # Added pages_read key with initial value 0
    notes.append(note)
    save_notes() # Save the updated list of notes to the JSON file
    clear_terminal()
    print("note added successfully.")


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

# Modify the number of pages of a note in the list
def modify_note():
    print_notes()
    index = int(input("\n\nEnter index of note to modify: "))
    try:
        note = notes[index]
        print("Selected note:", note["name"])
        print("Current number of pages:", note["pages"])
        pages = int(input("Enter number of pages to add or remove: "))
        note["pages"] += pages
        clear_terminal()
        print("note modified successfully.")
    except IndexError:
        print("Invalid index.")
    except ValueError:
        print("Invalid number of pages.")

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

# Display a list of all the notes
def print_notes():
    print("\n\nIndex\tName\t\t\t      Pages\t\t Progress")
    for i, note in enumerate(notes):
        pages_read = note.get('pages_read', 0)  # get pages_read value, default to 0 if not present
        progress = int(pages_read * 100 / note['pages']) if note['pages'] != 0 else 0  # calculate progress percentage
        print(f"{i}\t{note['name'].ljust(30)}{note['pages']}\t\t   {progress}%")

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


# Show notes divided into a time interval t
def show_notes_by_time_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([note.get("pages_read", 0) for note in notes])
    total_pages_left = sum([note["pages"] - note.get("pages_read", 0) for note in notes])
    pages_per_week = total_pages_left / (t/7)
    pages_per_day = total_pages_left / t
    pages_per_hour = total_pages_left / (t*int(daycalculator.sum_values)/7)
    pages_per_today = pages_per_hour * daycalculator.todayhours

    print(f"\n\n{'='*30}\n{' '*2}NOTES BY TIME INTERVAL\n{'='*30}\n")
    print(f"Time interval: {t} days")
    print(f"Total pages: {sum([note['pages'] for note in notes])}")
    print(f"Total pages read: {total_pages_read}")
    print(f"Total pages left: {total_pages_left}")
    print(f"Pages per week: {pages_per_week:.2f}")
    print(f"Pages per day: {pages_per_day:.2f}")
    print(f"Pages per hour: {pages_per_hour:.2f}")
    print(f"Pages per today: {pages_per_today:.2f}\n\n")

    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages per week':<20} {'Pages per day':<20}")
    print("-"*100)
    for note in notes:
        pages_read = note.get("pages_read", 0)
        pages_left = note["pages"] - pages_read
        pages_per_week = pages_left / (t/7)
        pages_per_day = pages_left / t
        print(f"{note['name']:<30} {pages_read:<15} {pages_left:<15} {pages_per_week:<20.2f} {pages_per_day:<20.2f}")
    input("\n\npress any key to continue......")
    clear_terminal()

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
        print("r. Remove note")
        print("m. Modify note")
        print("u. Update page")
        print("s. Show notes")
        print("f. Flush notes")
        print("v. save notes")
        print("d. show time interval")
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