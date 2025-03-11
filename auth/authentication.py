import hashlib
from database.serverConnection import create_connection


def hash_password(password):
    """Hashes the password with SHA-256"""
    return hashlib.sha256(password.encode()).digest()


def register_customer(customer_name, customer_password):
    """Adds a new customer"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        hashed_password = hash_password(customer_password)

        cursor.execute(
            "INSERT INTO Customer (customer_name, customer_password) VALUES (?, ?)",
            (customer_name, hashed_password)
        )

        conn.commit()
        conn.close()
        print(f"{customer_name} successfully registered!")


def login_customer(customer_name, input_password):
    """Allows the customer to log in"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_password FROM Customer WHERE customer_name = ?", (customer_name,))
        stored_password = cursor.fetchone()

        conn.close()

        if stored_password and hash_password(input_password) == stored_password[0]:
            return True
        else:
            print("Incorrect username or password.")
            return False
