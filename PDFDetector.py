from tkinter import *


root = Tk()
root.title('PDFPortfolioDetector')
root.geometry("900x600") #default size when opened
root.configure(background='cyan') #background color
#root.attributes('-alpha',0.5) #transparent window

footer = Label(root, background='white')
button1 = Button(root, text='Edit', background='white', borderwidth=1, relief='solid') #edit button
button2 = Button(root, text='Close', background='white', command=root.destroy, borderwidth=1, relief='solid') #close button
status = Label(root, text='Status:', font='black', background='cyan') #status text header

sourcetext = Label(root, text='Source: (source folder) Loading... All Done! Check: (destination folder)', 
                   background='cyan', borderwidth=2, relief='solid') #status text window

#orientation of buttons and windows
footer.place(x=0, y=550, height=50, width=900)
status.place(x=253, y=78, height=20, width=60, anchor='ne')
button1.place(x=780, y=587, anchor ='se', height=20, width=60)
button2.place(x=870, y=587, anchor ='se', height=20, width=60)
sourcetext.place(x=200, y=100, height=400, width=500)


root.mainloop()