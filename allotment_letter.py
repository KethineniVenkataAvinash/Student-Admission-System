from datetime import datetime
import utils2

def generate(student, fee_amount):
    filename = f"Allotment_Letter_{student['Application Number']}.txt"
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    course_name = "N/A"
    for v in utils2.BTECH_COURSES.values():
        if v['code'] == student['Course Code']:
            course_name = v['name']

    with open(filename, "w") as f:
        f.write("======================================================\n")
        f.write("        PROVISIONAL SEAT ALLOTMENT LETTER  \n")
        f.write("======================================================\n")
        f.write(f"Date Issued   : {timestamp}\n")
        f.write(f"Application No : {student['Application Number']}\n")
        f.write(f"Candidate Name : {student['Name']}\n")
        f.write(f"Date of Birth  : {student['Date of Birth']} (Age: {student['Age']})\n")
        f.write(f"All India Rank : {student['Rank']}\n")
        f.write("------------------------------------------------------\n")
        f.write("             ALLOTMENT DETAILS \n")
        f.write("------------------------------------------------------\n")
        f.write(f"Seat Status     : {student['Seat Status'].upper()}\n")
        f.write(f"Allocated Branch: {course_name}\n")
        f.write(f"Registration No : {student['Registration Number']}\n")
        f.write("------------------------------------------------------\n")
        f.write("            FEE & SCHOLARSHIP    \n")
        f.write("------------------------------------------------------\n")
        f.write(f"Academic Fee    : INR {fee_amount}\n")
        f.write(f"Scholarship     : {student['Scholarship']}\n")
        f.write(f"Payment Status  : {student['Fee Status']}\n")
        f.write("======================================================\n")
        f.write("Instructions:\n")
        f.write("1. Report to the college admin block by 30th July.\n")
        
        # --- SMART INSTRUCTIONS UPDATED ---
        if "Paid" in student['Fee Status']:
            f.write("2. Complete final document verification (Fee Waived).\n")
        else:
            f.write("2. Pay the pending fee via Demand Draft.\n")
             
        f.write("======================================================\n")
    
    print(f"\n[SUCCESS] Allotment Letter generated: {filename}")