from tkinter import *
from tkinter import ttk
from global_variables import GlobalHelper, HelperFunction
import json
import mysql.connector
import pathlib
from tkinter import messagebox

UPLOAD_URL = str(pathlib.Path().absolute())+'\\uploads\\'
SERVER_URL = 'http://134.209.158.52/library/'
treev = None
Selected_member_relation_id = 0


def RemoveBook(Root_Frame, _Root_):
    global Selected_member_relation_id
    if Selected_member_relation_id == 0:
        messagebox.showerror("Error", "Select a book first")
        return
    _Root_.show_frame("Global_Loading")

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    _id = str(Selected_member_relation_id)
    library_member_sql = "DELETE FROM library_books WHERE id ='"+_id+"'"
    mycursor.execute(library_member_sql)
    mydb.commit()

    messagebox.showerror("Success", "Book removed Successfully")
    render_books_list(Root_Frame, _Root_)
    _Root_.show_frame("Library_Books")
    return

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


def render_books_list(Root_Frame, _Root_):
    global treev
    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    library_id = str(library_info['id'])

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM library_books WHERE library_id='" + library_id + "'")
    field_map = fields(mycursor)
    books_list = []
    for row in mycursor:
        eachbook = {
            'id': row[field_map['id']],
            'name': row[field_map['name']],
            'author': row[field_map['author']],
            'library_id': row[field_map['library_id']],
            'description': row[field_map['description']],
            'cover': row[field_map['cover']],
            'file_path': row[field_map['file_path']],
        }
        books_list.append(eachbook)

    # Using treeview widget
    treev = ttk.Treeview(Root_Frame, selectmode='browse')

    # Calling pack method w.r.to treeview
    treev.grid(row=1, column=0, sticky="nsew")

    # Constructing vertical scrollbar
    # with treeview
    verscrlbar = ttk.Scrollbar(Root_Frame,orient="vertical",command=treev.yview)
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
    treev.heading("1", text="Name", anchor=W)
    treev.heading("2", text="Author", anchor=W)
    treev.heading("3", text="Description", anchor=W)
    treev.bind('<ButtonRelease-1>', selectItem)

    for i in range(len(books_list)):
        row = books_list[i]
        treev.insert("", 'end', text=row['id'], values=(row['name'], row['author'], row['description']))


def manage_library_books(Root_Frame, _Root_):

    Root_Frame.grid_rowconfigure(0, weight=0)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_columnconfigure(0, weight=1)


    HeaderFrame = Frame(Root_Frame, background="#fff", highlightbackground="#dfdfdf", highlightcolor="#dfdfdf", highlightthickness=1, bd=0)
    HeaderFrame.grid(row=0, column=0, sticky="nsew")

    HeaderFrame.grid_rowconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(1, weight=0)
    HeaderFrame.grid_columnconfigure(2, weight=0)
    HeaderFrame.grid_columnconfigure(3, weight=0)


    Button(HeaderFrame, text="Add Book", bg=GlobalHelper.theme_color, command=lambda: _Root_.show_frame("Library_Book_Create"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=1, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Delete Book", bg='#fc383e', command=lambda: RemoveBook(Root_Frame, _Root_), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="Back to Dashboard", bg=GlobalHelper.gray_color, command=lambda: _Root_.show_frame("Dashboard_Manager"), fg='#fff',
           height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")


    render_books_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





