import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  
import os
import openpyxl 

# Global variables to track the current state
current_view = "homepage"
current_college = ""
current_clubs = {}
bg_photo = None  # To hold the background image
exercise_icon = None  # To hold the exercise icon
contact_icon = None  # To hold the contact icon

# Define a new font style
FONT_TITLE = ('Helvetica Neue', 26, 'bold')
FONT_INFO = ('Arial', 12)
FONT_BUTTON = ('Helvetica Neue', 12)

# Function to display the events of a club
def explore_club_events(club_name, events):
    global current_view
    current_view = "club_events"

    # Clear previous widgets from the main canvas
    for widget in canvas.winfo_children():
        widget.destroy()

    # Show the club name in a label
    title_label = tk.Label(canvas, text=f"Events for {club_name}", font=FONT_TITLE, fg='#333', bg='#737070')
    title_label.place(relx=0.5, rely=0.1, anchor='center')

    # Frame for club events with a nice border
    event_frame = tk.Frame(canvas, bg='#5D7394', bd=5, relief=tk.SUNKEN)
    event_frame.pack(pady=40, padx=300, fill=tk.BOTH, expand=True)

    # Show the events for the club
    for event, details in events.items():
        event_card = tk.Frame(event_frame, bg='#FFFFFF', bd=2, relief=tk.RAISED, padx=10, pady=10)
        event_card.pack(pady=10, fill=tk.X, padx=10)
        
        event_label = tk.Label(event_card, text=event, font=('Helvetica Neue', 14, 'bold'), fg='#015582', bg='#FFFFFF')
        event_label.pack(anchor='w', pady=5)

        event_info = tk.Label(event_card, text=f"Date: {details['date']}\nTime: {details['time']}\nLocation: {details['location']}\nDescription: {details['description']}", 
                              font=FONT_INFO, fg='#333', bg='#FFFFFF', wraplength=600, justify='left')
        event_info.pack(anchor='w', pady=5)

        # Add an "Apply" button for each event
        apply_button = tk.Button(event_card, text="Apply", command=lambda e=event: apply_for_event(e), bg='#FF7043', fg='white', font=FONT_BUTTON)
        apply_button.pack(pady=5)
        

    # Add a back button to return to the clubs view
    back_button = tk.Button(canvas, text='Back to Clubs', command=lambda: display_clubs(current_college, current_clubs), bg='#FF7043', fg='white', font=FONT_BUTTON)
    back_button.place(relx=0.5, rely=0.9, anchor='center')
    

# Function to simulate applying for an event
def apply_for_event(event_name):
    global apply_window
    apply_window = tk.Toplevel(window)
    apply_window.title("Event Application Form")
    apply_window.geometry("500x600")
    apply_window.configure(bg='#E0F7FA')

    # Create a frame for the form entries
    form_frame = tk.Frame(apply_window, bg='#E0F7FA', bd=2, relief='ridge')
    form_frame.pack(pady=20, padx=20, fill='both', expand=True)

    # Add a title to the form
    title_label = tk.Label(form_frame, text=f"Apply for {event_name}", font=('Helvetica Neue', 18, 'bold'), bg='#E0F7FA', fg='#004D40')
    title_label.pack(pady=(20, 10))

    # Add a list of labels and entries
    labels = ["Name:", "Email:", "Contact Number:", "College:", "Branch:"]
    entries = []

    for label in labels:
        label_frame = tk.Frame(form_frame, bg='#E0F7FA')
        label_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(label_frame, text=label, bg='#E0F7FA', fg='#004D40', font=('Helvetica Neue', 12, 'bold')).pack(side='left')
        entry = tk.Entry(label_frame, font=('Helvetica Neue', 12), width=30, bd=0, relief='flat')
        entry.pack(side='right', ipady=5)
        entry.config(highlightthickness=1, highlightbackground="#B2EBF2", highlightcolor="#00BCD4")
        entries.append(entry)

    # Add a text area for additional comments
    tk.Label(form_frame, text="Additional Comments:", bg='#E0F7FA', fg='#004D40', font=('Helvetica Neue', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
    comments_text = tk.Text(form_frame, height=4, width=40, font=('Helvetica Neue', 12), bd=0, relief='flat')
    comments_text.pack(padx=20, pady=5)
    comments_text.config(highlightthickness=1, highlightbackground="#B2EBF2", highlightcolor="#00BCD4")

    # Function to handle the submission
    def submit_form():
        # Retrieve data from entries
        name, email, contact, college, branch = [entry.get() for entry in entries]  # Fixed: Added college to the retrieval
        comments = comments_text.get("1.0", tk.END).strip()

        # Validate inputs
        if not all([name, email, contact, college, branch]):  # Fixed: Added college to the validation
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        # Save data to Excel
        save_to_excel(event_name, name, email, contact, college, branch, comments)  # Fixed: Added college to the save function

        messagebox.showinfo("Submitted", f"Thank you, {name}! Your application for {event_name} has been recorded.")
        apply_window.destroy()  # Close the form window

    # Submit Button with rounded corners and custom style
    submit_button = tk.Button(form_frame, text="Submit Application", command=submit_form, 
                              bg='#00BCD4', fg='white', font=('Helvetica Neue', 14, 'bold'),
                              relief='flat', padx=20, pady=10)
    submit_button.pack(pady=20)

    # Hover effect for the submit button
    submit_button.bind("<Enter>", lambda e: submit_button.config(bg='#00ACC1'))
    submit_button.bind("<Leave>", lambda e: submit_button.config(bg='#00BCD4'))

# Function to save form data to Excel
def save_to_excel(event_name, name, email, contact, college, branch, comments):
    excel_file = r"D:\Data\applications.xlsx"
    
    # Create a new workbook if the file doesn't exist
    if not os.path.exists(excel_file):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Event Name', 'Name', 'Email', 'Contact', 'College', 'Branch', 'Comments'])  # Added College to the header
    else:
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

    # Append the new data
    sheet.append([event_name, name, email, contact, college, branch, comments])  # Added college to the data being saved

    # Save the workbook
    try:
        workbook.save(excel_file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the Excel file: {e}")  # Added error handling for save operation

# Function to create college buttons dynamically
def show_colleges():
    global current_view
    current_view = "colleges"

    # Clear previous widgets from the main canvas
    for widget in canvas.winfo_children():
        widget.destroy()

    # Add a back button with an enhanced design (optional: you can remove this if homepage is the first view)
    back_button = tk.Button(canvas, text='Back', command=go_to_homepage, 
                        bg='#FF7043', fg='white', font=FONT_BUTTON)
    back_button.pack(pady=15)

    # Frame for college buttons with a nice border
    college_frame = tk.Frame(canvas, bg='#667872', bd=5, relief=tk.SUNKEN)
    college_frame.pack(pady=40, padx=300, fill=tk.BOTH, expand=True)

    # College information
    colleges = {
        "COEP (College of Engineering, Pune)": {},
        "VJTI (Veermata Jijabai Technological Institute)": {},
        "DKTE (DKTE Society's Textile & Engineering Institute)": {
            "AISA": "AISA (Artificial Intelligence Student Association) focuses on advancing AI research and applications within the college.",
            "DSSA": "DSSA (Data Science Student Association) is dedicated to exploring data science, machine learning, and software development.",
            "ACSES": "ACSES (Associate of Computer Science Students) promotes innovation in computing and systems engineering projects.",
            "IEEE": "IEEE (Institute of Electrical and Electronics Engineers) supports students in electrical engineering and related fields through workshops and competitions."
        },
        "SIT (Sharad Institute of Technology College of Engineering)": {
            "AISA": "AISA at SIT integrates artificial intelligence with practical applications, fostering innovation and research.",
            "DSSA": "DSSA at SIT explores data analytics, machine learning, and software development to solve real-world problems.",
            "ACSES": "ACSES at SIT encourages students to engage in advanced computing and systems engineering projects.",
            "IEEE": "IEEE at SIT provides resources and opportunities for students in electrical and electronics engineering."
        },
        "WCE (Walchand College of Engineering)": {
            "AISA": "AISA at WCE focuses on AI-driven solutions and research initiatives within the college.",
            "DSSA": "DSSA at WCE delves into data science methodologies and software engineering practices.",
            "ACSES": "ACSES at WCE promotes cutting-edge computing and systems engineering projects.",
            "IEEE": "IEEE at WCE organizes workshops and competitions for aspiring electrical engineers."
        },
        "KIT (Kolhapur Institute of Technology)": {
            "AISA": "AISA at KIT emphasizes the development and application of artificial intelligence technologies.",
            "DSSA": "DSSA at KIT is committed to advancing data science and software development skills among students.",
            "ACSES": "ACSES at KIT fosters innovation in computing and systems engineering through collaborative projects.",
            "IEEE": "IEEE at KIT offers platforms for students to engage in electrical engineering projects and competitions."
        },
        "RIT (Rajarambapu Institute of Technology)": {
            "AISA": "AISA at RIT integrates AI with engineering solutions, promoting interdisciplinary research.",
            "DSSA": "DSSA at RIT focuses on data science, machine learning, and cutting-edge software development.",
            "ACSES": "ACSES at RIT encourages students to innovate in computing and systems engineering.",
            "IEEE": "IEEE at RIT provides opportunities for electrical engineering students through workshops and events."
        },
        "ADCET (Annasaheb Dange College of Engineering and Technology)": {},
        "PVPIT (Padmabhooshan Vasantraodada Patil Institute of Technology)": {},
        "DYPCET (D. Y. Patil College Of Engineering & Technology)": {},
        "WIT (Walchand Institute of Technology)": {},
        "PICT (Pune Institute of Computer Technology)": {},
        "VIT (Vishwakarma Institute of Technology)": {},
        "VIIT (Vishwakarma Institute Of Information Technology)": {},
        "GCEK (Government College of Engineering, Karad)": {},
        "MIT-WPU (MIT World Peace University)": {},
    }

    # Create and display college buttons with hover effect
    for college, clubs in colleges.items():
        button = tk.Button(college_frame, text=college, command=lambda c=college, cl=clubs: display_clubs(c, cl), 
                           bg='#015582', fg='white', font=FONT_BUTTON, relief=tk.FLAT)
        button.pack(pady=5, padx=10, fill=tk.X)

        # Hover effects for enlarging
        button.bind("<Enter>", lambda e, btn=button: btn.config(font=('Helvetica Neue', 14, 'bold')))
        button.bind("<Leave>", lambda e, btn=button: btn.config(font=FONT_BUTTON))

# Function to display clubs of a college
def display_clubs(college_name, clubs):
    global current_view, current_college, current_clubs
    current_view = "clubs"
    current_college = college_name
    current_clubs = clubs

    # Clear previous widgets from the main canvas
    for widget in canvas.winfo_children():
        widget.destroy()

    # Show the college name in a label
    title_label = tk.Label(canvas, text="Clubs", font=FONT_TITLE, fg='#333', bg='#737070')
    title_label.place(relx=0.5, rely=0.1, anchor='center')

    # Frame for club cards with a nice border
    club_frame = tk.Frame(canvas, bg='#5D7394', bd=5, relief=tk.SUNKEN)
    club_frame.pack(pady=40, padx=300, fill=tk.BOTH, expand=True)

    # Show the clubs for the college
    for club, details in clubs.items():
        club_card = tk.Frame(club_frame, bg='#FFFFFF', bd=2, relief=tk.RAISED, padx=10, pady=10)
        club_card.pack(pady=10, fill=tk.X, padx=10)

        club_label = tk.Label(club_card, text=club, font=('Helvetica Neue', 14, 'bold'), fg='#015582', bg='#FFFFFF')
        club_label.pack(anchor='w', pady=5)

        club_info = tk.Label(club_card, text=details, font=FONT_INFO, fg='#333', bg='#FFFFFF', wraplength=600, justify='left')
        club_info.pack(anchor='w', pady=5)

        # Add an "Explore" button to explore the events for each club
        explore_button = tk.Button(club_card, text="Explore", command=lambda c=club: explore_club_events(c, club_events.get(c, {})),
                                   bg='#FF7043', fg='white', font=FONT_BUTTON)
        explore_button.pack(pady=5)

        # Hover effects for the club cards
        club_card.bind("<Enter>", lambda e, btn=club_card: btn.config(bg='#f2f2f2'))
        club_card.bind("<Leave>", lambda e, btn=club_card: btn.config(bg='#FFFFFF'))

    # Add a "Back to Colleges" button
    back_to_colleges_button = tk.Button(canvas, text='Back to Colleges', command=show_colleges, 
                                        bg='#FF7043', fg='white', font=FONT_BUTTON)
    back_to_colleges_button.place(relx=0.5, rely=0.9, anchor='center')

# Define the events for each club
club_events = {
    "AISA": {
        "AI Symposium": {
            "date": "January 15, 2025",
            "time": "10:00 AM",
            "location": "DKTE Hall 101",
            "description": "Join us for an in-depth symposium on the latest advancements in Artificial Intelligence and their real-world applications."
        },
        "Machine Learning Workshop": {
            "date": "May 20, 2024",
            "time": "2:00 PM",
            "location": "DKTE Conference Room",
            "description": "Enhance your machine learning skills through hands-on projects and expert-led sessions."
        }
    },
    "DSSA": {
        "Data Science Hackathon": {
            "date": "January 5, 2024",
            "time": "11:00 AM",
            "location": "DKTE Auditorium",
            "description": "Compete in our data science hackathon to solve real-world problems using data analytics and machine learning."
        },
        "Software Development Bootcamp": {
            "date": "January 15, 2025",
            "time": "10:00 AM",
            "location": "DKTE Conference Room",
            "description": "Intensive bootcamp covering the latest in software development practices and technologies."
        }
    },
    "ACSES": {
        "Advanced Computing Workshop": {
            "date": "May 10, 2024",
            "time": "8:00 AM",
            "location": "WCE Main Hall",
            "description": "Dive into advanced computing topics with hands-on sessions and expert guidance."
        },
        "Systems Engineering Seminar": {
            "date": "June 18, 2024",
            "time": "1:00 PM",
            "location": "WCE Lab 3",
            "description": "Explore the fundamentals and latest trends in systems engineering through interactive seminars."
        }
    },
    "IEEE": {
        "Electrical Engineering Expo": {
            "date": "April 25, 2024",
            "time": "4:00 PM",
            "location": "KIT Auditorium",
            "description": "Showcase your projects and innovations in electrical engineering at our annual expo."
        },
        "Robotics and Automation Workshop": {
            "date": "May 30, 2024",
            "time": "10:00 AM",
            "location": "KIT Lab 5",
            "description": "Learn about the latest in robotics and automation through hands-on workshops and demonstrations."
        }
    }
    # Add more events for other clubs as needed
}

# Function to change the background image
def change_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        update_background(file_path)

# Function to update the background image
def update_background(image_path):
    global bg_photo
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((window.winfo_width(), window.winfo_height()))  # Adjust to window size
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image.\n{e}")

# Function to display help information
def toggle_help():
    if help_check_string.get() == 'on':
        help_message = ("This project not only fosters community engagement among students but also provides a "
                        "centralized hub for college activities, enhancing the overall college experience. Would "
                        "you like to dive deeper into any specific aspect?")
        messagebox.showinfo("Help", help_message)

# Function to close the application
def close_application():
    window.quit()

# Function to go back to the homepage
def go_to_homepage():
    global current_view
    current_view = "homepage"
    
    # Clear the canvas to go back to the homepage view
    for widget in canvas.winfo_children():
        widget.destroy()  # Clear previous widgets

    # Re-add the background image
    if bg_photo:
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
    # Add the title label
    title_label = tk.Label(canvas, text='Welcome to Event Hunt', font=FONT_TITLE, fg='white', bg='#012d54')
    title_label.place(relx=0.5, rely=0.05, anchor='center')
    
    # Add the information label
    info_text = ("Navigating the vibrant landscape of college extracurricular activities shouldn't be a challenge. "
        "At Event Hunt, we recognize that college students often struggle to stay updated on events organized by various student clubs. "
        "The current process can be fragmented and inefficient, forcing students to sift through multiple sources like individual club websites, "
        "social media, and bulletin boards.\n\n"
        "Event Hunt serves as a centralized hub where students can effortlessly explore, engage, and participate in a wide array of activities tailored to their interests. "
        "Whether you're passionate about artificial intelligence, data science, computer science, or electrical engineering, Event Hunt connects you with the right associations and events to enrich your college journey.\n\n"
        "Join us in transforming your college experience into a vibrant tapestry of learning and networking opportunities. "
        "With Event Hunt, you can discover workshops, competitions, and social gatherings that align with your passions and career aspirations. "
        "Let us help you make the most of your time in college, ensuring that every moment is filled with growth and excitement!")
    info_label = tk.Label(canvas, text=info_text, 
                          font=FONT_INFO, fg='#FFFFFF', bg='#007ACC', wraplength=1000, padx=10, pady=10, 
                          relief=tk.RAISED, bd=1)
    info_label.place(relx=0.5, rely=0.25, anchor='center')

    # Upcoming Events Section
    upcoming_events_text = ("Upcoming Events:\n\n"
                            "1. Electrical Engineering Expo\n"
                            "   Date: December 25, 2024\n"
                            "   Time: 10:00 AM\n"
                            "   Location: KIT (Kolhapur Institute of Technology), Kolhapur \n"
                            "   Description: Showcase your projects and innovations in electrical engineering at our annual expo.\n\n"
                            "2. Robotics and Automation Workshop\n"
                            "   Date: December 30, 2024\n"
                            "   Time: 10:00 AM\n"
                            "   Location: COEP, Pune\n"
                            "   Description: Learn about the latest in robotics and automation through hands-on workshops and demonstrations.\n\n"
                            "3. AI and Machine Learning Symposium\n"
                            "   Date: January 15, 2025\n"
                            "   Time: 10:00 AM\n"
                            "   Location: DKTE (DKTE Society's Textile & Engineering Institute), Ichalkaranji\n"
                            "   Description: Join industry experts to discuss the future of AI and its applications in various fields.\n\n")
    upcoming_events_label = tk.Label(canvas, text=upcoming_events_text, 
                                      font=FONT_INFO, fg='#FFFFFF', bg='#697565', wraplength=1000, padx=10, pady=10, 
                                      relief=tk.RAISED, bd=1)
    upcoming_events_label.place(relx=0.5, rely=0.7, anchor='center')  # Position below the info label

def show_contact_info():
    contact_info = ("For any inquiries or support, please contact us:\n\n"
                    "Email: support@eventhunt.com\n"
                    "Phone: +91 7066954209\n"
                    "Address: Rajwada, Ichalkaranji, Maharashtra 416115\n\n"
                    "Follow us on social media:\n"
                    "Twitter: @EventHunt\n"
                    "Facebook: /EventHuntOfficial\n"
                    "Instagram: @event_hunt")
    messagebox.showinfo("Contact Information", contact_info)

# Create the main window
window = tk.Tk()
window.attributes('-fullscreen', True)  # Set to full screen
window.title('Event Hunt')

# Load default background image
def load_default_background():
    global bg_photo
    default_bg_path = "gradient2.jpg"  # Replace with your default background image path
    if os.path.exists(default_bg_path):
        try:
            bg_image = Image.open(default_bg_path)
            bg_image = bg_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))  # Resize to screen size
            bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load default background image.\n{e}")
            bg_photo = ImageTk.PhotoImage(Image.new('RGB', (window.winfo_screenwidth(), window.winfo_screenheight()), color='#737070'))
    else:
        # If the image is not found, create a plain background
        bg_photo = ImageTk.PhotoImage(Image.new('RGB', (window.winfo_screenwidth(), window.winfo_screenheight()), color='#737070'))

# Call the function to load the background
load_default_background()

# Create a canvas and add the background image
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Add an information label about the program
title_label = tk.Label(canvas, text='Welcome to Event Hunt', font=FONT_TITLE, fg='white', bg='#012d54')
title_label.place(relx=0.5, rely=0.1, anchor='center')

# Enhance the information label
info_text = ('Navigating the vibrant landscape of college extracurricular activities shouldn\'t be a challenge. '
             'At Event Hunt, we recognize that college students often struggle to stay updated on events organized by '
             'various student clubs. The current process can be fragmented and inefficient, forcing students to sift '
             'through multiple sources like individual club websites, social media, and bulletin boards.')
info_label = tk.Label(canvas, text=info_text, 
                      font=FONT_INFO, fg='white', bg='#5D7394', wraplength=1000, padx=10, pady=10, 
                      relief=tk.RAISED, bd=0.5)
info_label.place(relx=0.5, rely=0.25, anchor='center')

# Create the menu
menu = tk.Menu(window)

# File menu with submenus
file_menu = tk.Menu(menu, tearoff=False)
file_menu.configure(bg='#2196F3', fg='white', activebackground='#FF5733', activeforeground='white')

# New submenu
new_sub_menu = tk.Menu(file_menu, tearoff=False)
new_sub_menu.add_command(label='Home', command=go_to_homepage)  # Go to homepage
new_sub_menu.add_command(label='New Template', command=change_background)  # Change background here
file_menu.add_cascade(label='New', menu=new_sub_menu)

# Open submenu
open_sub_menu = tk.Menu(file_menu, tearoff=False)
open_sub_menu.add_command(label='Open Recent', command=lambda: messagebox.showinfo("Info", "Recent file opened!"))
file_menu.add_cascade(label='Open', menu=open_sub_menu)

file_menu.add_separator()
file_menu.add_command(label='Close', command=close_application)  # Close command

# Add "Show Colleges" option
file_menu.add_separator()
file_menu.add_command(label='Show Colleges', command=show_colleges)

# Change the label of the menu from 'File' to 'Menu'
menu.add_cascade(label='Menu', menu=file_menu)

# Help menu
help_menu = tk.Menu(menu, tearoff=False)
help_menu.configure(bg='#2196F3', fg='white', activebackground='#FF5733', activeforeground='white')

help_check_string = tk.StringVar(value='off')
help_menu.add_checkbutton(label='Enable Help', onvalue='on', offvalue='off', variable=help_check_string, command=toggle_help)
menu.add_cascade(label='Help', menu=help_menu)

# Contact menu
contact_menu = tk.Menu(menu, tearoff=False)
contact_menu.configure(bg='#2196F3', fg='white', activebackground='#FF5733', activeforeground='white')
contact_menu.add_command(label='Contact Us', command=show_contact_info)
menu.add_cascade(label='Contact', menu=contact_menu)

# Configure the window to display the menu
window.config(menu=menu)

# Show the homepage when the app starts
go_to_homepage()

# Run the application
window.mainloop()