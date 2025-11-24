import csv
import os
import utils2
import allotment_letter

def admin_dashboard(all_students):

    print("\n=== ADMIN DASHBOARD: SEAT MATRIX ===")
    counts = utils2.get_current_seat_counts(all_students)
    print(f"{'Code':<6} {'Branch Name':<30} {'Filled':<8} {'Total':<8} {'Status'}")
    print("-" * 65)
    
    for key, details in utils2.BTECH_COURSES.items():
        code = details['code']
        filled = counts.get(code, 0)
        total = details['seats']
        status = "FULL" if filled >= total else "OPEN"
        print(f"{code:<6} {details['name']:<30} {filled:<8} {total:<8} {status}")
    print("=" * 65)

def main():
    print("--- Login for Seat Allotment ---")
    if not os.path.exists(utils2.FILENAME):
        try:
            with open(utils2.FILENAME, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=utils2.FIELDS)
                writer.writeheader()
            print(f"[INFO] Created new database: {utils2.FILENAME}")
        except IOError as e:
            print(f"Error creating file: {e}")
            return

    while True:
        print("\n(Enter a space and hit Enter to quit)")
        print("(Admin: Type 'ADMIN' to view Seat Matrix)")
        search_app_id = input("Enter Application Number: ").strip()
        
        all_students = []
        try:
            with open(utils2.FILENAME, 'r', newline='') as f:
                reader = csv.DictReader(f)
                all_students = list(reader)
        except FileNotFoundError:
            print("Database file not found.")
            continue
        except PermissionError:
            print("Error: The CSV file is open in another program. Please close it.")
            continue

        if search_app_id == ' ' or search_app_id == '': 
            print("Exiting...")
            break
        
        if search_app_id == "ADMIN":
            admin_dashboard(all_students)
            continue

        student_found = False
        target_index = -1

        for i, student in enumerate(all_students):
            if student['Application Number'] == search_app_id:
                student_found = True
                target_index = i
                print(f"User found: {student['Name']}")
                break
        
        if not student_found:
            print("Error: Student Application Number not found.")
            continue

        while True:
            search_password = input("Enter Password (Date of Birth DDMMYYYY): ").strip()
            if search_password == '': 
                break 
            
            if search_password == all_students[target_index].get('Password', ''):
                print("\nLogin Successful!")
                
                try:
                    rank_str = all_students[target_index].get('Rank', '99999')
                    if rank_str == 'NA':
                         student_rank = 99999
                    else:
                         student_rank = int(float(rank_str))
                except ValueError:
                    student_rank = 99999

                print(f"Your Current Rank: {student_rank}")

                current_counts = utils2.get_current_seat_counts(all_students)

                print("\n--- Available B.Tech Courses ---")
                print(f"{'No.':<4} {'Course Name':<35} {'Cutoff':<8} {'Fee':<10} {'Availability'}")
                print("-" * 75)
                
                for key, details in utils2.BTECH_COURSES.items():
                    filled = current_counts.get(details['code'], 0)
                    total = details['seats']
                    avail_str = "FULL" if filled >= total else f"{total - filled} Left"
                    print(f"{key:<4} {details['name']:<35} {details['cutoff_rank']:<8} {details['fee']:<10} {avail_str}")

                print("\nPlease select your Top 3 Preferences (enter the number 1-8):")
                selected_keys = []
                count = 1
                while count <= 3:
                    choice = input(f"Enter Preference {count}: ").strip()
                    if choice in utils2.BTECH_COURSES:
                        if choice in selected_keys:
                            print("Duplicate choice. Choose a different course.")
                        else:
                            selected_keys.append(choice)
                            count += 1
                    else:
                        print("Invalid choice. Please enter a valid number from the list.")

                final_course_code = "N/A"
                final_seat_status = "Seat Not Allotted"
                allocated_course_name = "None"
                generated_reg_no = "N/A"
                fee_status = "N/A"
                scholarship = "0%"
                fee_amount = 0

                print("\n--- Processing Allocation ---")
                
                for key in selected_keys:
                    course_obj = utils2.BTECH_COURSES[key]
                    code = course_obj['code']
                    
                    rank_ok = student_rank <= course_obj['cutoff_rank']
                    filled = current_counts.get(code, 0)
                    vacancy_ok = filled < course_obj['seats']
                    
                    if rank_ok and vacancy_ok:
                        print(f"-> Checked {course_obj['name']}: ELIGIBLE & AVAILABLE (Allocated)")
                        final_course_code = code
                        final_seat_status = "Allocated"
                        allocated_course_name = course_obj['name']
                        fee_amount = course_obj['fee']
                        
                        scholarship = utils2.get_scholarship(student_rank)
                        
                        if scholarship == "100%":
                            fee_status = "Paid (100% Scholarship)"
                        else:
                            fee_status = "Payment Pending"
                        break 
                    elif not rank_ok:
                        print(f"-> Checked {course_obj['name']}: Not Eligible (Rank > Cutoff)")
                    elif not vacancy_ok:
                        print(f"-> Checked {course_obj['name']}: Not Eligible (SEATS FULL)")

                if final_seat_status == "Allocated":
                    existing_reg = all_students[target_index].get("Registration Number", "")
                    prefix = f"25{final_course_code}"
                    
                    if existing_reg and existing_reg.startswith(prefix):
                        generated_reg_no = existing_reg
                    else:
                        max_seq = 0
                        for student in all_students:
                            reg = student.get("Registration Number", "")
                            if reg and reg.startswith(prefix):
                                try:
                                    seq_part = int(reg[len(prefix):])
                                    if seq_part > max_seq: max_seq = seq_part
                                except ValueError: 
                                    continue
                        
                        new_seq = max_seq + 1
                        generated_reg_no = f"{prefix}{new_seq:05d}"
                else:
                    generated_reg_no = "N/A"
                    fee_status = "N/A"
                    scholarship = "N/A"

                pref_names = [utils2.BTECH_COURSES[k]['name'] for k in selected_keys]
                all_students[target_index]["Course Preference"] = " > ".join(pref_names)
                all_students[target_index]["Course Code"] = final_course_code
                all_students[target_index]["Seat Status"] = final_seat_status
                all_students[target_index]["Registration Number"] = generated_reg_no
                all_students[target_index]["Fee Status"] = fee_status
                all_students[target_index]["Scholarship"] = scholarship

                try:
                    with open(utils2.FILENAME, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=utils2.FIELDS)
                        writer.writeheader()
                        writer.writerows(all_students)
                    
                    print("\n" + "="*48)
                    print(f"FINAL STATUS: {final_seat_status.upper()}")
                    if final_seat_status == "Allocated":
                        print(f"Course:       {allocated_course_name}")
                        print(f"REG NO:       {generated_reg_no}")
                        print(f"Scholarship:  {scholarship}")
                        print(f"Fee Status:   {fee_status}")
                        
                        allotment_letter.generate(all_students[target_index], fee_amount)
                        
                    print("="*48)
                    print("Data saved successfully.")
                except PermissionError:
                    print("ERROR: Could not save! Close the CSV file if it is open.")
                
                break 
            else:
                print("Incorrect Password. Try again.")

if __name__ == "__main__":
    main()