from db import connect_db

def register_member(first_name, last_name, age, gender, weight, address, email, phone):
    c, conn = connect_db()
    
    member_id = 1 #Change later -> See assignment description for algorith to use
    encrypted_address = encrypt_data(address)
    encrypted_email = encrypt_data(email)
    encrypted_phone = encrypt_data(phone)

    c.execute("INSERT INTO members (member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (member_id, first_name, last_name, age, gender, weight, encrypted_address, encrypted_email, encrypted_phone, str(datetime.date.today())))
    
    conn.commit()
