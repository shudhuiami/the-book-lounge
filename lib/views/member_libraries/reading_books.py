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
import textwrap
import requests

UPLOAD_URL = str(pathlib.Path().absolute())+'\\uploads\\'
SERVER_URL = 'http://134.209.158.52/library/'
account_avatar = ''
account_name = StringVar()
account_address = StringVar()
account_phone = StringVar()
account_password = StringVar()
Selected_book_path = ''
Selected_book_relation = 0
treev = None

def RemoveBook(Root_Frame, _Root_):
    global Selected_book_path
    _Root_.show_frame("Global_Loading")
    if Selected_book_relation == 0:
        messagebox.showerror("Error", "Select a books first")
        return

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    _id = str(Selected_book_relation)
    print(_id)
    library_member_sql = "DELETE FROM reading_list WHERE id ='"+_id+"'"
    mycursor.execute(library_member_sql)
    mydb.commit()

    messagebox.showerror("Success", "Successfully")
    render_books_list(Root_Frame, _Root_)
    _Root_.show_frame("Reading_List")
    return

def wrap(string, lenght=80):
    return '\n'.join(textwrap.wrap(string, lenght))

def render_books_list(Root_Frame, _Root_    ):
    global treev

    with open(GlobalHelper.user_json, 'r') as json_file:
        user_info = json.load(json_file)
    user_id = str(user_info['id'])

    library_id = str(GlobalHelper.selected_library_id)
    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT reading_list.id as relation_id, library_books.* FROM reading_list JOIN library_books ON library_books.id = reading_list.book_id WHERE reading_list.user_id='" + user_id + "'")
    field_map = fields(mycursor)
    members_list = []

    for row in mycursor:
        eachbook = {
            'id':  row[field_map['id']],
            'name':  row[field_map['name']],
            'author':  row[field_map['author']],
            'genre':  row[field_map['genre']],
            'library_id':  row[field_map['library_id']],
            'description':  row[field_map['description']],
            'relation_id':  row[field_map['relation_id']],
            'cover':  row[field_map['cover']],
            'file_path':  row[field_map['file_path']],
        }
        members_list.append(eachbook)


    # Using treeview widget
    treev = ttk.Treeview(Root_Frame, selectmode='browse')

    # Calling pack method w.r.to treeview
    treev.grid(row=1, column=0, sticky="nsew")

    style = ttk.Style()
    style.configure("Treeview.Heading",
                    font=(None, 10),
                    rowheight=25,
                    )
    style.configure("Treeview",
                    font=(None, 10),
                    rowheight=50,
                    )

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
    treev["columns"] = ("0", "1", "2", "3", "4")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("0", stretch=NO, anchor=W, width=0)
    treev.column("1", stretch=NO, anchor=W)
    treev.column("2", stretch=NO, anchor=W)
    treev.column("3", stretch=NO, anchor=W)
    treev.column("4", anchor=W)

    # Assigning the heading names to the
    # respective columns
    treev.heading("0", text="", anchor=W)
    treev.heading("1", text="Name", anchor=W)
    treev.heading("2", text="Author", anchor=W)
    treev.heading("3", text="Genre", anchor=W)
    treev.heading("4", text="Description", anchor=W)
    treev.bind('<ButtonRelease-1>', selectItem)

    # Inserting the items and their features to the
    # columns built
    for i in range(len(members_list)):
        row = members_list[i]
        treev.insert("", 'end', text=row['file_path'], values=(row['relation_id'], row['name'], row['author'],  row['genre'], wrap(row['description'])))

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
    global Selected_book_relation
    curItem = treev.focus()
    Selected_item = treev.item(curItem)
    Selected_book_path = Selected_item['text']
    Selected_book_relation = Selected_item['values']
    book_relations = Selected_book_relation[0];
    Selected_book_relation = book_relations

def member_reading_books(Root_Frame, _Root_):

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

    Label(HeaderFrame, text="Dashboard > Borrowed Books list", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=0)


    Button(HeaderFrame, text="  Download Book", image=GlobalHelper.library, width=140, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: download_book(Root_Frame, _Root_),
          font=GlobalHelper.font_medium).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Remove Book", image=GlobalHelper.remove, width=150, height=22, compound=LEFT, fg='#fff',
           borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: RemoveBook(Root_Frame, _Root_),
           font=GlobalHelper.font_medium).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Back to Dashboard", image=GlobalHelper.back, width=150, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID, bg='#c7c7c7', command=lambda: _Root_.show_frame("Dashboard_Manager"),
          font=GlobalHelper.font_medium).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")

    render_books_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





