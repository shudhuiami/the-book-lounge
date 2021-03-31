from tkinter import *
import mysql.connector
import json
import os



root = Tk()

screen_width = root.winfo_screenwidth() * 0.6
screen_height = root.winfo_screenheight() * 0.7
screen_size = str(int(screen_width))+'x'+str(int(screen_height))

root.title("The Book Lounge")
root.geometry(screen_size)
from global_variables import GlobalHelper, HelperFunction


root.tk.call('wm', 'iconphoto', root._w, GlobalHelper.logo)

HelperFunction.SetRootPATH(os.path.dirname(os.path.abspath(__file__)))

class __Root__:
    def show_frame(path):
        if path == 'Authentication_Login':
            authentication_login_view()
        elif path == 'Authentication_Register':
            authentication_register_view()
        elif path == 'Dashboard_Manager':
            dashobard_manager_view()
        elif path == 'Manage_Account':
            manage_account()
        elif path == 'Manage_Library':
            manage_library()
        elif path == 'Library_List':
            library_list_view()




root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

Authentication_Login = Frame(root, bg='#fff')
Authentication_Register = Frame(root, bg='#fff')
Dashboard_Manager = Frame(root, bg='#fff')
Manage_Account = Frame(root, bg='#fff')
Manage_Library = Frame(root, bg='#fff')
Library_List = Frame(root, bg='#fff')

for frame in (Authentication_Login, Authentication_Register, Dashboard_Manager, Manage_Account, Manage_Library):
    frame.grid(row=0, column=0, sticky='nsew')


import lib.views.authentication as authentication
import lib.views.dashboard as dashboard
import lib.views.account as account
import lib.views.library as library
import lib.views.library_list as library_list

def authentication_login_view():
    authentication.login(Authentication_Login, __Root__)

def authentication_register_view():
    authentication.register(Authentication_Register, __Root__)

def dashobard_manager_view():
    dashboard.manager_dashboard(Dashboard_Manager, __Root__)

def manage_account():
    account.manage_account(Manage_Account, __Root__)

def manage_library():
    library.manage_library(Manage_Library, __Root__)

def library_list_view():
    library_list.library_list(Manage_Library, __Root__)




with open(GlobalHelper.user_json) as json_file:
    user_info = json.load(json_file)
    if len(str(user_info['token'])) == 0:
        __Root__.show_frame("Authentication_Login")
    else:
        __Root__.show_frame("Dashboard_Manager")

root.mainloop()
