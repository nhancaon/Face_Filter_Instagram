import customtkinter as ctk
import subprocess
import sys
from tkinter import *
from PIL import Image

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("Login Form")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the dimensions and position of the window
window_width = 300
window_height = 350
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def login():
    command = [sys.executable, "checkLogin.py"]
    subprocess.Popen(command)
    root.destroy()

def exit_program():
    root.destroy()

title_label = ctk.CTkLabel(root, text="Welcome to Face Filter app", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Load and display the image
avatar = ctk.CTkImage(light_image=Image.open("setting_img/face-login.jpg"), dark_image=Image.open("setting_img/face-login.jpg"), size=(100, 100))
ava_label = ctk.CTkLabel(root, text="", image=avatar)
ava_label.pack(pady=10)


# Create buttons
login_button = ctk.CTkButton(root, text="Login", command=login)
exit_button = ctk.CTkButton(root, text="Exit", command=exit_program)

# Place labels, entry fields, and buttons using grid layout
login_button.pack(pady=20)
exit_button.pack(pady=10)

root.mainloop()
