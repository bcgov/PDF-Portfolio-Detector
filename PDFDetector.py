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

        self.show_frame(SidePage) # staring page is MainPage class

    def show_frame(self, content): # function to choose which frame to put to the front (what the viewer sees)
        frame = self.frames[content]
        frame.tkraise() # puts to front


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text = "Source:", font = 'bold', background = self.cget('background'), foreground ='black').place(x = 300, y = 300)




class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background = 'cyan')

        ttk.Button(self, text = "Edit", command = lambda: controller.show_frame(MainPage)).place(x = 700, y = 550)
        ttk.Button(self, text = "Close", command = controller.destroy).place(x = 800, y = 550)

        ttk.Label(self, text = "Source:", font = 'bold', background = self.cget('background'), foreground ='black').place(x = 200, y = 100)
        text_box_width = 500
        frame_width = 900  # Width of the main window
        x_position = (frame_width - text_box_width) // 2

        tk.Text(self, height=25, width=75).place(x=x_position, y=130)  # Centered and adjusted y-position
                

        

if __name__ == "__main__":
    detector = windows()
    detector.resizable(False, False)
    detector.mainloop()