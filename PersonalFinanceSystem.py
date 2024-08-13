import sqlite3
import tkinter as tk
import matplotlib.pyplot as plt

# Database Handler
def connect_db():
    return sqlite3.connect('finance.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS savings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        goal REAL,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    conn.commit()
    conn.close()

create_tables()

# Finance Logic
def add_income(user_id, amount, category, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO income (user_id, amount, category, date) VALUES (?, ?, ?, ?)', 
                   (user_id, amount, category, date))
    conn.commit()
    conn.close()

def add_expense(user_id, amount, category, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)', 
                   (user_id, amount, category, date))
    conn.commit()
    conn.close()

def calculate_savings(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(amount) FROM income WHERE user_id=?', (user_id,))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id=?', (user_id,))
    total_expenses = cursor.fetchone()[0] or 0
    
    savings = total_income - total_expenses
    
    cursor.execute('INSERT INTO savings (user_id, amount) VALUES (?, ?)', (user_id, savings))
    conn.commit()
    conn.close()
    
    return savings

# Report Generation
def generate_report(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT category, SUM(amount) FROM income WHERE user_id=? GROUP BY category', (user_id,))
    income_data = cursor.fetchall()
    
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category', (user_id,))
    expense_data = cursor.fetchall()
    
    conn.close()
    
    categories, income_amounts = zip(*income_data) if income_data else ([], [])
    _, expense_amounts = zip(*expense_data) if expense_data else ([], [])
    
    fig, ax = plt.subplots()
    ax.bar(categories, income_amounts, label='Income', color='g')
    ax.bar(categories, expense_amounts, label='Expenses', color='r', bottom=income_amounts)
    
    ax.set_ylabel('Amount')
    ax.set_title('Income vs. Expenses')
    ax.legend()
    
    plt.show()

# Tkinter GUI
def add_income_gui():
    user_id = 1  # Assuming logged-in user with ID 1
    amount = float(amount_entry.get())
    category = category_entry.get()
    date = date_entry.get()
    add_income(user_id, amount, category, date)
    status_label.config(text="Income added!")

def add_expense_gui():
    user_id = 1  # Assuming logged-in user with ID 1
    amount = float(amount_entry.get())
    category = category_entry.get()
    date = date_entry.get()
    add_expense(user_id, amount, category, date)
    status_label.config(text="Expense added!")

def show_savings_gui():
    user_id = 1  # Assuming logged-in user with ID 1
    savings = calculate_savings(user_id)
    status_label.config(text=f"Total Savings: {savings}")

def show_report_gui():
    user_id = 1  # Assuming logged-in user with ID 1
    generate_report(user_id)

# Setting up the GUI
root = tk.Tk()
root.title("Personal Finance Management System")

# Labels and Entries
tk.Label(root, text="Amount:").grid(row=0, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add Income", command=add_income_gui).grid(row=3, column=0)
tk.Button(root, text="Add Expense", command=add_expense_gui).grid(row=3, column=1)
tk.Button(root, text="Show Savings", command=show_savings_gui).grid(row=4, column=0)
tk.Button(root, text="Show Report", command=show_report_gui).grid(row=4, column=1)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=5, columnspan=2)

# Run the GUI
root.mainloop()
