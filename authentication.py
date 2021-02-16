from tkinter import *
from global_variables import GlobalHelper


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
    username = StringVar()
    password = StringVar()
    Label(screen_login_frame, text="Sign in", bg='#ffffff', font=("Bahnschrift SemiLight Condensed", 25)).grid(row=0, column=1, pady=10, sticky=NW, )
    Label(screen_login_frame, text="Email Address", bg='#ffffff').grid(row=1, column=1, pady=1, sticky=NW, )
    Entry(screen_login_frame, textvariable=username, width=50, relief=SOLID).grid(row=2, column=1, pady=3, ipady=5)
    Label(screen_login_frame, text="Password", bg='#ffffff').grid(row=3, column=1, pady=1, sticky=NW)
    Entry(screen_login_frame, textvariable=password, show='*', width=50, relief=SOLID).grid(row=4, column=1, pady=3,
                                                                                            ipady=5)
    Button(screen_login_frame, text="SIGN IN", bg=GlobalHelper.theme_color, fg='#fff', width='30', height='1', borderwidth=0, relief=SOLID, command=lambda: _Root_.show_frame("Dashboard_Manager")).grid(row=5, column=1, ipady=5, pady=10)
    Button(screen_login_frame, cursor="hand2", text="New here? Sign up Now", bg='#ffffff', bd=0, height='1', command=lambda: _Root_.show_frame("Authentication_Register")).grid(row=6, column=1)

    ##Show Frame
    Root_Frame.tkraise()
