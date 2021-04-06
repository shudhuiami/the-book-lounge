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
    if Selected_member_relation_id == 0:
        messagebox.showerror("Error", "Select a member first")
        return
    _Root_.show_frame("Global_Loading")

    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    _id = str(Selected_member_relation_id)
    library_member_sql = "DELETE FROM library_members WHERE id ='"+_id+"'"
    mycursor.execute(library_member_sql)
    mydb.commit()

    messagebox.showerror("Success", "Member removed Successfully")
    render_member_list(Root_Frame, _Root_)
    _Root_.show_frame("library_Members_List")
    return
def render_member_list(Root_Frame, _Root_):
    global treev
    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    library_id = str(library_info['id'])
    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT users.*, library_members.id as relation_id FROM library_members JOIN users on users.id = library_members.member_id WHERE library_members.library_id='" + library_id + "' AND library_members.member_type = 2")
    field_map = fields(mycursor)

    members_list = []

    for row in mycursor:
        eachbook = {
            'id':  row[field_map['id']],
            'name':  row[field_map['name']],
            'email':  row[field_map['email']],
            'phone':  row[field_map['phone']],
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
        treev.insert("", 'end', text=row['relation_id'], values=(row['name'], row['email'], row['phone']))
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
def manage_library_members(Root_Frame, _Root_):
    global treev

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

    Button(HeaderFrame, text="Add Member", bg=GlobalHelper.theme_color,
           command=lambda: _Root_.show_frame("library_Members_Add"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=1, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Remove Member", bg='#fc383e',
           command=lambda: RemoveMember(Root_Frame, _Root_), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Back to Dashboard", bg='#c7c7c7',
           command=lambda: _Root_.show_frame("Dashboard_Manager"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")

    render_member_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





