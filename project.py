import csv
import os

FILENAME = "campus_crowd.csv"

DEFAULT_DATA = [
    ["Facility", "Date", "Time", "People", "Category"],
    ["Library", "01-10-2026", "08:30 AM", "45", "Low"],
    ["Library", "02-10-2026", "12:30 PM", "150", "Medium"],
    ["Library", "05-10-2026", "02:00 PM", "225", "Very High"],
    ["Library", "04-10-2026", "10:00 AM", "190", "Medium"],
    ["Library", "06-10-2026", "04:30 PM", "215", "High"],
    ["Canteen", "02-10-2026", "01:15 PM", "240", "Very High"],
    ["Canteen", "03-10-2026", "04:00 PM", "60", "Low"],
    ["Gym", "02-10-2026", "06:30 PM", "210", "High"],
    ["Gym", "03-10-2026", "07:00 AM", "80", "Low"],
    ["Gym", "04-10-2026", "05:30 PM", "165", "Medium"],
    ["Canteen", "05-10-2026", "08:30 AM", "135", "Medium"],
    ["Shuttle Stop", "02-10-2026", "09:00 AM", "230", "Very High"],
    ["Shuttle Stop", "03-10-2026", "03:00 PM", "55", "Low"],
]


def initialize_csv():
    if not os.path.isfile(FILENAME):
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(DEFAULT_DATA)


def classify_crowd(people):
    if people < 100:
        return "Low"
    elif people < 200:
        return "Medium"
    elif people < 220:
        return "High"
    else:
        return "Very High"


def add_observation():
    print("\nAdd new observation")
    facility = input("Facility: ").strip().title()
    if not facility:
        print("[ERROR] Facility cannot be empty.")
        return

    date = input("Date (DD-MM-YYYY): ").strip()
    time_obs = input("Time (eg 01:15 PM): ").strip().upper()
    raw_people = input("Number of people: ").strip()

    try:
        people = int(raw_people)
        if people < 0:
            print("[ERROR] Cannot be negative.")
            return
    except ValueError:
        print("[ERROR] Enter a whole number.")
        return

    category = classify_crowd(people)

    with open(FILENAME, mode="a", newline="") as file:
        csv.writer(file).writerow([facility, date, time_obs, people, category])

    print("Saved:", facility, date, time_obs, people, category)


def view_records():
    with open(FILENAME, mode="r", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    header = rows[0]
    print(f"\n{'No.':<5} | {header[0]:<15} | {header[1]:<12} | {header[2]:<10} | {header[3]:<8} | {header[4]:<10}")
    print("-" * 70)

    for idx, row in enumerate(rows[1:], start=1):
        if len(row) >= 5:
            print(f"{idx:<5} | {row[0]:<15} | {row[1]:<12} | {row[2]:<10} | {row[3]:<8} | {row[4]:<10}")

    print(f"\nTotal Stored Observations: {len(rows) - 1}")


def analyze_facility():
    target = input("Enter Facility: ").strip().title()

    total_people = 0
    count = 0
    highest_crowd = -1
    lowest_crowd = float("inf")
    peak_period = ""
    low_period = ""
    category_counts = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}

    with open(FILENAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header

        for row in reader:
            if len(row) >= 5 and row[0].strip().title() == target:
                people = int(row[3])
                total_people += people
                count += 1
                category_counts[row[4].strip()] += 1

                if people > highest_crowd:
                    highest_crowd = people
                    peak_period = f"{row[1]} at {row[2]}"
                if people < lowest_crowd:
                    lowest_crowd = people
                    low_period = f"{row[1]} at {row[2]}"

    if count == 0:
        print("No records found for", target)
        return

    avg_crowd = round(total_people / count, 1)
    avg_category = classify_crowd(int(round(avg_crowd)))

    print(f"\nReport for {target}")
    print("Records:", count)
    print("Average crowd:", avg_crowd, f"({avg_category})")
    print("Peak:", highest_crowd, "on", peak_period)
    print("Quietest:", lowest_crowd, "on", low_period)
    print("Category breakdown:")
    for cat, num in category_counts.items():
        print(f"  {cat}: {num}")


def campus_summary():
    stats = {}

    with open(FILENAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) < 5:
                continue
            fac = row[0].strip().title()
            people = int(row[3])

            if fac not in stats:
                stats[fac] = {"total": 0, "count": 0, "max": people, "min": people}

            stats[fac]["total"] += people
            stats[fac]["count"] += 1
            if people > stats[fac]["max"]:
                stats[fac]["max"] = people
            if people < stats[fac]["min"]:
                stats[fac]["min"] = people

    print(f"\n{'Facility':<15} | {'Records':<8} | {'Avg Crowd':<10} | {'Peak':<6} | {'Lowest':<7} | Status")
    print("-" * 70)
    for fac, d in stats.items():
        avg = int(round(d["total"] / d["count"]))
        print(f"{fac:<15} | {d['count']:<8} | {avg:<10} | {d['max']:<6} | {d['min']:<7} | {classify_crowd(avg)}")


def main():
    initialize_csv()
    while True:
        print("\n1. Add record")
        print("2. View records")
        print("3. Analyze facility")
        print("4. Campus summary")
        print("5. Exit")
        choice = input("Select (1-5): ").strip()

        if choice == "1":
            add_observation()
        elif choice == "2":
            view_records()
        elif choice == "3":
            analyze_facility()
        elif choice == "4":
            campus_summary()
        elif choice == "5":
            print("Exiting safely...")
            break
        else:
            print("[ERROR] Enter 1 to 5.")


main()
