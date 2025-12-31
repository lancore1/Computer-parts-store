from PIL import Image
from tkinter import ttk
import customtkinter as ctk
from DB_connector import CONNECT
import global_state # for get login 
import globalQuery 


current_products = []  # stores current table data for filtering


# Function who sort data in table by cost
def sort_by_cost(combobox, tree) -> None: 
    # get choose from combobox
    choose = combobox.get()

    # get all data from table as list
    tree_list = [tree.item(row)["values"] for row in tree.get_children()]

    # sort data by cost
    if choose == "Від дешевих до дорогих":
        tree_list.sort(key=lambda item: float(item[-1]))
    if choose == "Від дорогих до дешевих":
        tree_list.sort(key=lambda item: float(item[-1]), reverse=True)

    # remove all data in table, work faster than delete by row in for
    tree.delete(*tree.get_children())

    # populate table with sorted data
    for row in tuple(tree_list):
        tree.insert("", "end", values=row)


# Function who filtered data in table by type category
def filter_by_type(combobox, tree) -> None:
    global current_products
    # get choose
    choose = combobox.get()

    # remove all data in table, work faster than delete by row in for 
    tree.delete(*tree.get_children())

    # saved data who filtered 
    filtered = []

    # save the data source for the table as current data 
    sourse = current_products

    if choose == "Усі":
        # we copy the current data, keeping in mind that current_products contains all the default data.
        filtered = current_products.copy()

    if choose == "Процесор":
        filtered = [item for item in sourse if item[4] == "Процесор"]

    if choose == "Відеокарта":
        filtered = [item for item in sourse if item[4] == "Відеокарта"]

    if choose == "Материнська плата":
        filtered = [item for item in sourse if item[4] == "Материнська плата"]

    # populate table with filtered data
    tree.delete(*tree.get_children())
    for row in tuple(filtered):
        tree.insert("", "end", values=row)


# Function who filtere data by entered text from entry search
def search_by_entry(entry_search, tree) -> None:
    global current_products

    cursor_tab = CONNECT.cursor()
    cursor_tab.execute(globalQuery.QUERY_TAB) # exucutes an SQL query
    all_products = cursor_tab.fetchall() #list of tuples

    cursor_tab.close()
    CONNECT.commit()

    text = entry_search.get().lower().strip()

    # clear table 
    tree.delete(*tree.get_children())

    filtered_list = []

    # if text is empty
    if text == "":
        current_products = all_products.copy()
    else:
        # if text not empty, we save copy in current_products from filtered_list
        for item in all_products:
            if text in item[1].lower():
                filtered_list.append(item)
        current_products = filtered_list.copy()

    # populate table with current_products
    tree.delete(*tree.get_children())
    for row in tuple(current_products):
        tree.insert("", "end", values=row)


#Function who add data from current_products to cart
def add_data_to_card(APP,entry_id: ctk.CTkEntry, entry_quantity: ctk.CTkEntry, table: ttk.Treeview) -> None:
    from message import message_window
    global current_products
    product_id = entry_id.get()
    quantity = entry_quantity.get()

    try:
        # converts product_id,quantity because ctk.CTkEntry.get() return "str" not number
        product_id = int(product_id)
        quantity = int(quantity)

        product_data = None
        for item in current_products:
            if int(item[0]) == product_id:
                product_data = item
                break

        if product_data is None:
            message_window(APP,"Помилка!","Товару з таким номером не існує!")
            print("Товар з таким ID не знайдено в current_products")
            return

        max_quantity = int(product_data[7])  # available quantity in stock for a specific product_id


        # checking the product for duplicates
        for iid in table.get_children(): # iid have a unique id of row in table 
            row = table.item(iid)["values"]
            print(row)

            if int(row[0]) == product_id:  # if product exists
                price = float(row[4])

                new_quantity = int(row[3]) + quantity

                # if new count biggest than max, we don't do anymore
                if new_quantity > max_quantity:
                    message_window(APP,"Помилка!","Немає такої кількості товару у наявності!")
                    print("Немає такої кількості товару у наявності!")
                    return
                if new_quantity > 6:
                    price = float(price*0.93)

                new_sum = price * new_quantity
                new_row = [row[0], row[1], row[2], new_quantity, f"{price:.2f}",f"{new_sum:.2f}"]

                table.delete(iid)
                table.insert("", "end", values=new_row)
                return

        #  if the product is not available we search for it in current_products
        for item in current_products:
            if int(item[0]) == product_id:
                if int(item[7]) < quantity:
                    message_window(APP,"Помилка!","Немає такої кількості товару у наявності!")
                    return
                price = float(item[-1])
                if quantity > 6:
                    price = float(price*0.93)
                new_row = [item[0],item[1],item[2],quantity,f"{price:.2f}",f"{price * quantity:.2f}"]

                table.insert("", "end", values=new_row)
                return

        print("Товар з таким ID не знайдено")

    except ValueError:
        print("Помилка: неправильні дані")
    finally:
        entry_id.delete(0, "end")
        entry_quantity.delete(0, "end")


# Function who clear basket
def clear_basket(table:ttk.Treeview) -> None:
    # clear table 
    table.delete(*table.get_children())


# Function who make sale about 
def make_sale(APP,state:ctk.CTkCheckBox,cl_name:ctk.CTkEntry, cl_email:ctk.CTkEntry, cl_phone:ctk.CTkEntry, 
              table:ttk.Treeview, tree_table:ttk.Treeview) -> None:
    from message import message_window
    global current_products

    name = cl_name.get().strip() 
    email = cl_email.get().strip()
    phone = cl_phone.get().strip()
    basket = [table.item(row)["values"] for row in table.get_children()]

    if not name or not email or not phone:
        print("is null")
    if not basket:
        message_window(APP,"Помилка!","Кошик порожній, додайте товар!")
        return
    if state == 1 and (not name or not email or not phone):
        message_window(APP,"Помилка!","Введіть усі необхідні поля!")
        raise Exception("Missing client data")
    
    try:
        cursor_tab = CONNECT.cursor()
        # Start transaction
        CONNECT.start_transaction()
        
        # Create one check for all product
        cursor_tab.execute(f'''
            call create_sale_check(
                '{global_state.current_employee_login}',
                '{name}',
                '{email}',
                '{phone}',
                @check_id
            )
        ''')
        
        # Get id created check
        cursor_tab.execute("SELECT @check_id")
        check_id = cursor_tab.fetchone()[0]
        
        # Add all product to check
        for row in basket:
            curr_prod_id = int(row[0])
            curr_prod_count = int(row[3])
            curr_prod_price = float(row[4])
            
            cursor_tab.execute(f'''
                call add_product_to_check(
                    {check_id},
                    {curr_prod_id},
                    {curr_prod_price},
                    {curr_prod_count}
                )
            ''')
        
        # Save all changes
        CONNECT.commit()
        print(f"Продаж успішно завершено! ID чеку: {check_id}")
        message_window(APP,"Успіх!",f"Продаж успішно завершено! Номер чеку:{check_id}")
    except Exception as e:
        CONNECT.rollback()
        print(f"Помилка: {e}")
        return
    
    # clean all entry
    table.delete(*table.get_children())
    for e in (cl_name, cl_email, cl_phone):
        e.delete(0, "end")
    
    # Update product table
    tree_table.delete(*tree_table.get_children())
    try:
        cursor_tab.execute(globalQuery.QUERY_TAB)
        all_products = cursor_tab.fetchall()
        cursor_tab.close()
        CONNECT.commit()
        current_products.clear()
        for row in all_products:
            tree_table.insert("", "end", values=row)
            current_products.append(row)
    except Exception as e:
        print(f"Помилка оновлення таблиці: {e}")


# Function who get back to Main_frame
def get_back(APP) -> None:
    import Main_Frame 
    try:
        for widget in APP.winfo_children():
            widget.destroy()
        Main_Frame.Main_window(app=APP)
    except Exception as e:
        print(f"Error: {e}")


def get_summary_from_basket(table:ttk.Treeview) -> str:
    total = 0
    basket = [table.item(row)["values"] for row in table.get_children()]
    for row in basket:
        print(row)
        print(row[-1])
        total += float(row[-1])

    return str(round(total,2))


def show_entries(state:int, frame_entries:ctk.CTkFrame) -> None:
    if state == 0:
        frame_entries.pack_forget()
    elif state == 1:
        frame_entries.pack(side="left", fill="both", expand=True)
        
    


def Purchase_window(*, app: ctk.CTk) -> None:
    global current_products

    app.geometry("1920x1080")
    app.title("Оформлення замовлення")
    app.configure(fg_color="#FFFFFF")
    # open app in full screen
    app.after(50, lambda: app.state("zoomed"))

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
        values=["Усі","Процесор","Відеокарта","Материнська плата"],
        command=lambda value: filter_by_type(combobox_category,tree_table)
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
        command=lambda value: sort_by_cost(combobox_sort,tree_table)
    )
    combobox_sort.grid(row=1,column=0,padx=(90,0), pady=(19,0))

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
        corner_radius=20,
        command=lambda: search_by_entry(entry_search,tree_table)

    )
    button_search.place(relx=0.90, rely=0.5, anchor="center")
    # add hotkey for button search on press "ENTER"
    app.bind("<Return>", lambda event: button_search.invoke())


    # Frame for button sale and supply
    retrun_button_frame = ctk.CTkFrame(master=frame_top_widget, width=200, height=65,fg_color="transparent")
    retrun_button_frame.place(relx=0.725, rely=0.5, anchor="w") 

    # Button for sale
    return_button = ctk.CTkButton(
        master=retrun_button_frame,
        text="До головного меню",
        width=115,
        height=39,
        corner_radius=5,
        fg_color="#34D399",
        hover_color="#2ECC71",
        font=("Lato", 14, "bold"),
        compound="right",
        command=lambda:get_back(APP=app) 
    )
    return_button.pack(side="left")


    # Frame for user info
    frame_user = ctk.CTkFrame(master=frame_top_widget,width=200,height=65,fg_color="transparent")
    frame_user.place(x=1380,y=30)
    frame_user.propagate(False)

    # User name
    user_label = ctk.CTkLabel(   
        master=frame_user,  
        text=global_state.curr_user_last_name, 
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


    # =================================================================================
    #                           ГОЛОВНИЙ ФРЕЙМ (RIGHT CONTAINER)
    # =================================================================================
    # Цей фрейм містить ВСІ таблиці та поля вводу праворуч від меню
    frame_right_container = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_right_container.pack(side="right", fill="both", expand=True, padx=(220, 0), pady=(115, 0))


    # ------------------ 1. ТАБЛИЦЯ ТОВАРІВ (Верхня частина) ------------------
    frame_table = ctk.CTkFrame(master=frame_right_container, fg_color="transparent", border_width=1)
    # expand=True дозволяє цій таблиці займати все вільне місце по вертикалі, яке залишиться
    frame_table.pack(side="top", fill="both", expand=True, padx=5, pady=(5, 5))
    
    frame_table.grid_columnconfigure(0, weight=1) 
    frame_table.grid_rowconfigure(0, weight=1)
    
    columns = ("id", "name", "model","specs","category","vendor","supplier","available_quantity","cost")
    titles  = ["№","Назва","Модель","Характеристики","Тип категорії","Виробник","Постачальник","В наявності","Ціна товару"]
    
    tree_table = ttk.Treeview(master=frame_table,columns=columns, show="headings")
    for col, title in zip(columns, titles):
        tree_table.heading(col, text=title)
    
    tree_table.grid(row=0, column=0, sticky="nsew", padx=(5,0), pady=(5,5))
    
    # Scrollbar
    scrollbar_y = ctk.CTkScrollbar(frame_table, orientation="vertical",command=tree_table.yview,height=1)
    scrollbar_y.grid(row=0, column=1, sticky="ns", padx=(0,5), pady=(5,5))
    tree_table.configure(yscrollcommand=scrollbar_y.set)

    # Style
    style = ttk.Style()
    style.theme_use("clam")  
    style.configure("Treeview", font=("Lato", 12,"normal"), rowheight=30)       
    style.configure("Treeview.Heading",  font=("Lato", 16,"bold"))  

    # Wigth
    tree_table.column("id", width=40)  
    tree_table.column("name", width=230)  
    tree_table.column("model", width=120)  
    tree_table.column("specs", width=450)  
    tree_table.column("vendor", width=120)  
    tree_table.column("category", width=175)  
    tree_table.column("available_quantity", width=138)  
    tree_table.column("cost", width=150) 


    # ------------------ 2. ПАНЕЛЬ ДОДАВАННЯ (Між таблицями) ------------------
    frame_controls_add = ctk.CTkFrame(master=frame_right_container, height=68, fg_color="transparent")
    frame_controls_add.pack(side="top", fill="x", padx=5, pady=(0, 5))

    # Entry: ID
    entry_id = ctk.CTkEntry(
        master=frame_controls_add, 
        placeholder_text="Номер товару", 
        width=230, 
        height=68,
        fg_color="transparent",
        border_color="#00BFFF",
        border_width= 2,
        corner_radius=10,
        font=("Lato", 16),
        placeholder_text_color="#7F7F7F",
        text_color="#000000"
    )
    entry_id.pack(side="left", padx=(5, 10))

    # Entry: Quantity
    entry_quantity = ctk.CTkEntry(
        master=frame_controls_add, 
        placeholder_text="Кількість", 
        width=230, 
        height=68,
        fg_color="transparent",
        border_color="#00BFFF",
        border_width= 2,
        corner_radius=10,
        font=("Lato", 16),
        placeholder_text_color="#7F7F7F",
        text_color="#000000",
    )
    entry_quantity.pack(side="left", padx=(0, 10))

    # Button: Add to Cart
    button_add = ctk.CTkButton(
        master=frame_controls_add,
        text="Додати",
        width=230,
        height=68,
        corner_radius=5,
        fg_color="#00BFFF",
        hover_color="#009BCF",
        font=("Lato", 24, "bold"),
        text_color="#FFFFFF",
        command=lambda:on_add_click()
    )
    button_add.pack(side="left")

    # Button who clear basket
    button_clear_basket = ctk.CTkButton(
        master=frame_controls_add,
        text="Очистити кошик",
        width=193,
        height=39,
        corner_radius=5,
        fg_color="#FF3C00",
        hover_color="#E32600",
        font=("Lato", 16, "bold"),
        text_color="#FFFFFF",
        command=lambda:on_clear_click()
    )
    button_clear_basket.pack(side="right")


    # ------------------ 3. ТАБЛИЦЯ КОШИКА (Нижня таблиця) ------------------
    frame_cart = ctk.CTkFrame(master=frame_right_container, fg_color="transparent", border_width=1, height=200)
    frame_cart.pack(side="top", fill="x", expand=False, padx=5, pady=(0, 5))
    
    frame_cart.grid_columnconfigure(0, weight=1)
    frame_cart.grid_rowconfigure(0, weight=1)

    # Columns for the cart
    cart_columns = ("id", "name", "model", "quantity", "price", "total")
    cart_titles = ["№", "Назва", "Модель", "Кількість", "Ціна", "Сума"]
    # Table for cart 
    tree_cart = ttk.Treeview(master=frame_cart, columns=cart_columns, show="headings", height=6)
    
    for col, title in zip(cart_columns, cart_titles):
        tree_cart.heading(col, text=title)

    tree_cart.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=(5, 5))

    # Scrollbar for cart
    scrollbar_cart_y = ctk.CTkScrollbar(frame_cart, orientation="vertical", command=tree_cart.yview)
    scrollbar_cart_y.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=(5, 5))
    
    tree_cart.configure(yscrollcommand=scrollbar_cart_y.set)

    # Width for cart table
    tree_cart.column("id", width=50, anchor="center")
    tree_cart.column("name", width=400)
    tree_cart.column("model", width=200)
    tree_cart.column("quantity", width=100, anchor="center")
    tree_cart.column("price", width=150, anchor="e")
    tree_cart.column("total", width=150, anchor="e")

      
    # ------------------ 4. ПАНЕЛЬ ОФОРМЛЕННЯ (Під кошиком) ------------------
    frame_controls_checkout = ctk.CTkFrame(master=frame_right_container, height=68, fg_color="transparent")
    frame_controls_checkout.pack(side="top", fill="x", padx=5, pady=(0, 20))

    # Frame for checkbox
    frame_check_box_sale = ctk.CTkFrame(
        master=frame_controls_checkout,
        width=160,
        height=68,
        fg_color="transparent"
    )
    frame_check_box_sale.pack(side="left", fill="y", padx=(0, 10))

    # Checkbox for register or authorize client
    checkbox_auth = ctk.CTkCheckBox(
        master=frame_check_box_sale,
        text="Реєстрація/Авторизація клієнта",
        text_color="#000000",
        text_color_disabled="#E90000",
        font=("Lato", 16),
        fg_color="#00BFFF",    
        border_color="#00BFFF",
        border_width=3,
        corner_radius=5,
        hover_color="#0080C0",
        command=lambda:show_entries(checkbox_auth.get(),frame_entries_container)
    )
    checkbox_auth.pack(expand=True, anchor="center") 

    # Frame for button checkout
    frame_button_container = ctk.CTkFrame(
        master=frame_controls_checkout,
        height=68,
        fg_color="transparent"
    )
    frame_button_container.pack(side="right", fill="y", padx=(10, 0))

    button_checkout = ctk.CTkButton(
        master=frame_button_container,
        text="Завершити замовлення",
        width=230,
        height=68,
        corner_radius=5,
        fg_color="#34D399",
        hover_color="#2ECC71",
        font=("Lato", 24, "bold"),
        text_color="#FFFFFF",
        command=lambda:on_sale_click()
    )
    button_checkout.pack(expand=True, anchor="center")


    # Central frame
    frame_entries_container = ctk.CTkFrame(
        master=frame_controls_checkout,
        height=68,
        fg_color="transparent"
    )
    frame_entries_container.pack(side="left", fill="both", expand=True)
    frame_entries_container.pack_forget()
    
    frame_entries_inner = ctk.CTkFrame(master=frame_entries_container, fg_color="transparent")
    frame_entries_inner.pack(expand=True, fill="y")

    # Entry 1: Client Name
    entry_client_name = ctk.CTkEntry(
        master=frame_entries_inner, 
        placeholder_text="ПІБ Клієнта", 
        width=230, 
        height=68,
        fg_color="transparent",
        border_color="#00BFFF",
        border_width=2,
        corner_radius=10,
        font=("Lato", 16),
        placeholder_text_color="#7F7F7F",
        text_color="#000000",
    )
    entry_client_name.pack(side="left", padx=5)

    # Entry 2: Phone
    entry_client_phone = ctk.CTkEntry(
        master=frame_entries_inner, 
        placeholder_text="Номер телефону", 
        width=230, 
        height=68,
        fg_color="transparent",
        border_color="#00BFFF",
        border_width=2,
        corner_radius=10,
        font=("Lato", 16),
        placeholder_text_color="#7F7F7F",
        text_color="#000000",
    )
    entry_client_phone.pack(side="left", padx=5)

    # Entry 3: Additional (Address/Email)
    entry_client_info = ctk.CTkEntry(
        master=frame_entries_inner, 
        placeholder_text="Email", 
        width=230, 
        height=68,
        fg_color="transparent",
        border_color="#00BFFF",
        border_width=2,
        corner_radius=10,
        font=("Lato", 16),
        placeholder_text_color="#7F7F7F",
        text_color="#000000",
    )
    entry_client_info.pack(side="left", padx=5)
        

    # Frame for sum
    frame_sum = ctk.CTkFrame(master=frame_controls_add,width=160,height=45,fg_color="transparent")
    frame_sum.pack(expand=True)
    # Variable for save total sum
    sum_var = ctk.StringVar(value="Загальна сума: 0 ₴")
    # Entry for summary
    label_summary = ctk.CTkLabel(master=frame_sum,textvariable=sum_var,text_color="#000000",font=("Lato", 16, "bold"))
    label_summary.pack(expand=True)


    def on_add_click() -> None:
        add_data_to_card(app, entry_id, entry_quantity, tree_cart)
        total = get_summary_from_basket(tree_cart)
        sum_var.set(f"Загальна сума: {total} ₴")


    def on_clear_click() -> None:
        clear_basket(tree_cart)
        sum_var.set("Загальна сума: 0 ₴")


    def on_sale_click() -> None:
        total = get_summary_from_basket(tree_cart)
        try: 
            make_sale(app, checkbox_auth.get(), entry_client_name, entry_client_info, entry_client_phone, tree_cart, tree_table)
            sum_var.set("Загальна сума: 0 ₴")
        except Exception as e:
            print(f"Продаж скасовано: {e}")
            sum_var.set(f"Загальна сума: {total} ₴")        
            
    
    try:
        # Query for data in table
        cursor_tab = CONNECT.cursor(buffered=True)
        cursor_tab.execute(globalQuery.QUERY_TAB) # exucutes an SQL query
        all_products = cursor_tab.fetchall() # converts the response into a list of tuples
        cursor_tab.close()
        CONNECT.commit()
        # clean our list
        current_products.clear()

        # Add data in table by row
        for row in all_products:
            tree_table.insert("", "end", values=row)
            # DEFAULT value for current_products
            current_products.append(row)
    except:
        print("We have a problem with get data about product in Purchase Frame")

