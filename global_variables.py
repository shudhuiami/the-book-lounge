from tkinter import *
from tkinter import messagebox

class GlobalHelper:
    theme_color = '#6159e6'
    gray_color = '#c9c9c9'
    logo = PhotoImage(file='.//images//logo.png')
    login_cover = PhotoImage(file='.//images//login.png')
    register_cover = PhotoImage(file='.//images//register.png')

    icon_exit = PhotoImage(file='.//images//home-icons//exit.png')
    icon_library = PhotoImage(file='.//images//home-icons//library.png')
    icon_book = PhotoImage(file='.//images//home-icons//book.png')
    icon_members = PhotoImage(file='.//images//home-icons//members.png')
    icon_question = PhotoImage(file='.//images//home-icons//question.png')
    icon_wishlist = PhotoImage(file='.//images//home-icons//wishlist.png')
    icon_profile = PhotoImage(file='.//images//home-icons//profile.png')

def ViewSection(_Root_, section_path):
    _Root_.show_frame(section_path)

class HelperFunction:
    def create_home_button(root_frame, _root_, section_frame, section_title, section_path):
        section_frame.grid_columnconfigure(0, weight=1)
        section_frame.grid_columnconfigure(1, weight=1)
        section_frame.grid_columnconfigure(2, weight=1)
        section_frame.grid_rowconfigure(0, weight=1)
        section_frame.grid_rowconfigure(1, weight=1)
        section_frame.grid_rowconfigure(2, weight=1)

        Inner_layer = Frame(section_frame, bg='#fff', cursor="hand2")
        Inner_layer.grid(row=1, column=1, sticky="nsew")
        canvas = Canvas(Inner_layer, width=90, height=90, bg='#fff', bd=0, highlightthickness=0, )
        canvas.bind("<Button-1>", lambda event:ViewSection(_root_, section_path))
        canvas.pack()
        if (section_title == 'Manage Library'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_library, anchor=NW)
        elif (section_title == 'Manage Books'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_book, anchor=NW)
        elif (section_title == 'Manage Members'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_members, anchor=NW)
        elif (section_title == 'Manage Book Request'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_question, anchor=NW)
        elif (section_title == 'Manage Wishlist'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_wishlist, anchor=NW)
        elif (section_title == 'Manage Account'):
            canvas.create_image(0, 0, image=GlobalHelper.icon_profile, anchor=NW)

        button_two = Label(Inner_layer, text=section_title, bg='#fff', font=("Bahnschrift SemiLight Condensed", 15))
        button_two.pack(pady=15)
