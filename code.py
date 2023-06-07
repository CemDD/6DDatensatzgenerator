import tkinter as tk
from tkinter import filedialog
import os
import argparse
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # CAD file selection button
        self.cad_file_label = tk.Label(self)
        self.cad_file_label["text"] = "Select CAD file:"
        self.cad_file_label.pack(side="top")

        self.cad_file_button = tk.Button(self, text="Browse", command=self.select_cad_file)
        self.cad_file_button.pack(side="top")

        # Object name entry
        self.object_name_label = tk.Label(self)
        self.object_name_label["text"] = "Object name:"
        self.object_name_label.pack(side="top")

        self.object_name_entry = tk.Entry(self)
        self.object_name_entry.pack(side="top")

        # Number of samples entry
        self.num_samples_label = tk.Label(self)
        self.num_samples_label["text"] = "Number of samples:"
        self.num_samples_label.pack(side="top")

        self.num_samples_entry = tk.Entry(self)
        self.num_samples_entry.pack(side="top")

        # Image size entries
        self.image_size_label = tk.Label(self)
        self.image_size_label["text"] = "Image size (width x height):"
        self.image_size_label.pack(side="top")

        self.image_size_frame = tk.Frame(self)
        self.image_size_frame.pack(side="top")

        self.image_width_entry = tk.Entry(self.image_size_frame, width=10)
        self.image_width_entry.pack(side="left")

        self.image_height_entry = tk.Entry(self.image_size_frame, width=10)
        self.image_height_entry.pack(side="left")

        # Output directory entry
        self.output_dir_label = tk.Label(self)
        self.output_dir_label["text"] = "Output directory:"
        self.output_dir_label.pack(side="top")

        self.output_dir_entry = tk.Entry(self)
        self.output_dir_entry.pack(side="top")

        # Render button
        self.render_button = tk.Button(self)
        self.render_button["text"] = "Render"
        self.render_button["command"] = self.run_program
        self.render_button.pack(side="top")

    def select_cad_file(self):
        file_path = filedialog.askopenfilename()
        self.cad_file_label["text"] = f"Selected CAD file: {file_path}"
        self.cad_file_path = file_path

    def run_program(self):
        # Get input parameters from GUI entries
        cad_file_path = self.cad_file_path
        object_name = self.object_name_entry.get()
        num_samples = int(self.num_samples_entry.get())
        image_width = int(self.image_width_entry.get())
        image_height = int(self.image_height_entry.get())
        output_dir = self.output_dir_entry.get()

        # Set the path to the Blender executable
        blender_executable = "C:/Program Files/Blender Foundation/Blender 3.5/blender.exe"

        # Set the path to the program file
        program_file = "C:/Users/dikgoz321/Desktop/program.py"

        # Call the program with the input parameters
        subprocess.call(["blender", "--background", "--python", program_file, "--", cad_file_path, "--object-name", object_name, "--num-samples", str(num_samples), "--image-width", str(image_width), "--image-height", str(image_height), "--output-dir", output_dir]) 


root = tk.Tk()
app = Application(master=root)
app.mainloop()