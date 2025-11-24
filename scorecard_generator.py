
def generate_scorecard(student):

    filename = f"Scorecard_{student['Application Number']}.txt"
    
    with open(filename, "w") as f:
        f.write("======================================================\n")
        f.write("            OFFICIAL SCORECARD 2025   \n")
        f.write("======================================================\n")
        f.write(f"Application No : {student['Application Number']}\n")
        f.write(f"Candidate Name : {student['Name']}\n")
        f.write(f"Date of Birth  : {student['Date of Birth']}\n")
        f.write("------------------------------------------------------\n")
        f.write("              ACADEMIC RESULTS   \n")
        f.write("------------------------------------------------------\n")
        f.write(f"Entrance Marks : {student['Marks']} / 120\n")
        f.write(f"All India Rank : {student['Rank']}\n")
        f.write(f"Final Status   : {student['Status'].upper()}\n")
        f.write("------------------------------------------------------\n")

        if student.get("Scholarship") and student["Scholarship"] != "None":
            f.write(f"SCHOLARSHIP   : {student['Scholarship']}\n")
            f.write("NOTE: Please contact admin to claim fee waiver.\n")
        else:
            f.write("SCHOLARSHIP  : Not Eligible\n")
        
        f.write("======================================================\n")
        f.write("This is a computer-generated document.\n")
    
    print(f"\n[SUCCESS] Scorecard generated successfully: {filename}")
    print("Please open this file to view your official result.")