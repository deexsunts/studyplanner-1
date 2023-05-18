import json
import matplotlib.pyplot as plt
from datetime import datetime, date
from clearterminal import clear_terminal

def save_data(data):
    with open('weight_data.json', 'w') as file:
        json.dump(data, file)


def load_data():
    try:
        with open('weight_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


def add_entry(data):
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    weight = float(input("\nEnter the weight: "))

    entry = {"date": date_str, "weight": weight}
    data.append(entry)
    save_data(data)
    clear_terminal()
    print("Entry saved successfully.")


def plot_graph(data):
    dates = [datetime.strptime(entry["date"], "%Y-%m-%d") for entry in data]
    weights = [entry["weight"] for entry in data]

    plt.plot(dates, weights)
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.title("Weight Tracker")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    clear_terminal()


def main():
    clear_terminal()
    data = load_data()

    while True:
        save_data(data)
        print("\n=== Weight Tracker Menu ===")
        print("a. Add weight entry")
        print("s. Save data")
        print("l. Load data")
        print("p. Plot weight graph")
        print("q. Exit")

        choice = input("Enter your choice: ")

        if choice == "a":
            add_entry(data)
            clear_terminal()
        elif choice == "s":
            save_data(data)
            clear_terminal()
        elif choice == "l":
            data = load_data()
            clear_terminal()
        elif choice == "p":
            plot_graph(data)
            clear_terminal()
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
