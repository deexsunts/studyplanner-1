import json
import os
import PyPDF2
import daycalculator
import datetime
from clearterminal import clear_terminal

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

# Add a new book to the list
def add_book():
    name = input("\n\nEnter book name: ")
    pages = int(input("Enter number of pages: "))
    book = {"name": name, "pages": pages, "pages_read": 0} # Added pages_read key with initial value 0
    books.append(book)
    save_books() # Save the updated list of books to the JSON file
    clear_terminal()
    print("Book added successfully.")


# Remove a book from the list
def remove_book():
    print_books()
    index = int(input("\n\nEnter index of book to remove: "))
    try:
        del books[index]
        clear_terminal()
        print("Book removed successfully.")
    except IndexError:
        print("Invalid index.")

# Modify the number of pages of a book in the list
def modify_book():
    print_books()
    index = int(input("\n\nEnter index of book to modify: "))
    try:
        book = books[index]
        print("Selected book:", book["name"])
        print("Current number of pages:", book["pages"])
        pages = int(input("Enter number of pages to add or remove: "))
        book["pages"] += pages
        clear_terminal()
        print("Book modified successfully.")
    except IndexError:
        print("Invalid index.")
    except ValueError:
        print("Invalid number of pages.")

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

# Display a list of all the books
def print_books():
    print("\n\nIndex\tName\t\t\t      Pages\t\t Progress")
    for i, book in enumerate(books):
        pages_read = book.get('pages_read', 0)  # get pages_read value, default to 0 if not present
        progress = int(pages_read * 100 / book['pages']) if book['pages'] != 0 else 0  # calculate progress percentage
        print(f"{i}\t{book['name'].ljust(30)}{book['pages']}\t\t   {progress}%")

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

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\booknote.txt"
        editor = 'notepad'
    else:
        notes_file = os.path.expanduser("~/plannerconf/booknote.txt")
        editor = 'vim'
    os.system(f"{editor} {notes_file}")

# Show books divided into a time interval t
def show_books_by_time_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([book.get("pages_read", 0) for book in books])
    total_pages_left = sum([book["pages"] - book.get("pages_read", 0) for book in books])
    pages_per_week = total_pages_left / (t/7)
    pages_per_day = total_pages_left / t
    pages_per_hour = total_pages_left / (t*int(daycalculator.sum_values)/7)
    pages_per_today = pages_per_hour * daycalculator.todayhours

    print(f"\n\n{'='*30}\n{' '*2}BOOKS BY TIME INTERVAL\n{'='*30}\n")
    print(f"Time interval: {t} days")
    print(f"Total pages: {sum([book['pages'] for book in books])}")
    print(f"Total pages read: {total_pages_read}")
    print(f"Total pages left: {total_pages_left}")
    print(f"Pages per week: {pages_per_week:.2f}")
    print(f"Pages per day: {pages_per_day:.2f}")
    print(f"Pages per hour: {pages_per_hour:.2f}")
    print(f"Pages per today: {pages_per_today:.2f}\n\n")

    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages per week':<20} {'Pages per day':<20}")
    print("-"*100)
    for book in books:
        pages_read = book.get("pages_read", 0)
        pages_left = book["pages"] - pages_read
        pages_per_week = pages_left / (t/7)
        pages_per_day = pages_left / t
        print(f"{book['name']:<30} {pages_read:<15} {pages_left:<15} {pages_per_week:<20.2f} {pages_per_day:<20.2f}")
    input("\n\npress any key to continue......")
    clear_terminal()


# Clear the list of books
def flush_books():
    confirm = input("Are you sure you want to delete all books? (y/n) ")
    if confirm.lower() == "y":
        global books
        books = []
        print("Books flushed successfully. remember to save!")
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
        print("r. Remove book")
        print("m. Modify book")
        print("u. Update page")
        print("s. Show books")
        print("n. Show notes")
        print("f. Flush books")
        print("v. save books")
        print("d. show time interval")
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
        elif choice == "n":
            edit_notes()
            clear_terminal()
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