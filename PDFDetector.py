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
        self.geometry("900x600") # default size when opened

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
        self.var=1




class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        self.var = 1
        

        

if __name__ == "__main__":
    detector = windows()
    detector.mainloop()