from tkinter import *

root = Tk()

screen_size = "1000x700"
root.title("The Book Lounge")
root.geometry(screen_size)

from global_variables import GlobalHelper

root.tk.call('wm', 'iconphoto', root._w, GlobalHelper.logo)


class __Root__:
    def show_frame(path):
        if path == 'Authentication_Login':
            authentication_login_view()
        elif path == 'Authentication_Register':
            authentication_register_view()
        elif path == 'Dashboard_Manager':
            dashobard_manager_view()


root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

Authentication_Login = Frame(root, bg='#fff')
Authentication_Register = Frame(root, bg='#fff')
Dashboard_Manager = Frame(root, bg='#fff')

for frame in (Authentication_Login, Authentication_Register, Dashboard_Manager):
    frame.grid(row=0, column=0, sticky='nsew')

import authentication
import dashboard


def authentication_login_view():
    authentication.login(Authentication_Login, __Root__)


def authentication_register_view():
    authentication.register(Authentication_Register, __Root__)


def dashobard_manager_view():
    dashboard.manager_dashboard(Dashboard_Manager, __Root__)


__Root__.show_frame("Authentication_Login")
root.mainloop()
