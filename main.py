import os
from tkinter import Tk, Button, filedialog, Canvas, Frame, Label, OptionMenu, StringVar, messagebox, PhotoImage
from customtkinter import *
import math
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
from function import *
import tkinter as tk
from simple_facerec import SimpleFacerec


class ImageDisplayApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Display App")

        self.modified_image_data = None
        self.cap = None  # OpenCV VideoCapture object for webcam
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("saved_face/")

        button_frame = CTkScrollableFrame(
            master=self.master, fg_color="#000000", border_color="#FFCC70", border_width=5, orientation="horizontal", scrollbar_button_color="#FFCC70", label_anchor="s", width=620, height=100)
        button_frame.pack(expand=True, side="bottom", anchor="nw", pady=5)

        # Create a frame for the canvas
        self.image_frame = CTkFrame(master, fg_color="transparent")
        self.image_frame.pack(side="left", anchor="n")

        # Create a canvas to display the webcam feed
        self.canvas = Canvas(self.image_frame, width=640, height=480)
        self.canvas.pack()

        # Create a frame for the canvas
        self.reg_frame = CTkFrame(master, fg_color="transparent")
        self.reg_frame.pack(side="right", anchor="n", padx=5)

        # Create a canvas to display the webcam feed
        self.canvas_2 = Canvas(self.reg_frame, width=640, height=480)
        self.canvas_2.pack()

        # Create a button to close the app
        self.close_button = CTkButton(
            button_frame, text="Exit", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=self.close_app)
        self.close_button.grid(row=0, column=0, padx=4, pady=10)

        # Create a button to open camera
        self.open_cam_button = CTkButton(
            button_frame, text="Open Cam", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=self.open_camera)
        self.open_cam_button.grid(row=0, column=1, padx=4, pady=10)

        # Create a button to filter
        self.sun_glass_button = CTkButton(
            button_frame, text="SunGlass", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(1, "SunGlass_filter"))
        self.sun_glass_button.grid(row=0, column=2, padx=4, pady=10)

        self.clown_button = CTkButton(
            button_frame, text="Clown", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(2, "Clown"))
        self.clown_button.grid(row=0, column=3, padx=4, pady=10)

        self.cry_button = CTkButton(
            button_frame, text="Cry", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(3, "Cry_filter"))
        self.cry_button.grid(row=0, column=4, padx=4, pady=10)

        self.bat_button = CTkButton(
            button_frame, text="Batman", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(4, "Bat_Filter"))
        self.bat_button.grid(row=0, column=5, padx=4, pady=10)

        self.tear_button = CTkButton(
            button_frame, text="Tear", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(5, "Tear_filter"))
        self.tear_button.grid(row=1, column=0, padx=4, pady=10)

        self.sharingan_button = CTkButton(
            button_frame, text="Sharingan", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(6, "Sharingan_filter"))
        self.sharingan_button.grid(row=1, column=1, padx=4, pady=10)

        self.venom_button = CTkButton(
            button_frame, text="Venom", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(7, "SkiMask_filter"))
        self.venom_button.grid(row=1, column=2, padx=4, pady=10)

        self.thief_button = CTkButton(
            button_frame, text="Thief", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(9, "SkiMask_filter"))
        self.thief_button.grid(row=1, column=3, padx=4, pady=10)

        self.regco_button = CTkButton(
            button_frame, text="Recognition", corner_radius=32, fg_color="transparent", hover_color="#76520e", border_color="#FFCC70", border_width=2, command=lambda: self.turn_flag(10, ""))
        self.regco_button.grid(row=1, column=4, padx=4, pady=10)
        # Keep a reference to the PhotoImage object and the loaded image path
        self.photo = None
        self.photo2 = None
        self.loaded_image_path = None

        self.test = [None]
        self.thread = [None]
        self.heightResize = 200
        # used to record the time when we processed last frame
        self.prev_frame_time = 0

        # used to record the time at which we processed current frame
        self.new_frame_time = 0
        self.flag = 0
        self.filter_name = ""

    def close_app(self):
        self.master.destroy()

    def open_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)  # Open the default camera
            self.show_webcam()  # Start displaying the webcam feed
        else:
            # If webcam is already opened, release it
            self.cap.release()
            self.cap = None
            # Delete previous image from canvas
            self.canvas.delete("all")

    def show_webcam(self):
        if self.cap is not None:
            success, frame = self.cap.read()
            if success:
                if self.flag == 10:
                    save_image = copy.deepcopy(frame)
                    self.regconition(save_image)
                    save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2RGB)
                    reg_img = Image.fromarray(save_image)
                    self.photo2 = ImageTk.PhotoImage(image=reg_img)

                    # Delete previous image from canvas
                    self.canvas_2.delete("all")

                    # Display the photo on the canvas
                    self.canvas_2.create_image(
                        0, 0, anchor="nw", image=self.photo2)
                    self.flag = 0

                elif self.flag != 0:
                    # Gather necessary arguments for filter function
                    height = frame.shape[0]
                    size = frame.shape[0:2]
                    frame_resize_scale = float(height) / self.heightResize
                    img = frame
                    thread = self.thread
                    test = self.test
                    prev_frame_time = self.prev_frame_time
                    new_frame_time = self.new_frame_time

                    # Apply filter to the frame
                    frame, self.prev_frame_time = filter(
                        height, size, frame_resize_scale, img, thread, test, self.prev_frame_time, new_frame_time, self.filter_name)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                self.photo = ImageTk.PhotoImage(image=image)

                # Delete previous image from canvas
                self.canvas.delete("all")

                # Display the photo on the canvas
                self.canvas.create_image(
                    0, 0, anchor="nw", image=self.photo)

                # Call this function again after 15 milliseconds
                self.master.after(15, self.show_webcam)
            else:
                messagebox.showerror(
                    "Error", "Failed to get frame from webcam!")
                self.cap.release()  # Release the webcam feed if it's opened
                self.cap = None

    def turn_flag(self, number, filter_name):
        if self.flag != 10:
            self.filter_name = filter_name
        if self.flag != 0:
            self.flag = 0
        else:
            self.flag = number

    def regconition(self, save_img):
        face_locations, face_names = self.sfr.detect_known_faces(save_img)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(save_img, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(save_img, (x1, y1), (x2, y2), (0, 0, 200), 4)


if __name__ == "__main__":
    root = CTk()
    root.geometry("1200x700")
    set_appearance_mode("dark")
    app = ImageDisplayApp(root)
    root.mainloop()
