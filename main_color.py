import customtkinter as ctk
import subprocess
import sys
from tkinter import *
from PIL import Image

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("Color Filter Option")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the dimensions and position of the window
window_width = 300
window_height = 350
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def spatial():
    command = [sys.executable, "domain_spatial.py"]
    subprocess.Popen(command)
    root.destroy()

def frequency():
    command = [sys.executable, "domain_frequency.py"]
    subprocess.Popen(command)
    root.destroy()

def back_to_option():
    command = [sys.executable, "main_option.py"]
    subprocess.Popen(command)
    root.destroy()

# Load and display the image
avatar = ctk.CTkImage(light_image=Image.open("setting_img/lena.jpg"), dark_image=Image.open("setting_img/lena.jpg"), size=(130, 130))
ava_label = ctk.CTkLabel(root, text="", image=avatar)
ava_label.pack(pady=10)


# Create buttons
spatial_button = ctk.CTkButton(root, text="Spatial Domain", font=("Arial", 13, "bold"), corner_radius=32, command=spatial)
frequency_button = ctk.CTkButton(root, text="Frequency Domain", font=("Arial", 13, "bold"), corner_radius=32, command=frequency)
back_to_option_button = ctk.CTkButton(root, text="Back to option", font=("Arial", 13, "bold"), corner_radius=32, command=back_to_option)

# Place labels, entry fields, and buttons using grid layout
spatial_button.pack(pady=15)
frequency_button.pack(pady=15)
back_to_option_button.pack(pady=15)

root.mainloop()
