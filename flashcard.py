import json
import random
from clearterminal import clear_terminal

# Global variable to store flashcards
flashcards = []


# Load data from JSON file if exists
try:
    with open('flashcards.json', 'r') as f:
        flashcards = json.load(f)
except:
    pass

# Function to add a new flashcard
def add_flashcard():
    word = input('Enter the word: ')
    meaning = input('Enter the meaning: ')
    score = 0
    flashcard = {'word': word, 'meaning': meaning, 'score': score}
    flashcards.append(flashcard)
    save_flashcards()
    clear_terminal()
    print(f'Flashcard for "{word}" added successfully!\n')

# Function to remove a flashcard
def remove_flashcard():
    word = input('\nEnter the word to remove: ')
    for flashcard in flashcards:
        if flashcard['word'] == word:
            flashcards.remove(flashcard)
            save_flashcards()
            print(f'Flashcard for "{word}" removed successfully!\n')
            return
    print(f'Flashcard for "{word}" not found!\n')


# Function to flush all flashcards
def flush_flashcards():
    confirm = input("Are you sure you want to delete all cards? (y/n) ")
    if confirm.lower() == "y":
        global flashcards
        flashcards = []
        clear_terminal()
        print("\nAll studies removed successfully. remember to save")
    else:
        clear_terminal()
        print("cancelled.\n")


# Function to show a flashcard and ask for meaning
def show_flashcard():
    # Choose a random flashcard with lower scores
    min_score = min(flashcards, key=lambda x:x['score'])['score']
    max_score = min(min_score + 3, max(flashcards, key=lambda x:x['score'])['score'] + 1)
    candidates = [flashcard for flashcard in flashcards if min_score <= flashcard['score'] < max_score]
    if not candidates:
        print('No flashcards to show!\n')
        return
    flashcard = random.choice(candidates)
    # Ask for meaning
    meaning = input(f'What is the meaning of "{flashcard["word"]}"? ')
    if meaning == flashcard['meaning']:
        flashcard['score'] += 1
        print('Correct!\n')
    else:
        flashcard['score'] -= 2
        print(f'Incorrect! The correct meaning is "{flashcard["meaning"]}".\n')
    save_flashcards()

# Function to show a random flashcard
def random_flashcard():
    if not flashcards:
        print('No flashcards to show!\n')
        return
    flashcard = random.choice(flashcards)
    print(f'The word is "{flashcard["word"]}". Its meaning is "{flashcard["meaning"]}".\n')

# Function to show flashcards sorted by score with word and meaning
def show_flashcards():
    if not flashcards:
        print('No flashcards to show!\n')
        return
    sorted_flashcards = sorted(flashcards, key=lambda x:x['score'])
    print('{:<20} {:<20} {:<10}'.format('Word', 'Meaning', 'Score'))
    for flashcard in sorted_flashcards:
        print('{:<20} {:<20} {:<10}'.format(flashcard['word'], flashcard['meaning'], flashcard['score']))

# Function to show flashcards sorted by score with word only
def show_words_only():
    if not flashcards:
        print('No flashcards to show!\n')
        return
    sorted_flashcards = sorted(flashcards, key=lambda x:x['score'])
    print('{:<20} {:<10}'.format('Word', 'Score'))
    for flashcard in sorted_flashcards:
        print('{:<20} {:<10}'.format(flashcard['word'], flashcard['score']))

# Function to save flashcards to JSON file
def save_flashcards():
    with open('flashcards.json', 'w') as f:
        json.dump(flashcards, f)

def main():
    clear_terminal()
    while True:
        print("\n||German flashcards||\n\nMenu:")
        print('a. Add flashcard')
        print('r. Remove flashcard')
        print('f. Flush all flashcards')
        print('s. Show a flashcard and ask for meaning')
        print('d. Show a random flashcard')
        print('x. Show flashcards sorted by score with word and meaning')
        print('z. Show flashcards sorted by score with word only')
        print('w. save')
        print('q. Exit')
        choice = input('\nEnter your choice: ')
        if choice == 'a':
            clear_terminal()
            add_flashcard()
        elif choice == 'r':
            clear_terminal()
            show_words_only()
            remove_flashcard()
            clear_terminal()
        elif choice == 'f':
            clear_terminal()
            flush_flashcards()
        elif choice == 's':
            clear_terminal()
            show_flashcard()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'd':
            clear_terminal()
            random_flashcard()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'x':
            clear_terminal()
            show_flashcards()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'z':
            clear_terminal()
            show_words_only()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'w':
            save_flashcards()
            clear_terminal()
            print("file saved!\n")
        elif choice == 'q':
            clear_terminal()
            break
        else:
            print('Invalid choice!')


if __name__ == '__main__':
    main()