def generate_receipt(student_data, original_password):
    app_no = student_data['Application Number']
    filename = f"{app_no}_receipt.txt"

    with open(filename, 'w') as f:
        f.write("==============================================\n")
        f.write("          COLLEGE ADMISSION SLIP              \n")
        f.write("==============================================\n")
        f.write(f"Application ID : {app_no}\n")
        f.write(f"Student Name   : {student_data['Name']}\n")
        f.write(f"Email ID       : {student_data['Email']}\n")
        f.write(f"Course Applied : {student_data['12th Course']}\n")
        f.write(f"Generated Pass : {original_password}\n")
        f.write("----------------------------------------------\n")
        f.write("NOTE: Keep this password safe.\n")
        f.write("==============================================\n")
    print(f"\n[SUCCESS] Receipt generated: {filename}")