import sqlite3
import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime

# Database Handler
def connect_db():
    return sqlite3.connect('expenses.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT
                      )''')
    
    conn.commit()
    conn.close()

create_tables()

# Expense Logic
def add_expense(amount, category, description, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)', 
                   (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses_by_category(category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE category=?', (category,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Report Generation
def generate_report_by_category(category):
    expenses = get_expenses_by_category(category)
    amounts = [expense[1] for expense in expenses]
    dates = [expense[4] for expense in expenses]
    
    plt.figure(figsize=(10, 6))
    plt.bar(dates, amounts, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title(f'Expenses for {category}')
    plt.show()

def generate_overall_report():
    expenses = get_all_expenses()
    categories = {}
    
    for expense in expenses:
        category = expense[2]
        amount = expense[1]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
    
    labels = categories.keys()
    sizes = categories.values()
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Overall Expenses by Category')
    plt.show()

# Tkinter GUI
def add_expense_gui():
    amount = float(amount_entry.get())
    category = category_entry.get()
    description = description_entry.get()
    date = date_entry.get()
    add_expense(amount, category, description, date)
    status_label.config(text="Expense added!")

def show_category_report_gui():
    category = category_entry.get()
    generate_report_by_category(category)

def show_overall_report_gui():
    generate_overall_report()

# Setting up the GUI
root = tk.Tk()
root.title("Expense Tracker")

# Labels and Entries
tk.Label(root, text="Amount:").grid(row=0, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

tk.Label(root, text="Description:").grid(row=2, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense_gui).grid(row=4, column=0)
tk.Button(root, text="Show Category Report", command=show_category_report_gui).grid(row=4, column=1)
tk.Button(root, text="Show Overall Report", command=show_overall_report_gui).grid(row=5, columnspan=2)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=6, columnspan=2)

# Run the GUI
root.mainloop()
