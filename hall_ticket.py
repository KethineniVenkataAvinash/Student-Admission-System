def generate_hall_ticket(student):

    app_id = student['Application Number']
    filename = f"HallTicket_{app_id}.txt"
    
    with open(filename, "w") as f:
        f.write("*************************************************\n")
        f.write("             OFFICIAL HALL TICKET                \n")
        f.write("*************************************************\n")
        f.write(f"Application No : {app_id}\n")
        f.write(f"Candidate Name : {student['Name']}\n")
        f.write(f"Gender         : {student['Gender']}\n")
        f.write(f"Date of Birth  : {student['Date of Birth']}\n")
        f.write("-------------------------------------------------\n")
        f.write("             EXAM CENTRE DETAILS                 \n")
        f.write("-------------------------------------------------\n")
        f.write(f"INSTITUTE      : {student['Exam Centre Name']}\n")
        f.write(f"CENTRE CODE    : {student['Exam Centre Code']}\n")
        f.write(f"ROOM NUMBER    : {student['Room Number']}\n")
        f.write(f"SEAT NUMBER    : {student['Seat Number']}\n")
        f.write("-------------------------------------------------\n")
        f.write("Instructions:\n")
        f.write("1. This ticket is mandatory for entry.\n")
        f.write("2. Bring a valid Government ID Proof.\n")
        f.write("3. Electronic gadgets are strictly prohibited.\n")
        f.write("*************************************************\n")
    
    print(f"\n[SUCCESS] Hall Ticket generated: {filename}")
    print("You can open this file to print your ticket.")
