from tkinter import Tk, filedialog, messagebox
from PIL import ImageTk, Image
from function import *
import cv2
import customtkinter as ctk
import subprocess
import sys

class Test:
    def __init__(self):
        # Create the main UI
        self.app = ctk.CTk()
        self.app.title("Face Filter")

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        window_width = 690
        window_height = 780
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Configure grid layout (3x7)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=2)
        self.app.grid_columnconfigure((2,3,4), weight=0)
        self.app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Check if the webcam successfully captured a frame
        self.cap = None
        self.cam_success = None
        self.frame = None

        # Keep a reference to the PhotoImage object and the loaded image path
        self.photo = None
        self.photo2 = None
        self.loaded_image_path = None

        self.test = [None]
        self.thread = [None]
        self.heightResize = 200

        self.prev_frame_time = 0    # Record the time when we processed last frame
        self.new_frame_time = 0     # Record the time at which we processed current frame

        self.create_widgets()

    def create_widgets(self):
        # Frame controls on the left side bar
        self.frame_button = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_button.grid(row=0, column=0, rowspan=20, sticky="nsew")

        self.optionmenu = ctk.CTkOptionMenu(master=self.frame_button, values=["Default", "Sun Glass", "Clown", "Cry", "Tear", "Batman", "Sharingan", "Thief", "Venom"])
        self.optionmenu.grid(row=0, column=0, padx=20, pady=(20, 30))
        self.optionmenu.set("Select filter")

        self.btn_open_cam = ctk.CTkButton(master=self.frame_button, text="Open camera", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.open_camera)
        self.btn_open_cam.grid(row=1, column=0, padx=20, pady=10)

        self.btn_capture_img = ctk.CTkButton(master=self.frame_button, text="Capture image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.capture_image)
        self.btn_capture_img.grid(row=2, column=0, padx=20, pady=10)

        self.btn_export = ctk.CTkButton(master=self.frame_button, text="Export image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.close_app)
        self.btn_export.grid(row=3, column=0, padx=20, pady=10)

        self.btn_back = ctk.CTkButton(master=self.frame_button, text="Back to option", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.back_to_option)
        self.btn_back.grid(row=4, column=0, padx=20, pady=10)

        self.btn_exit_app = ctk.CTkButton(master=self.frame_button, text="Exit application", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.close_app)
        self.btn_exit_app.grid(row=5, column=0, padx=20, pady=10)

        # Frame for display image
        # Frame on the top right
        self.frame_input = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_input.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew")
        # Frame on the bottom right
        self.frame_output = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_output.grid(row=5, column=1, columnspan=1, rowspan=5, sticky="nsew")

        # Display the image in frame_input
        self.canvas_input = ctk.CTkCanvas(master=self.frame_input, bg="white")
        self.canvas_input.pack(fill="both", expand=True)
        self.canvas_input.create_image(0, 0, anchor="center", tags="image_tag")
        
        # Display the image in frame_output
        self.canvas_output = ctk.CTkCanvas(master=self.frame_output)
        self.canvas_output.pack(fill="both", expand=True)
        self.canvas_output.create_image(0, 0, anchor="center", tags="image_tag")

        self.canvas_output.output_image_canvas = self.canvas_output

    def convert_filter_name(self, filter_name):
        if filter_name == "Sun Glass":
            return "sunglass_filter"
        elif filter_name == "Clown":
            return "clown_filter"
        elif filter_name == "Cry":
            return "cry_filter"
        elif filter_name == "Tear":
            return "tear_filter"
        elif filter_name == "Batman":
            return "bat_filter"
        elif filter_name == "Sharingan":
            return "sharingan_filter"
        elif filter_name == "Thief":
            return "skimask_filter"
        elif filter_name == "Venom":
            return "skimask_filter"

    def open_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.show_webcam() 
        else:
            self.cap.release()
            self.cap = None
            self.canvas_input.delete("all")

    def show_webcam(self):
        if self.cap is not None:
            self.cam_success, self.frame = self.cap.read()
            option = self.optionmenu.get()  # Return selected filter
            option = self.convert_filter_name(option)

            if self.cam_success:
                if option and option != "Select filter":
                    # Gather necessary arguments for filter function
                    height = self.frame.shape[0]
                    size = self.frame.shape[0:2]
                    frame_resize_scale = float(height) / self.heightResize
                    img = self.frame
                    thread = self.thread
                    test = self.test
                    prev_frame_time = self.prev_frame_time
                    new_frame_time = self.new_frame_time

                    # Apply filter to the frame
                    self.frame, self.prev_frame_time = filter(height, size, frame_resize_scale, img, thread, test, self.prev_frame_time, new_frame_time, option)

                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(self.frame)
                self.photo = ImageTk.PhotoImage(image=image)

                # Delete previous image from canvas
                self.canvas_input.delete("all")

                # Display the photo on the canvas
                self.canvas_input.create_image(0, 0, anchor="nw", image=self.photo)

                # Call this function again after 15 milliseconds
                self.app.after(15, self.show_webcam)
            else:
                messagebox.showerror("Error", "Failed to get frame from webcam!")
                self.cap.release()
                self.cap = None

    def capture_image(self):
        if self.cam_success:
            self.photo2 = self.photo
            self.canvas_output.delete("all")
            self.canvas_output.create_image(0, 0, anchor="nw", image=self.photo2)
        else:
            messagebox.showerror("Error", "You have not opened camera")

    def back_to_option(self):
        command = [sys.executable, "option.py"]
        subprocess.Popen(command)
        self.app.destroy()

    def close_app(self):
        self.app.destroy()

    def export_img(self):
        pass

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = Test()
    app.app.mainloop()
