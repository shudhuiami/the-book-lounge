from tkinter import *

root = Tk()

from global_variables import GlobalHelper

screen_size = "1000x700"
root.title("The Book Lounge")
root.geometry(screen_size)
root.tk.call('wm', 'iconphoto', root._w, GlobalHelper.logo)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

Authentication_Login = Frame(root, bg='#fff')
Authentication_Login.grid(row=0, column=0, sticky='nsew')

class __Root__:
    def show_frame(path):
        if path == 'Authentication_Login':
            authentication_login_view()


import authentication


def authentication_login_view():
    authentication.login(Authentication_Login, __Root__)


__Root__.show_frame("Authentication_Login")
root.mainloop()
