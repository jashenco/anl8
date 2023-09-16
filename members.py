from db import DBManager

def register_member(first_name, last_name, age, gender, weight, address, email, phone):
    db = DBManager()
    
    member_id = 1 #Change later -> See assignment description for algorithm to use
    encrypted_address = encrypt_data(address)
    encrypted_email = encrypt_data(email)
    encrypted_phone = encrypt_data(phone)

    db.execute_query("INSERT INTO members (member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (member_id, first_name, last_name, age, gender, weight, encrypted_address, encrypted_email, encrypted_phone, str(datetime.date.today())))
