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


def library_list(Root_Frame, _Root_):

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

    ##Show Frame
    Root_Frame.tkraise()





