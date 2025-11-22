from PIL import Image
import customtkinter as ctk


def validate_login_and_password(login:str,password:str) -> bool:
    pass


def Authorize_window(*, app: ctk.CTk) -> None:
    app.geometry("1280x800")
    app.title("Авторизація")
    app.configure(fg_color="#00BFFF")

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
    frame_container.propagate(False) # Фрейм не змінює свої розміри залежно від його елементів всередині

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
        hover_color="#28AAE2"
    )
    button_log_in.pack()





if __name__ == "__main__":
    APP = ctk.CTk()
    Authorize_window(app = APP)
    APP.mainloop()