import subprocess
import sys
from tkinter import *
from PIL import Image
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("Filter Option")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the dimensions and position of the window
window_width = 700
window_height = 450
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def filter_color():
    command = [sys.executable, "checkLogin.py"]
    subprocess.Popen(command)
    root.destroy()

def filter_face():
    command = [sys.executable, "checkLogin.py"]
    subprocess.Popen(command)
    root.destroy()

# Load and display the images
image1 = ctk.CTkImage(light_image=Image.open("setting_img/filter_color.jpg"), dark_image=Image.open("setting_img/filter_color.jpg"), size=(270, 370))
image2 = ctk.CTkImage(light_image=Image.open("setting_img/filter_face.png"), dark_image=Image.open("setting_img/filter_face.png"), size=(270, 370))

# Create labels to display the images
label1 = ctk.CTkLabel(root, text="", image=image1)
label2 = ctk.CTkLabel(root, text="", image=image2)

# Create buttons
filter_color_button = ctk.CTkButton(root, text="Filter Color", font=("Arial", 13, "bold"), corner_radius=32, command=filter_color)
filter_face_button = ctk.CTkButton(root, text="Filter Face", font=("Arial", 13, "bold"), corner_radius=32, command=filter_face)

# Place labels using grid() method
label1.grid(row=0, column=0, padx=10, pady=10)
label2.grid(row=0, column=1, padx=10, pady=10)

# Place buttons using grid() method
filter_color_button.grid(row=1, column=0, padx=10, pady=10)
filter_face_button.grid(row=1, column=1, padx=10, pady=10)

# Center widgets horizontally in the window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()
