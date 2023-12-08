import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
from functools import partial
from cryptography.fernet import Fernet
import os

# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
root = None  # Declare root as a global variable
# List to store passwords
password = []


def update(app_name_entry, user_name_entry, old_password_entry, new_password_entry, update_result_label):
    app_name = app_name_entry.get()
    user_name = user_name_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    if not app_name or not user_name or not old_password or not new_password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    with open("passwords.txt", "r") as file:
        lines = file.readlines()
        updated_lines = []
        is_updated = False
        current_password = {}
        for line in lines:
            if line.strip() == "":
                # and current_password.get("User Name") == user_name
                if (current_password.get("App Name") == app_name and current_password.get("Username") == user_name
                        and current_password.get("Password") == old_password):
                    current_password["Password"] = new_password
                    is_updated = True
                for key, value in current_password.items():
                    updated_lines.append(f"{key}: {value}\n")
                updated_lines.append("\n")
                current_password = {}
            else:
                key, value = line.split(": ")
                current_password[key] = value.strip()

        with open("passwords.txt", "w") as file:
            file.writelines(updated_lines)

        if is_updated:
            update_result_label.config(text="Password updated successfully!")
        else:
            update_result_label.config(text="Password not found!")


# Function to generate a random password
def generate_password():
    length = random.randint(10, 20)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def encrypt(password):
    with open ("crypto.key", "rb") as file:
        key = file.read()
    fernet = Fernet(key)

        # encrypted_password = cipher_suite.encrypt(password.encode())
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt(encrypted_password):
    with open ("crypto.key", "rb") as file:
        key = file.read()
    fernet = Fernet(key)

    decrypted_password = fernet.decrypt(password.decode())
    return decrypted_password

    # encrypted_password = cipher_suite.encrypt(password.encode())

    # decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    # return decrypted_password


# Function to go back to the main menu
# def back():
#     window.destroy()  # Close the current window


def test(field):
    field.delete(0, tk.END)
    field.insert(0, generate_password())


def save(app_name_entry, user_name_entry, password_entry):

    app_name = app_name_entry.get()
    username = user_name_entry.get()
    password = password_entry.get()

    if app_name and username and password:
        with open("passwords.txt", "a") as file:
            file.write(f"App Name: {app_name.encode}\n")
            file.write(f"Username: {username.encode}\n")
            file.write(f"Password: {enc_password}\n\n")

        app_name_entry.delete(0, tk.END)
        user_name_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        # password = encrypt(password.get())
        messagebox.showinfo("Success", "Password saved successfully.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


def exit_app():
    root.destroy()

def goBack(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()

# def get():
def get(app_name_retrieve_entry, username_retrieve_entry, result_label):
    app_name = app_name_retrieve_entry.get()
    user_name = username_retrieve_entry.get()

    with open("passwords.txt", "rb") as file:
        lines = file.readlines()
        passwords = []
        current_password = {}
        for line in lines:
            if line.strip() == "":
                passwords.append(current_password)
                current_password = {}
            else:
                key, value = line.split(": ")
                current_password[key] = value.strip()

        for password in passwords:
            if password.get("App Name") == app_name and password.get("Username") == user_name:
                result_label.config(text=f"App Name: {password.get('App Name')}\n"
                                         f"Username: {password.get('Username')}\n"
                                         f"Password: {password.get('Password')}")
                return

        result_label.config(text="Password not found!")


def retrieve_password(previous_window):
    """Tkinter function to retrieve passwords to a file"""
    previous_window.withdraw()  # Hide the main window

    window3 = tk.Tk()
    window3.title("Retrieve")
    frame = tk.Frame(window3)
    frame.pack()
    app_name_retrieve_label = tk.Label(frame, text="Application Name:")
    app_name_retrieve_label.grid(row=0, column=0, padx=10, pady=5)
    # app_name_retrieve_entry = tk.Entry(frame)
    # app_name_retrieve_entry.grid(row = 0, column = 1, padx= 10, pady= 5)
    app_name_retrieve_entry = ttk.Combobox(frame,
                                           values=["Facebook", "Instagram", "Twitter", "Snapchat", "Google", "Netflix",
                                                   "Discord", "Spotify", "Youtube", "Reddit", "TikTok", "Pinterest",
                                                   "Github", "LinkedIn", "Wordpress", "Gmail", "Protonmail", "Outlook",
                                                   "Gmail"])
    app_name_retrieve_entry.grid(row=0, column=1, padx=10, pady=5)
    username_retrieve_label = tk.Label(frame, text="Username:")
    username_retrieve_label.grid(row=1, column=0, padx=10, pady=5)
    username_retrieve_entry = tk.Entry(frame)
    username_retrieve_entry.grid(row=1, column=1, padx=10, pady=5)

    back_button = tk.Button(frame, text="Back", command=lambda: goBack(window3, previous_window))
    back_button.grid(row=4, column=0, sticky="news", padx=20, pady=5)
    get_button = tk.Button(frame, text="Get",
                           command=lambda: get(app_name_retrieve_entry, username_retrieve_entry, result_label))
    get_button.grid(row=4, column=2, sticky="news", padx=20, pady=5)
    result_label = tk.Label(frame, text="")
    result_label.grid(row=2, column=1, sticky="news", padx=20, pady=5)

    def close_window3():
        window3.destroy()
        previous_window.deiconify()

    window3.protocol("WM_DELETE_WINDOW", close_window3)


#   """Tkinter function to update password"""
def update_password(previous_window):
    """Tkinter function to update passwords to a file"""
    previous_window.withdraw()  # Hide the main window

    window2 = tk.Tk()
    window2.title("Update Password Menu")
    frame = tk.Frame(window2)
    frame.pack()
    app_name_label = tk.Label(frame, text="Application Name:")
    # app_name = tkinter.Label(frame, text= "Application Name")
    # app_name_entry = tk.Entry(frame)
    app_name_entry = ttk.Combobox(frame, values=["Facebook", "Instagram", "Twitter", "Snapchat", "Google", "Netflix",
                                                 "Discord", "Spotify", "Youtube", "Reddit", "TikTok", "Pinterest",
                                                 "Github", "LinkedIn", "Wordpress", "Gmail", "Protonmail", "Outlook",
                                                 "Gmail"])

    user_name_label = tk.Label(frame, text="User Name:")
    user_name_entry = tk.Entry(frame)
    old_password_label = tk.Label(frame, text="Old Password:")
    old_password_entry = tk.Entry(frame)
    new_password_label = tk.Label(frame, text="New Password:")
    new_password_entry = tk.Entry(frame)
    back_button = tk.Button(frame, text="Back", command=lambda: goBack(window2, previous_window))
    update_button = tk.Button(frame, text="Update",
                              command=lambda: update(app_name_entry, user_name_entry, old_password_entry,
                                                     new_password_entry, update_result_label))
    update_result_label = tk.Label(frame, text="")

    # app_name_label.pack()
    app_name_label.grid(row=0, column=0, padx=10, pady=5)
    # app_name_entry.pack()
    app_name_entry.grid(row=0, column=1, padx=10, pady=5)
    # user_name_label.pack()
    user_name_label.grid(row=1, column=0, sticky="news", padx=10, pady=5)

    # user_name_entry.pack()
    user_name_entry.grid(row=1, column=1, sticky="news", padx=10, pady=5)
    # old_password_label.pack()
    old_password_label.grid(row=2, column=0, sticky="news", padx=5, pady=5)
    # old_password_entry.pack()
    old_password_entry.grid(row=2, column=1, sticky="news", padx=10, pady=5)
    # new_password_label.pack()
    new_password_label.grid(row=3, column=0, sticky="news", padx=5, pady=5)
    # new_password_entry.pack()
    new_password_entry.grid(row=3, column=1, sticky="news", padx=10, pady=5)
    # update_button.pack()
    update_button.grid(row=4, column=2, sticky="news", padx=10, pady=5)

    back_button.grid(row=4, column=0, sticky="news", padx=10, pady=5)
    # update_result_label.pack()
    update_result_label.grid(row=4, column=1, sticky="news", padx=10, pady=5)

    def close_window3():
        window2.destroy()
        previous_window.deiconify()

    window2.protocol("WM_DELETE_WINDOW", close_window3)


def save_password(previous_window):
    """Tkinter function to save passwords to a file"""
    if not os.path.exists("crypto.key"):
        with open ("crypto.key", 'wb') as file:
            key = Fernet .generate_key()
            file.write(key)

    previous_window.withdraw()  # Hide the main window

    window1 = tk.Tk()
    window1.title("Save Password Menu")
    frame = tk.Frame(window1)
    frame.pack()
    app_name = tk.Label(frame, text="Application Name")
    app_name.grid(row=0, column=0, padx=10, pady=5)
    app_name_entry = ttk.Combobox(frame, values=["Facebook", "Instagram", "Twitter", "Snapchat", "Google", "Netflix",
                                                 "Discord", "Spotify", "Youtube", "Reddit", "TikTok", "Pinterest",
                                                 "Github", "LinkedIn", "Wordpress", "Gmail", "Protonmail", "Outlook",
                                                 "Gmail"])
    app_name_entry.grid(row=0, column=1, padx=10, pady=5)
    user_name = tk.Label(frame, text="User Name")
    user_name.grid(row=1, column=0, sticky="news", padx=10, pady=5)
    user_name_entry = tk.Entry(frame)
    user_name_entry.grid(row=1, column=1, sticky="news", padx=10, pady=5)
    password = tk.Label(frame, text="Password")
    password.grid(row=2, column=0, sticky="news", padx=5, pady=5)
    password_entry = tk.Entry(frame)
    password_entry.grid(row=2, column=1, sticky="news", padx=10, pady=5)
    generate_pass = tk.Button(frame, text="Generate Password", command=partial(test, password_entry))
    generate_pass.grid(row=3, column=2, sticky="news", padx=1, pady=1)
    # back_button = tk.Button(frame, text="Back", command=partial(goBack, window1))
    back_button = tk.Button(frame, text="Back", command=lambda: goBack(window1, previous_window))
    back_button.grid(row=4, column=0, sticky="news", padx=10, pady=5)
    # save_button = tk.Button(frame, text="Save Password", command= save)
    save_button = tk.Button(frame, text="Save", command=lambda: save(app_name_entry, user_name_entry, password_entry))
    save_button.grid(row=4, column=2, sticky="news", padx=10, pady=5)

    def close_window1():
        window1.destroy()
        previous_window.deiconify()

    window1.protocol("WM_DELETE_WINDOW", close_window1)





def main_UI():
    global root
    root = tk.Tk()
    root.title("Main Menu")
    frame = tk.Frame(root)
    frame.pack()
    user_info = tk.Label(frame, text="Welcome to the Password Managing System")
    user_info.grid(row=0, column=1, padx=20, pady=5)

    button = tk.Button(frame, text="Save Password", command=lambda: save_password(root))
    button.grid(row=1, column=1, padx=20, pady=5)
    # button = tk.Button(frame, text="Save Password", command=lambda: open_save_password(root))
    retrieve_pass = tk.Button(frame, text="Retrieve Password", command=lambda: retrieve_password(root))
    retrieve_pass.grid(row=2, column=1, padx=20, pady=5)

    update_pass = tk.Button(frame, text="Update Password", command=lambda: update_password(root))
    update_pass.grid(row=3, column=1, padx=20, pady=5)

    exit = tk.Button(frame, text="Exit", command=lambda: exit_app() )
    exit.grid(row=4, column=1, padx=20, pady=5)


    root.mainloop()

if __name__ == "__main__":
    main_UI()