from tkinter import *
from tkinter import messagebox
import pandas as pd
import os
import subprocess
from PIL import Image, ImageTk

# Function to check user credentials against the Excel file
def check_credentials(username, password):
    save_path = r"D:\Data\resistration.xlsx"
    if os.path.exists(save_path):
        df = pd.read_excel(save_path)
        # Check if the username (name in Excel) and password match any entry
        return not df[(df['Name'] == username) & (df['Password'] == password)].empty
    return False

# Initialize the main application window
root = Tk()
root.title('Login')
root.attributes('-fullscreen', True)
root.configure(bg="#fff")
root.resizable(False, False)

# Add title label at the top center
event_label = Label(root, text="Event", fg='#57a1f8', bg='white', font=('Arial', 36, 'bold italic'))
event_label.place(relx=0.48, rely=0.05, anchor='center')

hunt_label = Label(root, text="Hunt", fg='#FF5733', bg='white', font=('Arial', 36, 'bold italic'))
hunt_label.place(relx=0.5, rely=0.05, anchor='center', x=100)  # Adjust x for spacing

def login():
    username = user.get().strip()
    password = code.get().strip()
  
    if username == '' or password == '':
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    if check_credentials(username, password):
        messagebox.showinfo("Success", "Login successful!")
        root.quit()
        subprocess.Popen(['python', 'main.py'])
    else:
        messagebox.showerror("Invalid", "Invalid username or password")

# Exit full-screen mode when pressing the Escape key
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind('<Escape>', exit_fullscreen)

# Load and place the logo image
img_path = r"C:\Users\DARSHAN\Downloads\login.png"
img = Image.open(img_path)
img = img.resize((500, 500), Image.LANCZOS)  # Resize image
photo = ImageTk.PhotoImage(img)
img_label = Label(root, image=photo, bg='white')
img_label.place(x=100, y=200)

# Create a frame for the sign-in form with rounded corners and shadow effect
frame = Frame(root, width=500, height=400, bg="#ffffff", highlightbackground="#57aaf8", highlightthickness=2, relief='groove')
frame.place(x=900, y=250)

heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=185, y=6)

# Username Entry
user = Entry(frame, width=30, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
user.place(x=30, y=100)
user.insert(0, 'Username')
user.bind('<FocusIn>', lambda e: user.delete(0, 'end') if user.get() == 'Username' else None)
user.bind('<FocusOut>', lambda e: user.insert(0, 'Username') if user.get() == '' else None)

# Password Entry
code = Entry(frame, width=30, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show='*')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', lambda e: code.delete(0, 'end') if code.get() == 'Password' else None)
code.bind('<FocusOut>', lambda e: code.insert(0, 'Password') if code.get() == '' else None)

# Sign In Button with hover effect
def on_enter(e):
    e.widget['bg'] = '#0056b3'

def on_leave(e):
    e.widget['bg'] = '#57aaf8'

login_button = Button(frame, width=29, pady=7, text='Login', bg='#57aaf8', fg='white', border=0, command=login)
login_button.place(x=30, y=200)
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

# Sign Up Prompt
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Arial', 12))  # Increased font size
label.place(x=30, y=250)

# Sign Up Button
def open_signup_window():
    root.destroy()
    subprocess.Popen(['python', 'login.py'])

sign_up = Button(frame, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57aaf8', font=('Arial', 12), command=open_signup_window)  # Increased font size
sign_up.place(x=30, y=275)

# Add a footer with a copyright notice
footer = Label(root, text="© 2024 ", fg='gray', bg='#fff', font=('Arial', 10))
footer.place(relx=0.5, rely=0.95, anchor='center')

root.mainloop()