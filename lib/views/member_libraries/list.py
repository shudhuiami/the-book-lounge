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
Selected_member_relation_id = 0
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
    render_library_list(Root_Frame, _Root_)
    _Root_.show_frame("library_Members_List")
    return
def render_library_list(Root_Frame, _Root_):
    global treev

    with open(GlobalHelper.user_json, 'r') as json_file:
        user_info = json.load(json_file)

    user_id = str(user_info['id'])
    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT libraries.*, library_members.id as relation_id FROM library_members JOIN libraries on libraries.id = library_members.library_id WHERE library_members.member_id='" + user_id + "' AND library_members.member_type = 2")
    field_map = fields(mycursor)

    members_list = []

    for row in mycursor:
        eachbook = {
            'id':  row[field_map['id']],
            'title':  row[field_map['title']],
            'logo':  row[field_map['logo']],
            'email':  row[field_map['email']],
            'phone':  row[field_map['phone']],
            'address':  row[field_map['address']],
            'relation_id':  row[field_map['relation_id']],
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
    treev.column("1", anchor='c')
    treev.column("2", anchor='c')
    treev.column("3", anchor='c')

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="Name")
    treev.heading("2", text="Email")
    treev.heading("3", text="Phone")
    treev.bind('<ButtonRelease-1>', selectItem)

    # Inserting the items and their features to the
    # columns built
    for i in range(len(members_list)):
        row = members_list[i]
        treev.insert("", 'end', text=row['id'], values=(row['title'], row['email'], row['phone']))

def view_library_books(Root_Frame, _Root_):
    global Selected_member_relation_id
    if Selected_member_relation_id == 0:
        messagebox.showerror("Error", "Select a Library first")
        return

    GlobalHelper.selected_library_id = Selected_member_relation_id
    _Root_.show_frame("Member_Library_books")


def fields(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results
def selectItem(a):
    global Selected_member_relation_id
    curItem = treev.focus()
    Selected_item = treev.item(curItem)
    Selected_member_relation_id = Selected_item['text']
def manage_my_libraries(Root_Frame, _Root_):

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

    Button(HeaderFrame, text="View Books of Library", bg=GlobalHelper.theme_color,
           command=lambda: view_library_books(Root_Frame, _Root_), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=1, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Join New Library", bg='#43e070',
           command=lambda: _Root_.show_frame("library_Members_Add"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Leave Library", bg='#fc383e',
           command=lambda: RemoveMember(Root_Frame, _Root_), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Back to Dashboard", bg='#c7c7c7',
           command=lambda: _Root_.show_frame("Dashboard_Manager"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")

    render_library_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





