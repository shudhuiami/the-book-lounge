from tkinter import *
root = Tk()

screen_size = "1000x700"
root.title("The Book Lounge")
root.geometry(screen_size)
logo = PhotoImage(file='.//images//logo.png')
root.tk.call('wm', 'iconphoto', root._w, logo)

root.mainloop()