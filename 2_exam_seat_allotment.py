import csv
import os
import random
import utils
import hall_ticket

# --- Configuration: Exam Centers ---
EXAM_CENTERS_DATA = [
    {
        "name": "Vellore Institute of Technology", 
        "code": "VITAP", 
        "room_range": (401, 430), 
        "seat_range": (1, 45)
    },
    {
        "name": "SRM Institute of Science and Technology", 
        "code": "SRMAP", 
        "room_range": (501, 525), 
        "seat_range": (1, 50)
    },
    {
        "name": "Amrita Vishwa Vidyapeetham", 
        "code": "AVVAP", 
        "room_range": (201, 220), 
        "seat_range": (1, 55)
    }
]

def main():
    print("--- Login for Exam Seat Allotment ---")  
    
    if not os.path.exists(utils.FILENAME):
        print("Error: No data file found. Please register student first.")
        return

    while True:
        print("\n(Enter a space and hit Enter to quit)")
        search_app_id = input("Enter Application Number: ").strip()   
        
        if search_app_id == "":
            print("Exiting system...")
            break

        # 1. Load fresh data every time (Handles external updates)
        all_students = []
        try:
            with open(utils.FILENAME, 'r', newline='') as f:
                reader = csv.DictReader(f)
                all_students = list(reader)
        except Exception as e:
            print(f"Error reading file: {e}")
            continue

        # 2. Find the student
        target_student_index = -1
        for i, student in enumerate(all_students):
            if student['Application Number'] == search_app_id:
                target_student_index = i
                print(f"User found: {student['Name']}")
                break
        
        if target_student_index == -1:
            print("Error: Student Application Number not found.")
            continue

        # 3. Password Loop
        while True:
            search_password = input("Enter Password (Date of Birth (DDMMYYYY)): ").strip()
            
            if search_password == "":
                print("Login cancelled.")
                break 
            
            stored_password = all_students[target_student_index].get('Password', '')
            
            if search_password == stored_password:
                print("\nLogin Successful!")
                current_student = all_students[target_student_index]

                # Check if already allotted
                if current_student.get("Exam Centre Code") and current_student.get("Seat Number"):
                    print("\n--- You have already been allotted a Exam Centre ---")
                    print(f"Centre: {current_student['Exam Centre Name']}")
                    print(f"Room:   {current_student['Room Number']}")
                    print(f"Seat:   {current_student['Seat Number']}")
                    hall_ticket.generate_hall_ticket(current_student)
                    break

                print("Allocating seat... please wait...")

                # 4. Rebuild Occupied Seats set dynamically from current data
                # This ensures we never overwrite a seat even if the file changed recently
                occupied_seats = set()
                for s in all_students:
                    if s.get("Exam Centre Code") and s.get("Room Number") and s.get("Seat Number"):
                        occupied_seats.add((s["Exam Centre Code"], s["Room Number"], s["Seat Number"]))

                assigned = False
                max_retries = 20000
                
                for _ in range(max_retries):
                    selected_center = random.choice(EXAM_CENTERS_DATA)
                    exam_code = selected_center["code"]
                    
                    # Randomly pick room and seat within range
                    room_num = str(random.randint(selected_center["room_range"][0], selected_center["room_range"][1]))
                    seat_num = str(random.randint(selected_center["seat_range"][0], selected_center["seat_range"][1]))
                    
                    if (exam_code, room_num, seat_num) not in occupied_seats:
                        # Update in memory
                        all_students[target_student_index]["Exam Centre Name"] = selected_center["name"]
                        all_students[target_student_index]["Exam Centre Code"] = exam_code
                        all_students[target_student_index]["Room Number"] = room_num
                        all_students[target_student_index]["Seat Number"] = seat_num
                        
                        assigned = True
                        break
                
                if not assigned:
                    print("Error: Could not allocate a seat. All centers might be full.")
                    break

                # 5. Write back to file
                try:
                    with open(utils.FILENAME, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=utils.FIELDS)
                        writer.writeheader()
                        writer.writerows(all_students)
                        
                    print(f"Centre: {all_students[target_student_index]['Exam Centre Name']}")
                    print(f"Code:   {exam_code}")
                    print(f"Room:   {room_num} | Seat: {seat_num}")
                    
                    hall_ticket.generate_hall_ticket(all_students[target_student_index])
                except Exception as e:
                    print(f"Error saving data: {e}")

                break # Break out of password loop after success
            else:
                print("Incorrect Password. Try again.")

if __name__ == "__main__":
    main()