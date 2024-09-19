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



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        footer = tk.Label(self, background='white')
        button1 = ttk.Button(self, text='Edit', background='white', borderwidth=1, relief='solid') #edit button
        button2 = ttk.Button(self, text='Close', background='white', command=self.destroy, borderwidth=1, relief='solid') #close button
        status = tk.Label(self, text='Status:', font='black', background='cyan') #status text header
        sourcetext = tk.Label(self, text='Source: (source folder) Loading... All Done! Check: (destination folder)', 
                           background='cyan', borderwidth=2, relief='solid') #status text window   
        
        footer.place(relx=0, rely=1, height=50, width=900)
        status.place(relx=0.26, rely=0.17, height=20, width=60, anchor='ne')
        button1.place(relx=0.85, rely=0.97, anchor ='se', height=20, width=60)
        button2.place(relx=0.95, rely=0.97, anchor ='se', height=20, width=60)
        sourcetext.place(relx=0.2, rely=0.2, height=400, width=500)

        

if __name__ == "__main__":
    detector = windows()
    detector.mainloop()