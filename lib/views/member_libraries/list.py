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
Selected_library_id = 0
treev = None

def LeaveLibrary(Root_Frame, _Root_):
    global Selected_library_id
    with open(GlobalHelper.user_json, 'r') as json_file:
        user_info = json.load(json_file)

    _Root_.show_frame("Global_Loading")
    if Selected_library_id == 0:
        messagebox.showerror("Error", "Select a library first")
        return
    _id = str(Selected_library_id)
    user_id = str(user_info['id'])


    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    library_member_sql = "DELETE FROM library_members WHERE library_id ='"+_id+"' AND member_id = '"+user_id+"'"
    mycursor.execute(library_member_sql)
    mydb.commit()

    messagebox.showerror("Success", "Successfully")
    render_library_list(Root_Frame, _Root_)
    _Root_.show_frame("My_Libraries")
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

    library_list = []

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
        library_list.append(eachbook)


    render_data = []
    for library in library_list:
        user_id = str(user_info['id'])
        library_id = str(library['id'])

        mycursor.execute("SELECT id FROM library_books WHERE library_id='" + library_id + "'")
        total_bk = mycursor.fetchall()
        if total_bk is None:
            library['total_books'] = 0
        else:
            library['total_books'] = len(total_bk)

        mycursor.execute("SELECT id FROM reading_list WHERE library_id='" + library_id + "' AND user_id = '"+user_id+"'")
        reading_bk = mycursor.fetchall()
        if total_bk is None:
            library['reading_books'] = 0
        else:
            library['reading_books'] = len(reading_bk)

        mycursor.execute("SELECT id FROM favourite_books WHERE library_id='" + library_id + "' AND user_id = '"+user_id+"'")
        done_bk = mycursor.fetchall()
        if total_bk is None:
            library['favourite_books'] = 0
        else:
            library['favourite_books'] = len(done_bk)



        render_data.append(library)

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

    style = ttk.Style()
    style.configure("Treeview.Heading",
                    font=(None, 10),
                    rowheight=25,
                    )
    style.configure("Treeview",
                    font=(None, 10),
                    rowheight=50,
                    )

    # Configuring treeview
    treev.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    treev["columns"] = ("1", "2", "3", "4")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", anchor='c')
    treev.column("2", anchor='c')
    treev.column("3", anchor='c')
    treev.column("4", anchor='c')

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="Library Name")
    treev.heading("2", text="Total Books")
    treev.heading("3", text="Reading List Books")
    treev.heading("4", text="Favourite Books")
    treev.bind('<ButtonRelease-1>', selectItem)

    # Inserting the items and their features to the
    # columns built
    for i in range(len(render_data)):
        row = render_data[i]
        treev.insert("", 'end', text=row['id'], values=(row['title'], row['total_books'], row['reading_books'], row['favourite_books']))

def view_library_books(Root_Frame, _Root_):
    global Selected_library_id
    if Selected_library_id == 0:
        messagebox.showerror("Error", "Select a Library first")
        return

    GlobalHelper.selected_library_id = Selected_library_id
    _Root_.show_frame("Member_Library_books")


def fields(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results
def selectItem(a):
    global Selected_library_id
    curItem = treev.focus()
    Selected_item = treev.item(curItem)
    Selected_library_id = Selected_item['text']
def manage_my_libraries(Root_Frame, _Root_):

    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=0)
    Root_Frame.grid_rowconfigure(0, weight=0)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(2, weight=0)


    HeaderFrame = Frame(Root_Frame, background="#fff", highlightbackground="#dfdfdf", highlightcolor="#dfdfdf", highlightthickness=1, bd=0)
    HeaderFrame.grid(row=0, column=0, sticky="nsew")


    HeaderFrame.grid_rowconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(0, weight=0)
    HeaderFrame.grid_columnconfigure(1, weight=1)
    HeaderFrame.grid_columnconfigure(2, weight=0)
    HeaderFrame.grid_columnconfigure(3, weight=0)
    HeaderFrame.grid_columnconfigure(4, weight=0)

    Label(HeaderFrame, text="Dashboard > Libraries", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=0)

    Button(HeaderFrame, text="  View Books of Library", image=GlobalHelper.book, width=150, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: view_library_books(Root_Frame, _Root_),
          font=GlobalHelper.font_medium).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    # Button(HeaderFrame, text="  Join New Library", image=GlobalHelper.library, width=140, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: (),
    #       font=GlobalHelper.font_medium).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Leave Library", image=GlobalHelper.leave, width=140, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID,  bg=GlobalHelper.theme_color, command=lambda: LeaveLibrary(Root_Frame, _Root_),
          font=GlobalHelper.font_medium).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Back to Dashboard", image=GlobalHelper.back, width=150, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID, bg='#c7c7c7', command=lambda: _Root_.show_frame("Dashboard_Manager"),
          font=GlobalHelper.font_medium).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")

    render_library_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





