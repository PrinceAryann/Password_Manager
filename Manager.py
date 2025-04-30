import os  # For handling system environment variables
from tkinter import *
from tkinter import messagebox
import random  # For generating random passwords
import string  # For accessing letters and digits
import re  # For password validation using regex

# Fonts used for the UI elements
FONT = ('Times New Roman', 15, 'bold')
INPUT_FONT = ('Times New Roman', 15)

# Function to generate a random password
def create_password():
    """Generates a random password containing letters, symbols, and numbers."""
    # Define characters used in the password
    letters = string.ascii_letters  
    symbols = "!@#$%^&*()-+=_"
    numbers = string.digits  

    # Generate random counts for letters, symbols, and numbers
    num_letters = random.randint(8, 10)
    num_symbols = random.randint(2, 4)
    num_numbers = random.randint(2, 4)

    # Create the password by randomly choosing characters
    password = (
        random.choices(letters, k=num_letters) +
        random.choices(symbols, k=num_symbols) +
        random.choices(numbers, k=num_numbers)
    )
    random.shuffle(password)  # Shuffle characters for randomness

    final_password = "".join(password)  # Convert list to string
    password_value.set(final_password)  # Display in password entry

    # Copy password to clipboard for convenience
    window.clipboard_clear()
    window.clipboard_append(final_password)
    window.update()

# Validate password using regex pattern
def validate_password(password):
    """Validates password using regex pattern."""
    pattern = (
        r"^(?=.*[a-zA-Z])"  # At least one letter
        r"(?=.*\d)"  # At least one digit
        r"(?=.*[!%&'()*+,-./:;<=>?@[\]^_`{|}~])"  # At least one special char
        r"[A-Za-z\d!%&'()*+,-./:;<=>?@[\]^_`{|}~]{8,}$"  # Min 8 chars
    )
    return bool(re.match(pattern, password))  # Return validation result

# Toggle password visibility between hidden and visible
def toggle_password():
    """Toggles password visibility between hidden and visible."""
    if password_entry.cget('show') == '*':  # If hidden
        password_entry.config(show='')  # Show password
        eye.config(text='👁')  # Update button text to indicate visibility
        window.after(500, toggle_password)  # Auto-hide after 500ms
    else:
        password_entry.config(show='*')  # Hide password
        eye.config(text='🙈')  # Update button text to indicate hidden state

# Store the credentials in system environment variables
def store_data():
    """Stores the credentials in system environment variables."""
    if not website_entry.get() or not username_entry.get() or not password_value.get():
        messagebox.showwarning("Oops!", "All fields are mandatory!")
    else:
        is_ok = messagebox.askokcancel(
            title=website_entry.get(),
            message=f"Details:\nEmail: {username_entry.get()}\nPassword: {password_value.get()}\nSave?"
        )
        if is_ok:
            if validate_password(password_value.get()):
                # Create a new variable for website credentials using uppercase
                website_key = website_entry.get().replace(" ", "_").upper()
                os.environ[website_key + "_EMAIL"] = username_entry.get()  # Save username in env variable
                os.environ[website_key + "_PASSWORD"] = password_value.get()  # Save password in env variable

                # Clear input fields and show success message
                website_entry.delete(0, END)
                username_entry.delete(0, END)
                password_value.set("")
                messagebox.showinfo("Success", "Data Saved")
            else:
                messagebox.showwarning("Error", "Password Validation Failed!")
                password_value.set("")  # Clear password if validation fails
        else:
            username_entry.delete(0, END)
            password_value.set("")  # Clear password if user cancels

# Search for stored credentials based on website name
def search_data():
    """Searches for stored credentials in environment variables."""
    website = website_entry.get().replace(" ", "_").upper()  # Standardize website name
    if not website:
        messagebox.showwarning("Blank Field", "Please Enter Website Name!")
        return

    # Check if environment variables exist for the entered website
    email_key = website + "_EMAIL"
    password_key = website + "_PASSWORD"

    if email_key in os.environ and password_key in os.environ:
        username = os.environ[email_key]  # Retrieve email from env variable
        password = os.environ[password_key]  # Retrieve password from env variable
        User_name.set(username)  # Display username
        password_value.set(password)  # Display password
    else:
        messagebox.showinfo("Not Found", "No details for the entered website.")

# Set up the main application window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Display logo using a Canvas widget
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file=r"logo_placeholder.png")  # Replace with actual logo file path
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Website input field
Label(text="Website:", font=FONT).grid(row=1, column=0,padx=10,pady=10, sticky="w")
website_frame = Frame(window)
website_frame.grid(row=1, column=1, columnspan=2,padx=10,pady=10, sticky="w")
website_name = StringVar()
website_entry = Entry(website_frame, textvariable=website_name, width=35, font=INPUT_FONT)
website_entry.grid(padx=10,pady=10,row=1, column=1)
Button(website_frame, text="Search", command=search_data).grid(padx=10,pady=10,row=1, column=2)

# Username input field
Label(text="Email/Username:", font=FONT).grid(row=2, column=0,padx=10,pady=10, sticky="w")
User_name = StringVar()
username_entry = Entry(textvariable=User_name, width=35, font=INPUT_FONT)
username_entry.grid(row=2, column=1, columnspan=2,padx=20,pady=10, sticky="w")

# Password input field and controls
Label(text="Password:", font=FONT).grid(row=3, column=0,padx=10,pady=10, sticky="w")
password_frame = Frame(window)
password_frame.grid(row=3, column=1, columnspan=2,padx=10,pady=10, sticky="w")
password_value = StringVar()
password_entry = Entry(password_frame, textvariable=password_value, width=21, font=INPUT_FONT, show="*")
password_entry.grid(pady=10,row=3, column=1)
eye = Button(password_frame, text='👁', command=toggle_password)
eye.grid(row=3, column=2)
Button(password_frame, text="Generate password", command=create_password).grid(padx=10, pady=10, row=3, column=3)

# Add button to store credentials
Button(text="Add", width=50, command=store_data).grid(row=4, column=1, columnspan=2,padx=10,pady=10, sticky="w")

# Start the main event loop
window.mainloop()
