from tkinter import *
from tkinter import ttk, messagebox
import pymysql

# ------------------ Database Connection ------------------
def get_connection():
    return pymysql.connect(
        host="localhost", user="root", password="641658", database="employeemanagement_db"
    )

# ------------------ GUI Setup ------------------
root = Tk()
root.title("Employee Management System")
root.geometry("950x650")
root.configure(bg="#f0f6f6")

title = Label(root, text="EMPLOYEE MANAGEMENT SYSTEM", font=("Helvetica", 24, "bold"), 
              bg="#006699", fg="white", padx=20, pady=10, relief=RIDGE)
title.pack(fill=X, pady=10)

# ------------------ Clear Fields ------------------
def clear_fields():
    emp_id_entry.delete(0, END)
    emp_name_entry.delete(0, END)
    designation_entry.delete(0, END)
    salary_entry.delete(0, END)
    contact_entry.delete(0, END)
    gender_var.set("")
    dept_entry.delete(0, END)

# ------------------ Insert Data ------------------
def insert_data():
    name = emp_name_entry.get()
    desig = designation_entry.get()
    salary = salary_entry.get()
    contact = contact_entry.get()
    gender = gender_var.get()
    dept = dept_entry.get()

    if name == "" or contact == "":
        messagebox.showwarning("Input Error", "Please fill all required fields!")
        return

    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO employee (emp_name, designation, salary, contact, gender, department) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, desig, salary, contact, gender, dept)
        )
        con.commit()
        messagebox.showinfo("Success", "Employee record added successfully!")
        clear_fields()
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
    finally:
        con.close()

# ------------------ Search Data ------------------
def search_data():
    emp_id = emp_id_entry.get()
    if emp_id == "":
        messagebox.showinfo("Input Error", "Please enter Employee ID to search.")
        return
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee WHERE emp_id=%s", (emp_id,))
    row = cur.fetchone()
    con.close()
    if row:
        emp_name_entry.delete(0, END)
        emp_name_entry.insert(0, row[1])
        designation_entry.delete(0, END)
        designation_entry.insert(0, row[2])
        salary_entry.delete(0, END)
        salary_entry.insert(0, row[3])
        contact_entry.delete(0, END)
        contact_entry.insert(0, row[4])
        gender_var.set(row[5])
        dept_entry.delete(0, END)
        dept_entry.insert(0, row[6])
    else:
        messagebox.showinfo("Not Found", "Employee not found!")

# ------------------ Update Data ------------------
def update_data():
    emp_id = emp_id_entry.get()
    name = emp_name_entry.get()
    desig = designation_entry.get()
    salary = salary_entry.get()
    contact = contact_entry.get()
    gender = gender_var.get()
    dept = dept_entry.get()

    if emp_id == "":
        messagebox.showwarning("Input Error", "Enter Employee ID to update.")
        return

    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE employee SET emp_name=%s, designation=%s, salary=%s, contact=%s, gender=%s, department=%s WHERE emp_id=%s",
        (name, desig, salary, contact, gender, dept, emp_id),
    )
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Record updated successfully!")
    clear_fields()
    fetch_data()

# ------------------ Delete Data ------------------
def delete_data():
    emp_id = emp_id_entry.get()
    if emp_id == "":
        messagebox.showwarning("Input Error", "Enter Employee ID to delete.")
        return
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM employee WHERE emp_id=%s", (emp_id,))
    con.commit()
    con.close()
    messagebox.showinfo("Deleted", "Employee record deleted successfully!")
    clear_fields()
    fetch_data()

# ------------------ Display All Data ------------------
def fetch_data():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee")
    rows = cur.fetchall()
    if len(rows) != 0:
        employee_table.delete(*employee_table.get_children())
        for row in rows:
            employee_table.insert("", END, values=row)
    con.close()

# ------------------ GUI Layout ------------------
frame = Frame(root, bg="#dff0f7", bd=5, relief=RIDGE)
frame.place(x=50, y=100, width=850, height=220)

Label(frame, text="Emp ID:", font=("Arial", 14), bg="#dff0f7").grid(row=0, column=0, padx=10, pady=10, sticky="w")
emp_id_entry = Entry(frame, font=("Arial", 14), width=15)
emp_id_entry.grid(row=0, column=1, padx=10, pady=10)

Label(frame, text="Name:", font=("Arial", 14), bg="#dff0f7").grid(row=0, column=2, padx=10, pady=10, sticky="w")
emp_name_entry = Entry(frame, font=("Arial", 14), width=15)
emp_name_entry.grid(row=0, column=3, padx=10, pady=10)

Label(frame, text="Designation:", font=("Arial", 14), bg="#dff0f7").grid(row=1, column=0, padx=10, pady=10, sticky="w")
designation_entry = Entry(frame, font=("Arial", 14), width=15)
designation_entry.grid(row=1, column=1, padx=10, pady=10)

Label(frame, text="Salary:", font=("Arial", 14), bg="#dff0f7").grid(row=1, column=2, padx=10, pady=10, sticky="w")
salary_entry = Entry(frame, font=("Arial", 14), width=15)
salary_entry.grid(row=1, column=3, padx=10, pady=10)

Label(frame, text="Contact:", font=("Arial", 14), bg="#dff0f7").grid(row=2, column=0, padx=10, pady=10, sticky="w")
contact_entry = Entry(frame, font=("Arial", 14), width=15)
contact_entry.grid(row=2, column=1, padx=10, pady=10)

Label(frame, text="Gender:", font=("Arial", 14), bg="#dff0f7").grid(row=2, column=2, padx=10, pady=10, sticky="w")
gender_var = StringVar()
gender_dropdown = ttk.Combobox(frame, textvariable=gender_var, font=("Arial", 13), state="readonly", width=13)
gender_dropdown["values"] = ("Male", "Female", "Other")
gender_dropdown.grid(row=2, column=3, padx=10, pady=10)

Label(frame, text="Department:", font=("Arial", 14), bg="#dff0f7").grid(row=3, column=0, padx=10, pady=10, sticky="w")
dept_entry = Entry(frame, font=("Arial", 14), width=15)
dept_entry.grid(row=3, column=1, padx=10, pady=10)

# ------------------ Buttons ------------------
btn_frame = Frame(root, bg="#f0f6f6")
btn_frame.place(x=100, y=340, width=750)

Button(btn_frame, text="Add", command=insert_data, font=("Arial", 14, "bold"), bg="#009999", fg="white", width=10).grid(row=0, column=0, padx=10, pady=10)
Button(btn_frame, text="Search", command=search_data, font=("Arial", 14, "bold"), bg="#33b5e5", fg="white", width=10).grid(row=0, column=1, padx=10, pady=10)
Button(btn_frame, text="Update", command=update_data, font=("Arial", 14, "bold"), bg="#00b894", fg="white", width=10).grid(row=0, column=2, padx=10, pady=10)
Button(btn_frame, text="Delete", command=delete_data, font=("Arial", 14, "bold"), bg="#d63031", fg="white", width=10).grid(row=0, column=3, padx=10, pady=10)
Button(btn_frame, text="Clear", command=clear_fields, font=("Arial", 14, "bold"), bg="#636e72", fg="white", width=10).grid(row=0, column=4, padx=10, pady=10)

# ------------------ Data Table ------------------
table_frame = Frame(root, bg="#d1f0f5", bd=5, relief=RIDGE)
table_frame.place(x=50, y=430, width=850, height=200)

scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame, orient=VERTICAL)
employee_table = ttk.Treeview(
    table_frame,
    columns=("id", "name", "desig", "salary", "contact", "gender", "dept"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=employee_table.xview)
scroll_y.config(command=employee_table.yview)

employee_table.heading("id", text="Emp ID")
employee_table.heading("name", text="Name")
employee_table.heading("desig", text="Designation")
employee_table.heading("salary", text="Salary")
employee_table.heading("contact", text="Contact")
employee_table.heading("gender", text="Gender")
employee_table.heading("dept", text="Department")
employee_table["show"] = "headings"

for col in ("id", "name", "desig", "salary", "contact", "gender", "dept"):
    employee_table.column(col, width=120)

employee_table.pack(fill=BOTH, expand=1)
fetch_data()

# ------------------ Mainloop ------------------
root.mainloop()
