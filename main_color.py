from tkinter import Tk, filedialog, messagebox
from PIL import ImageTk, Image, ImageOps
from color_algorithm import *
import cv2
import subprocess
import sys
import customtkinter as ctk
import pywinstyles

class ColorFilter:
    def __init__(self):
        self.photo = None
        self.photo2 = None
        self.loaded_image_path = None
        self.modified_image_data = None
        self.img_original = None

        # Create the main application
        self.app = ctk.CTk()
        pywinstyles.apply_style(self.app, "dark")
        self.app.geometry("1000x775")
        self.app.title("Image enhancement in the Spatial Domain")

        # configure grid layout (3x7)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=2)
        self.app.grid_columnconfigure((2,3,4), weight=0)
        self.app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.app.grid_rowconfigure((10, 11, 12, 13, 14, 15, 16, 17, 18, 19), weight=1)

        # Check if the webcam successfully captured a frame
        self.cap = None
        self.cam_success = None
        self.frame = None

        self.create_widgets()
        self.create_index()

    def create_widgets(self):
        # Frame controls on the left side bar
        self.frame_button = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_button.grid(row=0, column=0, rowspan=20, sticky="nsew")

        self.optionmenu = ctk.CTkOptionMenu(master=self.frame_button, values=["Log", "Gamma", "Piecewise Linear", "Mean", "Median", "Gaussian", "Histogram"])
        self.optionmenu.grid(row=0, column=0, padx=20, pady=(20, 30))
        self.optionmenu.set("Select transformation")

        self.btn_select = ctk.CTkButton(master=self.frame_button, text="Select image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.load_image)
        self.btn_select.grid(row=1, column=0, padx=20, pady=10)

        self.btn_update = ctk.CTkButton(master=self.frame_button, text="Update image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.update_image)
        self.btn_update.grid(row=2, column=0, padx=20, pady=10)

        self.btn_negative = ctk.CTkButton(master=self.frame_button, text="Negative image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.activateNegative)
        self.btn_negative.grid(row=3, column=0, padx=20, pady=10)

        self.btn_return_original = ctk.CTkButton(master=self.frame_button, text="Return original image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.return_original)
        self.btn_return_original.grid(row=4, column=0, padx=20, pady=10)

        self.btn_open_cam = ctk.CTkButton(master=self.frame_button, text="Open camera", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.open_camera)
        self.btn_open_cam.grid(row=5, column=0, padx=20, pady=10)

        self.btn_capture_img = ctk.CTkButton(master=self.frame_button, text="Capture image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.capture_image)
        self.btn_capture_img.grid(row=6, column=0, padx=20, pady=10)

        self.btn_combobox = ctk.CTkComboBox(master=self.frame_button, values=[".png", ".jpg", ".jpeg", ".gif", ".bmp", ".pdf", ".webp"])
        self.btn_combobox.grid(row=7, column=0, padx=20, pady=10)
        self.btn_combobox.set("Select export type")

        self.btn_export_img = ctk.CTkButton(master=self.frame_button, text="Export image", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export_image)
        self.btn_export_img.grid(row=8, column=0, padx=20, pady=10)

        self.btn_back = ctk.CTkButton(master=self.frame_button, text="Back to option", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.back_to_option)
        self.btn_back.grid(row=9, column=0, padx=20, pady=10)

        self.btn_close_app = ctk.CTkButton(master=self.frame_button, text="Close app", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.close_app)
        self.btn_close_app.grid(row=10, column=0, padx=20, pady=10)

        # Load the image logo
        logo_image = cv2.imread("setting_img/logo.jpg")
        logo_image = cv2.resize(logo_image, (150, 200))
        logo_image = cv2.cvtColor(logo_image, cv2.COLOR_BGR2RGBA)
        self.logo_photo = ImageTk.PhotoImage(Image.fromarray(logo_image))
        self.logo_label = ctk.CTkLabel(master=self.frame_button, image=self.logo_photo, text="")
        self.logo_label.grid(row=11, column=0, padx=20, pady=10)

        # Frame for display image
        # Frame on the top right
        self.frame_input = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_input.grid(row=0, column=1, columnspan=1, rowspan=10, sticky="nsew")
        # Frame on the bottom right
        self.frame_output = ctk.CTkFrame(master=self.app, corner_radius=0)
        self.frame_output.grid(row=10, column=1, columnspan=1, rowspan=10, sticky="nsew")

        # Display the image in frame_input
        self.canvas_input = ctk.CTkCanvas(master=self.frame_input, bg="black")
        self.canvas_input.pack(fill="both", expand=True)
        self.canvas_input.create_image(0, 0, anchor="center", tags="image_tag")
        
        # Display the image in frame_output
        self.canvas_output = ctk.CTkCanvas(master=self.frame_output)
        self.canvas_output.pack(fill="both", expand=True)
        self.canvas_output.create_image(0, 0, anchor="center", tags="image_tag")

        self.canvas_output.output_image_canvas = self.canvas_output

    def create_index(self):
        # Frame slider
        self.frame_slider = ctk.CTkFrame(self.app, corner_radius=0, fg_color="#09555c")
        self.frame_slider.grid(row=0, column=2, sticky="nsew", rowspan=20, columnspan=3)

        # Log
        # region
        self.log_label = ctk.CTkLabel(self.frame_slider, text="Log", bg_color="#2C67F2")
        self.log_label.grid(row=0, column=2, rowspan=2, sticky="news")

        # Coefficient c
        self.logC_value_label = ctk.CTkLabel(master=self.frame_slider, text="Coefficient c: 0", bg_color="green")
        self.logC_value_label.grid(row=0, column=3, columnspan=2, sticky="news")

        self.logC_slider = ctk.CTkSlider(master=self.frame_slider, from_=0, to=100, number_of_steps=100, hover=True, command=lambda value: self.update_slider_value(value))
        self.logC_slider.grid(row=1, column=3, columnspan=2, sticky="news")
        self.logC_slider.set(10)
        # endregion

        # Gamma
        # region
        self.gamma_label = ctk.CTkLabel(self.frame_slider, text="Gamma", bg_color="#275AD4")
        self.gamma_label.grid(row=2, column=2, rowspan=4, sticky="news")

        # Gamma
        self.gamma_value_label = ctk.CTkLabel(master=self.frame_slider, text="Gamma: 0", bg_color="green")
        self.gamma_value_label.grid(row=2, column=3, columnspan=2, sticky="news")

        self.gamma_slider = ctk.CTkSlider(master=self.frame_slider, from_=0.1, to=3, number_of_steps=int((3-0.1)/0.1), hover=True, command=lambda value: self.update_slider_value(value))
        self.gamma_slider.grid(row=3, column=3, columnspan=2, sticky="news")
        self.gamma_slider.set(1.0)

        # Coefficient c
        self.gammaC_value_label = ctk.CTkLabel(master=self.frame_slider, text="Coefficient c: 0", bg_color="green")
        self.gammaC_value_label.grid(row=4, column=3, columnspan=2, sticky="news")

        self.gammaC_slider = ctk.CTkSlider(master=self.frame_slider, from_=0.5, to=2, number_of_steps=int((2-0.5)/0.1), hover=True, command=lambda value: self.update_slider_value(value))
        self.gammaC_slider.grid(row=5, column=3, columnspan=2, sticky="news")
        self.gammaC_slider.set(1.3)
        # endregion

        # Piecewise-linear
        # region
        self.piecewise_label = ctk.CTkLabel(self.frame_slider, text="Piecewise Linear", bg_color="#214DB5")
        self.piecewise_label.grid(row=6, column=2, rowspan=4, sticky="news")

        # Low coefficient
        self.low_value_label = ctk.CTkLabel(master=self.frame_slider, text="Low coefficient: 0", bg_color="green")
        self.low_value_label.grid(row=6, column=3, columnspan=2, sticky="news")

        self.low_slider = ctk.CTkSlider(master=self.frame_slider, from_=0, to=255, number_of_steps=255, hover=True, command=lambda value: self.update_slider_value(value))
        self.low_slider.grid(row=7, column=3, columnspan=2, sticky="news")
        self.low_slider.set(70)

        # High coefficient
        self.high_value_label = ctk.CTkLabel(master=self.frame_slider, text="High coefficient: 0", bg_color="green")
        self.high_value_label.grid(row=8, column=3, columnspan=2, sticky="news")

        self.high_slider = ctk.CTkSlider(master=self.frame_slider, from_=0, to=255, number_of_steps=255, hover=True, command=lambda value: self.update_slider_value(value))
        self.high_slider.grid(row=9, column=3, columnspan=2, sticky="news")
        self.high_slider.set(200)
        # endregion

        # Mean
        # region
        self.mean_label = ctk.CTkLabel(self.frame_slider, text="Mean", bg_color="#1B4097")
        self.mean_label.grid(row=10, column=2, rowspan=2, sticky="news")

        # Kernel
        self.mean_value_label = ctk.CTkLabel(master=self.frame_slider, text="Kernel: 0", bg_color="green")
        self.mean_value_label.grid(row=10, column=3, columnspan=2, sticky="news")

        self.mean_slider = ctk.CTkSlider(master=self.frame_slider, from_=3, to=15, number_of_steps=(15 - 3) // 2, hover=True, command=lambda value: self.update_slider_value(value))
        self.mean_slider.grid(row=11, column=3, columnspan=2, sticky="news")
        self.mean_slider.set(7)
        # endregion

        # Median
        # region
        self.median_label = ctk.CTkLabel(self.frame_slider, text="Median", bg_color="#163479")
        self.median_label.grid(row=12, column=2, rowspan=2, sticky="news")

        # Kernel
        self.median_value_label = ctk.CTkLabel(master=self.frame_slider, text="Kernel: 0", bg_color="green")
        self.median_value_label.grid(row=12, column=3, columnspan=2, sticky="news")

        self.median_slider = ctk.CTkSlider(master=self.frame_slider, from_=3, to=25, number_of_steps=(25 - 3) // 2, hover=True, command=lambda value: self.update_slider_value(value))
        self.median_slider.grid(row=13, column=3, columnspan=2, sticky="news")
        self.median_slider.set(7)
        # endregion

        # Gaussian
        # region
        self.gauss_label = ctk.CTkLabel(self.frame_slider, text="Gaussian", bg_color="#10275B")
        self.gauss_label.grid(row=14, column=2, rowspan=4, sticky="news")

        # Kernel
        self.gauss_kernel_value_label = ctk.CTkLabel(master=self.frame_slider, text="Kernel: 0", bg_color="green")
        self.gauss_kernel_value_label.grid(row=14, column=3, columnspan=2, sticky="news")

        self.gauss_kernel_slider = ctk.CTkSlider(master=self.frame_slider, from_=3, to=15, number_of_steps=(15 - 3) // 2, hover=True, command=lambda value: self.update_slider_value(value))
        self.gauss_kernel_slider.grid(row=15, column=3, columnspan=2, sticky="news")
        self.gauss_kernel_slider.set(7)

        # Sigma
        self.sigma_value_label = ctk.CTkLabel(master=self.frame_slider, text="Sigma: 0", bg_color="green")
        self.sigma_value_label.grid(row=16, column=3, columnspan=2, sticky="news")

        self.sigma_slider = ctk.CTkSlider(master=self.frame_slider, from_=0.5, to=3, number_of_steps=(3-0.5)//0.1, hover=True, command=lambda value: self.update_slider_value(value))
        self.sigma_slider.grid(row=17, column=3, columnspan=2, sticky="news")
        self.sigma_slider.set(0.5)
        # endregion

        # Histogram
        # region
        self.histogram_label = ctk.CTkLabel(self.frame_slider, text="Histogram Equalization", bg_color="#0B1A3C")
        self.histogram_label.grid(row=18, column=2, rowspan=2, sticky="news")

        # Clip limit
        self.histogram_value_label = ctk.CTkLabel(master=self.frame_slider, text="Clip limit: 0", bg_color="green")
        self.histogram_value_label.grid(row=18, column=3, columnspan=2, sticky="news")

        self.histogram_slider = ctk.CTkSlider(master=self.frame_slider, from_=1, to=40, number_of_steps=39, hover=True, command=lambda value: self.update_slider_value(value))
        self.histogram_slider.grid(row=19, column=3, columnspan=2, sticky="news")
        self.histogram_slider.set(5)
        # endregion

        # Schedule the update function to run every 100 milliseconds
        self.app.after(100, self.update_slider_value)

    def update_slider_value(self, value=None):
        # Update the displayed value in real-time
        self.logC_value_label.configure(text=f"Coefficient c: {int(self.logC_slider.get())}")

        self.gamma_value_label.configure(text=f"Gamma: {round(float(self.gamma_slider.get()), 1)}")
        self.gammaC_value_label.configure(text=f"Coefficient c: {round(float(self.gammaC_slider.get()), 1)}")

        self.low_value_label.configure(text=f"Low coefficient: {int(self.low_slider.get())}")
        self.high_value_label.configure(text=f"High coefficient: {int(self.high_slider.get())}")

        self.mean_value_label.configure(text=f"Kernel: {int(self.mean_slider.get())}")

        self.median_value_label.configure(text=f"Kernel: {int(self.median_slider.get())}")

        self.gauss_kernel_value_label.configure(text=f"Kernel: {int(self.gauss_kernel_slider.get())}")
        self.sigma_value_label.configure(text=f"Sigma: {round(float(self.sigma_slider.get()),1)}")

        self.histogram_value_label.configure(text=f"Clip limit: {int(self.histogram_slider.get())}")

    def load_image(self):
        if self.cap is None:
            file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
            if file_path:
                self.loaded_image_path = file_path
                self.show_image()
        else:
            messagebox.showwarning("Warning", "Turn off camera to selected image file!")

    def show_image(self):
        image = cv2.imread(self.loaded_image_path)
        # Resize image to fit canvas without anti-aliasing
        image = cv2.resize(image, (500, 490))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(image))

        # Original image
        self.img_original = image

        self.canvas_input.delete("image_tag")  # Clear previous content
        self.canvas_input.create_image(self.canvas_input.winfo_width() / 2, 
                                   self.canvas_input.winfo_height() / 2, 
                                   anchor="center", image=self.photo, tags="image_tag")

    def export_image(self):
        if self.photo2 is not None:
            export_type = self.btn_combobox.get()
            # Image type
            if export_type in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".pdf"]:
                # Select a file path
                file_path = filedialog.asksaveasfilename(defaultextension=export_type, filetypes=[("Images", "*" + export_type), ("All files", "*.*")])
                if file_path:
                    try:
                        file_path = file_path.replace("/", "\\")
                        # Convert PIL.ImageTk.PhotoImage to PIL.Image.Image
                        img = ImageTk.getimage(self.photo2)
                        img = img.convert("RGB")
                        img = img.save(file_path)
                        messagebox.showinfo("Success", "Done saving image!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error saving image: {str(e)}!")
            else:
                messagebox.showerror("Error", "Invalid export type")
        else:
            messagebox.showwarning("Warning", "No image to export!")

    def back_to_option(self):
        command = [sys.executable, "main_option.py"]
        subprocess.Popen(command)
        self.app.destroy()

    def close_app(self):
        self.app.destroy()

    def activateLog(self):
        scale_value = int(self.logC_slider.get())
        if self.loaded_image_path:
            img_bgr = cv2.imread(self.loaded_image_path, 0)
            img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            self.drawFilteredImage(log_c(img_bgr, scale_value))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            self.drawFilteredImage(log_c(img, scale_value))

    def activateGamma(self):
        Gamma = round(float(self.gamma_slider.get()), 1)
        c = round(float(self.gammaC_slider.get()), 1)
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path, cv2.IMREAD_GRAYSCALE)
            self.drawFilteredImage(gamma(img, Gamma, c))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to GRAYSCALE
            img = img.convert("L")
            img = np.array(img)
            self.drawFilteredImage(gamma(img, Gamma, c))

    def activatePiecewiseLinear(self):
        r1 = int(self.low_slider.get())
        s2 = int(self.high_slider.get())
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path)
            print(type(img))
            self.drawFilteredImage(piecewise_linear(img, r1, s2))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            img = np.array(img)
            self.drawFilteredImage(piecewise_linear(img, r1, s2))

    def activateMean(self):
        kernel = int(self.mean_slider.get())
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path)
            self.drawFilteredImage(MeanFiltered(img, kernel))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            img = np.array(img)
            self.drawFilteredImage(MeanFiltered(img, kernel))

    def activateMedian(self):
        kernel = int(self.median_slider.get())
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path)
            self.drawFilteredImage(MedianFiltered(img, kernel))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            img = np.array(img)
            self.drawFilteredImage(MedianFiltered(img, kernel))

    def activateGaussian(self):
        kernel = int(self.gauss_kernel_slider.get())
        sig = round(float(self.sigma_slider.get()),1)
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path)
            self.drawFilteredImage(GaussianFiltered(img, kernel, sig))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            img = np.array(img)
            self.drawFilteredImage(GaussianFiltered(img, kernel, sig))

    def activateHistogram(self):
        clip_limit = int(self.histogram_slider.get())
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path)
            self.drawFilteredImage(Histogram(img, clip_limit))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to RGB image
            img = img.convert("RGB")
            img = np.array(img)
            self.drawFilteredImage(Histogram(img, clip_limit))

    def activateNegative(self):
        if self.loaded_image_path:
            img = cv2.imread(self.loaded_image_path, cv2.IMREAD_GRAYSCALE)
            self.drawFilteredImage(Negative(img))
        elif self.photo2 is not None:
            img = ImageTk.getimage(self.photo2)
            # Convert PhotoImage to Grayscale
            img = img.convert("L")
            img = np.array(img)
            self.drawFilteredImage(Negative(img))

    def return_original(self):
        self.drawFilteredImage(self.img_original)

    def update_image(self):
        if self.loaded_image_path or self.photo2 is not None:
            option = self.optionmenu.get()
            if option == "Log":
                self.activateLog()
            elif option == "Gamma":
                self.activateGamma()
            elif option == "Piecewise Linear":
                self.activatePiecewiseLinear()
            elif option == "Mean":
                self.activateMean()
            elif option == "Median":
                self.activateMedian()
            elif option == "Gaussian":
                self.activateGaussian()
            elif option == "Histogram":
                self.activateHistogram()
            else:
                messagebox.showerror("Error", "You have not selected any transformation")
        else:
            messagebox.showerror("Error", "You have not captured or selected any images")
            
    def drawFilteredImage(self, image):
        if self.loaded_image_path:
            self.modified_image_data = image
            image = cv2.resize(image, (500, 490))
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.canvas_output.delete("image_tag")  # Clear previous content
            self.canvas_output.create_image(self.canvas_output.winfo_width() / 2, 
                                        self.canvas_output.winfo_height() / 2, 
                                        anchor="center", image=self.photo2, tags="image_tag")
        elif self.photo2 is not None:
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.canvas_output.delete("image_tag")  # Clear previous content
            self.canvas_output.create_image(self.canvas_output.winfo_width() / 2, 
                                        self.canvas_output.winfo_height() / 2, 
                                        anchor="center", image=self.photo2, tags="image_tag")

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

            if self.cam_success:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(self.frame)
                self.photo = ImageTk.PhotoImage(image=image)

                self.canvas_input.delete("image_tag")  # Clear previous content
                self.canvas_input.create_image(self.canvas_input.winfo_width() / 2, 
                                   self.canvas_input.winfo_height() / 2, 
                                   anchor="center", image=self.photo, tags="image_tag")

                # Call this function again after 15 milliseconds
                self.app.after(15, self.show_webcam)
            else:
                messagebox.showerror("Error", "Failed to get frame from webcam!")
                self.cap.release()
                self.cap = None

    def capture_image(self):
        if self.cam_success:
            self.photo2 = self.photo

            # Original image
            image = ImageTk.getimage(self.photo2)
            image = image.convert("RGB")
            self.img_original = np.array(image)

            self.canvas_output.delete("all")
            self.canvas_output.create_image(0, 0, anchor="nw", image=self.photo2)
            self.loaded_image_path = None
        else:
            messagebox.showerror("Error", "You have not opened camera")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ColorFilter()
    app.app.mainloop()
