from tkinter import *
from tkinter import ttk
from global_variables import GlobalHelper, HelperFunction
import json
import mysql.connector
import pathlib
import textwrap
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

def wrap(string, lenght=80):
    return '\n'.join(textwrap.wrap(string, lenght))


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
            'genre': row[field_map['genre']],
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
    verscrlbar = ttk.Scrollbar(Root_Frame,orient="vertical",command=treev.yview)
    # Calling pack method w.r.to verical
    # scrollbar
    verscrlbar.grid(row=1, column=1, sticky="nsew")

    # Configuring treeview
    treev.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    treev["columns"] = ("1", "2", "3", "4")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", stretch=NO, anchor=W)
    treev.column("2", stretch=NO, anchor=W)
    treev.column("3", stretch=NO, anchor=W)
    treev.column("4", anchor=W)

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="Name", anchor=W)
    treev.heading("2", text="Author", anchor=W)
    treev.heading("3", text="Genre", anchor=W)
    treev.heading("4", text="Description", anchor=W)
    treev.bind('<ButtonRelease-1>', selectItem)

    for i in range(len(books_list)):
        row = books_list[i]
        treev.insert("", 'end', text=row['id'], values=(row['name'], row['author'],  row['genre'], wrap(row['description'])))


def manage_library_books(Root_Frame, _Root_):

    Root_Frame.grid_rowconfigure(0, weight=0)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_columnconfigure(0, weight=1)


    HeaderFrame = Frame(Root_Frame, background="#fff", highlightbackground="#dfdfdf", highlightcolor="#dfdfdf", highlightthickness=1, bd=0)
    HeaderFrame.grid(row=0, column=0, sticky="nsew")

    HeaderFrame.grid_rowconfigure(0, weight=1)
    HeaderFrame.grid_columnconfigure(0, weight=0)
    HeaderFrame.grid_columnconfigure(1, weight=1)
    HeaderFrame.grid_columnconfigure(2, weight=0)
    HeaderFrame.grid_columnconfigure(3, weight=0)
    HeaderFrame.grid_columnconfigure(4, weight=0)

    Label(HeaderFrame, text="Dashboard  >  Books", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=0)

    Button(HeaderFrame, text="  Add Book", image=GlobalHelper.add_book, width=100, height=22, compound=LEFT, fg='#fff', borderwidth=0, relief=SOLID, bg=GlobalHelper.theme_color, command=lambda: _Root_.show_frame("Library_Book_Create"),
          font=GlobalHelper.font_medium).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Delete Book", image=GlobalHelper.remove, width=100, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID,  bg=GlobalHelper.theme_color, command=lambda: RemoveBook(Root_Frame, _Root_),
          font=GlobalHelper.font_medium).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    Button(HeaderFrame, text="  Back to Dashboard", image=GlobalHelper.back, width=150, height=22, compound=LEFT, fg='#fff',  borderwidth=0, relief=SOLID, bg='#c7c7c7', command=lambda: _Root_.show_frame("Dashboard_Manager"),
          font=GlobalHelper.font_medium).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")


    # Button(HeaderFrame, text="Add Book", image=GlobalHelper.icon_exit, width=30, height=30, bg=GlobalHelper.theme_color, command=lambda: _Root_.show_frame("Library_Book_Create"), fg='#fff',
    #         borderwidth=0, relief=SOLID).grid(row=0, column=2, ipady=3, padx=5, pady=15, sticky="we")
    # Button(HeaderFrame, text="Delete Book", bg='#fc383e', command=lambda: RemoveBook(Root_Frame, _Root_), fg='#fff',
    #        height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=3, ipady=3, padx=5, pady=15, sticky="we")
    # Button(HeaderFrame, text="Back to Dashboard", bg='#c7c7c7', command=lambda: _Root_.show_frame("Dashboard_Manager"), fg='#fff',
    #        height='1', borderwidth=0, relief=SOLID, width=20).grid(row=0, column=4, ipady=3, padx=5, pady=15, sticky="we")


    render_books_list(Root_Frame, _Root_)

    ##Show Frame
    Root_Frame.tkraise()





