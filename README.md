# CampusCrowd: Peak-Time & Crowd Analysis System

A Python CLI application that logs, classifies, and analyzes campus facility occupancy (Library, Canteen, Gym, Shuttle Stop) using persistent CSV storage.

## Features
- **Auto-Healing CSV Storage:** Automatically creates campus_crowd.csv with 12 default seed records if missing.
- **4-Tier Classification:** Categorizes crowd levels into Low (0-99), Medium (100-199), High (200-219), and Very High (220+).
- **Input Validation:** Prevents empty entries, negative numbers, and non-numeric inputs.
- **Facility Peak-Time Analysis:** Calculates average occupancy, peak rush hour, quietest time, and category breakdown.
- **All-Campus Summary:** Compares all recorded facilities side by side in an aligned table.

## How to Run

    python3 project.py
