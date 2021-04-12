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
import textwrap
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
Selected_book_path = 0
treev = None

def wrap(string, lenght=60):
    return '\n'.join(textwrap.wrap(string, lenght))



def render_books_list(Root_Frame, _Root_, HeaderFrame):
    global treev

    library_id = str(GlobalHelper.selected_library_id)
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)
    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM libraries WHERE id='" + library_id + "'")
    library_details = mycursor.fetchone()

    Label(HeaderFrame, text='Libraries > '+library_details[1], bg='#ffffff',
          font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=0)

    mycursor.execute("SELECT * FROM library_books WHERE library_id='" + library_id + "'")
    # mycursor.execute("SELECT * FROM library_books WHERE library_id='" + library_id + "' AND id NOT IN (SELECT book_id FROM reading_list WHERE library_id = '"+library_id+"' AND user_id = '"+logged_user['id']+"')")
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

    book_list_render = []
    for book in members_list:
        user_id = str(logged_user['id'])
        book_id = str(book['id'])

        mycursor.execute("SELECT id FROM reading_list WHERE library_id='" + library_id + "' AND user_id = '"+user_id+"' AND book_id = '"+book_id+"'")
        read_count = mycursor.fetchone()
        if read_count is None:
            book['is_reading'] = ''
        else:
            book['is_reading'] = 'In Reading'

        mycursor.execute(
            "SELECT id FROM favourite_books WHERE library_id='" + library_id + "' AND user_id = '" + user_id + "' AND book_id = '" + book_id + "'")
        read_count = mycursor.fetchone()
        if read_count is None:
            book['is_favourite'] = ''
        else:
            book['is_favourite'] = 'In Favourite'

        book_list_render.append(book)


    # Using treeview widget
    treev = ttk.Treeview(Root_Frame, selectmode='browse')

    # Calling pack method w.r.to treeview
    treev.grid(row=1, column=0, sticky="nsew")

    style = ttk.Style()
    style.configure("Treeview.Heading",
                    font=(None, 10),
                    rowheight= 25,
                    )
    style.configure("Treeview",
                    font=(None, 10),
                    rowheight= 50,
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
    treev["columns"] = ("1", "2", "3", "4", "5")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", anchor=W)
    treev.column("2", stretch=NO, width=150, anchor=W)
    treev.column("3", stretch=NO, anchor='c')
    treev.column("4", stretch=NO, anchor='c')
    treev.column("5", anchor=W)

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="Name", anchor=W)
    treev.heading("2", text="Author", anchor=W)
    treev.heading("3", text="Is in Reading", anchor='c')
    treev.heading("4", text="Is in Favourite", anchor='c')
    treev.heading("5", text="Description", anchor=W)
    treev.bind('<ButtonRelease-1>', selectItem)

    # Inserting the items and their features to the
    # columns built
    for i in range(len(book_list_render)):
        row = book_list_render[i]
        treev.insert("", 'end', text=row['id'], values=(row['name'], row['author'], row['is_reading'], row['is_favourite'], wrap(row['description'])))

def Add_to_Reading(Root_Frame, _Root_, HeaderFrame):
    global Selected_book_path
    library_id = str(GlobalHelper.selected_library_id)
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)

    if Selected_book_path == 0:
        messagebox.showerror("Error", "Select a book first")
        return

    _Root_.show_frame("Global_Loading")

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    sql = "INSERT INTO reading_list (book_id, library_id, user_id) VALUES (%s, %s, %s)"
    val = (Selected_book_path, library_id, logged_user['id'])
    mycursor.execute(sql, val)
    mydb.commit()

    messagebox.showerror("Success", "Successfully added in reading list")
    render_books_list(Root_Frame, _Root_, HeaderFrame)
    _Root_.show_frame("Member_Library_books")

def Add_to_fav(Root_Frame, _Root_, HeaderFrame):
    global Selected_book_path
    library_id = str(GlobalHelper.selected_library_id)
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)

    if Selected_book_path == 0:
        messagebox.showerror("Error", "Select a book first")
        return

    _Root_.show_frame("Global_Loading")

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME,
                                   password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    sql = "INSERT INTO favourite_books (book_id, library_id, user_id) VALUES (%s, %s, %s)"
    val = (Selected_book_path, library_id, logged_user['id'])
    mycursor.execute(sql, val)
    mydb.commit()

    messagebox.showerror("Success", "Successfully added in favourite list")
    render_books_list(Root_Frame, _Root_, HeaderFrame)
    _Root_.show_frame("Member_Library_books")

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
    HeaderFrame.grid_columnconfigure(0, weight=0)
    HeaderFrame.grid_columnconfigure(1, weight=1)
    HeaderFrame.grid_columnconfigure(2, weight=0)
    HeaderFrame.grid_columnconfigure(3, weight=0)
    HeaderFrame.grid_columnconfigure(4, weight=0)

    Button(HeaderFrame, text="  Add To Reading List", image=GlobalHelper.reading, width=160, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: Add_to_Reading(Root_Frame, _Root_, HeaderFrame),
          font=GlobalHelper.font_medium).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Add To Favourite", image=GlobalHelper.heart, width=160, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: Add_to_fav(Root_Frame, _Root_, HeaderFrame),
          font=GlobalHelper.font_medium).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Back to Libraries", image=GlobalHelper.back, width=160, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID, bg='#c7c7c7', command=lambda: _Root_.show_frame("My_Libraries"),
          font=GlobalHelper.font_medium).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")

    render_books_list(Root_Frame, _Root_, HeaderFrame)

    ##Show Frame
    Root_Frame.tkraise()





