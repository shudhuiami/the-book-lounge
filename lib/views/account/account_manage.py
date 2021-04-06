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
account_name = StringVar()
account_address = StringVar()
account_phone = StringVar()
account_password = StringVar()


def SelectImage(Root_Frame, _Root_, screen_left_frame):
    global account_avatar
    Button(screen_left_frame, text="Uploading Picture...", bg=GlobalHelper.theme_color,
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady= 5, pady=5)
    selected_file = filedialog.askopenfilename()

    if len(selected_file) > 0:
        extension = os.path.splitext(selected_file)[1]
        unique_filename = str(uuid.uuid4()) + extension
        HelperFunction.Upload_to_server(selected_file, unique_filename)
        account_avatar = unique_filename
        render_avatar(screen_left_frame, unique_filename)

    Button(screen_left_frame, text="Choose Picture", bg=GlobalHelper.theme_color,
           command=lambda: SelectImage(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady=5, pady=5)

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

    name = account_name.get()
    address = account_address.get()
    password = account_password.get()
    phone = account_phone.get()

    DB_TOKEN: ''

    with open(GlobalHelper.user_json, 'r') as json_file:
        user_info = json.load(json_file)

    if name == '':
        messagebox.showerror("Error", "Name field is required")
        return
    else:
        user_info['name'] = name

    if address != '':
        user_info['address'] = address

    if phone != '':
        user_info['phone'] = phone

    if account_avatar != '':
        user_info['avatar'] = account_avatar


    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()
    if password != '':
        HASH_PASS = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = "UPDATE users SET name=%s, avatar=%s, password=%s, address=%s, phone=%s WHERE token=%s"
        val = (user_info['name'], user_info['avatar'], HASH_PASS, user_info['address'], user_info['phone'], user_info['token'])
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        sql = "UPDATE users SET name=%s, avatar=%s, address=%s, phone=%s WHERE token=%s"
        val = (user_info['name'], user_info['avatar'], user_info['address'], user_info['phone'], user_info['token'])
        mycursor.execute(sql, val)
        mydb.commit()

    with open(GlobalHelper.user_json, 'w') as json_file:
        json.dump(user_info, json_file)

    _Root_.show_frame("Dashboard_Manager")

def manage_account(Root_Frame, _Root_):
    print(HelperFunction.ROOT_PATH)
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)

    if logged_user['name'] is not None:
        account_name.set(str(logged_user['name']))

    if logged_user['phone'] is not None:
        account_phone.set(str(logged_user['phone']))

    if logged_user['address'] is not None:
        account_address.set(str(logged_user['address']))

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


    Label(screen_left_frame, text="Manage Account", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(row=1, column=1, pady=10)
    if logged_user['avatar'] is None:
        Label(screen_left_frame, text="Select Profile Picture", bg=GlobalHelper.gray_color, height= 12, width=32,  font=("Bahnschrift SemiLight Condensed", 15)).grid(row=2, column=1)
    else:
        render_avatar(screen_left_frame, str(logged_user['avatar']))

    Button(screen_left_frame, text="Choose Picture", bg=GlobalHelper.theme_color, command=lambda: SelectImage(Root_Frame, _Root_, screen_left_frame),
           fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID).grid(row=3, column=1, ipady= 5, pady=5)



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

    Label(screen_login_frame, text="Personal Details", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 15)).grid(row=0, column=1, pady=10)
    Label(screen_login_frame, text="Name", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=account_name, width=70, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Phone", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=account_phone, width=70, relief=SOLID).grid(row=4, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Street Address", bg='#ffffff').grid(row=5, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=account_address, width=70, relief=SOLID).grid(row=6, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="New Password", bg='#ffffff').grid(row=7, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=account_password, show='*', width=70, relief=SOLID).grid(row=8, column=1, pady=3, ipady=5)


    Button(screen_login_frame, text="Update", bg=GlobalHelper.theme_color, command=lambda: SaveUpdates(_Root_),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10, sticky=NW)
    Button(screen_login_frame, text="Cancel", bg=GlobalHelper.gray_color, command=lambda: _Root_.show_frame("Dashboard_Manager"),
           fg='#fff', width='25', height='1', borderwidth=0, relief=SOLID).grid(row=9, column=1, ipady=5, pady=10, sticky=NE)

    ##Show Frame
    Root_Frame.tkraise()





