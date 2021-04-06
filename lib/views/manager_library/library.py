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
account_avatar = ''
library_name = StringVar()
library_email = StringVar()
library_phone = StringVar()
library_address = StringVar()

def SelectImage(Root_Frame, _Root_, screen_left_frame):
    global account_avatar
    selected_file = filedialog.askopenfilename()
    extension = os.path.splitext(selected_file)[1]
    unique_filename = str(uuid.uuid4()) + extension
    HelperFunction.Upload_to_server(selected_file, unique_filename)
    account_avatar = unique_filename
    render_avatar(screen_left_frame, unique_filename)

def render_avatar(screen_left_frame, image_file):
    if image_file != '':
        img_url = SERVER_URL+image_file
        im = Image.open(requests.get(img_url, stream=True).raw)
        tkimage = ImageTk.PhotoImage(im.resize((150, 150)))
        myvar = Label(screen_left_frame, bg='#ffffff', image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=2, column=1, sticky="nsew")

def SaveUpdates(_Root_):
    global account_avatar

    name = library_name.get()
    email = library_email.get()
    phone = library_phone.get()
    address = library_address.get()

    DB_TOKEN: ''

    with open(GlobalHelper.library_info_json, 'r') as json_file:
        library_info = json.load(json_file)

    if name == '':
        messagebox.showerror("Error", "Name field is required")
        return
    else:
        library_info['title'] = name

    if email != '':
        library_info['email'] = email

    if phone != '':
        library_info['phone'] = phone

    if address != '':
        library_info['address'] = address

    if account_avatar != '':
        library_info['logo'] = account_avatar


    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    sql = "UPDATE libraries SET title=%s, logo=%s, email=%s, phone=%s, address=%s  WHERE id=%s"
    val = (library_info['title'], library_info['logo'], library_info['email'],  library_info['phone'], library_info['address'], library_info['id'])
    mycursor.execute(sql, val)
    mydb.commit()

    with open(GlobalHelper.library_info_json, 'w') as json_file:
        json.dump(library_info, json_file)
    _Root_.show_frame("Dashboard_Manager")

def manage_library(Root_Frame, _Root_):
    json_file = open(GlobalHelper.library_info_json, 'r')
    logged_user = json.load(json_file)

    if logged_user['title'] is not None:
        library_name.set(str(logged_user['title']))

    if logged_user['email'] is not None:
        library_email.set(str(logged_user['email']))

    if logged_user['phone'] is not None:
        library_phone.set(str(logged_user['phone']))

    if logged_user['address'] is not None:
        library_address.set(str(logged_user['address']))

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
    screen_left_frame.grid_rowconfigure(4, weight=1)

    Label(screen_left_frame, text="Manage Library", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(
        row=1, column=1, pady=10)
    if logged_user['logo'] is None:
        Label(screen_left_frame, text="Select Library Logo", bg=GlobalHelper.gray_color, height=8, width=24,
              font=("Bahnschrift SemiLight Condensed", 15)).grid(row=2, column=1)
    else:
        render_avatar(screen_left_frame, str(logged_user['logo']))

    Button(screen_left_frame, text="CHOOSE LOGO", bg=GlobalHelper.theme_color,
           command=lambda: SelectImage(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady=5, pady=5)

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

    Label(screen_login_frame, text="Library Details", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=1, pady=10, sticky=NW,)
    Label(screen_login_frame, text="Library Name", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=library_name, width=70, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Email Address", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=library_email, width=70, relief=SOLID).grid(row=4, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Phone", bg='#ffffff').grid(row=5, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=library_phone, width=70, relief=SOLID).grid(row=6, column=1, pady=3,
                                                                                         ipady=5)
    Label(screen_login_frame, text="Street Address", bg='#ffffff').grid(row=7, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=library_address, width=70, relief=SOLID).grid(row=8, column=1,
                                                                                                    pady=3, ipady=5)

    Button(screen_login_frame, text="Save", bg=GlobalHelper.theme_color, command=lambda: SaveUpdates(_Root_),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10,
                                                                                sticky=NW)
    Button(screen_login_frame, text="Cancel", bg=GlobalHelper.gray_color,
           command=lambda: _Root_.show_frame("Dashboard_Manager"),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10,
                                                                                sticky=NE)

    ##Show Frame
    Root_Frame.tkraise()





