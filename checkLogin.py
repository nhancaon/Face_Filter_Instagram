import pygame
from simple_face_recognition import SimpleFaceRecognition
from function import *
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import copy
import subprocess
import sys
import numpy

class CheckLogin:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition for Login")

        self.cap = None
        self.sfr = SimpleFaceRecognition()
        self.sfr.load_encoding_images("saved_face/")

        self.photo = None
        self.photo2 = None

        self.image_frame = ctk.CTkFrame(root, fg_color="white")
        self.image_frame.pack(side="left", anchor="n")

        self.canvas = ctk.CTkCanvas(self.image_frame, width=640, height=480)
        self.canvas.pack()

        self.recognition_button = ctk.CTkButton(root, text="Recognition", font=("Arial", 13, "bold"), corner_radius=32, command=self.capture_image) #, hover_color="#0E46A3", fg_color="transparent", border_color="#FFCC70", border_width=2
        self.recognition_button.pack(padx=4, pady=160)

        self.open_camera()

    def open_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.show_webcam()
        else:
            self.cap.release()
            self.cap = None
            self.canvas.delete("all")

    def show_webcam(self):
        success = False
        if self.cap is not None:
            success, frame = self.cap.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            self.master.after(15, self.show_webcam)
        else:
            if self.cap is not None:
                messagebox.showerror("Error", "Failed to get frame from webcam!")
                self.cap.release()
                self.cap = None
        
    def capture_image(self):
        if self.cap is not None:
            success, frame = self.cap.read()
            if success:
                self.cap.release()
                self.cap = None
                self.recognition(frame)

    def recognition(self, save_img):
        face_locations, face_names = self.sfr.detect_known_faces(save_img)
        if face_locations.any():
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(save_img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(save_img, (x1, y1), (x2, y2), (0, 0, 200), 4)

            save_img = cv2.cvtColor(save_img, cv2.COLOR_BGR2RGB)
            reg_img = Image.fromarray(save_img)
            self.photo2 = ImageTk.PhotoImage(image=reg_img)

            # Delete previous image from canvas
            self.canvas.delete("all")

            # Display the photo on the canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo2)

            # Check if any recognized name is "Unknown"
            if "Unknown" in face_names:
                messagebox.showerror("Error", "Failed to login!")
                self.master.after(1000, self.return_login)
            else:
                # Delay execution of login method by 5 seconds
                self.master.after(2000, self.clear_canvas)
        else:
            messagebox.showerror("Error", "No face detected!")
            self.master.after(1000, self.return_login)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_countdown_circle(3)

    def draw_countdown_circle(self, counter):
        if counter >= 0:
            # Clear canvas
            self.canvas.delete("all")

            # Draw circle
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            center_x = canvas_width // 2
            center_y = canvas_height // 2
            radius = min(canvas_width, canvas_height) // 3

            # Calculate start angle and end angle for the arc
            start_angle = 0  # Start angle for a circle
            if counter == 3:
                end_angle = 360
            else:
                end_angle = counter * 120

            # Draw the arc or full circle based on the counter
            if counter == 3:
                self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="red", width=10)
            else:
                self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius, start=start_angle, extent=end_angle, style="arc", outline="red", width=10)

            # Draw counter text
            self.canvas.create_text(center_x, center_y, text=str(counter), font=("Helvetica", 48), fill="green")

            # Schedule the next draw
            self.master.after(1000, self.draw_countdown_circle, counter - 1)
        else:
            # Clear canvas after countdown is finished
            self.canvas.delete("all")
            self.login()

    def return_login(self):
        command = [sys.executable, "login.py"]
        subprocess.Popen(command)
        self.master.destroy()

    def login(self):
        command = [sys.executable, "main.py"]
        subprocess.Popen(command)
        self.master.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 650
    window_height = 380
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    app = CheckLogin(root)
    root.mainloop()
