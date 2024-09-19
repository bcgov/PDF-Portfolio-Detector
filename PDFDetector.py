from tkinter import *
from tkinter import messagebox
import tkinter

root = Tk()
root.geometry("900x600") #default size when opened
root.configure(background='cyan') #background color
root.attributes('-alpha',0.5) #transparent window

def popup_msg():
    msg = messagebox.showinfo("Result", "Process Finished")

 
button = Button(root, text = 'Click me !', command = popup_msg)
# button.pack(side = 'middle') #makes button position be at the top
button.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()