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


def main():
    while True:
        clear_terminal()
        print("{:+^80}\n".format(""))
        print("{:^80}".format("STUDY GUIDE"))
        print("{:+^80}\n".format(""))
        print("|{:<39}|{:<39}|".format(" p. plan      - day planner", " t. tasks     - university tasks"))
        print("|{:<39}|{:<39}|".format(" s. study     - study planner", " d. day       - day planner"))
        print("|{:<39}|{:<39}|".format(" r. remind    - spaced repetition", " b. books     - current books repo"))
        print("|{:<39}|{:<39}|".format(" n. notes     - current notes repo", " v. video     - video lecture"))
        print("+{:-^78}+\n".format(""))
        print("|{:<39}|{:<39}|".format(" m. german    - german flashcards", " g. gym       - exercise plan"))
        print("+{:-^78}+\n".format(""))
        print("|{:<39}|{:<39}|".format(" c. track     - study tracker", " u. subjects  - subject list"))
        print("|{:<39}|{:<39}|".format(" q. quit      ", ""))
        print("{:+^80}\n".format(""))
        print("{:<50}{:>30}".format(f"{daycalculator.days} days left", f"hours in a week is {daycalculator.sum_values}\n"))
        print("{:<50}{:>30}".format(f"Today is {daycalculator.weektoday}, estimated work is {daycalculator.todayhours} hour and {round(books.pages_per_today)} pages.", f"\ntime left till end of the day: {daycalculator.hours} hours, {daycalculator.minutes} minutes.\n"))
        print("{:<50}{:>30}".format(f"pages per hour is at {'{0:.2f}'.format(books.pages_per_hour)}", ""))
        select = input("\n\nwhat you wanna do? :   ")

        

        if select == "p":
            clear_terminal()
            planner.main()
        elif select == "t":
            clear_terminal()
            task.main()
        elif select == "s":
            clear_terminal()
            studytask.main()
        elif select == "d":
            clear_terminal()
            study.main()
        elif select == "c":
            clear_terminal()
            tracker.main()
        elif select == "v":
            clear_terminal()
            videolecture.main()    
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
        elif select == "n":
            clear_terminal()
            notes.main()
        elif select == "q":
            clear_terminal()
            break


if __name__ == '__main__':
    main()