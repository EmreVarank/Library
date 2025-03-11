from database.serverConnection import create_connection

def buy_book(customer_id, book_id):
    """Makes a book purchase"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Get the book price
        cursor.execute("SELECT book_price FROM Book WHERE book_id = ?", (book_id,))
        book_price = cursor.fetchone()

        if book_price:
            total_price = book_price[0]

            # Record the purchase transaction
            cursor.execute(
                "INSERT INTO TransactionHistory (customer_id, book_id, total_price) VALUES (?, ?, ?)",
                (customer_id, book_id, total_price)
            )

            conn.commit()
            conn.close()
            print(f"Purchase completed! Customer ID: {customer_id}, Book ID: {book_id}, Price: {total_price} TL")
        else:
            print("Error: Book not found!")


def get_customer_purchases(customer_id):
    """Lists the customer's purchase history"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT B.book_name, T.transaction_date, T.total_price 
            FROM TransactionHistory T
            JOIN Book B ON T.book_id = B.book_id
            WHERE T.customer_id = ?
        """, (customer_id,))

        purchases = cursor.fetchall()
        conn.close()

        if purchases:
            print(f"Customer ID {customer_id} purchase history:")
            for book_name, date, price in purchases:
                print(f"- {book_name} ({date}) - {price} TL")
        else:
            print("No purchase history found.")
