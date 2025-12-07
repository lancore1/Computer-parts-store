from PIL import Image
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from DB_connector import CONNECT
from Main_Frame import *
import global_state 




def Supply_window(*, app: ctk.CTk) -> None:
    global current_products

    app.geometry("1920x1080")
    app.title("Постачання товару")
    app.configure(fg_color="#FFFFFF")
    # open app in full screen
    app.after(50, lambda: app.state("zoomed"))

   
    #Frame top widget
    frame_top_widget = ctk.CTkFrame(master=app,
        width=1920,
        height=115,
        corner_radius=0,
        fg_color="#00BFFF"
    )
    frame_top_widget.place(x=0, y=0,relwidth=1)
    frame_top_widget.propagate(False)


    # Frame for search 
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
    entry_search.configure(state="disable")


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
    button_search.configure(state="disable")

    # Frame for button sale and supply
    return_button_frame = ctk.CTkFrame(master=frame_top_widget, width=200, height=65,fg_color="transparent")
    return_button_frame.place(relx=0.725, rely=0.5, anchor="w") 

  # Button for supply
    return_button = ctk.CTkButton(
        master=return_button_frame,
        text="До головного меню",
        width=115,
        height=39,
        corner_radius=5,
        fg_color="#FFB030",
        hover_color="#FF9933",
        font=("Lato", 14, "bold"),
        compound="right",
    )
    return_button.pack(side="left")

    # Frame for user info
    frame_user = ctk.CTkFrame(master=frame_top_widget,width=200,height=65,fg_color="transparent")
    frame_user.place(x=1380,y=30)
    frame_user.propagate(False)

    # User name
    user_label = ctk.CTkLabel(   
        master=frame_user,  
        text="Прізвище", 
        width=10, 
        height=1    , 
        fg_color="transparent", 
        text_color="#FFFFFF", 
        font=("Lato", 18, "bold")
    )
    user_label.grid(row=0,column=0,padx=0)

    # User image
    user_image = ctk.CTkImage(
        light_image=Image.open("images/image_title_reverse.png"),
        dark_image=Image.open("images/image_title_reverse.png"),
        size=(50,50)
    )
    label_user_image = ctk.CTkLabel(master=frame_user, image=user_image, text="")
    label_user_image.grid(row=0, column=1, padx=10)

    #Frame for main label
    frame_label = ctk.CTkFrame(master=app,width=506,height=100,fg_color="transparent")
    frame_label.pack(anchor="center",pady=(115,0))

    # text for label
    label_text = ctk.CTkLabel(master=frame_label,
        width=506,
        height=100,
        text="ПОСТАЧАННЯ НОВОГО ТОВАРУ",
        text_color="#000000",
        font=("Lato", 32, "bold")
    )
    label_text.pack(anchor="center")


    #Frame for supply product
    frame_supply = ctk.CTkFrame(master=app,width=1920,fg_color="transparent")
    frame_supply.pack(fill="both",expand=True)
    frame_supply.propagate(False)

    #Frame for static element 
    frame_for_non_adaptive_element = ctk.CTkFrame(master=frame_supply,width=500,height=500,fg_color="transparent")
    frame_for_non_adaptive_element.pack(side="top", anchor="nw",padx=(100,0))
    frame_for_non_adaptive_element.propagate(False)


    #Frame for combobox from supplier
    frame_supplier = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_supplier.grid(row=0, column=0, pady=(5, 10), sticky="w")

    label_supplier = ctk.CTkLabel(
        master=frame_supplier,
        text="ПОСТАЧАЛЬНИК",
        text_color="#000000",
        font=("Lato", 20, "bold")
    )
    label_supplier.grid(row=0,column=0)

    combobox_supplier = ctk.CTkComboBox(
        master=frame_supplier,
        width=153, 
        height=25, 
        corner_radius=5,
        text_color="#000000", font=("Lato", 16, "bold"),
        fg_color="#FFFFFF", button_color="#00BFFF",
        border_color="#00BFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#000000",
        dropdown_font=("Lato", 14),
        dropdown_hover_color="#E5E5E5",
        values=["Усі", "CPU", "GPU", "Motherboard"]
    )
    combobox_supplier.grid(row=1,column=0)


    #Frame for combobox from category
    frame_type_category = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_type_category.grid(row=0, column=1)

    label_category = ctk.CTkLabel(
        master=frame_type_category,
        text="ТИП КАТЕГОРІЇ",
        text_color="#000000",
        font=("Lato", 20, "bold")
    )
    label_category.grid(row=0,column=0)

    combobox_category = ctk.CTkComboBox(
        master=frame_type_category,
        width=153, 
        height=25, 
        corner_radius=5,
        text_color="#000000", font=("Lato", 16, "bold"),
        fg_color="#FFFFFF", button_color="#00BFFF",
        border_color="#00BFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#000000",
        dropdown_font=("Lato", 14),
        dropdown_hover_color="#E5E5E5",
        values=["CPU", "GPU", "Motherboard"]
    )
    combobox_category.grid(row=1,column=0)


    #Frame for combobox from vendor
    frame_vendor = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_vendor.grid(row=2, column=0, padx=7,pady=(5, 10), sticky="w")

    label_vendor = ctk.CTkLabel(
        master=frame_vendor,
        text="ВИРОБНИК",
        text_color="#000000",
        font=("Lato", 20, "bold")
    )
    label_vendor.grid(row=0,column=0)

    combobox_vendor = ctk.CTkComboBox(
        master=frame_vendor,
        width=153, 
        height=25, 
        corner_radius=5,
        text_color="#000000", font=("Lato", 16, "bold"),
        fg_color="#FFFFFF", button_color="#00BFFF",
        border_color="#00BFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#000000",
        dropdown_font=("Lato", 14),
        dropdown_hover_color="#E5E5E5",
        values=["AMD", "Intel", "Asus"]
    )
    combobox_vendor.grid(row=1,column=0)

    #Frame for product name
    frame_product_name = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_product_name.grid(row=3, column=0, pady=(20, 10), sticky="w")

    entry_name_product = ctk.CTkEntry(
        master=frame_product_name,
        width=275, 
        height=50, 
        corner_radius=10,
        fg_color="transparent",
        border_width=2, border_color="#00BFFF",
        placeholder_text="Назва товару",
        placeholder_text_color="#000000",
        text_color="#000000",
        font=("Lato", 16)
    )
    entry_name_product.pack(side="left")

    #Frame for product name
    frame_product_model= ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_product_model.grid(row=4, column=0, pady=(0, 10), sticky="w")

    entry_name_model = ctk.CTkEntry(
        master=frame_product_model,
        width=275, 
        height=50, 
        corner_radius=10,
        fg_color="transparent",
        border_width=2, border_color="#00BFFF",
        placeholder_text="Модель",
        placeholder_text_color="#000000",
        text_color="#000000",
        font=("Lato", 16)
    )
    entry_name_model.pack(side="left")

    #Frame for count of product delivery
    frame_product_quantity= ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_product_quantity.grid(row=5, column=0, pady=(0, 10), sticky="w")

    entry_count_delivery = ctk.CTkEntry(
        master=frame_product_quantity,
        width=275, 
        height=50, 
        corner_radius=10,
        fg_color="transparent",
        border_width=2, border_color="#00BFFF",
        placeholder_text="Кількість постачі, шт",
        placeholder_text_color="#000000",
        text_color="#000000",
        font=("Lato", 16)
    )
    entry_count_delivery.pack(side="left")

    #Frame for delivery sum
    frame_delivery_sum= ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_delivery_sum.grid(row=6, column=0, pady=(0, 10), sticky="w")

    entry_sum_delivery = ctk.CTkEntry(
        master=frame_delivery_sum,
        width=275, 
        height=50, 
        corner_radius=10,
        fg_color="transparent",
        border_width=2, border_color="#00BFFF",
        placeholder_text="Загальна сумма постачі, грн",
        placeholder_text_color="#000000",
        text_color="#000000",
        font=("Lato", 16)
    )
    entry_sum_delivery.pack(side="left")

    #Frame for unit price
    frame_unit_price= ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_unit_price.grid(row=7, column=0, pady=(0, 10), sticky="w")

    entry_unit_price = ctk.CTkEntry(
        master=frame_unit_price,
        width=275, 
        height=50, 
        corner_radius=10,
        fg_color="transparent",
        border_width=2, border_color="#00BFFF",
        placeholder_text="Модель",
        placeholder_text_color="#000000",
        text_color="#000000",
        font=("Lato", 16)
    )
    entry_unit_price.pack(side="left")



   
    
if __name__ == "__main__":
    APP = ctk.CTk()
    Supply_window(app = APP)
    APP.mainloop()






