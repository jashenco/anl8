import datetime
from db import connect_db
from encryption import encrypt_data, decrypt_data

def register_member(first_name, last_name, age, gender, weight, address, email, phone):
    c, conn = connect_db()
    
    encrypted_address = encrypt_data(address)
    encrypted_email = encrypt_data(email)
    encrypted_phone = encrypt_data(phone)

    c.execute("INSERT INTO members (first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (first_name, last_name, age, gender, weight, encrypted_address, encrypted_email, encrypted_phone, str(datetime.date.today())))
    
    conn.commit()
    conn.close()

def get_member_details(member_id):
    c, conn = connect_db()
    
    c.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
    row = c.fetchone()
    
    member_details = None
    
    if row is not None:
        decrypted_address = decrypt_data(row['address'])
        decrypted_email = decrypt_data(row['email'])
        decrypted_phone = decrypt_data(row['phone'])
        
        member_details = {
            'member_id': row['member_id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'age': row['age'],
            'gender': row['gender'],
            'weight': row['weight'],
            'address': decrypted_address,
            'email': decrypted_email,
            'phone': decrypted_phone,
            'registration_date': row['registration_date']
        }
    
    conn.close()
    return member_details
