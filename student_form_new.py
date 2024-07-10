import tkinter as tk
from tkinter import messagebox
import pyodbc

# Function to connect to the SQL Server and create table if not exists
def connect_db():
    conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=SAURABH-PC\\SQLEXPRESS;'
                              'DATABASE=SAURABH;'
                              'Trusted_Connection=yes;'
                              )
    cursor = conn.cursor()
    cursor.execute('''
                   IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='students' AND xtype='U')
                   CREATE TABLE students (
                       id INT IDENTITY(1,1) PRIMARY KEY,
                       name NVARCHAR(100) NOT NULL,
                       age INT NOT NULL,
                       gender NVARCHAR(10) NOT NULL,
                       course NVARCHAR(100) NOT NULL)
                   ''')
    conn.commit()
    conn.close()

# Function to save data to the SQL Server
def save_to_db(name, age, gender, course):
    conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=SAURABH-PC\\SQLEXPRESS;'
                              'DATABASE=SAURABH;'
                              'Trusted_Connection=yes;'
                              )
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO students (name, age, gender, course)
                   VALUES (?, ?, ?, ?)
                   ''', (name, age, gender, course))
    conn.commit()
    conn.close()

def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    course = entry_course.get()

    if name and age and gender and course:
        save_to_db(name, age, gender, course)
        messagebox.showinfo("Form Submitted", f"Student Details:\n\nName: {name}\nAge: {age}\nGender: {gender}\nCourse: {course}")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Connect to the SQL Server and create table if not exists
connect_db()

# Create the main application window
root = tk.Tk()
root.title("Student Application Form")

# Create and place the labels and entry widgets for each field
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Age").grid(row=1, column=0, padx=10, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Gender").grid(row=2, column=0, padx=10, pady=5)
gender_var = tk.StringVar()
gender_var.set("Male")  # Default value
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

tk.Label(root, text="Course").grid(row=3, column=0, padx=10, pady=5)
entry_course = tk.Entry(root)
entry_course.grid(row=3, column=1, padx=10, pady=5)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
