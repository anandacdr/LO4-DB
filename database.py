import psycopg2  # Database connection
import tkinter as tk
from tkinter import ttk  # GUI widgets

# Database connection details
database = "Students"
user = "postgres"
password = "Storage321@@"
host = "localhost"
port = "5432"

def connect_to_database():
    try:
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if query.lower().startswith("select"):
            return cursor.fetchall()
        connection.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def insert_student_data(connection, student):
    query = f"INSERT INTO Student (name, address, roll, marks) VALUES {student}"
    return execute_query(connection, query)

def main():
    connection = connect_to_database()  # Try establishing database connection

    # If connection fails, display error message and exit
    if not connection:
        error_window = tk.Tk()
        error_label = tk.Label(
            error_window, text="Error connecting to database.", font=("Helvetica", 14)
        )
        error_label.pack()
        error_window.mainloop()
        return

    # Create the main window
    root = tk.Tk()
    root.title("Student Information Table")

    # Function to handle inserting data into the database
    def insert_data():
        name = name_entry.get()
        address = address_entry.get()
        roll = int(roll_entry.get())
        marks = int(marks_entry.get())
        student = (name, address, roll, marks)
        insert_student_data(connection, student)
        refresh_data()

    # Function to refresh the data displayed in the Treeview
    def refresh_data():
        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Retrieve updated data from the database and insert it into the Treeview
        query = "SELECT address FROM Student"
        data = execute_query(connection, query)
        if data:
            for student in data:
                tree.insert("", tk.END, values=(student[0],))

    # Create input fields and labels
    name_label = tk.Label(root, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    address_label = tk.Label(root, text="Address:")
    address_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    address_entry = tk.Entry(root)
    address_entry.grid(row=1, column=1, padx=5, pady=5)

    roll_label = tk.Label(root, text="Roll:")
    roll_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    roll_entry = tk.Entry(root)
    roll_entry.grid(row=2, column=1, padx=5, pady=5)

    marks_label = tk.Label(root, text="Marks:")
    marks_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    marks_entry = tk.Entry(root)
    marks_entry.grid(row=3, column=1, padx=5, pady=5)

    insert_button = tk.Button(root, text="Insert", command=insert_data)
    insert_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Create the Treeview widget
    tree = ttk.Treeview(root, columns=("Address",))

    # Define column headings
    tree.heading("#0", text="ID")  # Add an invisible column for ID
    tree.heading("Address", text="Address")
    

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
