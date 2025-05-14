import os
from tkinter import *
from tkinter import messagebox
import pandas as pd
import re
import subprocess
from PIL import Image, ImageTk

root = Tk()
root.title('Login')
root.attributes('-fullscreen', True)  # Set to full screen
root.configure(bg="#fff")
root.resizable(False, False)

# Add title label at the top center
event_label = Label(root, text="Event", fg='#57a1f8', bg='white', font=('Arial', 36, 'bold italic'))
event_label.place(relx=0.48, rely=0.05, anchor='center')

hunt_label = Label(root, text="Hunt", fg='#FF5733', bg='white', font=('Arial', 36, 'bold italic'))
hunt_label.place(relx=0.5, rely=0.05, anchor='center', x=100)  # Adjust x for spacing

# Load and display the image
img_path = r"C:\Users\DARSHAN\Downloads\login.png"
img = Image.open(img_path)
img = img.resize((500, 500), Image.LANCZOS)  # Resize image
photo = ImageTk.PhotoImage(img)
img_label = Label(root, image=photo, bg='white')
img_label.place(x=100, y=200)

frame = Frame(root, width=500, height=580, bg='white')
frame.place(x=1000, y=250)

# Sign in options
names = []
colleges = []
branches = []
passwords = []
mobnos = []
emails=[]

heading = Label(frame, text="Sign Up", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=140, y=5)

def on_enter(e, entry):
    if entry.get() == entry.placeholder:
        entry.delete(0, 'end')

def on_leave(e, entry):
    if entry.get() == '':
        entry.insert(0, entry.placeholder)

# Create Entry fields with placeholder functionality
def create_entry(frame, y_position, placeholder):
    entry = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    entry.place(x=30, y=y_position)
    entry.insert(0, placeholder)
    entry.placeholder = placeholder
    Frame(frame, width=310, height=2, bg='black').place(x=25, y=y_position + 27)
    entry.bind('<FocusIn>', lambda e: on_enter(e, entry))
    entry.bind('<FocusOut>', lambda e: on_leave(e, entry))
    return entry

# Entry fields
user = create_entry(frame, 80, 'Name')
college = create_entry(frame, 150, 'College')
branch = create_entry(frame, 220, 'Branch')
password = create_entry(frame, 290, 'Password')
mobno = create_entry(frame, 360, 'Mob no')
email = create_entry(frame, 430, 'Email (e.g. example@gmail.com)')

# Add label for toggle password visibility
show_password = BooleanVar(value=False)

def toggle_password_visibility(event):
    if show_password.get():
        password.config(show='*')  # Hide password
        visibility_label.config(text='Show')  # Change label to 'Show'
        show_password.set(False)  # Update the state
    else:
        password.config(show='')  # Show password
        visibility_label.config(text='Hide')  # Change label to 'Hide'
        show_password.set(True)  # Update the state

visibility_label = Label(frame, text='Show', bg='white', fg='#57a1f8', cursor='hand2')
visibility_label.place(x=380, y=290)
visibility_label.bind('<Button-1>', toggle_password_visibility)  # Bind left-click to toggle

# Validation functions
def validate_string(input_str):
    return all(char.isalpha() or char.isspace() for char in input_str)

def validate_email(email):
    if not email.endswith("@gmail.com"):
        return False
    local_part = email.split('@')[0]
    if local_part.count('.') > 1:  # Ensure at most one '.' in the local part
        return False
    return bool(re.match(r"^[A-Za-z0-9]+(\.[A-Za-z0-9]+)?$", local_part))  # Allow letters, numbers, and a single dot

def validate_mobile(mobile):
    return len(mobile) == 10 and mobile.isdigit()

def validate_no_symbols(input_str):
    return not any(char in input_str for char in ".,")  # Deny '.', ','

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

# Login button
def save_data():
    Name = user.get().strip()
    College = college.get().strip()
    Branch = branch.get().strip()
    Password = password.get().strip()
    Mob = mobno.get().strip()
    Email = email.get().strip()

    # Check for empty inputs
    if not Name or not College or not Branch or not Password or not Mob or not Email:
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    # Validate Name
    if not validate_string(Name) or not validate_no_symbols(Name):
        messagebox.showerror("Error", "Name must consist only of alphabets (A-Z, a-z) and spaces, and must not contain symbols like '.' or ','.")
        return

    # Validate College
    if not validate_string(College) or not validate_no_symbols(College):
        messagebox.showerror("Error", "College must consist only of alphabets (A-Z, a-z) and spaces, and must not contain symbols like '.' or ','.")
        return

    # Validate Branch
    if not validate_string(Branch) or not validate_no_symbols(Branch):
        messagebox.showerror("Error", "Branch must consist only of alphabets (A-Z, a-z) and spaces, and must not contain symbols like '.' or ','.")
        return

    # Validate password
    if not validate_password(Password):
        messagebox.showerror("Error", "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one digit.")
        return

    # Validate email
    if not validate_email(Email):
        messagebox.showerror("Error", "Email must consist of valid format ending with '@gmail.com'.")
        return

    # Validate mobile number
    if not validate_mobile(Mob):
        messagebox.showerror("Error", "Mobile number must be exactly 10 digits long.")
        return

    # Check for duplicates
    if (Name in names) and (College in colleges) and (Branch in branches) and (Password in passwords) and (Mob in mobnos) and (Email in emails):
        messagebox.showinfo("Info", "This entry already exists!")
        return

    names.append(Name)
    colleges.append(College)
    branches.append(Branch)
    passwords.append(Password)
    mobnos.append(Mob)
    emails.append(Email)

    data = {
        'Name': names,
        'College': colleges,
        'Branch': branches,
        'Password': passwords,
        'Mob no': mobnos,
        'Email': emails
    }

    save_path = r"C:\Users\DARSHAN\OneDrive\Documents\resistration.xlsx"

    # Try to read the existing Excel file and append new data
    try:
        if os.path.exists(save_path):
            existing_df = pd.read_excel(save_path)
            new_df = pd.DataFrame(data)

            # Append new data and remove duplicates
            combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates()
            combined_df.to_excel(save_path, index=False)
        else:
            pd.DataFrame(data).to_excel(save_path, index=False)

        messagebox.showinfo("Success", "Data saved successfully!")  # Show success message
        
        # Clear inputs after saving
        for entry in [user, college, branch, password, mobno, email]:
            entry.delete(0, 'end')
            entry.insert(0, entry.placeholder)

        # Close the login window
        root.destroy()

        # Open main.py
        subprocess.Popen(['python', 'main.py'])

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

Button(frame, command=save_data, width=15, padx=40, pady=7, text='Sign in', fg='white', bg='#cf4c30', border=1).place(x=55, y=500)

# Exit full screen on Escape key
root.bind('<Escape>', lambda e: root.quit())

root.mainloop()