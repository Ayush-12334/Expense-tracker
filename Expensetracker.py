import sqlite3               # For working with SQLite database
from datetime import datetime  # For validating dates
import matplotlib.pyplot as plt  # For plotting expense graphs

# ---------- DATABASE SETUP ----------
def create_table():
    """
    Create the 'expenses' table if it does not already exist.
    Columns:
        id          -> unique auto-incremented ID
        date        -> expense date
        category    -> expense category (Food, Travel, etc.)
        description -> details about the expense
        amount      -> amount spent
    """
    conn = sqlite3.connect("expenses.db")  # Connect to the database (creates file if not found)
    cursor = conn.cursor()  # Cursor is used to execute SQL commands
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        description TEXT,
                        amount REAL)''')  # SQL to create table if it doesn't exist
    conn.commit()  # Save changes
    conn.close()   # Close database connection

# ---------- ADD EXPENSE ----------
def add_expense(date, category, description, amount):
    """
    Add a new expense record into the expenses table.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Insert a new expense row into the table
    cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                   (date, category, description, amount))
    conn.commit()
    conn.close()

# ---------- VIEW EXPENSES ----------
def view_expenses():
    """
    Display all expenses stored in the database in a table format.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")  # Fetch all rows
    rows = cursor.fetchall()
    conn.close()

    # If no records found
    if not rows:
        print("No expenses recorded.")
    else:
        # Print table headers
        print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Description':<20}{'Amount':<10}")
        print("-"*65)
        # Print each row neatly
        for row in rows:
            print(f"{row[0]:<5}{row[1]:<12}{row[2]:<15}{row[3]:<20}{row[4]:<10.2f}")

# ---------- SHOW TOTAL EXPENSE ----------
def total_expense():
    """
    Calculate and display the total of all expenses.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")  # Add up all amounts
    total = cursor.fetchone()[0]
    conn.close()

    # If total is None (no expenses yet), set to 0
    value = total if total else 0
    print(f"Total expense: {value:.2f}")

# ---------- DELETE EXPENSE ----------
def delete_expense(id):
    """
    Delete a specific expense from the database by ID.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

# ---------- UPDATE EXPENSE ----------
def update_expense(id, date, category, description, amount):
    """
    Update an existing expense record with new details.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET date=?, category=?, description=?, amount=? WHERE id=?",
                   (date, category, description, amount, id))
    conn.commit()
    conn.close()

# ---------- VALIDATE DATE ----------
def get_valid_date():
    """
    Ask user to input a date in YYYY-MM-DD format.
    Keeps asking until a valid format is entered.
    """
    while True:
        raw = input("Enter date (YYYY-MM-DD): ").strip()

        # Check for proper format: length 10 and hyphens in correct positions
        if len(raw) != 10 or raw[4] != '-' or raw[7] != '-':
            print("Invalid format! Use YYYY-MM-DD with dashes.")
            continue

        try:
            # Try converting to datetime to ensure validity
            valid_date = datetime.strptime(raw, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date! Please enter a valid date (e.g., 2025-08-03)")

# ---------- MONTHLY EXPENSE ----------
def monthly_expense():
    """
    Show total expenses for a particular month.
    User inputs month as YYYY-MM.
    """
    month = input("Enter month in YYYY-MM format: ").strip()

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Get sum of all expenses where date starts with the given month
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE substr(date,1,7)=?", (month,))
    total = cursor.fetchone()[0]
    conn.close()

    value = total if total else 0
    print(f"Total expense for {month}: {value:.2f}")

# ---------- PLOT CATEGORY EXPENSES ----------
def plot_category_expenses():
    """
    Display a bar graph showing total spending per category.
    Bars above 30000 are shown in red to indicate overspending.
    """
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()

    # If no data available
    if not rows:
        print("No expenses to display.")
        return

    # Separate data into lists
    categories = [row[0] for row in rows]
    amounts = [row[1] for row in rows]

    # Assign colors: red if over 30000, skyblue otherwise
    colors = ['red' if amt > 30000 else 'skyblue' for amt in amounts]

    # Create a bar chart
    plt.figure(figsize=(8, 3))  # Set figure size
    plt.bar(categories, amounts, color=colors)  # Use colors based on amounts
    plt.xlabel("Category")   # Label for X-axis
    plt.ylabel("Total Expense")  # Label for Y-axis
    plt.title("Expenses by Category")  # Title of the graph
    plt.xticks(rotation=45)  # Rotate X-axis labels for better visibility

    # Set Y-axis range
    plt.ylim(1000, 90000)   # Set minimum to 1000 and maximum to 90000

    # Add a red horizontal line at y=30000
    plt.axhline(30000, color='red', linestyle='--', linewidth=2, label='Limit (30000)')
    plt.legend()

    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()  # Display the graph



# ---------- MAIN MENU ----------
def menu():
    """
    Display the main menu and handle user choices.
    """
    create_table()  # Ensure table exists before starting
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expense")
        print("4. Delete Expense")
        print("5. Update Expense")
        print("6. Show Monthly Expense")
        print("7. Show Graph of Category-wise Expenses")
        print("8. Exit")

        choice = input("Enter choice: ")

        # Choice handling
        if choice == "1":
            date = get_valid_date()
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            add_expense(date, category, description, amount)
            print("Expense added successfully.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            id = int(input("Enter the ID of the expense to delete: "))
            delete_expense(id)
            print("Expense deleted successfully.")
        elif choice == "5":
            id = int(input("Enter the ID of the expense to update: "))
            date = get_valid_date()
            category = input("Enter new category: ")
            description = input("Enter new description: ")
            amount = float(input("Enter new amount: "))
            update_expense(id, date, category, description, amount)
            print("Expense updated successfully.")
        elif choice == "6":
            monthly_expense()
        elif choice == "7":
            plot_category_expenses()
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, try again.")

# ---------- RUN ----------
if __name__ == "__main__":
    menu()
