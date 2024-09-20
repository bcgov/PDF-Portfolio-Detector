from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import os
import sys

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) # for the class Tk

        self.wm_title("PDF Portfolio Detector") # adding a title to the window
        # self.wm_attributes('-transparentcolor', self['bg'])
        self.geometry("650x400") # default size when opened

        self.frames = {} # initialization of the frames array (where the different containers are going to be stored)

        container = tk.Frame(self)  # creating a container (each container is basically 1 page)

        container.pack(side = "top", fill = "both", expand = True) # change customizations later
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        for F in (MainPage, SidePage): #looops through each individual page layout provided by the classes
            
            frame = F(container,self) # individual frame

            self.frames[F] = frame # putting in the individual frames (pages) into the "frames" array

            frame.grid(row=0, column=0, sticky = 'nsew')


        self.show_frame(MainPage) # staring page is MainPage class

    def show_frame(self, content): # function to choose which frame to put to the front (what the viewer sees)
        frame = self.frames[content]
        frame.tkraise() # puts to front


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='lightblue')

        def selectPath1():   
            path_ = filedialog.askdirectory()
            path1.set(path_)

        def selectPath2():   
            path_ = filedialog.askdirectory()
            path2.set(path_)

        path1 = tk.StringVar()   # Receiving user's file_path selection
        folder1 = tk.StringVar() # Receiving user's folder_name selection

        path2 = tk.StringVar()   # Receiving user's file_path selection
        folder2 = tk.StringVar() # Receiving user's folder_name selection

        ttk.Label(self, text = "PDF Portfolio Detector", width=50, background='lightblue', font=("Arial", 25)).place(x=40, y= 60) # page header

        # source to scan
        ttk.Label(self, text = "Folder to scan: ", width=50, background='lightblue').place(x=40, y= 200)
        ttk.Entry(self, textvariable = path1, width=50).place(x=150, y= 200)
        ttk.Button(self, text = "Browse Source ", command = selectPath1, width=20).place(x=460, y= 198)

        # destination to place
        ttk.Label(self, text = "Place to put results: ", background='lightblue').place(x=40, y= 300)
        ttk.Entry(self, textvariable = path2, width=50).place(x=150, y= 300)
        ttk.Button(self, text = "Browse Destination ", command = selectPath2, width=20).place(x=460, y= 298) 

        ttk.Button(self, text = "Start", command = lambda: controller.show_frame(SidePage), width=10).place(x=560, y= 360) # button for going to next page




class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background = 'lightblue')

        ttk.Button(self, text = "Back", command = lambda: controller.show_frame(MainPage)).place(x=460, y= 360)
        ttk.Button(self, text = "Close", command = controller.destroy).place(x=560, y= 360)

        ttk.Label(self, text = "Source:", font = 'bold', background = self.cget('background'), foreground ='black').place(x = 100, y = 100)
        tk.Text(self, height = 10, width = 60).place(x = 100, y = 130)  #centered and adjusted text box
                

        

if __name__ == "__main__":
    detector = windows()
    detector.resizable(False, False)
    detector.mainloop()