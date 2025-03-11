from database.serverConnection import create_connection

def add_book(book_name, book_price):
    """Adds a new book"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Book (book_name, book_price) VALUES (?, ?)", (book_name, book_price))
        conn.commit()
        conn.close()
        print(f"Book added: {book_name} - {book_price} TL")

def update_book_price(book_id, new_price):
    """Updates the book price"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Book SET book_price = ? WHERE book_id = ?", (new_price, book_id))
        conn.commit()
        conn.close()
        print(f"Book price updated: {book_id} → {new_price} TL")

def delete_book(book_id):
    """Deletes a book"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Book WHERE book_id = ?", (book_id,))
        conn.commit()
        conn.close()
        print(f"Book deleted: {book_id}")
