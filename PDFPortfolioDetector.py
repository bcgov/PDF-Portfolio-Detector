from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import csv
from spire.pdf.common import *  #type: ignore
from spire.pdf import *  #type: ignore
from datetime import datetime
import PyPDF2
from pypdf import PdfReader
from PIL import Image, ImageTk
from itertools import islice
import shutil

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)# for the class Tk

        self.wm_title("PDF Portfolio Detector") # Adding a title to the window

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

        tk.Frame.__init__(self, parent)
        
        self.controller = controller  # Store controller reference

        with open('./Do Not Touch/cache.txt', "r") as f:

            temp = f.readline().split('\n')[0] # Reads folder to scan
            # print("readline1: ", temp)
            self.path_1 = temp

            temp = f.readline().split('\n')[0] # Reads folder to place results
            # print("readline2: ", temp)
            self.path_2 = temp

        path1 = tk.StringVar() # Receiving user's source file_path selection
        path2 = tk.StringVar() # Receiving user's destination file_path selection

        path1.set(self.path_1)
        path2.set(self.path_2)

        def bracket_checker(check_path):
            # Updates the input path to fix backwards slashes in directory string
            temp = ""
            for char in check_path:
                if char == "/":
                    char = "\\"
                elif char == "//":
                    char = '\\\\'
                temp = temp + char
            check_path = temp
            return check_path


        def selectPath1(): # Source path
            self.path_1 = filedialog.askdirectory()

            # Reads the cache and saves the selected directory into the first line of the txt
            with open('./Do Not Touch/cache.txt', "r") as f: 
                lines = f.readlines()
            lines[0] = self.path_1 + "\n"
            with open('./Do Not Touch/cache.txt', "w") as f:
                f.writelines(lines)

            path1.set(self.path_1)

        def selectPath2(): # Destination path
            self.path_2 = filedialog.askdirectory()

            # Reads the cache and saves the selected directory into the second line of the txt
            with open('./Do Not Touch/cache.txt', "r") as f:
                lines = f.readlines()
            lines[1] = self.path_2 + "\n"
            with open('./Do Not Touch/cache.txt', "w") as f:
                f.writelines(lines)

            path2.set(self.path_2)

        def next_step_start(input_files, output_path): # Makes sure that both source and destination folders are selected

            if self.path_1 == '' or self.path_2 == '': 
                messagebox.showerror("Error", "Please Select Both Source and Destination Folders")
            elif os.path.isdir(self.path_1) == False or os.path.isdir(self.path_2) == False: # Checks if the both directories exists/accessible
                messagebox.showerror("Error", "Invalid Folder or Destination chosen")
            else:
                fileProcessor(input_files, output_path)
                
        def fileProcessor(input_files, output_path): # Convert input files and output path to string

            input_files = str(input_files)
            output_path = str(output_path)

            # Debugging output
            # print("Input Directory:", input_files)
            # print("Output Directory:", output_path)

            # Create a timestamped directory for output
            date_title = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            user = os.getlogin()
            title = f"{date_title} {user}" # Shows time then user idir
            new_dir_path = os.path.join(output_path, title)
            print(new_dir_path)
            os.mkdir(new_dir_path)
            os.mkdir(new_dir_path + '\\Encrypted_files') # Encrypted folder
            os.mkdir(new_dir_path + '\\Form_Fields_files') # Form Field folder
            os.mkdir(new_dir_path + '\\Portfolio_files') # Portfolio folder

            # CSV file paths - update to use new_dir_path
            full_report_csv = os.path.join(new_dir_path, f'Full Report - {title}.csv')
            encrypted_report_csv = os.path.join(new_dir_path, f'Encrypted & Form Fields - {title}.csv')
            portfolio_report_csv = os.path.join(new_dir_path, f'PDF Portfolios - {title}.csv')
            
            # Initialize report lists
            full_report_rows = [['Document Type', '', '', 'PDF Version', '', 'File Name', '', '', '', '', '', '', 'Path to files'],[]]
            portfolio_report_rows = [['Document Type', '', '', 'PDF Version', '', 'File Name', '', '', '', '', '', '', 'Path to files'],[]]
            encrypted_report_rows = [['Document Type', '', '', 'PDF Version', '', 'File Name', '', '', '', '', '', '', 'Path to files'],[]]

            for current_path, folders, files in os.walk(input_files):
                for file in files:
                    path = os.path.join(current_path, file)

                    if file.lower().endswith(".pdf"):
                        
                        
                        if PyPDF2.PdfReader(path).is_encrypted:
                            path = bracket_checker(path)

                            try:
                                test = current_path + '/' + file
                                reader = PdfReader(test)
                                version = reader.pdf_header[1:]
                            except:
                                print("Can't get version")

                            full_report_rows.append(['ENCRYPTED', '', '', version, '', file, '', '', '', '', '', '', path])
                            encrypted_report_rows.append(['ENCRYPTED', '', '', version, '', file, '', '', '', '', '', '', path])
                            shutil.copy2(path, new_dir_path + '\\Encrypted_files') # Copies encrypted files to new destination
                            # print("IT'S PASSWORD PROTECTED")
                            continue

                        test = current_path + '/' + file
                        reader = PdfReader(test)
                        version = reader.pdf_header[1:]

                        # reader = PdfReader(file)
                        # fields = reader.get_fields()
                        # print("Testtest: ", fields)

                        with open(path, 'rb') as cur:
                            if PyPDF2.PdfReader(path).get_fields():
                                path = bracket_checker(path)
                                full_report_rows.append(['FORM FIELDS', '', '', version, '', file, '', '', '', '', '', '', path])
                                encrypted_report_rows.append(['FORM FIELDS', '', '', version, '', file, '', '', '', '', '', '', path])
                                shutil.copy2(path, new_dir_path + '\\Form_Fields_files') # Copies form fields files to new destination
                                # print('GOT FORM FIELDS')
                                continue

                        doc = PdfDocument()
                        doc.LoadFromFile(path)

                        if doc.IsPortfolio:
                            path = bracket_checker(path)
                            portfolio_report_rows.append(['PDF PORTFOLIO', '', '', version, '', file, '', '', '', '', '', '', path])
                            full_report_rows.append(['PDF PORTFOLIO', '', '', version, '', file, '', '', '', '', '', '', path])
                            shutil.copy2(path, new_dir_path + '\\Portfolio_files') # Copies portfolio files to new destination
                        else:
                            path = bracket_checker(path)
                            full_report_rows.append(['NONE', '', '', version, '', file, '', '', '', '', '', '', path])

                        doc.Close()
                    else:
                        path = bracket_checker(path)
                        version = ''
                        full_report_rows.append(['NONE', '', '', version, '', file, '', '', '', '', '', '', path])

            
            # Write reports
            with open(full_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(full_report_rows)

            with open(portfolio_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(portfolio_report_rows)

            with open(encrypted_report_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerows(encrypted_report_rows)

            # Controller.show_frame(SidePage)
            controller.frames[SidePage].update_output_path(input_files, output_path, title) # Updates output path on SidePage
            controller.show_frame(SidePage)

        #background image
        canvas = tk.Canvas(self, height=400, width=650)
        canvas.pack()

        img = (Image.open("./Do Not Touch/abstract.png"))

        resized_image= img.resize((650,400), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(resized_image)

        canvas.create_image( 0, 0, image = self.new_image, anchor="nw")

        # Page header
        canvas.create_text(220, 80, text="PDF Portfolio Detector", fill="black", font=('Arial 25 bold'))

        # Source to scan
        canvas.create_text(85, 207, text="Folder to Scan: *", fill="black", font=('bold'))
        entry1 = ttk.Entry(self, textvariable=path1, width=50, state="disabled").place(x=160, y=200)
        button1 = ttk.Button(self, text="Browse Source", command=selectPath1, width=20).place(x=470, y=198)

        # Destination to place results
        canvas.create_text(85, 310, text="Folder to Place\n     Results: *", fill="black", font=('bold'))
        entry2 = ttk.Entry(self, textvariable=path2, width=50, state="disabled").place(x=160, y=300)
        button2 = ttk.Button(self, text="Browse Destination", command=selectPath2, width=20).place(x=470, y=298)

        # Button for going to next page
        ttk.Button(self, text="Start", command=lambda: next_step_start(self.path_1, self.path_2), width=10).place(x=560, y=360)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.output_path = ""

        # Background image
        canvas = tk.Canvas(self, height=400, width=650)
        canvas.pack()

        img = (Image.open("./Do Not Touch/abstract.png"))

        resized_image= img.resize((650,400), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(resized_image)

        canvas.create_image( 0, 0, image = self.new_image, anchor="nw")

        # Page header
        canvas.create_text(137, 110, text="Source:", fill="black", font=('Arial 16 bold'))

        # Text widget to store the text
        self.text_box = tk.Text(self, height=10, width=60, background = '#F0F0F0')
        self.text_box.place(x=100, y=130)

        # Buttons for rerunning code and closing gui
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage)).place(x=460, y=360)
        ttk.Button(self, text="Close", command=controller.destroy).place(x=560, y=360)

        # Button for the results file directory
        ttk.Button(self, text="Results", command=self.open_results).place(x=30, y=360)

    def open_results(self):
        if os.path.exists(self.output_path):
            os.startfile(self.output_path)  # Opens the file explorer at the specified path
        else:
            messagebox.showerror("Error", "The specified path does not exist.")
    

    def update_output_path(self, input_path, output_path, title):

        # Updates output path to fix backwards slashes in directory string
        temp = ""
        for char in output_path:
            if char == "/":
                char = "\\"
            elif char == "//":
                    char = '\\\\'
            temp = temp + char

        output_path = temp

        # Updates output path to fix backwards slashes in directory string
        temp = ""
        for char in input_path:
            if char == "/":
                char = "\\"
            elif char == "//":
                    char = '\\\\'
            temp = temp + char

        input_path = temp
        
        self.text_box.config(state=tk.NORMAL)  # Enable editing
        self.text_box.delete(1.0, tk.END)  # Clears previous text
        # self.output_path = output_path +"\\"+ title  # Updates the output path
        self.output_path = output_path + "\\" + title
        # print("output path: ", output_path)

        self.text_box.insert(tk.END, "Processing Complete!\n")  # Adds a completion message
        self.text_box.insert(tk.END, f"Source Path: {input_path}\n")
        # print(input_path)
        self.text_box.insert(tk.END, f"Output Path: {output_path}\\{title}\n")
        # print(output_path)
        self.text_box.config(state=tk.DISABLED)  # Makes text read only


if __name__ == "__main__":
    detector = windows()
    detector.resizable(False, False)
    detector.mainloop()
