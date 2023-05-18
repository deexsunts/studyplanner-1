import json
import os
import PyPDF2
import daycalculator
import datetime
from clearterminal import clear_terminal

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\booknote.txt"
        editor = 'notepad'
    else:
        notes_file = os.path.expanduser("~/plannerconf/booknote.txt")
        editor = 'vim'
    os.system(f"{editor} {notes_file}")

# Initialize an empty list to hold the books
books = []

# Load the books data from a JSON file
def load_books():
    global books
    try:
        with open('books.json', 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty one
        save_books()

# Save the books data to a JSON file
def save_books():
    with open('books.json', 'w') as f:
        json.dump(books, f)

# Remove a book from the list
def remove_book():
    print_books()
    index = int(input("\n\nEnter index of book to remove: "))
    try:
        del books[index]
        clear_terminal()
        print("book removed successfully.")
    except IndexError:
        print("Invalid index.")

# Add a new book to the list
def add_book():
    name = input("\n\nEnter book name: ")
    pages = int(input("Enter number of pages: "))
    active = input("Active or Deactive? (A/D): ").upper() == "A"  # Added active status
    book = {"name": name, "pages": pages, "pages_read": 0, "active": active}  # Added active key
    books.append(book)
    save_books()  # Save the updated list of books to the JSON file
    clear_terminal()
    print("book added successfully.")

def show_on_hold_books():
    clear_terminal()
    on_hold_books = [book for book in books if not book.get('active', True)]  # Get on-hold books

    if not on_hold_books:
        clear_terminal()
        print("No books are currently on hold.\n")
        return

    print("\n\nIndex\tName\t\t\t      Pages\t\t Status")
    for i, book in enumerate(on_hold_books):
        print(f"{i}\t{book['name'].ljust(30)}{book['pages']}\t\t On Hold")

    index = int(input("\n\nEnter index of book to modify: "))
    try:
        book = on_hold_books[index]
        print("Selected book:", book["name"])
        print("Current status: On Hold")
        activate = input("Activate this book? (Y/N): ").upper() == "Y"
        book["active"] = activate
        clear_terminal()
        clear_terminal()
        print("book status modified successfully.\n")
    except IndexError:
        clear_terminal()
        print("Invalid index.")



# Display a list of all the books
def print_books():
    print("\n\nIndex\tName\t\t\t      Pages\t\t Progress")
    total_pages = sum(book['pages'] for book in books if book.get('active', True))  # Calculate total pages only for active books
    total_pages_read = sum(book.get('pages_read', 0) for book in books if book.get('active', True))  # Calculate total pages read only for active books
    progress_bar_length = 20
    progress_bar_fill = '█'

    for i, book in enumerate(books):
        if book.get('active', True):  # Only display active books
            pages_read = book.get('pages_read', 0)
            progress = int(pages_read * 100 / total_pages) if total_pages != 0 else 0
            print(f"{i}\t{book['name'].ljust(30)}{book['pages']}\t\t   {progress}%")

    progress_bar_fill_count = int(total_pages_read / total_pages * progress_bar_length)
    progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
    print(f"\nProgress: {progress_bar} {int(total_pages_read / total_pages * 100)}%")

# Show books divided into a time interval t
def show_books_by_time_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([book.get("pages_read", 0) for book in books if book.get('active', True)])  # Calculate total pages read only for active books
    total_pages_left = sum([book["pages"] - book.get("pages_read", 0) for book in books if book.get('active', True)])  # Calculate total pages left only for active books
    pages_per_week = total_pages_left / (t / 7)
    pages_per_day = total_pages_left / t
    pages_per_hour = total_pages_left / (t * int(daycalculator.sum_values) / 7)
    pages_per_today = pages_per_hour * daycalculator.todayhours

    print(f"\n\n{'='*30}\n{' '*2}bookS BY TIME INTERVAL\n{'='*30}\n")
    print(f"Time interval: {t} days")
    print(f"Total pages: {sum([book['pages'] for book in books if book.get('active', True)])}")  # Calculate total pages only for active books
    print(f"Total pages read: {total_pages_read}")
    print(f"Total pages left: {total_pages_left}")
    print(f"Pages per week: {pages_per_week:.2f}")
    print(f"Pages per day: {pages_per_day:.2f}")
    print(f"Pages per hour: {pages_per_hour:.2f}")
    print(f"Pages per today: {pages_per_today:.2f}\n\n")

    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages per week':<20} {'Pages per day':<20}")
    print("-" * 100)
    for book in books:
        if book.get('active', True):  # Only display active books
            pages_read = book.get("pages_read", 0)
            pages_left = book["pages"] - pages_read
            pages_per_week = pages_left / (t / 7)
            pages_per_day = pages_left / t
            print(
                f"{book['name']:<30} {pages_read:<15} {pages_left:<15} {pages_per_week:<20.2f} {pages_per_day:<20.2f}")
    input("\n\nPress any key to continue...")
    clear_terminal()

def modify_book():
    print_books()
    index = int(input("\n\nEnter index of book to modify: "))
    try:
        book = books[index]
        print("Selected book:", book["name"])
        print("Current number of pages:", book["pages"])
        print("Active status:", "Active" if book.get("active", True) else "Inactive")
        pages = input("Enter number of pages to add or remove: ")
        if pages != "":
            book["pages"] += int(pages)
        else:
            pass
        active = input("Activate or Deactivate? (A/D): ").upper() == "A"
        book["active"] = active
        clear_terminal()
        print("book modified successfully.")
    except IndexError:
        print("Invalid index.")


# Update the number of pages read for a book
def update_pages_read():
    clear_terminal()
    print("List of books:")
    for i, book in enumerate(books):
        print(f"{i}: {book['name']} - {book['pages']} pages")
    index = int(input("\n\nEnter the index of the book you want to update: "))
    pages_read = int(input("Enter the number of pages read: "))
    if 0 <= index < len(books):
        books[index]["pages_read"] += pages_read
        save_books()
        clear_terminal()
        print("Pages read updated successfully.")
    else:
        clear_terminal()
        print("Invalid index.")

# Save PDF books from a directory to a JSON file
def save_pdf_books(directory):
    global books
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: directory does not exist.")
        return
    # Find PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    # Add each PDF book to the books list
    for i, pdf_file in enumerate(pdf_files):
        with open(os.path.join(directory, pdf_file), 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            book_name = os.path.splitext(pdf_file)[0]
            book_pages = pdf_reader.getNumPages()
            book = {'name': book_name, 'pages': book_pages}
            books.append(book)
    # Save the books to a JSON file
    save_books()
    print(f"{len(pdf_files)} PDF books saved successfully.")



# Clear the list of books
def flush_books():
    confirm = input("Are you sure you want to delete all books? (y/n) ")
    if confirm.lower() == "y":
        global books
        books = []
        print("books flushed successfully. remember to save!")
        clear_terminal()
        print("\nAll books removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

# Load the books data from the file at program start
load_books()
clear_terminal()

# Main menu loop
def main():
    while True:
        print("\n||currently working books||\n\nMenu:")
        print("a. Add book")
        print("u. Update page")
        print("s. Show books")        
        print("d. Show time interval")
        print("n. Edit notes")
        print("h. Change Status")
        print("v. save books")
        print("f. Flush books")
        print("m. Modify book")
        print("r. Remove book")
        print("y. import books from directory.")
        print("q. Quit")
        choice = input("\nEnter choice: ")

        if choice == "a":
            clear_terminal()
            add_book()
            save_books()
        elif choice == "r":
            clear_terminal()
            remove_book()
            save_books()
        elif choice == "m":
            clear_terminal()
            modify_book()
            save_books()
        elif choice == "s":
            clear_terminal()
            print_books()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == "f":
            clear_terminal()
            flush_books()
        elif choice == "u":
            update_pages_read()
        elif choice == "d":
            clear_terminal()
            show_books_by_time_interval()
        elif choice == "v":
            clear_terminal()
            save_books()
        elif choice == "h":
            show_on_hold_books()
            save_books()
        elif choice == "h":
            clear_terminal()
            edit_notes()
        elif choice == "y":
            directory = input("Enter directory path: ")
            save_pdf_books(directory)
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")

t = int(daycalculator.days)
pages_per_hour = sum([book["pages"] for book in books]) / (t*int(daycalculator.sum_values)/7)
pages_per_today = pages_per_hour * daycalculator.todayhours

if __name__ == '__main__':
    main()