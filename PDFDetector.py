from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        self.wm_title("PDF Portfolio Detector") # adding a title to the window
        self.geometry("900x600") # default size when opened



# class MainPage(tk.Frame):
#     def __init__(self, parent, controller):
        


# class SidePage(tk.Frame):
#     def __init__(self, parent, controller):
        

        

if __name__ == "__main__":
    detector = windows()
    detector.mainloop()