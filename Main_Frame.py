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

    #Frame for type category
    frame_type_category = ctk.CTkFrame(master=frame_top_widget,width=200,height=90,fg_color="transparent")
    frame_type_category.place(x=8,y=16)
    frame_type_category.propagate(False)

    #Label category
    label_category = ctk.CTkLabel(   
        master=frame_type_category,  
        text="Тип категорії", 
        width=10, 
        height=1, 
        corner_radius=8, 
        fg_color="transparent", 
        text_color="#FFFFFF", 
        font=("Lato", 24, "bold")
    )
    label_category.grid(row=0,column=0,padx=0)

    category = ["CPU","GPU","Motherboard"] #test data

    #Combobox type category
    combobox_category = ctk.CTkComboBox(
        master=frame_type_category,
        width=153,
        height=25,  
        corner_radius=5, 
        text_color="#000000", 
        font=("Lato", 16, "bold"),
        fg_color="#FFFFFF",
        button_color="#FFFFFF",
        border_color="#FFFFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#000000",
        dropdown_font=("Lato", 14, "normal"),
        dropdown_hover_color="#E5E5E5",
        values=category
    )
    combobox_category.grid(row=1,column=0,padx=(25,0), pady=(19,0))

     #Frame for variable sort
    frame_var_sort = ctk.CTkFrame(master=frame_top_widget,width=200,height=90,fg_color="transparent")
    frame_var_sort.place(x=190,y=16)
    frame_var_sort.propagate(False)

    #Label category
    label_sort = ctk.CTkLabel(   
        master=frame_var_sort,  
        text="Сортування", 
        width=10, 
        height=1, 
        corner_radius=8, 
        fg_color="transparent", 
        text_color="#FFFFFF", 
        font=("Lato", 24, "bold")
    )
    label_sort.grid(row=0,column=0,padx=0)

    sort = ["Від дешевих до дорогих", "Від дорогих до дешевих"] #test data

    #Combobox for sort
    combobox_sort = ctk.CTkComboBox(
        master=frame_var_sort,
        width=231,
        height=25,  
        corner_radius=5, 
        text_color="#000000", 
        font=("Lato", 16, "bold"),
        fg_color="#FFFFFF",
        button_color="#FFFFFF",
        border_color="#FFFFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#000000",
        dropdown_font=("Lato", 14, "normal"),
        dropdown_hover_color="#E5E5E5",
        values=sort
    )
    combobox_sort.grid(row=1,column=0,padx=(90,0), pady=(19,0))

    # Frame for search (це буде сірий фон)
    frame_search = ctk.CTkFrame(
        master=frame_top_widget,
        width=480,
        height=65,
        fg_color="transparent",
        bg_color="#D9D9D9"
    )
    frame_search.pack(anchor="center", pady=25, padx=(150, 0))
    frame_search.pack_propagate(False)

    # Entry for search
    entry_search = ctk.CTkEntry(
        master=frame_search,
        height=60,
        width=470,
        placeholder_text="Пошук за назвою",
        placeholder_text_color="#FFFFFF",
        text_color="#000000",
        font=("Lato", 20, "bold"),
        fg_color="#D9D9D9", 
        bg_color="transparent",
        border_width=0,
        corner_radius=27
    )
    entry_search.grid(row=0,column=0)

    # Button for search
    button_search = ctk.CTkButton(
        master=frame_search,
        width=40,
        height=40,
        image=ctk.CTkImage(
            light_image=Image.open("images/search.png"),
            size=(30, 30)
        ),
        text="",
        fg_color="#D9D9D9",
        bg_color="#D9D9D9",
        hover_color="#BFBFBF",
        corner_radius=20
    )
    button_search.place(relx=0.90, rely=0.5, anchor="center")

if __name__ == "__main__":
    APP = ctk.CTk()
    Main_window(app = APP)
    APP.mainloop()