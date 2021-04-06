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


def global_loading(Root_Frame, _Root_):
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)

    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=1)
    Root_Frame.grid_columnconfigure(2, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(2, weight=1)

    Label(Root_Frame, text="Loading...", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(row=0,column=1,pady=10,)

    ##Show Frame
    Root_Frame.tkraise()





