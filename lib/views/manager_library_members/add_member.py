from tkinter import *
from global_variables import GlobalHelper, HelperFunction
import json
from tkinter import messagebox
import mysql.connector

member_email = StringVar()

def AddMember(Root_Frame, _Root_):
    global member_email
    member_email_address = member_email.get()
    if member_email_address == '':
        messagebox.showerror("Error", "Email address field is required")
        return

    with open(GlobalHelper.library_info_json, 'r') as library_json_file:
        library_info = json.load(library_json_file)

    mydb = mysql.connector.connect(host=GlobalHelper.SERVER_HOST, user=GlobalHelper.SERVER_USERNAME, password=GlobalHelper.SERVER_PASSWORD, database=GlobalHelper.SERVER_DATABASE)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id FROM users WHERE email='" + member_email_address + "' AND user_type = 2")
    result = mycursor.fetchone()
    if result is None:
        messagebox.showerror("Error", "Email address is Invalid")
        return

    member_id = str(result[0])
    library_id = str(library_info['id'])

    mycursor.execute("SELECT id FROM library_members WHERE member_id='" + member_id + "' AND library_id ='"+library_id+"'")
    result = mycursor.fetchone()
    if result is not None:
        messagebox.showerror("Error", "Member already exist")
        return

    library_member_sql = "INSERT INTO library_members (library_id, member_id) VALUES (%s, %s)"
    library_member_val = (library_id, member_id)
    mycursor.execute(library_member_sql, library_member_val)
    mydb.commit()
    member_email.set('')

    _Root_.show_frame("library_Members_List")

def Add_member_to_library(Root_Frame, _Root_):
    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=0)
    Root_Frame.grid_columnconfigure(2, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)
    Root_Frame.grid_rowconfigure(1, weight=0)
    Root_Frame.grid_rowconfigure(2, weight=0)
    Root_Frame.grid_rowconfigure(3, weight=0)
    Root_Frame.grid_rowconfigure(4, weight=0)
    Root_Frame.grid_rowconfigure(5, weight=1)

    Label(Root_Frame, text="Member's Email Address", bg='#fff', width=80, anchor='w').grid(row=1, column=1, ipadx=20, pady=1)

    Entry(Root_Frame, textvariable=member_email, relief=SOLID, width=100).grid(row=2, column=1, pady=3, ipady=5)

    Button(Root_Frame, text="Create", bg=GlobalHelper.theme_color, command=lambda: AddMember(Root_Frame, _Root_),
           fg='#fff', height='1', borderwidth=0, relief=SOLID, width=85).grid(row=3, column=1, ipady=5, pady=10)

    Button(Root_Frame, text="Cancel", bg=GlobalHelper.gray_color,
           command=lambda: _Root_.show_frame("library_Members_List"),
           fg='#fff', height='1', borderwidth=0, relief=SOLID, width=85).grid(row=4, column=1, ipady=5, pady=10)

    ##Show Frame
    Root_Frame.tkraise()





