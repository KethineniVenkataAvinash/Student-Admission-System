End-to-End Student Admission & Counselling System

Project Title: Automated Student Admission & Counselling Management System

Overview
This project is a comprehensive, Python-based console application designed to simulate and automate the entire lifecycle of a university admission process. Unlike simple data entry systems, this project implements complex logic to handle the workflow from the initial Student Registration to Logistics (Exam Seat Allocation), Analytics (Ranking & Scoring), and finally Counselling (Branch Seat Allotment).
The system utilizes a centralized CSV file as a database to ensure data persistence across different modules and generates official text-based documents (Hall Tickets, Allotment Letters) as proof of record.
Features
1. Robust Registration Module
•	Data Validation: Enforces strict age limits (16-25 years), validates email formats, and prevents duplicate phone number registrations.
•	Security: Implements SHA-256 Hashing to store passwords securely in the database; no plain text passwords are stored.
2. Conflict-Free Exam Logistics
•	Randomized Allocation: Assigns Exam Centres, Room Numbers, and Seat Numbers randomly.
•	Collision Detection: Uses a set-based algorithm to ensure no two students are assigned the same seat in the same centre.
3. Logic-Based Ranking System
•	Merit Calculation: Automatically calculates entrance scores based on academic history.
•	Multi-Key Sorting: Implements a tie-breaker algorithm that ranks students by Marks (Descending) and then by Date of Birth (Ascending), giving preference to older candidates in case of a tie.
4. Dynamic Counselling & Seat Allotment
•	Live Seat Matrix: Displays real-time seat availability for B.Tech branches (CSE, ECE, EEE, etc.).
•	Rank-Based Access: Restricts course selection if the student's rank does not meet the required cutoff.
•	Greedy Allocation: Automatically assigns the student's highest preferred course based on vacancy.
5. Automated Document Generation
The system automatically generates downloadable .txt files at every stage:
•	 Registration_Slip.txt
•	 HallTicket.txt
•	 Scorecard.txt
•	 Allotment_Letter.txt
 Technologies & Tools Used
•	Programming Language: Python 3.x
•	Data Storage: CSV (Comma Separated Values) Flat File System
•	Standard Libraries:
o	csv: For CRUD operations on the database.
o	hashlib: For password encryption.
o	datetime: For age validation and timestamping.
o	random: For generating unique seat allocations.
o	os: For file path handling and validation.
Steps to Install & Run
Prerequisites
•	Ensure Python 3.10 or higher is installed on your system.
•	No external pip packages are required (uses standard library).
Installation
1.	Clone the Repository:
git clone https://github.com/KethineniVenkataAvinash/student-admission-system.git
cd student-admission-system
2.	Run the Modules Sequentially: The system follows a strict timeline. You must run the files in the following order:
Step 1: Registration
o	Run: python 1_registration_form.py
o	Action: Register a new student. This initializes the data_store.csv database. Note down the generated Application Number.
Step 2: Exam Logistics
o	Run: python 2_exam_seat_allotment.py
o	Action: Login with App ID and Password (DOB). The system will assign an exam center and generate a Hall Ticket.
Step 3: Ranking & Results
o	Run: python 3_rank_allotment.py
o	Action: (Admin Step) This script processes all students, calculates ranks, and generates Scorecards.
Step 4: Counselling
o	Run: python 4_seat_allotment.py
o	Action: Login to view the Seat Matrix. Enter your top 3 branch preferences. The system will allot a seat based on your Rank and Vacancy.
Instructions for Testing
To verify the system works as expected, try these test scenarios:
1.	Test Age Validation:
o	During registration, try entering a Date of Birth that makes the student 15 years old (e.g., current year - 15).
o	Expected Result: System should reject the entry with an error message.
2.	Test Password Hashing:
o	After registering, open the data_store.csv file in Excel or Notepad.
o	Expected Result: Look at the Password_Hash column. It should contain a long string of random characters (the hash), not the actual date of birth.
3.	Test Tie-Breaker Logic:
o	Register two students with the same 12th Percentage but different Dates of Birth.
o	Run the ranking module (3_rank_allotment.py).
o	Expected Result: The older student (earlier DOB) should have a better (lower) Rank than the younger student.
4.	Test Seat Cutoffs:
o	In the Counselling module (4_seat_allotment.py), try to choose "CSE" (Computer Science) if your rank is very high (e.g., 5000) and the cutoff is 1000.
o	Expected Result: The system should print "Not Eligible (Rank > Cutoff)" and check your next preference.

<img width="1202" height="656" alt="UML Diagrams" src="https://github.com/user-attachments/assets/6b3c3d6a-76ec-48d0-a93c-be13e4e9efe3" />
<img width="1187" height="648" alt="System Architecture Diagram" src="https://github.com/user-attachments/assets/95df27b8-f497-43a1-b722-7c51a354d9d4" />
![Sequence Diagram](https://github.com/user-attachments/assets/2e946fa6-f46a-4010-a00b-e0bc842b5fe1)
<img width="1017" height="691" alt="scorecard" src="https://github.com/user-attachments/assets/ebde74f7-bf76-4265-b0f2-c9367f73d18a" />
<img width="1599" height="872" alt="Schema Design" src="https://github.com/user-attachments/assets/e942222f-6926-49af-9ffe-7743e031b374" />
<img width="975" height="453" alt="recipt" src="https://github.com/user-attachments/assets/448b15f9-70e9-421f-92a7-e31ba75e4c46" />
![Process Flow or Workflow Diagram](https://github.com/user-attachments/assets/4619f408-6764-47e8-a611-4e4f63b234d7)
<img width="1023" height="799" alt="hall_ticket" src="https://github.com/user-attachments/assets/9b75763c-5ced-4008-8f7f-2ed22c99a16e" />
<img width="1618" height="883" alt="ER Diagram" src="https://github.com/user-attachments/assets/618ebd66-5e7e-427f-bff9-f556ab20245e" />
![Component Diagram](https://github.com/user-attachments/assets/4cdd25c7-68fb-449b-be7b-879020a06ad9)
<img width="1172" height="639" alt="Class Diagram" src="https://github.com/user-attachments/assets/f449a89c-c570-4b64-ba58-3a86cae33664" />
<img width="983" height="990" alt="allotment letter" src="https://github.com/user-attachments/assets/f7aeb216-f37c-41f8-9998-1df5e4aa0b6c" />
<img width="1764" height="1422" alt="4_output" src="https://github.com/user-attachments/assets/53841af4-867e-49d4-9835-5762fc46ea9c" />
<img width="1762" height="651" alt="3_output" src="https://github.com/user-attachments/assets/c79e407d-1f9a-4f01-acbc-4412a54a1500" />
<img width="1852" height="547" alt="2_output" src="https://github.com/user-attachments/assets/9a088daa-14b6-4a33-b85e-d28b602aa1b6" />
<img width="1831" height="1470" alt="1_output" src="https://github.com/user-attachments/assets/ab76a800-bd50-412d-a1b1-7843c5eae280" />

Project Structure
Plaintext
├── 1_registration_form.py    # Main Entry: Student Data Collection
├── 2_exam_seat_allotment.py  # Logistics: Center & Seat Assignment
├── 3_rank_allotment.py       # Analytics: Scoring & Global Ranking
├── 4_seat_allotment.py       # Final Stage: Counseling & Branch Selection
├── utils.py                  # Shared Helper Functions & Constants
├── allotment_letter.py       # Doc Generator: Allotment Letter
├── hall_ticket.py            # Doc Generator: Hall Ticket
├── registration_slip.py      # Doc Generator: Receipt
├── scorecard_generator.py    # Doc Generator: Result Card
├── data_store.csv            # Central Database (Auto-generated)
└── README.md                 # Project Documentation
 License
This project is open-source and available under the MIT License.

