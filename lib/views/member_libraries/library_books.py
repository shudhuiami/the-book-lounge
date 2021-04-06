from tkinter import *
from tkinter import ttk
from global_variables import GlobalHelper, HelperFunction
import json
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector
from tkinter import filedialog
import bcrypt
import os
import shutil
import pathlib
import uuid
import requests

UPLOAD_URL = str(pathlib.Path().absolute())+'\\uploads\\'
SERVER_URL = 'http://134.209.158.52/library/'
account_avatar = ''
account_name = StringVar()
account_address = StringVar()
account_phone = StringVar()
account_password = StringVar()
Selected_book_path = ''
treev = None

def RemoveMember(Root_Frame, _Root_):
    global Selected_member_relation_id
    _Root_.show_frame("Global_Loading")
    if Selected_member_relation_id == 0:
        messagebox.showerror("Error", "Select a member first")
        return


    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    _id = str(Selected_member_relation_id)
    library_member_sql = "DELETE FROM library_members WHERE id ='"+_id+"'"
    mycursor.execute(library_member_sql)
    mydb.commit()

    messagebox.showerror("Success", "Member removed Successfully")
    render_books_list(Root_Frame, _Root_)
    _Root_.show_frame("library_Members_List")
    return

def render_books_list(Root_Frame, _Root_):
    global treev

    library_id = str(GlobalHelper.selected_library_id)
    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM library_books WHERE library_id='" + library_id + "'")
    field_map = fields(mycursor)
    members_list = []

    for row in mycursor:
        eachbook = {
            'id':  row[field_map['id']],
            'name':  row[field_map['name']],
            'author':  row[field_map['author']],
            'library_id':  row[field_map['library_id']],
            'description':  row[field_map['description']],
            'cover':  row[field_map['cover']],
            'file_path':  row[field_map['file_path']],
        }
        members_list.append(eachbook)


    # Using treeview widget
    treev = ttk.Treeview(Root_Frame, selectmode='browse')

    # Calling pack method w.r.to treeview
    treev.grid(row=1, column=0, sticky="nsew")

    # Constructing vertical scrollbar
    # with treeview
    verscrlbar = ttk.Scrollbar(Root_Frame,
                               orient="vertical",
                               command=treev.yview)

    # Calling pack method w.r.to verical
    # scrollbar
    verscrlbar.grid(row=1, column=1, sticky="nsew")

    # Configuring treeview
    treev.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    treev["columns"] = ("1", "2", "3")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", anchor=W)
    treev.column("2", anchor=W)
    treev.column("3", anchor=W)

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="Name")
    treev.heading("2", text="Author")
    treev.heading("3", text="Description")
    treev.bind('<ButtonRelease-1>', selectItem)

    # Inserting the items and their features to the
    # columns built
    for i in range(len(members_list)):
        row = members_list[i]
        treev.insert("", 'end', text=row['file_path'], values=(row['name'], row['author'], row['description']))

def download_book(Root_Frame, _Root_):
    global Selected_book_path
    if len(Selected_book_path) == 0:
        messagebox.showerror("Error", "Select a book first")
        return
    folder_selected = filedialog.askdirectory()
    HelperFunction.download_from_server(folder_selected,Selected_book_path)



def fields(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results

def selectItem(a):
    global Selected_book_path
    curItem = treev.focus()
    Selected_item = treev.item(curItem)
    Selected_book_path = Selected_item['text']

def libraries_books(Root_Frame, _Root_):

    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=0)
    Root_Frame.grid_rowconfigure(0, weight=0)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(2, weight=0)


    HeaderFrame = Frame(Root_Frame, background="#fff", highlightbackground="#dfdfdf", highlightcolor="#dfdfdf", highlightthickness=1, bd=0)
    HeaderFrame.grid(row=0, column=0, sticky="nsew")


    HeaderFrame.grid_rowconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(1, weight=0)
    HeaderFrame.grid_columnconfigure(2, weight=0)
    HeaderFrame.grid_columnconfigure(3, weight=0)
    HeaderFrame.grid_columnconfigure(4, weight=0)

    Button(HeaderFrame, text="Read Book", bg=GlobalHelper.theme_color,
           command=lambda: (), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=1, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Download Book", bg='#43e070',
           command=lambda: download_book(Root_Frame, _Root_), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Back to Libraries", bg='#c7c7c7',
           command=lambda: _Root_.show_frame("My_Libraries"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")

    render_books_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





