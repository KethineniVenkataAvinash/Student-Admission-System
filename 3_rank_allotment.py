import csv
import os
import utils
import scorecard_generator

def process_all_ranks(all_students):
    # 1. Calculate Scores
    for student in all_students:
        try:
            pct = float(student.get("12th Percentage", "0"))
        except ValueError:
            pct = 0.0
        
        # Logic: Base score is Percentage + 20, capped at 120
        marks = min(120, pct + 20)
        
        if marks >= 60:
            status = "Qualified"
        else:
            status = "Not Qualified"
            
        scholarship = "None"
        if marks >= 117:
            scholarship = "Merit Scholarship (100% Fee Waiver)"
        elif marks >= 100:
            scholarship = "Dean's List (50% Fee Waiver)"

        student["Marks"] = marks
        student["Status"] = status
        student["Scholarship"] = scholarship

    # 2. Sort (Primary: Marks Descending, Secondary: Age/DOB Ascending)
    # Note: We use a helper to safely parse date for sorting
    def get_sort_key(s):
        m = s["Marks"]
        d = utils.get_valid_date(s.get("Date of Birth"))
        # If date is invalid/None, put them last (max date)
        if d is None:
            import datetime
            d = datetime.date.max 
        return (-m, d)

    sorted_students = sorted(all_students, key=get_sort_key)

    # 3. Assign Ranks
    current_rank = 1
    for student in sorted_students:
        if student["Status"] == "Qualified":
            student["Rank"] = current_rank
            current_rank += 1
        else:
            student["Rank"] = "NA"
            
    return sorted_students

def main():
    print("--- Login for Rank Details ---")
    if not os.path.exists(utils.FILENAME):
        print("Error: Database file not found. Please register students first.")
        return
    
    all_students = []
    try:
        with open(utils.FILENAME, 'r', newline='') as f:
            reader = csv.DictReader(f)
            all_students = list(reader)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Process ranks
    all_students = process_all_ranks(all_students)

    # --- CRITICAL FIX: Update Headers ---
    # We must ensure the CSV writer knows about the new columns we just added.
    current_fields = list(all_students[0].keys()) if all_students else utils.FIELDS
    
    # Ensure standard order but include new fields
    output_fields = [f for f in utils.FIELDS if f in current_fields]
    for field in ["Marks", "Status", "Scholarship", "Rank"]:
        if field not in output_fields:
            output_fields.append(field)

    try:
        with open(utils.FILENAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=output_fields)
            writer.writeheader()
            writer.writerows(all_students)
    except IOError:
        print("Warning: Could not save ranks to file. Is the CSV open in Excel?")

    # --- Login Loop ---
    while True:
        print("\n(Enter a space and hit Enter to quit)")
        search_app_id = input("Enter Application Number: ").strip()
        
        if search_app_id == "":
            break

        target_student = None
        for student in all_students:
            if student['Application Number'] == search_app_id:
                target_student = student
                print(f"User found: {student['Name']}")
                break
        
        if not target_student:
            print("Error: Student Application Number not found.")
            continue

        while True:
            search_password = input("Enter Password (Date of Birth (DDMMYYYY)): ").strip()
            if search_password == "":
                break 
            
            stored_pass = target_student.get('Password', '')
            
            if search_password == stored_pass:
                print("\nLogin Successful!")
                print("-----------------------------------")
                print(f" Name:        {target_student['Name']}")
                print(f" Result:      {target_student['Status']}")
                print(f" Marks:       {target_student['Marks']} / 120")
                print(f" Global Rank: {target_student['Rank']}")
                
                if target_student.get("Scholarship") != "None":
                    print(f" Scholarship: {target_student['Scholarship']}!")
                print("-----------------------------------")

                # Generate visual scorecard
                scorecard_generator.generate_scorecard(target_student)
                break 
            else:
                print("Incorrect Password. Try again.")

if __name__ == "__main__":
    main()