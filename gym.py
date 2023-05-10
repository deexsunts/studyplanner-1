import json
import datetime
from clearterminal import clear_terminal

def read_exercise_plan():
    try:
        with open('exercise_plan.json') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create a new exercise plan
        plan = {
            '0': 'Cardio',
            '1': 'Yoga',
            '2': 'Strength training',
            '3': 'Rest day',
            '4': 'Cardio',
            '5': 'Yoga',
            '6': 'Strength training'
        }
        save_exercise_plan(plan)
        return plan

def save_exercise_plan(plan):
    with open('exercise_plan.json', 'w') as f:
        json.dump(plan, f)

def show_today(plan):
    print("\n\n")
    today = datetime.datetime.today()
    today1 = today + datetime.timedelta(days=0)
    today_index = today1.weekday()
    exercise = plan[str(today_index)]
    print(f"Today is {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][today_index]} and your exercise is: {exercise}")
    a= input("\n\n\npress enter to continue (q to exit)........")
    if a == "q":
        clear_terminal()
        exit()
    clear_terminal()

def modify_exercises(plan):
    clear_terminal()
    print("")
    show_plan(plan)
    day = int(input("\n\nWhich day do you want to modify (0 for Saturday, 6 for Friday)? "))
    if day < 0 or day > 6:
        print("Invalid day index!")
        return
    new_exercise = input(f"What is your new exercise for {['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][day]}? ")
    plan[str(day)] = new_exercise
    clear_terminal()
    print("Exercise modified successfully!")

def show_plan(plan):
    print("{:<10} {:<20}".format('Day', 'Exercise'))
    print("==============================")
    for day, exercise in plan.items():
        print("{:<10} {:<20}".format(day, exercise))

def current():
    plan = read_exercise_plan()
    today = datetime.datetime.today()
    today1 = today + datetime.timedelta(days=0)
    today_index = today1.weekday()
    exercise = plan[str(today_index)]
    return exercise

def main():
    clear_terminal()
    plan = read_exercise_plan()
    while True:
        print("\n||gym plan||\n\nMenu:")
        print("s. Show today's day and exercise")
        print("m. Modify exercises for each day")
        print("v. Save the modification")
        print("d. Show full exercises within the week in a chart")
        print("q. Quit")
        choice = input("\nEnter your choice: ").lower()
        if choice == 's':
            clear_terminal()
            show_today(plan)
        elif choice == 'm':
            modify_exercises(plan)
        elif choice == 'v':
            clear_terminal()
            save_exercise_plan(plan)
            print("Exercise plan saved successfully!")
        elif choice == 'd':
            clear_terminal()
            show_plan(plan)
        elif choice == 'q':
            clear_terminal()
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()