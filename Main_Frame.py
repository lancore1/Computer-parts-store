from PIL import Image
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from DB_connector import CONNECT





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


    #Function who sort data in table
    def sort_by_cost(event=None) -> None: 
        choose = combobox_sort.get()
        tree_list = [tree_table.item(row)["values"] for row in tree_table.get_children()] #the same as the one below, 2 options
        # for row in tree_table.get_children():
        #     tree_list.append(tree_table.item(row)["values"])
        #     print(tree_table.item(row)["values"])
        
        print(tree_list)
        if choose == "Від дешевих до дорогих":
            tree_list.sort(key=lambda item: float(item[-1]))
        if choose == "Від дорогих до дешевих":
            tree_list.sort(key=lambda item: float(item[-1]),reverse=True)

        for row in tree_table.get_children():
            tree_table.delete(row)

        for row in tuple(tree_list):
            tree_table.insert("", "end", values=row)
             

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
        values=["Від дешевих до дорогих", "Від дорогих до дешевих"],
        command=sort_by_cost
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
        font=("Lato", 20, "bold")
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


    # Frame table for product
    frame_table = ctk.CTkFrame(master=app, fg_color="transparent", border_width=1)
    frame_table.pack(side="right", padx=(220,0),pady=(110,0),fill="both", expand=True)
    
    # Label for table
    columns = ("id", "name", "model","specs","category","vendor","supplier","available_quantity","cost")
    scrollbar_y = ctk.CTkScrollbar(frame_table, orientation="vertical")
    scrollbar_y.pack(side="right", fill="y")
    
    # Table for product
    tree_table = ttk.Treeview(master=frame_table,columns=columns, show="headings",xscrollcommand=scrollbar_y.set)
    tree_table.heading("id", text="№")
    tree_table.heading("name", text="Назва")
    tree_table.heading("model", text="Модель"),
    tree_table.heading("specs", text="Характеристики"),
    tree_table.heading("category", text="Тип категорії"),
    tree_table.heading("vendor", text="Виробник"),
    tree_table.heading("supplier", text="Постачальник"),
    tree_table.heading("available_quantity", text="В наявності"),
    tree_table.heading("cost", text="Ціна товару")
    tree_table.pack(expand=True,fill="both",padx=(5,5),pady=(5,5))


    # Style for table
    style = ttk.Style()
    style.theme_use("clam")  
    style.configure("Treeview", font=("Lato", 13,"normal"))       
    style.configure("Treeview.Heading",  font=("Lato", 16,"bold"))  

    # Wigth
    tree_table.column("id", width=40)  
    tree_table.column("name", width=230)  
    tree_table.column("model", width=120)  
    tree_table.column("specs", width=450)  
    tree_table.column("vendor", width=120)  
    tree_table.column("category", width=175)  
    tree_table.column("available_quantity", width=150)  
    tree_table.column("cost", width=150)  


    # Query for data in table
    cursor_tab = CONNECT.cursor()
    # Big Query
    query_tab = """
    SELECT 
        p.product_id,
        p.product_name,
        p.product_model,
        GROUP_CONCAT(DISTINCT ps.productSpec_value SEPARATOR '/'),
        c.category_name,
        v.vendor_name,
        supp.supplier_name,
        p.product_quantity,
        p.product_price
    FROM product p
    JOIN product_specification ps ON p.product_id = ps.product_id
    JOIN category_specification cs ON cs.categorySpec_id = ps.categorySpec_id
    JOIN category c ON c.category_id = cs.category_id
    JOIN vendor v USING(vendor_id)
    JOIN supplier_product sp ON sp.product_id=p.product_id
    JOIN supply suppl ON suppl.supply_id=sp.supply_id
    JOIN supplier supp ON suppl.supplier_id=supp.supplier_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.product_model,
        c.category_name,
        v.vendor_name,
        supp.supplier_name,
        p.product_quantity,
        p.product_price; 
    """
    cursor_tab.execute(query_tab) # exucutes an SQL query
    response_tab = cursor_tab.fetchall() # converts the response into a list of tuples
    
    # Add data in table by row
    for row in response_tab:
        tree_table.insert("", "end", values=row)


    
if __name__ == "__main__":
    APP = ctk.CTk()
    Main_window(app = APP)
    APP.mainloop()