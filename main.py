import customtkinter as ctk
from Authorize import *
from error_login import *




def main():
    APP = ctk.CTk()
    APP.geometry("1280x800")
    APP.title("Авторизація")
    Authorize_window(APP)
    APP.configure(fg_color="#00BFFF")
    APP.after(0, lambda: APP.state("zoomed"))
    APP.mainloop()


if __name__ == "__main__":
    main()
    