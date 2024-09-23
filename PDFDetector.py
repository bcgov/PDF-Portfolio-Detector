from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import os
import sys
import csv
from spire.pdf.common import *  #type: ignore
from spire.pdf import *  #type: ignore
from datetime import datetime
import pypdf

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)# for the class Tk

        self.wm_title("PDF Portfolio Detector") # Adding a title to the window
        # self.wm_attributes('-transparentcolor', self['bg'])
        self.geometry("650x400") # Default size when opened

        self.frames = {} # Initialization of the frames array (where the different containers are going to be stored)

        container = tk.Frame(self) # Creating a container (each container is basically 1 page)

        container.pack(side="top", fill="both", expand=True) # Change customizations later
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MainPage, SidePage): # Loops through each individual page layout provided by the classes
            frame = F(container, self) # Individual frame

            self.frames[F] = frame# Putting in the individual frames (pages) into the "frames" array

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MainPage) # Starting page is MainPage class

    def show_frame(self, content, output_path=None):# Function to choose which frame to put to the front (what the viewer sees)
        frame = self.frames[content] 
        frame.tkraise() # Puts to front

        if content == SidePage and output_path: # Updates output path with path given by user
            frame.update_output_path(output_path)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='lightblue')
        self.controller = controller  # Store controller reference

        self.path_1 = ''
        self.path_2 = ''

        path1 = tk.StringVar() # Receiving user's source file_path selection
        path2 = tk.StringVar() # Receiving user's destination file_path selection

        def selectPath1(): # Source path
            self.path_1 = filedialog.askdirectory()
            path1.set(self.path_1)

        def selectPath2(): # Destination path
            self.path_2 = filedialog.askdirectory()
            path2.set(self.path_2)

        def next_step_start(input_files, output_path): # Makes sure that both source and destination folders are selected
            
            # try: # If there is nothing in the field then this will throw error

            if self.path_1 or self.path_2 == '':
                messagebox.showerror("Error", "Please Select Both Source and Destination Folders")
            else:
                fileProcessor(input_files, output_path)

            # except AttributeError:
            #     messagebox.showerror("Error", "Please Select Both Source and Destination Folders")

            # except:
            #     messagebox.showerror("Error", "Please Check Your Directory/Folder And Try Again")
                
        def fileProcessor(input_files, output_path): # Convert input files and output path to string

            input_files = str(input_files)
            output_path = str(output_path)

            # Debugging output
            print("Input Directory:", input_files)
            print("Output Directory:", output_path)

            # Create a timestamped directory for output
            date_title = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            user = os.getlogin()
            title = f"{user} {date_title}"
            new_dir_path = os.path.join(output_path, title)
            os.mkdir(new_dir_path)

            # CSV file paths - update to use new_dir_path
            full_report_csv = os.path.join(new_dir_path, f'Report - {title}.csv')
            true_report_csv = os.path.join(new_dir_path, f'Only True - {title}.csv')
            false_report_csv = os.path.join(new_dir_path, f'Only False - {title}.csv')
            
            # Initialize report lists
            full_report_rows = []
            true_report_rows = [['Is Portfolio', '', 'File Name', '', '', '', '', '', '', 'Path to portfolio files']]
            false_report_rows = [['Is Portfolio', '', 'File Name', '', '', '', '', '', '', 'Path to portfolio files']]

            for current_path, folders, files in os.walk(input_files):
                for file in files:
                    path = os.path.join(current_path, file)

                    if file.lower().endswith(".pdf"):

                        if pypdf.PdfReader(path).is_encrypted:
                            full_report_rows.append(['ENCRYPTED', '', file, '', '', '', '', '', '', path])
                            print("IT'S PASSWORD PROTECTED")
                            continue

                        doc = PdfDocument()
                        doc.LoadFromFile(path)

                        if doc.IsPortfolio:
                            true_report_rows.append(['True', '', file, '', '', '', '', '', '', path])
                            full_report_rows.append(['True', '', file, '', '', '', '', '', '', path])
                        else:
                            false_report_rows.append(['False', '', file, '', '', '', '', '', '', path])
                            full_report_rows.append(['False', '', file, '', '', '', '', '', '', path])

                        doc.Close()
                    else:
                        false_report_rows.append(['False', '', file, '', '', '', '', '', '', path])
                        full_report_rows.append(['False', '', file, '', '', '', '', '', '', path])

            
            # Write reports
            with open(full_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(full_report_rows)

            with open(true_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(true_report_rows)

            with open(false_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(false_report_rows)

            # Controller.show_frame(SidePage)
            controller.frames[SidePage].update_output_path(input_files, new_dir_path) # Updates output path on SidePage
            controller.show_frame(SidePage)

        # Page header
        ttk.Label(self, text="PDF Portfolio Detector", width=50, background='lightblue', font=("Arial", 25)).place(x=40, y=60)

        # Source to scan
        ttk.Label(self, text="Folder to Scan: *", width=50, background='lightblue').place(x=40, y=200)
        entry1 = ttk.Entry(self, textvariable=path1, width=50, state="disabled").place(x=160, y=200)
        ttk.Button(self, text="Browse Source", command=selectPath1, width=20).place(x=470, y=198)

        # Destination to place results
        ttk.Label(self, text="Folder to Place\n     Results: *", background='lightblue').place(x=40, y=295)
        entry2 = ttk.Entry(self, textvariable=path2, width=50, state="disabled").place(x=160, y=300)
        ttk.Button(self, text="Browse Destination", command=selectPath2, width=20).place(x=470, y=298)

        # Button for going to next page
        ttk.Button(self, text="Start", command=lambda: next_step_start(self.path_1, self.path_2), width=10).place(x=560, y=360)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='lightblue')
        self.output_path = ""

        # Text widget to store the text
        self.text_box = tk.Text(self, height=10, width=60)
        self.text_box.place(x=100, y=130)

        # Buttons for rerunning code and closing gui
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage)).place(x=460, y=360)
        ttk.Button(self, text="Close", command=controller.destroy).place(x=560, y=360)

        ttk.Label(self, text="Source:", font='bold', background=self.cget('background'), foreground='black').place(x=100, y=100)
        # Button for the results file directory
        ttk.Button(self, text="Results", command=self.open_results).place(x=30, y=360)

    def open_results(self):
        if os.path.exists(self.output_path):
            os.startfile(self.output_path)  # Opens the file explorer at the specified path
        else:
            messagebox.showerror("Error", "The specified path does not exist.")
        

    def update_output_path(self, input_path, output_path):
        self.text_box.config(state=tk.NORMAL)  # Enable editing
        self.text_box.delete(1.0, tk.END)  # Clears previous text
        self.output_path = output_path  # Updates the output path

        self.text_box.insert(tk.END, "Processing Complete!\n")  # Adds a completion message
        self.text_box.insert(tk.END, f"Source Path: {input_path}\n")
        self.text_box.insert(tk.END, f"Output Path: {output_path}\n")
        self.text_box.config(state=tk.DISABLED)  # Makes text read only


if __name__ == "__main__":
    detector = windows()
    detector.resizable(False, False)
    detector.mainloop()
