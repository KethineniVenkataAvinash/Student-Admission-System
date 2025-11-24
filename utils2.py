import csv
import os
from datetime import datetime

FILENAME = 'data_store.csv'

FIELDS = [
    "Name", "Date of Birth", "Age", "Gender", "Address", "Email", "12th School Name", 
    "12th Course", "12th Percentage", "Phone Number", "Application Number", "Password_Hash", 
    "Password", "Exam Centre Name", "Exam Centre Code", "Room Number", 
    "Seat Number", "Marks", "Rank", "Status", "Course Preference", 
    "Course Code", "Seat Status", "Registration Number", "Fee Status", "Scholarship"
]

BTECH_COURSES = {
    "1": {"name": "Computer Science (CSE Core)",       "code": "CSE", "cutoff_rank": 1000,  "seats": 700,  "fee": 250000},
    "2": {"name": "CSE (AI and ML)",                   "code": "CSM", "cutoff_rank": 1500,  "seats": 700,  "fee": 250000},
    "3": {"name": "Electronics & Comm (ECE)",          "code": "ECE", "cutoff_rank": 3500,  "seats": 500, "fee": 200000},
    "4": {"name": "Electrical Engineering (EEE)",      "code": "EEE", "cutoff_rank": 7500,  "seats": 450, "fee": 180000},
    "5": {"name": "CSE (Cyber Security)",              "code": "CSC", "cutoff_rank": 15000, "seats": 350,  "fee": 165000},
    "6": {"name": "Information Technology (IT)",       "code": "ITT", "cutoff_rank": 17500, "seats": 300, "fee": 150000},
    "7": {"name": "Mechanical Engineering (ME)",       "code": "MEC", "cutoff_rank": 20000, "seats": 400, "fee": 140000},
    "8": {"name": "Civil Engineering (CE)",            "code": "CES", "cutoff_rank": 25000, "seats": 600, "fee": 130000}
}

def calculate_age_from_str(dob_str):
    try:
        birth_date = datetime.strptime(dob_str, "%d%m%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return str(age)
    except (ValueError, TypeError):
        return "N/A"

def get_scholarship(rank):
    if rank <= 500: return "100%"
    elif rank <= 2000: return "50%"
    elif rank <= 5000: return "25%"
    return "0%"

def get_current_seat_counts(all_students):
    counts = {details['code']: 0 for details in BTECH_COURSES.values()}
    for student in all_students:
        code = student.get("Course Code")
        status = student.get("Seat Status")
        if code in counts and status == "Allocated":
            counts[code] += 1
    return counts