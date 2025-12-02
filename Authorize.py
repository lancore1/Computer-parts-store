from PIL import Image
import customtkinter as ctk
from DB_connector import CONNECT
from error_login import error_window
from Main_Frame import *

def validate_login_and_password(APP,login:str,password:str) -> None:
    print(login,password)
    
    try:
        # Create a cursor to execute SQL queries
        cursor_auth = CONNECT.cursor()
        # Query for validate input data, validate_login_password is a function created in SERVER!
        query_tab = f'''
            SELECT validate_login_password('{login}','{password}')
        '''
        cursor_auth.execute(query_tab) # exucutes an SQL query
        # converts the response into a list of tuples, for example this one [(0,)] - the structure of the fetchall() who was been return
        response = cursor_auth.fetchall() 

        result = response[0][0] # first row and column we get a NUMBER 0 or 1

        if result:
            # 
            for widget in APP.winfo_children():
                widget.destroy()
            Main_window(app=APP)
        else:
            error_window(APP)



    except:
        print("We have a problem with query or input data for validate in AUTH ")



def Authorize_window(app) -> None:
    # app = ctk.CTk()    
    # app.geometry("1280x800")
    # app.title("Авторизація")
    # app.configure(fg_color="#00BFFF")
    # # open app in full screen
    # app.after(50, lambda: app.state("zoomed"))

    #Frame Container 
    frame_container = ctk.CTkFrame(master=app,
        width=432, 
        height=325, 
        corner_radius=25, 
        fg_color="#ffffff", 
        border_width=1, 
        border_color="#e2e8f0"
    )
    frame_container.place(relx=0.5, rely=0.5, anchor="center")
    frame_container.propagate(False) # The frame does not change its dimensions depending on its elements inside

    #Frame for Title
    frame_title = ctk.CTkFrame(master=frame_container,width=300, height=60,fg_color="transparent")
    frame_title.pack(pady=(25,0),padx=(0,100),side="top",anchor="nw")
    frame_title.propagate(False)

    #Image for title
    image_title = ctk.CTkImage(
        light_image=Image.open("images/image_title.png"), 
        dark_image=Image.open("images/image_title.png"),
        size=(50,50)
    )

    #Label for image
    label_img = ctk.CTkLabel(master=frame_title, text="", image=image_title)
    label_img.grid(row=0,column=0,padx=(25,0))

    #Title
    label_title = ctk.CTkLabel(master=frame_title, 
        text="Авторизуйтесь", 
        width=10, 
        height=1, 
        corner_radius=8, 
        fg_color="transparent", 
        text_color="#000000", 
        font=("Lato", 24, "bold")
    )
    label_title.grid(row=0,column=1,padx=(25,0))

    #Frame for Input
    frame_input = ctk.CTkFrame(master=frame_container,width=382, height=200,fg_color="transparent")
    frame_input.pack(pady=(25,0))
    frame_input.propagate(False)

    #Frame for login
    frame_login = ctk.CTkFrame(master=frame_input,width=382,height=50,fg_color="transparent")
    frame_login.pack()

    #Entry login
    entry_login = ctk.CTkEntry(master=frame_login,
        width=382,
        height=50,
        corner_radius=10,
        fg_color="transparent",
        border_width=2,
        border_color="#00BFFF",
        placeholder_text_color="#7F7F7F",
        placeholder_text="Логін",
        text_color="#000000", 
        font=("Lato",16,"normal")
    )
    entry_login.pack()

    #Frame for login
    frame_password = ctk.CTkFrame(master=frame_input,width=382,height=50, fg_color="transparent")
    frame_password.pack(side="top", pady=(25,0))

    #Entry login
    entry_password = ctk.CTkEntry(master=frame_password,
        width=382,
        height=50,
        corner_radius=10,
        fg_color="transparent",
        border_width=2,
        border_color="#00BFFF",
        placeholder_text_color="#7F7F7F",
        placeholder_text="Пароль",
        text_color="#000000", 
        font=("Lato",16,"normal")
    )
    entry_password.pack()

    #Frame for button
    frame_button = ctk.CTkFrame(master=frame_input,width=150,height=50,fg_color="transparent")
    frame_button.pack(side="bottom", anchor="e", pady=(15,5))

    #Entry login
    button_log_in = ctk.CTkButton(master=frame_button,
        width=150,
        height=50,
        corner_radius=25,
        text="Увійти",
        fg_color="#00BFFF",
        text_color="#FFFFFF", 
        font=("Lato",24,"bold"),
        hover_color="#28AAE2",
        command=lambda: validate_login_and_password(app,entry_login.get(),entry_password.get())
    )
    button_log_in.pack()


