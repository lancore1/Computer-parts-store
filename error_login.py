import customtkinter as ctk



def error_window(parent) -> None:
    win_error = ctk.CTkToplevel(master=parent)     
    win_error.title("Помилка!")
    win_error.configure(fg_color="#00BFFF")
    # const of value size window error 
    WIDTH = 432
    HEIGHT = 190

    win_error.geometry(f"{WIDTH}x{HEIGHT}")
    # centered our window 
    x = (win_error.winfo_screenwidth() - win_error.winfo_width()) // 2
    y = (win_error.winfo_screenheight() - win_error.winfo_height()) // 2

    win_error.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    # Modal window
    win_error.grab_set()

    # Frame Container
    frame_container = ctk.CTkFrame(master=win_error,width=WIDTH,height=HEIGHT,fg_color="#ffffff")
    frame_container.place(rely=0.5,relx=0.5,anchor="center")

    #Frame for label
    frame_label = ctk.CTkFrame(master=frame_container,width=120,height=40,fg_color="transparent")
    frame_label.place(rely=0.100,relx=0.050)

    #Label for title
    title_label = ctk.CTkLabel(master=frame_label,
        width=109,
        height=20,
        text="Помилка!",
        text_color="#EF4444",
        fg_color="transparent",
        font=("Lato",24,"bold")
    )
    title_label.place(rely=0.5,relx=0.5,anchor="center")

    #Frame for text error
    frame_text_error = ctk.CTkFrame(master=frame_container,width=310,height=40,fg_color="transparent")
    frame_text_error.place(rely=0.380,relx=0.050)

    #Label for text error
    title_label = ctk.CTkLabel(master=frame_text_error,
        width=310,
        height=20,
        text="Неправильний логін або пароль",
        text_color="#000000",
        fg_color="transparent",
        font=("Lato",20,"normal")
    )
    title_label.place(rely=0.5,relx=0.5,anchor="center")

    #Frame for button 
    frame_button = ctk.CTkFrame(master=frame_container,width=270,height=60,fg_color="transparent")
    frame_button.place(rely=0.800,relx=0.670,anchor="center")

    #Entry login
    button_try_again = ctk.CTkButton(master=frame_button,
        width=250,
        height=50,
        corner_radius=25,
        text="Спробувати ще раз",
        fg_color="#00BFFF",
        text_color="#FFFFFF", 
        font=("Lato",20,"bold"),
        hover_color="#28AAE2",
        command=lambda:win_error.destroy()


    )
    button_try_again.place(rely=0.5,relx=0.5,anchor="center")

# app = ctk.CTk()
# app.geometry("1280x800")
# app.title("Авторизація")
# error_window(app)

# app.mainloop()
# if __name__ == "__main__":
#     error_win_errordow()