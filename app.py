# Created by Pratyush Mishra From Proxlight

import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Colors
background_color = "#264653"  # Modern dark teal
accent_color = "#FF2365"
text_color = "#FFFFFF"
hover_color = "#FF506A"  # Lighter accent for hover

# Initialize the main application window
root = ctk.CTk()
root.title("Student Management System")
root.geometry("750x550")
root.configure(bg=background_color)

# Connect to SQLite database (or create it)
conn = sqlite3.connect("student_management.db")
c = conn.cursor()

# Create the students table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                department TEXT NOT NULL
            )''')
conn.commit()

# Function to add a student
def add_student():
    if name_entry.get() == "" or age_entry.get() == "" or gender_entry.get() == "" or department_entry.get() == "":
        messagebox.showerror("Error", "All fields are required!")
    else:
        c.execute("INSERT INTO students (name, age, gender, department) VALUES (?, ?, ?, ?)",
                  (name_entry.get(), age_entry.get(), gender_entry.get(), department_entry.get()))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        display_students()

# Function to display all students
def display_students():
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    student_list.delete(*student_list.get_children())
    for row in rows:
        student_list.insert("", "end", values=row)

# Function to clear all input fields
def clear_fields():
    name_entry.delete(0, ctk.END)
    age_entry.delete(0, ctk.END)
    gender_entry.delete(0, ctk.END)
    department_entry.delete(0, ctk.END)

# Function to select a student
def select_student(event):
    try:
        selected_row = student_list.selection()[0]
        selected_student = student_list.item(selected_row, 'values')

        name_entry.delete(0, ctk.END)
        name_entry.insert(ctk.END, selected_student[1])
        age_entry.delete(0, ctk.END)
        age_entry.insert(ctk.END, selected_student[2])
        gender_entry.delete(0, ctk.END)
        gender_entry.insert(ctk.END, selected_student[3])
        department_entry.delete(0, ctk.END)
        department_entry.insert(ctk.END, selected_student[4])

    except IndexError:
        pass

# Function to update a student
def update_student():
    try:
        selected_row = student_list.selection()[0]
        student_id = student_list.item(selected_row, 'values')[0]

        c.execute("""UPDATE students SET name = ?, age = ?, gender = ?, department = ?
                     WHERE id = ?""",
                  (name_entry.get(), age_entry.get(), gender_entry.get(), department_entry.get(), student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        clear_fields()
        display_students()

    except IndexError:
        messagebox.showerror("Error", "Please select a student to update.")

# Function to delete a student
def delete_student():
    try:
        selected_row = student_list.selection()[0]
        student_id = student_list.item(selected_row, 'values')[0]

        c.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully!")
        clear_fields()
        display_students()

    except IndexError:
        messagebox.showerror("Error", "Please select a student to delete.")

# User Interface Layout

# Title and Heading
title_label = ctk.CTkLabel(root, text="Student Management System", text_color=text_color, font=("Arial", 24, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))

heading_label = ctk.CTkLabel(root, text="Manage Student Records", text_color=accent_color, font=("Arial", 18, "bold"))
heading_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 20))

# Labels and Entry Fields
name_label = ctk.CTkLabel(root, text="Name:", text_color=text_color, bg_color=background_color)
name_label.grid(row=2, column=0, padx=10, pady=5)
name_entry = ctk.CTkEntry(root, fg_color=accent_color, border_width=2, corner_radius=5)
name_entry.grid(row=2, column=1, padx=10, pady=5)

age_label = ctk.CTkLabel(root, text="Age:", text_color=text_color, bg_color=background_color)
age_label.grid(row=3, column=0, padx=10, pady=5)
age_entry = ctk.CTkEntry(root, fg_color=accent_color, border_width=2, corner_radius=5)
age_entry.grid(row=3, column=1, padx=10, pady=5)

gender_label = ctk.CTkLabel(root, text="Gender:", text_color=text_color, bg_color=background_color)
gender_label.grid(row=4, column=0, padx=10, pady=5)
gender_entry = ctk.CTkEntry(root, fg_color=accent_color, border_width=2, corner_radius=5)
gender_entry.grid(row=4, column=1, padx=10, pady=5)

department_label = ctk.CTkLabel(root, text="Department:", text_color=text_color, bg_color=background_color)
department_label.grid(row=5, column=0, padx=10, pady=5)
department_entry = ctk.CTkEntry(root, fg_color=accent_color, border_width=2, corner_radius=5)
department_entry.grid(row=5, column=1, padx=10, pady=5)

# Buttons with hover effect
add_button = ctk.CTkButton(root, text="Add Student", command=add_student, fg_color=accent_color, hover_color=hover_color)
add_button.grid(row=6, column=0, padx=10, pady=10)

update_button = ctk.CTkButton(root, text="Update Student", command=update_student, fg_color=accent_color, hover_color=hover_color)
update_button.grid(row=6, column=1, padx=10, pady=10)

delete_button = ctk.CTkButton(root, text="Delete Student", command=delete_student, fg_color=accent_color, hover_color=hover_color)
delete_button.grid(row=7, column=0, padx=10, pady=10)

clear_button = ctk.CTkButton(root, text="Clear Fields", command=clear_fields, fg_color=accent_color, hover_color=hover_color)
clear_button.grid(row=7, column=1, padx=10, pady=10)

# Treeview for displaying students
columns = ('ID', 'Name', 'Age', 'Gender', 'Department')
student_list = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    student_list.heading(col, text=col)
    student_list.column(col, anchor="center")

student_list.bind('<ButtonRelease-1>', select_student)
student_list.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Display the students on startup
display_students()

# Start the main loop
root.mainloop()

# Close the database connection when the application exits
conn.close()
