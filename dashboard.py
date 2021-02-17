from tkinter import *
from global_variables import GlobalHelper, HelperFunction

def manager_dashboard(Root_Frame, _Root_):
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

    account_title = Label(account_frame, bg='#fff', text="Ahmed Zobayer", anchor="e", font=("Bahnschrift SemiLight Condensed", 15))
    account_title.grid(row=0, column=0, sticky="nsew")

    exit_button = Button(account_frame, text='', image=GlobalHelper.icon_exit, bd=0, bg='#fff',  cursor="hand2", command=lambda: _Root_.show_frame("Authentication_Login"))
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

    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_one, 'Manage Library')
    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_two, 'Manage Books')
    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_three, 'Manage Members')
    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_four, 'Manage Book Request')
    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_five, 'Manage Wishlist')
    HelperFunction.create_home_button(Root_Frame, _Root_, section_frame_six, 'Manage Account')

    ##Show Frame
    Root_Frame.tkraise()





