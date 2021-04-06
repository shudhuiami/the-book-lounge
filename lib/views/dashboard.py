from tkinter import *
from global_variables import GlobalHelper, HelperFunction
import json

def logout(_Root_):
    with open(GlobalHelper.user_json, 'r') as json_file:
        user_info = json.load(json_file)
    user_info['id'] = None
    user_info['name'] = None
    user_info['email'] = None
    user_info['address'] = None
    user_info['avatar'] = None
    user_info['phone'] = None
    user_info['token'] = None
    with open(GlobalHelper.user_json, 'w') as json_file:
        json.dump(user_info, json_file)

    with open(GlobalHelper.library_info_json, 'r') as json_file_library:
        library_info = json.load(json_file_library)
    library_info['id'] = None
    library_info['title'] = None
    library_info['logo'] = None
    library_info['email'] = None
    library_info['phone'] = None
    library_info['address'] = None
    library_info['about_us'] = None

    with open(GlobalHelper.library_info_json, 'w') as json_file_library:
        json.dump(user_info, json_file_library)

    _Root_.show_frame("Authentication_Login")

def manager_dashboard(Root_Frame, _Root_):
    json_file = open(GlobalHelper.user_json, 'r')
    logged_user = json.load(json_file)
    Root_Frame.grid_columnconfigure(0, weight=1)
    Root_Frame.grid_columnconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(0, weight=1)
    Root_Frame.grid_rowconfigure(1, weight=1)
    Root_Frame.grid_rowconfigure(2, weight=1)
    Root_Frame.grid_rowconfigure(3, weight=1)

    header_frame = Frame(Root_Frame, bg='#fff')
    header_frame.grid(row=0, columnspan=2, sticky="nsew")

    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)

    account_frame = Frame(header_frame, bg='#fff')
    account_frame.grid(row=0, column=1, ipadx=10, sticky="nsew")

    account_title = Label(account_frame, bg='#fff', text=str(logged_user['name']), anchor="e", font=("Bahnschrift SemiLight Condensed", 15))
    account_title.grid(row=0, column=0, sticky="nsew")

    exit_button = Button(account_frame, text='', image=GlobalHelper.icon_exit, bd=0, bg='#fff',  cursor="hand2", command=lambda: logout(_Root_))
    exit_button.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

    section_frame_one = Frame(Root_Frame, bg='#fff')
    section_frame_one.grid(row=1, column=0, pady=30, sticky="nsew")

    section_frame_two = Frame(Root_Frame, bg='#fff')
    section_frame_two.grid(row=1, column=1, pady=30, sticky="nsew")

    section_frame_three = Frame(Root_Frame, bg='#fff')
    section_frame_three.grid(row=2, column=0, sticky="nsew")

    section_frame_four = Frame(Root_Frame, bg='#fff')
    section_frame_four.grid(row=2, column=1, sticky="nsew")

    section_frame_five = Frame(Root_Frame, bg='#fff')
    section_frame_five.grid(row=3, column=0, sticky="nsew")

    section_frame_six = Frame(Root_Frame, bg='#fff')
    section_frame_six.grid(row=3, column=1, sticky="nsew")

    if logged_user['user_type'] == 1:
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_one, 'Manage Library', 'Manage_Library')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_two, 'Manage Books', 'Library_Books')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_three, 'Manage Members', 'library_Members_List')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_four, 'Manage Account', 'Manage_Account')
    else:
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_one, 'Libraries', 'My_Libraries')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_two, 'Favourite Books', 'Manage_Account')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_three, 'Request Book', '')
        HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_four, 'Manage Account', 'Manage_Account')


    ##Show Frame
    Root_Frame.tkraise()





