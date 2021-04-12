from tkinter import *
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
            dashboard_manager_view()
        elif path == 'Manage_Account':
            manage_account()
        elif path == 'Manage_Library':
            manage_library()
        elif path == 'Library_Books':
            manage_library_books()
        elif path == 'Library_Book_Create':
            book_create_view()
        elif path == 'library_Members_List':
            library_members_view()
        elif path == 'library_Members_Add':
            library_member_add_view()
        elif path == 'Global_Loading':
            global_loading_view()
        elif path == 'My_Libraries':
            my_libraries_view()
        elif path == 'Member_Library_books':
            library_books_view()
        elif path == 'Reading_List':
            member_reading_book_view()
        elif path == 'Favourite_Books':
            member_favourite_book_view()






root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

Authentication_Login = Frame(root, bg='#fff')
Authentication_Register = Frame(root, bg='#fff')
Dashboard_Manager = Frame(root, bg='#fff')
Manage_Account = Frame(root, bg='#fff')
Manage_Library = Frame(root, bg='#fff')
Library_Books = Frame(root, bg='#fff')
Library_Book_Create = Frame(root, bg='#fff')
Library_Members_List = Frame(root, bg='#fff')
Library_Member_Add = Frame(root, bg='#fff')
Global_Loading_View = Frame(root, bg='#fff')
My_Libraries = Frame(root, bg='#fff')
Member_Library_Books = Frame(root, bg='#fff')
Member_Reading_List = Frame(root, bg='#fff')
Member_Favourite_List = Frame(root, bg='#fff')

for frame in (Authentication_Login, Authentication_Register, Dashboard_Manager, Manage_Account, Manage_Library, Library_Books, Library_Book_Create, Library_Members_List, Library_Member_Add, Global_Loading_View, My_Libraries, Member_Library_Books, Member_Reading_List, Member_Favourite_List):
    frame.grid(row=0, column=0, sticky='nsew')


import lib.views.authentication as authentication

import lib.views.dashboard as dashboard

import lib.views.account.account_manage as account

import lib.views.manager_library.library as library

import lib.views.manager_books.list as library_books
import lib.views.manager_books.create as book_create


import lib.views.manager_library_members.list as members
import lib.views.manager_library_members.add_member as member_add_to_library

import lib.views.member_libraries.list as my_libraries
import lib.views.member_libraries.library_books as member_library_books
import lib.views.member_libraries.reading_books as member_reading_list
import lib.views.member_libraries.favourite_books as member_favourite_list

# import lib.views.library_list as library_list
import lib.views.global_loading as global_loading

def authentication_login_view():
    authentication.login(Authentication_Login, __Root__)

def authentication_register_view():
    authentication.register(Authentication_Register, __Root__)

def dashboard_manager_view():
    dashboard.manager_dashboard(Dashboard_Manager, __Root__)

def manage_account():
    account.manage_account(Manage_Account, __Root__)

def manage_library():
    library.manage_library(Manage_Library, __Root__)

def manage_library_books():
    library_books.manage_library_books(Library_Books, __Root__)

def book_create_view():
    book_create.library_create_book(Library_Book_Create, __Root__)

def my_libraries_view():
    my_libraries.manage_my_libraries(My_Libraries, __Root__)

def library_books_view():
    member_library_books.libraries_books(Member_Library_Books, __Root__)


def library_members_view():
    members.manage_library_members(Library_Members_List, __Root__)

def library_member_add_view():
    member_add_to_library.Add_member_to_library(Library_Member_Add, __Root__)


def global_loading_view():
    global_loading.global_loading(Global_Loading_View, __Root__)

def member_reading_book_view():
    member_reading_list.member_reading_books(Member_Reading_List, __Root__)

def member_favourite_book_view():
    member_favourite_list.member_favourite_books(Member_Reading_List, __Root__)


with open(GlobalHelper.user_json) as json_file:
    user_info = json.load(json_file)
    if user_info['token'] is None:
        __Root__.show_frame("Authentication_Login")
    else:
        __Root__.show_frame("Dashboard_Manager")

root.mainloop()
