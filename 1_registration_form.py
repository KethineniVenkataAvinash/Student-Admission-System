import csv
import os
from datetime import datetime, date  # Changed import for better parsing
import registration_slip
import utils

FILENAME = "data_store.csv"

FIELDS = ["Name", "Date of Birth", "Age", "Gender", "Address", "Email", 
          "12th School Name", "12th Course", "12th Percentage", 
          "Phone Number", "Application Number", "Password_Hash", "Password"]

def initialize_file():
    if not os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
        except IOError as e:
            print(f"Error creating database: {e}")

def add_new_admission():
    print("\n--- New Admission Entry ---")
    phone_input = input("Phone Number (Enter space to cancel): ")
    if phone_input.strip() == "": return

    phone_number = phone_input.strip()
    # Assuming utils.is_phone_number_taken handles file not existing gracefully
    if utils.is_phone_number_taken(phone_number):
        print(f"Error: Phone Number {phone_number} already registered!")
        return

    while True:
        email = input("Email Address: ").strip()
        if utils.is_valid_email(email): break
        print("Invalid Email format! (Example: student@gmail.com)")
    
    name = input("Student Name: ")
    
    # --- FIX 1: Robust Date Parsing ---
    dob_input = input("Date of Birth (DD/MM/YYYY): ")
    try:
        # strict parsing ensures format is exactly DD/MM/YYYY
        birth_date_obj = datetime.strptime(dob_input, "%d/%m/%Y").date()
        age = utils.calculate_age(birth_date_obj)
        print(f"Age: {age}")
        
        day, month, year = birth_date_obj.day, birth_date_obj.month, birth_date_obj.year
    except ValueError:
        print("Error: Invalid Date Format. Please use DD/MM/YYYY exactly.")
        return

    # --- FIX 2: Dynamic Age Check (No hardcoded years) ---
    if age < 16 or age > 25:
        print(f"Error: Not Eligible based on Age ({age}). Must be between 16 and 25.")
        return
            
    date_of_birth = dob_input # Keep original string format
    gender = utils.get_menu_choice("Gender", ["Male", "Female", "Other"])
    
    address = input("Address: ")
    school_name = input("12th School Name: ")
    course = utils.get_menu_choice("Course", ["MPC", "BiPC", "MEC", "CEC", "HEC", "MBiPC"])
    
    try:
        percentage = float(input("12th Percentage (%): ")) 
    except ValueError:
        print("Error: Invalid number.")
        return

    if percentage > 100 or percentage <= 0: # Adjusted lower bound check
        print("Error: Invalid percentage.")
        return
    
    # ID Generation Logic
    next_id_num = 1
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        try:
            with open(FILENAME, mode='r', newline='') as file:
                reader = list(csv.DictReader(file)) 
                if reader:
                    last_id = reader[-1].get("Application Number", "")
                    # Ensure ID format matches expected length before slicing
                    if len(last_id) > 5:
                        next_id_num = int(last_id[5:]) + 1
        except Exception:
            pass # Default to 1 if read fails
    
    new_app_id = f"25142{next_id_num:05d}"
    raw_password = f"{day:02d}{month:02d}{year}" 
    secure_password_hash = utils.hash_password(raw_password)

    data_store = {
        "Name": name, 
        "Date of Birth": date_of_birth, 
        "Age": age,
        "Gender": gender, 
        "Address": address, 
        "Email": email,
        "12th School Name": school_name, 
        "12th Course": course,
        "12th Percentage": percentage, 
        "Phone Number": phone_number,
        "Application Number": new_app_id, 
        "Password_Hash": secure_password_hash,
        "Password" : raw_password
    }

    try:
        with open(FILENAME, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writerow(data_store)
            print(f"\n Student Application Number: {new_app_id}")
        registration_slip.generate_receipt(data_store, raw_password)
    except IOError:
        print("Error: Could not save data. Is the file open in Excel?")

def search_student():
    if not os.path.exists(FILENAME):
        print("\n[ERROR] Database empty.")
        return

    search_id = input("\nEnter Application Number to Search: ").strip()
    found = False

    with open(FILENAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Application Number'] == search_id:
                print("\n--- RECORD FOUND ---")
                print(f"Name:   {row['Name']}")
                print(f"Age:    {row['Age']}")
                print(f"Email:  {row['Email']}")
                print(f"Phone:  {row['Phone Number']}")
                print(f"Course: {row['12th Course']}")
                print(f"Status: Active")
                found = True
                break
    
    if not found:
        print(f"\n[INFO] No student found with ID: {search_id}")

def update_student():
    if not os.path.exists(FILENAME):
        print("\n[ERROR] Database empty.")
        return

    target_id = input("\nEnter Application Number to UPDATE: ").strip()
    rows = []
    found = False
    updated_this_session = False 
    
    with open(FILENAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Application Number'] == target_id:
                found = True
                print(f"Updating Record for: {row['Name']}")
                print("1. Phone Number")
                print("2. Address")
                print("3. Email")
                choice = input("What do you want to update? (1-3): ")
                
                # --- FIX 3: Validation inside update ---
                if choice == '1':
                    new_val = input("Enter new Phone Number: ")
                    row['Phone Number'] = new_val
                    updated_this_session = True
                elif choice == '2':
                    new_val = input("Enter new Address: ")
                    row['Address'] = new_val
                    updated_this_session = True
                elif choice == '3':
                    new_val = input("Enter new Email: ")
                    if utils.is_valid_email(new_val):
                        row['Email'] = new_val
                        updated_this_session = True
                    else:
                        print("Invalid Email. Update failed.")
                else:
                    print("Invalid choice. No changes made.")
            
            rows.append(row)

    if found and updated_this_session:
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print("[SUCCESS] Database file updated.")
    elif found and not updated_this_session:
        print("[INFO] No changes were made.")
    else:
        print("[ERROR] Student ID not found.")

def delete_student():
    if not os.path.exists(FILENAME):
        print("\n[ERROR] Database empty.")
        return

    target_id = input("\nEnter Application Number to DELETE: ").strip()
    rows = []
    found = False
    
    with open(FILENAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Application Number'] == target_id:
                found = True
                print(f"Deleting record for {row['Name']}...")
                # Delete receipt if it exists
                receipt_file = f"{target_id}_receipt.txt"
                if os.path.exists(receipt_file):
                    try: 
                        os.remove(receipt_file)
                    except: 
                        pass # Ignore error if file is open
            else:
                rows.append(row)
    
    if found:
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print("[SUCCESS] Student record deleted permanently.")
    else:
        print("[ERROR] Student ID not found.")

def show_analytics():
    if not os.path.exists(FILENAME):
        print("\nNo data available.")
        return

    male_count = 0
    female_count = 0
    total_score = 0
    count = 0

    with open(FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            count += 1
            if row['Gender'] == 'Male': male_count += 1
            elif row['Gender'] == 'Female': female_count += 1
            try: total_score += float(row['12th Percentage'])
            except: pass

    if count > 0:
        avg = total_score / count
        print(f"\n--- CLASS ANALYTICS ---")
        print(f"Total Students : {count}")
        print(f"Gender Split   : {male_count} Males | {female_count} Females")
        print(f"Avg Percentage : {avg:.2f}%")
    else:
        print("Not enough data.")

def main():
    initialize_file()
    while True:
        print("\n========================================")
        print("        STUDENT MANAGEMENT SYSTEM   ")
        print("========================================")
        print("1. Add New Admission")
        print("2. Search Student Details")
        print("3. Update Student Details")
        print("4. Delete Student Record")
        print("5. Show Class Analytics")
        print("6. Exit")
        choice = input("\nEnter choice (1-6): ")

        if choice == '1':
            add_new_admission()
        elif choice == '2':
            search_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            show_analytics()
        elif choice == '6':
            print("Exiting from Student Management System")
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()