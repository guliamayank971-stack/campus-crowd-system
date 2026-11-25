file_name = "campus_crowd.csv"

default_rows = [
    ["Facility", "Date", "Time", "People", "Category"],
    ["Library", "01-10-2026", "08:30 AM", "45", "Low"],
    ["Library", "02-10-2026", "12:30 PM", "150", "Medium"],
    ["Library", "05-10-2026", "02:00 PM", "225", "Very High"],
    ["Library", "06-10-2026", "04:15 PM", "205", "High"],
    ["Canteen", "02-10-2026", "01:15 PM", "240", "Very High"],
    ["Canteen", "03-10-2026", "04:50 PM", "135", "Medium"],
    ["Canteen", "04-10-2026", "10:00 AM", "60", "Low"],
    ["Gym", "02-10-2026", "06:30 PM", "210", "High"],
    ["Gym", "03-10-2026", "07:00 AM", "80", "Low"],
    ["Gym", "05-10-2026", "05:45 PM", "165", "Medium"],
    ["Shuttle Stop", "02-10-2026", "08:45 AM", "230", "Very High"],
    ["Shuttle Stop", "03-10-2026", "04:00 PM", "55", "Low"],
]


def setup_file():
    with open(file_name, "a+", encoding="utf-8") as f:
        f.seek(0)
        if f.read().strip() == "":
            for row in default_rows:
                f.write(",".join(row) + "\n")


def get_rows():
    rows = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(line.split(","))
    return rows


def get_crowd_level(people):
    if people < 100:
        return "Low"
    elif people < 200:
        return "Medium"
    elif people < 220:
        return "High"
    else:
        return "Very High"


def add_entry():
    print("\n" + "-" * 62)
    print("               ADD NEW CAMPUS CROWD OBSERVATION")
    print("-" * 62)

    place = input("Enter Facility Name (e.g., Library, Canteen, Gym): ").strip().title()
    if not place:
        print("[ERROR] Facility name cannot be empty.")
        return

    date = input("Enter Date (DD-MM-YYYY, e.g., 15-11-2026): ").strip()
    if not date:
        print("[ERROR] Date cannot be empty.")
        return

    time_val = input("Enter Time (e.g., 12:30 PM): ").strip().upper()
    if not time_val:
        print("[ERROR] Time cannot be empty.")
        return

    people_input = input("Enter Estimated Number of People: ").strip()

    if people_input.startswith("-") and people_input[1:].isdigit():
        print("[ERROR] Number of people cannot be negative.")
        return
    if not people_input.isdigit():
        print("[ERROR] Invalid input. Enter a whole number.")
        return

    people = int(people_input)
    level = get_crowd_level(people)

    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{place},{date},{time_val},{people},{level}\n")

    print("-" * 62)
    print(f"[SUCCESS] Record Saved for {place} on {date} at {time_val}.")
    print(f"          Estimated People : {people}")
    print(f"          Crowd Category   : {level}")
    print("-" * 62)


def show_all():
    print("\n" + "=" * 68)
    print("                  ALL RECORDED CROWD OBSERVATIONS")
    print("=" * 68)

    rows = get_rows()
    if len(rows) <= 1:
        print("No crowd observations recorded yet.")
        return

    header = rows[0]
    print(f"{'No.':<5} | {header[0]:<15} | {header[1]:<12} | {header[2]:<10} | {header[3]:<8} | {header[4]:<10}")
    print("-" * 68)

    num = 1
    for row in rows[1:]:
        if len(row) >= 5:
            print(f"{num:<5} | {row[0]:<15} | {row[1]:<12} | {row[2]:<10} | {row[3]:<8} | {row[4]:<10}")
            num += 1

    print("-" * 68)
    print(f"Total Stored Observations: {len(rows) - 1}")


def check_place():
    print("\n" + "=" * 68)
    print("             FACILITY PEAK-TIME & CROWD PATTERN ANALYSIS")
    print("=" * 68)

    place = input("Enter Facility Name to Analyze (e.g., Library, Canteen, Gym): ").strip().title()
    if not place:
        print("[ERROR] Facility name cannot be empty.")
        return

    rows = get_rows()
    total = 0
    count = 0
    max_crowd = -1
    min_crowd = None
    peak_time = ""
    quiet_time = ""

    counts = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}

    for row in rows[1:]:
        if len(row) >= 5 and row[0].strip().title() == place:
            people = int(row[3])
            total += people
            count += 1

            cat = row[4].strip()
            if cat in counts:
                counts[cat] += 1

            if people > max_crowd:
                max_crowd = people
                peak_time = f"{row[1]} at {row[2]}"

            if min_crowd is None or people < min_crowd:
                min_crowd = people
                quiet_time = f"{row[1]} at {row[2]}"

    if count == 0:
        print(f"\n[INFO] No observations found for facility: '{place}'.")
        return

    avg = round(total / count, 1)
    avg_level = get_crowd_level(int(round(avg)))
    peak_level = get_crowd_level(max_crowd)
    low_level = get_crowd_level(min_crowd)

    print("-" * 68)
    print(f"FACILITY REPORT          : {place.upper()}")
    print("-" * 68)
    print(f"Total Observations       : {count}")
    print(f"Average Crowd Level      : {avg} people ({avg_level})")
    print(f"Highest Recorded Peak    : {max_crowd} people ({peak_level})")
    print(f"Peak Crowd Date & Time   : {peak_time}")
    print(f"Lowest Recorded Crowd    : {min_crowd} people ({low_level})")
    print(f"Best / Quietest Time     : {quiet_time}")
    print("-" * 68)
    print("Category Breakdown:")
    print(f"   Low (0-99)       : {counts['Low']} time(s)")
    print(f"   Medium (100-199) : {counts['Medium']} time(s)")
    print(f"   High (200-219)   : {counts['High']} time(s)")
    print(f"   Very High (220+) : {counts['Very High']} time(s)")
    print("=" * 68)


def show_summary():
    print("\n" + "=" * 75)
    print("                 ALL-CAMPUS FACILITY COMPARISON SUMMARY")
    print("=" * 75)

    rows = get_rows()
    stats = {}

    for row in rows[1:]:
        if len(row) >= 5:
            place = row[0].strip().title()
            people = int(row[3])

            if place not in stats:
                stats[place] = {"total": 0, "count": 0, "max": people, "min": people}

            stats[place]["total"] += people
            stats[place]["count"] += 1

            if people > stats[place]["max"]:
                stats[place]["max"] = people
            if people < stats[place]["min"]:
                stats[place]["min"] = people

    if not stats:
        print("No facility data available to summarize.")
        return

    print(f"{'Facility':<16} | {'Records':<8} | {'Avg Crowd':<10} | {'Peak':<8} | {'Lowest':<8} | {'Usual Status':<12}")
    print("-" * 75)

    for place, data in stats.items():
        avg = int(round(data["total"] / data["count"]))
        status = get_crowd_level(avg)
        print(f"{place:<16} | {data['count']:<8} | {avg:<10} | {data['max']:<8} | {data['min']:<8} | {status:<12}")

    print("=" * 75)


def menu():
    setup_file()

    while True:
        print("\n+================================================================+")
        print("|       CAMPUSCROWD: PEAK-TIME & CROWD ANALYSIS SYSTEM           |")
        print("|             Bennett University (2026CSAE100)                   |")
        print("+================================================================+")
        print("|  1. Add New Crowd Observation                                  |")
        print("|  2. View All Recorded Observations                             |")
        print("|  3. Analyze Specific Facility (Peak & Low Finder)              |")
        print("|  4. View All-Campus Comparison Summary                         |")
        print("|  5. Exit Program                                               |")
        print("+================================================================+")

        choice = input("Select an operation (1-5): ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            show_all()
        elif choice == "3":
            check_place()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("\nThank you for using CampusCrowd! Exiting program safely...")
            break
        else:
            print("[ERROR] Invalid selection. Please enter a number from 1 to 5.")


menu()