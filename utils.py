import csv
import os
import re
import hashlib
from datetime import date, datetime

FILENAME = "data_store.csv"

FIELDS = ["Name", "Date of Birth", "Age", "Gender", "Address", "Email", 
          "12th School Name", "12th Course", "12th Percentage", 
          "Phone Number", "Application Number", "Password_Hash", "Password", 
          "Exam Centre Name", "Exam Centre Code", "Room Number", 
          "Seat Number", "Marks", "Rank", "Status", "Scholarship"]

def get_valid_date(date_str):
    if not date_str: return datetime.max 
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return datetime.max

def get_occupied_seats():
    occupied = set()
    if not os.path.exists(FILENAME):
        return occupied
        
    with open(FILENAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Exam Centre Code") and row.get("Room Number") and row.get("Seat Number"):
                seat_combo = (row["Exam Centre Code"], row["Room Number"], row["Seat Number"])
                occupied.add(seat_combo)
    return occupied

def is_phone_number_taken(phone_number):
    if not os.path.exists(FILENAME): return False
    with open(FILENAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Phone Number'] == phone_number: return True
    return False

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_menu_choice(field_name, options_list):
    print(f"\nSelect {field_name}:")
    for index, option in enumerate(options_list, 1):
        print(f"{index}. {option}")
    while True:
        choice = input(f"Enter option number (1-{len(options_list)}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options_list):
                return options_list[idx]
        print("Invalid selection. Try again.")
        