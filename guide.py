import daycalculator
import books
import notes
import planner
import task
import flashcard
import gym
import reminder
import study
import tracker
import datetime as dt
import subjects
import videolecture
import studytask
from clearterminal import clear_terminal
import daycalculator
import weighttracker
import calendarfile3
import notebook

def main():
    clear_terminal()
    while True:
        print("{:+^80}\n".format(""))
        print("{:^80}".format("STUDY GUIDE"))
        print("{:+^80}\n".format(""))
        print("|{:<39}|{:<39}|".format(" p. plan      - day planner", " k. tasks     - university tasks"))
        print("|{:<39}|{:<39}|".format(" s. study     - study planner", " d. day       - day planner"))
        print("|{:<39}|{:<39}|".format(" r. remind    - spaced repetition", " b. books     - current books repo"))
        print("|{:<39}|{:<39}|".format(" n. notes     - current notes repo", " v. video     - video lecture"))
        print("+{:-^78}+\n".format(""))
        print("|{:<39}|{:<39}|".format(" m. german    - german flashcards", " g. gym       - exercise plan"))
        print("|{:<39}|{:<39}|".format(" h. notebook  - notebook stuff", ""))
        print("+{:-^78}+\n".format(""))
        print("|{:<39}|{:<39}|".format(" t. track     - study tracker", " u. subjects  - subject list"))
        print("|{:<39}|{:<39}|".format(" w. weight    - weight tracker", " c. calendar  - calendar program" ))
        print("|{:<39}|{:<39}|".format(" q. quit      ", " j. date      - change semester date"))
        #print("|{:^79}|".format(""))
        print("|{:+^80}|".format(" "))
        print("{:<50}{:>30}".format(f"{daycalculator.days} days left", f"Today is {daycalculator.weektoday}\n "))
        print("{:<50}{:>30}".format(f"hours in a week is {daycalculator.sum_values}, estimated work is {daycalculator.todayhours} hour and {round(books.pages_per_today)} pages.", f"\ntime left till end of the day: {daycalculator.hours} hours, {daycalculator.minutes} minutes.\n"))
        print("{:<50}{:>30}".format(f"pages per hour is at {'{0:.2f}'.format(books.pages_per_hour)}", ""))

        select = input("\n\nwhat you wanna do? :   ")

        

        if select == "p":
            clear_terminal()
            planner.main()
        elif select == "k":
            clear_terminal()
            task.main()
        elif select == "s":
            clear_terminal()
            studytask.main()
        elif select == "d":
            clear_terminal()
            study.main()
        elif select == "h":
            clear_terminal()
            notebook.main()
        elif select == "t":
            clear_terminal()
            tracker.main()
        elif select == "v":
            clear_terminal()
            videolecture.main()
            clear_terminal()  
        elif select == "r":
            clear_terminal()
            reminder.main()
        elif select == "u":
            clear_terminal()
            subjects.main()
        elif select == "b":
            clear_terminal()
            books.main()
        elif select == "m":
            clear_terminal()
            flashcard.main()
        elif select == "g":
            clear_terminal()
            gym.main()
        elif select == "c":
            clear_terminal()
            calendarfile3.main()
        elif select == "j":
            clear_terminal()
            daycalculator.save_date_to_json()
            clear_terminal()
            print("!day changed, please reload the program\n")
        elif select == "n":
            clear_terminal()
            notes.main()
        elif select == "w":
            clear_terminal()
            weighttracker.main()
        elif select == "q":
            clear_terminal()
            break


if __name__ == '__main__':
    main()