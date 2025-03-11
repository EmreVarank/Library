import tkinter as tk
from tkinter import messagebox
from transactions.transactions import buy_book, get_customer_purchases
from auth.authentication import login_customer
from database.serverConnection import create_connection

# Global variable to store the current logged-in user's ID
current_user_id = None


def login():
    global current_user_id  # Access the global variable for current user ID
    username = entry_username.get()
    password = entry_password.get()

    if login_customer(username, password):
        # Get the user_id after successful login
        current_user_id = get_user_id(username)
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Error", "Login failed. Please check your username and password.")


def show_main_window():
    # Create the main window
    main_window = tk.Tk()
    main_window.title("Library System")

    # Function to get all books from the database
    def get_all_books():
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, book_name, book_price FROM Book")
            books = cursor.fetchall()  # Fetch all books
            conn.close()
            return books
        return []

    # Function to show all books in the library
    def show_books():
        books = get_all_books()
        if not books:
            messagebox.showerror("Error", "No books found.")
            return

        # Create a new window to display books
        books_window = tk.Toplevel(main_window)
        books_window.title("Available Books")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(books_window)
        scrollbar = tk.Scrollbar(books_window, orient="vertical", command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the book widgets
        frame = tk.Frame(canvas)

        # Add the frame to the canvas
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Loop through the books and display them
        for idx, (book_id, book_name, book_price) in enumerate(books):
            book_frame = tk.Frame(frame)
            book_frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)

            book_label = tk.Label(book_frame, text=f"ID: {book_id}\nName: {book_name}\nPrice: {book_price}")
            book_label.pack()

            purchase_button = tk.Button(book_frame, text="Buy Book", command=lambda b_id=book_id: purchase_book(b_id))
            purchase_button.pack()

        # Update the scroll region of the canvas to accommodate all items
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Function to purchase a book
    def purchase_book(book_id):
        if not current_user_id:
            messagebox.showerror("Error", "You must log in first.")
            return
        try:
            buy_book(current_user_id, book_id)  # Use current_user_id to record the purchase
            messagebox.showinfo("Success", f"Book with ID {book_id} purchased successfully!")
        except ValueError:
            messagebox.showerror("Error", "Error purchasing the book.")
            return

    # Function to show the purchase history of the logged-in user
    def show_purchase_history():
        if not current_user_id:
            messagebox.showerror("Error", "You must log in first.")
            return

        # Fetch the purchase history from the database
        purchases = get_customer_purchases(current_user_id)
        if not purchases:
            messagebox.showerror("Error", "No purchase history found.")
            return

        # Create a new window to display the purchase history
        history_window = tk.Toplevel(main_window)
        history_window.title("Purchase History")

        for purchase in purchases:
            purchase_id, book_id, book_name, purchase_date = purchase
            purchase_label = tk.Label(history_window, text=f"Purchase ID: {purchase_id} - Book ID: {book_id} - Book: {book_name} - Date: {purchase_date}")
            purchase_label.pack()

    # Show books button
    show_books_button = tk.Button(main_window, text="Show Books", command=show_books)
    show_books_button.pack()

    # Show purchase history button
    history_button = tk.Button(main_window, text="Purchase History", command=show_purchase_history)
    history_button.pack()

    # Start the window
    main_window.mainloop()


def show_register_window():
    register_window = tk.Toplevel()
    register_window.title("Register")

    tk.Label(register_window, text="Username:").pack()
    entry_register_username = tk.Entry(register_window)
    entry_register_username.pack()

    tk.Label(register_window, text="Password:").pack()
    entry_register_password = tk.Entry(register_window, show="*")
    entry_register_password.pack()

    def register_action():
        username = entry_register_username.get()
        password = entry_register_password.get()
        if username and password:
            if register_user(username, password):
                register_window.destroy()
                messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty.")

    register_button = tk.Button(register_window, text="Register", command=register_action)
    register_button.pack()


def register_user(username, password):
    """Registers a new user in the system"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM Customer WHERE customer_name = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "This username is already taken.")
            return False

        # Insert the new user into the database
        cursor.execute("INSERT INTO Customer (customer_name, customer_password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        conn.close()
        return True
    return False


def get_user_id(username):
    """Fetches the user_id for the given username"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM Customer WHERE customer_name = ?", (username,))
        user_id = cursor.fetchone()
        conn.close()
        if user_id:
            return user_id[0]
        else:
            return None
    return None


def get_customer_purchases(user_id):
    """Fetches the purchase history of the user from the TransactionHistory table"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT th.transaction_id, th.book_id, b.book_name, th.transaction_date
            FROM TransactionHistory th
            JOIN Book b ON th.book_id = b.book_id
            WHERE th.customer_id = ?
        """, (user_id,))
        purchases = cursor.fetchall()  # Get all purchases for the logged-in user
        conn.close()
        return purchases
    return []


# Login window
login_window = tk.Tk()
login_window.title("Login")

# Username and password input fields
tk.Label(login_window, text="Username:").pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

tk.Label(login_window, text="Password:").pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

# Register button
register_button = tk.Button(login_window, text="Register", command=show_register_window)
register_button.pack()

# Start the window
login_window.mainloop()
