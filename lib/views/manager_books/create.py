from tkinter import *
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
book_cover = ''
book_file_path = ''
book_name = StringVar()
book_author = StringVar()
book_description = None

def SelectImage(Root_Frame, _Root_, screen_left_frame):
    global book_cover
    Button(screen_left_frame, text="Uploading Cover...", bg=GlobalHelper.theme_color,
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady=5, pady=5)

    selected_file = filedialog.askopenfilename(defaultextension=".pdf, .jpg", filetypes=[('image files', '.png'), ('image files', '.jpg'), ])
    if len(selected_file) > 0:
        extension = os.path.splitext(selected_file)[1]
        unique_filename = str(uuid.uuid4()) + extension
        HelperFunction.Upload_to_server(selected_file, unique_filename)
        book_cover = unique_filename
        render_avatar(screen_left_frame, unique_filename)

    Button(screen_left_frame, text="CHOOSE BOOK COVER", bg=GlobalHelper.theme_color,
           command=lambda: SelectImage(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady=5, pady=5)


def SelectFile(Root_Frame, _Root_, screen_left_frame):
    Label(screen_left_frame, text="Uploading File...", bg=GlobalHelper.theme_color, height=2, width=24, fg='#fff',
          font=("Bahnschrift SemiLight Condensed", 15)).grid(row=5, column=1)
    global book_file_path
    selected_file = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[('pdf file', '*.pdf')])
    if len(selected_file) > 0:
        extension = os.path.splitext(selected_file)[1]
        unique_filename = str(uuid.uuid4()) + extension
        HelperFunction.Upload_to_server(selected_file, unique_filename)
        book_file_path = unique_filename
        Label(screen_left_frame, text="File Selected", bg=GlobalHelper.theme_color, height=2, width=24, fg='#fff',
              font=("Bahnschrift SemiLight Condensed", 15)).grid(row=5, column=1)
    else:
        Label(screen_left_frame, text="No File Selected", bg=GlobalHelper.gray_color, height=2, width=24, fg='#fff',
              font=("Bahnschrift SemiLight Condensed", 15)).grid(row=5, column=1)

def render_avatar(screen_left_frame, image_file):
    if image_file != '':
        img_url = SERVER_URL+image_file
        im = Image.open(requests.get(img_url, stream=True).raw)
        tkimage = ImageTk.PhotoImage(im.resize((150, 150)))
        myvar = Label(screen_left_frame, bg='#ffffff', image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=2, column=1, sticky="nsew")

def CreateBook(_Root_):
    global book_cover
    global book_file_path
    global book_description

    name = book_name.get()
    author = book_author.get()
    description = book_description.get("1.0",END)

    if name == '':
        messagebox.showerror("Error", "Name field is required")
        return

    if author == '':
        messagebox.showerror("Error", "Author field is required")
        return

    if len(description) > 1:
        messagebox.showerror("Error", "Description field is required")
        return

    if book_cover == '':
        messagebox.showerror("Error", "Book Cover is required")
        return

    if book_file_path == '':
        messagebox.showerror("Error", "Book file content is required")
        return

    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    library_member_sql = "INSERT INTO library_books (name, author, library_id, description, cover, file_path) VALUES (%s, %s, %s, %s, %s, %s)"
    library_member_val = (name, author, library_info['id'], description, book_cover, book_file_path)
    mycursor.execute(library_member_sql, library_member_val)
    mydb.commit()

    _Root_.show_frame("Library_Books")

def library_create_book(Root_Frame, _Root_):
    global book_description

    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)

    screen_left_frame = Frame(Root_Frame, bg='#fff')
    screen_left_frame.grid(row=0, column=0, sticky="nsew")
    screen_left_frame.grid_columnconfigure(0, weight=1)
    screen_left_frame.grid_columnconfigure(1, weight=1)
    screen_left_frame.grid_columnconfigure(2, weight=1)
    screen_left_frame.grid_rowconfigure(0, weight=1)
    screen_left_frame.grid_rowconfigure(1, weight=0)
    screen_left_frame.grid_rowconfigure(2, weight=0)
    screen_left_frame.grid_rowconfigure(3, weight=0)
    screen_left_frame.grid_rowconfigure(4, weight=0)
    screen_left_frame.grid_rowconfigure(5, weight=0)
    screen_left_frame.grid_rowconfigure(6, weight=1)

    Label(screen_left_frame, text="Create Book", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(
        row=1, column=1, pady=10)

    Label(screen_left_frame, text="Select Cover", bg=GlobalHelper.gray_color, height=8, width=24,
          font=("Bahnschrift SemiLight Condensed", 15)).grid(row=2, column=1)

    Button(screen_left_frame, text="CHOOSE BOOK COVER", bg=GlobalHelper.theme_color,
           command=lambda: SelectImage(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady=5, pady=5)

    Button(screen_left_frame, text="CHOOSE BOOK FILE", bg=GlobalHelper.theme_color,
           command=lambda: SelectFile(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=4, column=1, ipady=5, pady=5)

    Label(screen_left_frame, text="No File Selected", bg=GlobalHelper.gray_color, height=2, width=24,
          font=("Bahnschrift SemiLight Condensed", 15)).grid(row=5, column=1)


    screen_right_frame = Frame(Root_Frame, bg='#fff')
    screen_right_frame.grid(row=0, column=1, sticky="nsew")

    # Register Frame
    screen_right_frame.grid_columnconfigure(0, weight=1)
    screen_right_frame.grid_columnconfigure(1, weight=1)
    screen_right_frame.grid_columnconfigure(2, weight=1)
    screen_right_frame.grid_rowconfigure(0, weight=2)
    screen_right_frame.grid_rowconfigure(1, weight=1)
    screen_right_frame.grid_rowconfigure(2, weight=1)

    screen_login_frame = Frame(screen_right_frame, bg='#fff')
    screen_login_frame.grid(row=1, column=1, sticky="nsew")

    Label(screen_login_frame, text="Book Details", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=1, pady=10, sticky=NW,)

    Label(screen_login_frame, text="Book Name", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=book_name, width=70, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Book Author", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=book_author, width=70, relief=SOLID).grid(row=4, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Book Description", bg='#ffffff').grid(row=5, column=1, pady=1, sticky=NW, )
    book_description = Text(screen_login_frame, width=53, height=10, relief=SOLID, font=("Bahnschrift SemiLight Condensed", 15))
    book_description.grid(row=6, column=1, pady=3, ipady=5)

    Button(screen_login_frame, text="Create", bg=GlobalHelper.theme_color, command=lambda: CreateBook(_Root_),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10,
                                                                                sticky=NW)
    Button(screen_login_frame, text="Cancel", bg=GlobalHelper.gray_color,
           command=lambda: _Root_.show_frame("Library_Books"),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10,
                                                                                sticky=NE)

    ##Show Frame
    Root_Frame.tkraise()





