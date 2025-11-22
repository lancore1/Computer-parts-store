from PIL import Image
import customtkinter as ctk


def Main_window(*, app: ctk.CTk) -> None:
    app.geometry("1920x1080")
    app.title("Головне меню")
    app.configure(fg_color="#FFFFFF")

    
    #Frame left widget
    frame_left_widget = ctk.CTkFrame(master=app,
        width=220,
        height=965,
        corner_radius=0,
        fg_color="#00BFFF"
    )
    frame_left_widget.place(x=0, y=115,relheight=0.893)
    frame_left_widget.propagate(False)

    #Frame top widget
    frame_top_widget = ctk.CTkFrame(master=app,
        width=1920,
        height=115,
        corner_radius=0,
        fg_color="#00BFFF"
    )
    frame_top_widget.place(x=0, y=0,relwidth=1)
    frame_top_widget.propagate(False)





if __name__ == "__main__":
    APP = ctk.CTk()
    Main_window(app = APP)
    APP.mainloop()