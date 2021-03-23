from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from global_variables import GlobalHelper
import mysql.connector
import pymysql.cursors
import re
import bcrypt
import secrets
import json

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

reg_name = StringVar()
reg_email = StringVar()
reg_address = StringVar()
reg_username = StringVar()
reg_password = StringVar()
reg_confirm_password = StringVar()
reg_user_type = 1

username = StringVar()
password = StringVar()

def UserTypeSelected(eventObject):
    global reg_user_type
    selected_type = eventObject.widget.get()
    if selected_type == 'Library Manager':
        reg_user_type = 1
    else:
        reg_user_type = 2

def fields(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results

def RegisterUser(_Root_):
    global reg_user_type
    name = reg_name.get()
    email = reg_email.get()
    password = reg_password.get()
    confirm_password = reg_confirm_password.get()

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    # connection =  pymysql.connect(host=GlobalHelper.SERVER_HOST, port=3306, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    # mycursor = connection.cursor()

    if name == '':
        messagebox.showerror("Error", "Name field is required")
        return

    if email == '':
        messagebox.showerror("Error", "Email field is required")
        return

    if not re.search(email_regex, email):
        messagebox.showerror("Error", "Email address is invalid")
        return

    if len(password) < 6:
        messagebox.showerror("Error", "password must be at least 6 characters long")
        return

    if password == '':
        messagebox.showerror("Error", "Password field is required")
        return

    if confirm_password == '':
        messagebox.showerror("Error", "Confirm password did not match")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Confirm password did not match")
        return

    mycursor.execute("SELECT id FROM users WHERE email='" + email + "'")
    result = mycursor.fetchone()
    if result is not None:
        messagebox.showerror("Error", "Email address is already taken")
        return

    HASH_PASS = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    sql = "INSERT INTO users (name, email, user_type, password) VALUES (%s, %s, %s, %s)"
    val = (name, email, reg_user_type, HASH_PASS)
    mycursor.execute(sql, val)
    mydb.commit()
    _Root_.show_frame("Authentication_Login")
    messagebox.showinfo("Information", "Registration Successful. Please login")
    reg_name.set('')
    reg_email.set('')
    reg_address.set('')
    reg_password.set('')
    reg_confirm_password.set('')

def LoginUser(_Root_):
    # user_info = {
    #     "name": "",
    #     "email": "",
    #     "address": "",
    #     "avatar": "",
    #     "phone": "",
    #     "token": ""
    # }
    # with open(GlobalHelper.user_json, 'w') as json_file:
    #     json.dump(user_info, json_file)

    # with open(GlobalHelper.user_json, 'r') as json_file:
    #     user_info = json.load(json_file)
    #
    # user_info['name'] = "Zobayer"
    #
    # with open(GlobalHelper.user_json, 'w') as json_file:
    #     json.dump(user_info, json_file)

    login_email = username.get()
    login_password = password.get()

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    if login_email == '':
        messagebox.showerror("Error", "Email field is required")
        return

    if not re.search(email_regex, login_email):
        messagebox.showerror("Error", "Email address is invalid")
        return

    if login_password == '':
        messagebox.showerror("Error", "Password field is required")
        return

    if len(login_password) < 6:
        messagebox.showerror("Error", "password must be at least 6 characters long")
        return

    mycursor.execute("SELECT * FROM users WHERE email='" + login_email + "'")
    user = mycursor.fetchone()
    if user is None:
        messagebox.showerror("Error", "Email address is not registered")
        return

    mycursor.execute("SELECT * FROM users WHERE email='" + login_email + "'")
    field_map = fields(mycursor)
    for row in mycursor:
        DB_PASS = row[field_map['password']]
        if bcrypt.checkpw(login_password.encode('utf-8'), DB_PASS.encode('utf-8'), ):

            auth_token = secrets.token_hex(16)

            sql = "UPDATE users SET token = '" + auth_token + "' WHERE email='" + login_email + "'"
            mycursor.execute(sql)
            mydb.commit()

            with open(GlobalHelper.user_json, 'r') as json_file:
                user_info = json.load(json_file)

            user_info['name'] = row[field_map['name']]
            user_info['email'] = row[field_map['email']]
            user_info['address'] = row[field_map['address']]
            user_info['user_type'] = row[field_map['user_type']]
            user_info['avatar'] = row[field_map['avatar']]
            user_info['phone'] = row[field_map['phone']]
            user_info['token'] = auth_token

            with open(GlobalHelper.user_json, 'w') as json_file:
                json.dump(user_info, json_file)
            _Root_.show_frame("Dashboard_Manager")

            username.set('')
            password.set('')
            return
        else:
            messagebox.showinfo("Success", "Invalid Credentials")
            return

def register(Root_Frame, _Root_):
    global reg_user_type
    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)

    screen_left_frame = Frame(Root_Frame, bg='#fff')
    screen_left_frame.grid(row=0, column=0, sticky="nsew")
    screen_left_frame.grid_columnconfigure(0, weight=1)
    screen_left_frame.grid_columnconfigure(1, weight=1)
    screen_left_frame.grid_columnconfigure(2, weight=1)
    screen_left_frame.grid_rowconfigure(0, weight=1)
    screen_left_frame.grid_rowconfigure(1, weight=1)
    screen_left_frame.grid_rowconfigure(2, weight=1)
    screen_left_frame.grid_rowconfigure(3, weight=1)

    # create the canvas, size in pixels
    canvas = Canvas(screen_left_frame, width=350, height=270, bg='#fff', bd=0, highlightthickness=0, )
    canvas.grid(row=2, column=1, sticky="nsew")
    canvas.create_image(0, 0, image=GlobalHelper.register_cover, anchor=NW)
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

    Label(screen_login_frame, text="Sign up", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(row=0,column=1,pady=10,sticky=NW, )
    Label(screen_login_frame, text="Name", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=reg_name, width=50, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="Email Address", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=reg_email, width=50, relief=SOLID).grid(row=4, column=1, pady=3, ipady=5)

    Label(screen_login_frame, text="User type", bg='#ffffff').grid(row=5, column=1, pady=1, sticky=NW)
    choices = ['Library Manager', 'Library Member']
    selected_user_type = StringVar(screen_login_frame)
    selected_user_type.set('Library Manager')
    user_type_select = ttk.Combobox(screen_login_frame, value=choices, state="readonly", width=47)
    user_type_select.current(0)
    user_type_select.grid(row=6, column=1, pady=3, ipady=5)
    user_type_select.bind("<<ComboboxSelected>>", UserTypeSelected)

    Label(screen_login_frame, text="Password", bg='#ffffff').grid(row=7, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=reg_password, show='*', width=50, relief=SOLID).grid(row=8, column=1, pady=3,ipady=5)

    Label(screen_login_frame, text="Confirm Password", bg='#ffffff').grid(row=9, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=reg_confirm_password, show='*', width=50, relief=SOLID).grid(row=10,column=1,pady=3, ipady=5)

    Button(screen_login_frame, command=lambda: RegisterUser(_Root_), text="SIGN UP", bg=GlobalHelper.theme_color,fg='#fff', width='30',height='1', borderwidth=0, relief=SOLID).grid(row=11, column=1, ipady=5, pady=10)
    Button(screen_login_frame, cursor="hand2", text="Already have an account? Sign in Now", bg='#ffffff', bd=0,height='1', command=lambda: _Root_.show_frame("Authentication_Login")).grid(row=12, column=1)

    ##Show Frame
    Root_Frame.tkraise()


def login(Root_Frame, _Root_):
    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)

    screen_left_frame = Frame(Root_Frame, bg='#fff')
    screen_left_frame.grid(row=0, column=0, sticky="nsew")
    screen_left_frame.grid_columnconfigure(0, weight=1)
    screen_left_frame.grid_columnconfigure(1, weight=1)
    screen_left_frame.grid_columnconfigure(2, weight=1)
    screen_left_frame.grid_rowconfigure(0, weight=1)
    screen_left_frame.grid_rowconfigure(1, weight=1)
    screen_left_frame.grid_rowconfigure(2, weight=1)
    screen_left_frame.grid_rowconfigure(3, weight=1)

    # create the canvas, size in pixels
    canvas = Canvas(screen_left_frame, width=400, height=308, bg='#fff', bd=0, highlightthickness=0, )
    canvas.grid(row=2, column=1, sticky="nsew")
    canvas.create_image(0, 0, image=GlobalHelper.login_cover, anchor=NW)

    screen_right_frame = Frame(Root_Frame, bg='#fff')
    screen_right_frame.grid(row=0, column=1, sticky="nsew")

    # Login Frame
    screen_right_frame.grid_columnconfigure(0, weight=1)
    screen_right_frame.grid_columnconfigure(1, weight=1)
    screen_right_frame.grid_columnconfigure(2, weight=1)
    screen_right_frame.grid_rowconfigure(0, weight=1)
    screen_right_frame.grid_rowconfigure(1, weight=1)
    screen_right_frame.grid_rowconfigure(2, weight=1)
    screen_right_frame.grid_rowconfigure(3, weight=1)
    screen_login_frame = Frame(screen_right_frame, bg='#fff')
    screen_login_frame.grid(row=2, column=1, sticky="nsew")

    Label(screen_login_frame, text="Sign in", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(row=0,
                                                                                                               column=1,
                                                                                                               pady=10,
                                                                                                               sticky=NW, )
    Label(screen_login_frame, text="Email Address", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=username, width=50, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)
    Label(screen_login_frame, text="Password", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=password, show='*', width=50, relief=SOLID).grid(row=4, column=1, pady=3,
                                                                                            ipady=5)
    Button(screen_login_frame, text="SIGN IN", bg=GlobalHelper.theme_color, fg='#fff', width='30', height='1',
           borderwidth=0, relief=SOLID, command=lambda: LoginUser(_Root_)).grid(row=5, column=1,
                                                                                ipady=5, pady=10)
    Button(screen_login_frame, cursor="hand2", text="New here? Sign up Now", bg='#ffffff', bd=0, height='1',
           command=lambda: _Root_.show_frame("Authentication_Register")).grid(row=6, column=1)

    ##Show Frame
    Root_Frame.tkraise()
