from PIL import Image
import customtkinter as ctk
from DB_connector import CONNECT
from globalQuery import QUERY_SUPPLIER, QUERY_VENDOR 
import global_state 


def add_elem_to_adaptive_frame(cpu_frame: ctk.CTkFrame,
    gpu_frame: ctk.CTkFrame, mb_frame: ctk.CTkFrame, show_frame: ctk.CTkFrame) -> None:
    # Hide all frame
    cpu_frame.pack_forget()
    gpu_frame.pack_forget()
    mb_frame.pack_forget()
    
    # Show the required 
    show_frame.pack(expand=True, fill="both")
    print(f"Showing frame: {show_frame}")


def update_category_fields(choice: str,
                           cpu_frame: ctk.CTkFrame, 
                           gpu_frame: ctk.CTkFrame, 
                           mb_frame: ctk.CTkFrame) -> None:
    if choice == "Процесор":
        add_elem_to_adaptive_frame(cpu_frame, gpu_frame, mb_frame, cpu_frame)
    elif choice == "Відеокарта":
        add_elem_to_adaptive_frame(cpu_frame, gpu_frame, mb_frame, gpu_frame)
    elif choice == "Материнська плата":
        add_elem_to_adaptive_frame(cpu_frame, gpu_frame, mb_frame, mb_frame)
    
    print(f"Updated to: {choice}")


def get_supplier_list() -> list[str]:
    cursor = CONNECT.cursor()
    cursor.execute(QUERY_SUPPLIER)

    suppliers = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return suppliers


def get_vendor_list() -> list[str]:
    cursor = CONNECT.cursor()
    cursor.execute(QUERY_VENDOR)

    vendors = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return vendors

def get_back(APP) -> None:
    import Main_Frame 
    try:
        for widget in APP.winfo_children():
            widget.destroy()
        Main_Frame.Main_window(app=APP)
    except Exception as e:
        print(f"Error: {e}")


def Create_product_window(*, app: ctk.CTk) -> None:
    app.geometry("1920x1080")
    app.title("Створення нового товару")
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
        fg_color="#C3B1E1",
        hover_color="#A589D1",
        text_color="#FFFFFF", 
        font=("Lato", 14, "bold"),
        compound="right",
        command=lambda:get_back(APP=app)
    )
    return_button.pack(side="left")

    # Frame for user info
    frame_user = ctk.CTkFrame(master=frame_top_widget,width=200,height=65,fg_color="transparent")
    frame_user.place(relx=0.98, y=30, anchor="ne")
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
    try:
        user_image = ctk.CTkImage(
            light_image=Image.open("images/image_title_reverse.png"),
            dark_image=Image.open("images/image_title_reverse.png"),
            size=(50,50)
        )
        label_user_image = ctk.CTkLabel(master=frame_user, image=user_image, text="")
        label_user_image.grid(row=0, column=1, padx=10)
    except:
        pass

    #Frame for main label
    frame_label = ctk.CTkFrame(master=app,width=506,height=100,fg_color="transparent")
    frame_label.pack(anchor="center",pady=(115,0))

    # text for label
    label_text = ctk.CTkLabel(master=frame_label,
        width=506,
        height=100,
        text="СТВОРЕННЯ НОВОГО ТОВАРУ",
        text_color="#000000",
        font=("Lato", 32, "bold")
    )
    label_text.pack(anchor="center")


    #Frame for supply product CONTAINER
    frame_supply = ctk.CTkFrame(master=app,width=1920,fg_color="transparent")
    frame_supply.pack(fill="both",expand=True)

    # --- LEFT SIDE: NON ADAPTIVE ---
    frame_for_non_adaptive_element = ctk.CTkFrame(master=frame_supply,width=500,height=700,fg_color="transparent")
    frame_for_non_adaptive_element.pack(side="left", anchor="nw", padx=(100,50))


    #Frame for combobox from category
    frame_type_category = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_type_category.grid(row=0, column=0,sticky="w")

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
        values=["Процесор","Відеокарта", "Материнська плата", ]
    )
    combobox_category.grid(row=1,column=0)
    combobox_category.set("")

    #Frame for combobox from vendor
    frame_vendor = ctk.CTkFrame(master=frame_for_non_adaptive_element,fg_color="transparent")
    frame_vendor.grid(row=2, column=0, padx=0,pady=(5, 10), sticky="w")

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
        values=get_vendor_list()
    )
    combobox_vendor.grid(row=1,column=0)
    combobox_vendor.set("")

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

    #Frame for product name (Model)
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

    # --- RIGHT SIDE: ADAPTIVE FRAME ---
    
    frame_for_adaptive_element = ctk.CTkFrame(master=frame_supply, width=500, height=700, fg_color="transparent")
    frame_for_adaptive_element.pack(side="left", anchor="nw", padx=350, pady=0)
    frame_for_adaptive_element.pack_propagate(False)
    
    # Header Label for Adaptive Frame
    label_adaptive_header = ctk.CTkLabel(
        master=frame_for_adaptive_element,
        text="Оберіть значення характеристик\nтовару з перелічених:",
        text_color="#000000",
        font=("Lato", 16, "bold"),
        justify="center"
    )
    label_adaptive_header.pack(pady=(0, 20), anchor="center")

    # Inner container for the fields
    frame_adaptive_content = ctk.CTkFrame(master=frame_for_adaptive_element,fg_color="transparent")
    frame_adaptive_content.pack(fill="both", expand=True)

    cpu_frame = ctk.CTkFrame(master=frame_adaptive_content, fg_color="transparent")

    # Cores
    lbl_cores = ctk.CTkLabel(cpu_frame, text="Кількість ядер", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_cores.grid(row=0, column=0, sticky="w", pady=(0, 4))

    cpu_cores = ctk.CTkComboBox(cpu_frame, values=["2", "4", "6", "8", "12", "16","20","24","32"],
                                width=170, height=35, corner_radius=8,
                                border_color="#00BFFF", button_color="#00BFFF",
                                text_color="#000000", fg_color="#FFFFFF",
                                font=("Lato", 16), dropdown_font=("Lato", 14))
    cpu_cores.grid(row=1, column=0, pady=(0, 12), sticky="w")

    # Threads
    lbl_threads = ctk.CTkLabel(cpu_frame, text="Кількість потоків", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_threads.grid(row=2, column=0, sticky="w", pady=(0, 4))

    cpu_threads = ctk.CTkComboBox(cpu_frame, values=["4", "8","10","12", "16", "24", "32"],
                                width=170, height=35, corner_radius=8,
                                border_color="#00BFFF", button_color="#00BFFF",
                                text_color="#000000", fg_color="#FFFFFF",
                                font=("Lato", 16), dropdown_font=("Lato", 14))
    cpu_threads.grid(row=3, column=0, pady=(0, 12), sticky="w")

    # CPU speed: from -> to
    lbl_freq = ctk.CTkLabel(cpu_frame, text="Тактова частота (GHz)", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_freq.grid(row=4, column=0, sticky="w", pady=(0, 4))

    cpu_freq_from = ctk.CTkEntry(cpu_frame, placeholder_text="Від",
                                width=140, height=35, corner_radius=8,
                                border_width=2, border_color="#00BFFF",
                                text_color="#000000", fg_color="transparent",
                                font=("Lato", 16), placeholder_text_color="#555555")
    cpu_freq_from.grid(row=5, column=0, padx=(0, 10), pady=(0, 12), sticky="w")

    cpu_freq_to = ctk.CTkEntry(cpu_frame, placeholder_text="До",
                            width=140, height=35, corner_radius=8,
                            border_width=2, border_color="#00BFFF",
                            text_color="#000000", fg_color="transparent",
                            font=("Lato", 16), placeholder_text_color="#555555")
    cpu_freq_to.grid(row=5, column=1, padx=(0, 5), pady=(0, 12), sticky="w")

    # Socket
    lbl_socket = ctk.CTkLabel(cpu_frame, text="Сокет", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_socket.grid(row=6, column=0, sticky="w", pady=(0, 4))

    cpu_socket = ctk.CTkComboBox(cpu_frame, values=["AM5", "AM4", "LGA1851","LGA1700"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    cpu_socket.grid(row=7, column=0, pady=(0, 12), sticky="w")

    # Cache L3
    lbl_cache = ctk.CTkLabel(cpu_frame, text="Кеш L3", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_cache.grid(row=8, column=0, sticky="w", pady=(0, 4))

    cpu_cache = ctk.CTkComboBox(cpu_frame, values=["8", "16", "32", "64"],
                                width=170, height=35, corner_radius=8,
                                border_color="#00BFFF", button_color="#00BFFF",
                                text_color="#000000", fg_color="#FFFFFF",
                                font=("Lato", 16), dropdown_font=("Lato", 14))
    cpu_cache.grid(row=9, column=0, pady=(0, 12), sticky="w")


    gpu_frame = ctk.CTkFrame(master=frame_adaptive_content, fg_color="transparent")

    # Size of VRAM
    lbl_vram = ctk.CTkLabel(gpu_frame, text="Обсяг відеопам’яті", text_color="#000000", 
                font=("Lato", 16, "bold"))
    lbl_vram.grid(row=0, column=0, sticky="w", pady=4, padx=(0, 20))
    gpu_vram_entry = ctk.CTkComboBox(gpu_frame, values=["2", "4", "6","8","10","12","16","24","32"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    gpu_vram_entry.grid(row=1, column=0, pady=4,sticky="w")

    # GPU speed
    lbl_gpu_freq = ctk.CTkLabel(gpu_frame, text="Частота GPU", text_color="#000000", 
                font=("Lato", 16, "bold"))
    lbl_gpu_freq.grid(row=2, column=0, sticky="w", pady=4)
    gpu_freq_entry = ctk.CTkEntry(gpu_frame, placeholder_text="напр. 2.5 GHz", 
                                width=275, height=35, corner_radius=10, border_width=2, 
                                border_color="#00BFFF", text_color="#000000", fg_color="transparent", 
                                font=("Lato", 16), placeholder_text_color="#555555")
    gpu_freq_entry.grid(row=3, column=0, pady=4)

    # Technology
    lbl_tech = ctk.CTkLabel(gpu_frame, text="Технології", text_color="#000000", 
                font=("Lato", 16, "bold"))
    lbl_tech.grid(row=4, column=0, sticky="w", pady=4)
    gpu_tech_entry = ctk.CTkEntry(gpu_frame, placeholder_text="напр. DLSS 3.0, Ray Tracing", 
                                width=275, height=35, corner_radius=10, border_width=2, 
                                border_color="#00BFFF", text_color="#000000", fg_color="transparent", 
                                font=("Lato", 16), placeholder_text_color="#555555")
    gpu_tech_entry.grid(row=5, column=0, pady=4)

    # Інтерфейси
    lbl_int = ctk.CTkLabel(gpu_frame, text="Інтерфейси", text_color="#000000", 
                font=("Lato", 16, "bold"))
    lbl_int.grid(row=6, column=0, sticky="w", pady=4)
    gpu_int_entry = ctk.CTkEntry(gpu_frame, placeholder_text="напр. HDMI 2.1, DP 1.4", 
                                width=275, height=35, corner_radius=10, border_width=2, 
                                border_color="#00BFFF", text_color="#000000", fg_color="transparent", 
                                font=("Lato", 16), placeholder_text_color="#555555")
    gpu_int_entry.grid(row=7, column=0, pady=4)

    # TDP
    lbl_watt = ctk.CTkLabel(gpu_frame, text="Енергоспоживання", text_color="#000000", 
                font=("Lato", 16, "bold"))
    lbl_watt.grid(row=8, column=0, sticky="w", pady=4)
    gpu_tdp_entry = ctk.CTkEntry(gpu_frame, placeholder_text="напр. 280 W", 
                                width=275, height=35, corner_radius=10, border_width=2, 
                                border_color="#00BFFF", text_color="#000000", fg_color="transparent", 
                                font=("Lato", 16), placeholder_text_color="#555555")
    gpu_tdp_entry.grid(row=9, column=0, pady=4)


    mb_frame = ctk.CTkFrame(master=frame_adaptive_content, fg_color="transparent")

    # Socket
    lbl_mb_socket = ctk.CTkLabel(mb_frame, text="Сокет", text_color="#000000",
                font=("Lato", 18, "bold"))
    lbl_mb_socket.grid(row=0, column=0, sticky="w", pady=(0, 4))
    

    mb_socket = ctk.CTkComboBox(mb_frame, values=["AM5", "AM4", "LGA1851","LGA1700"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    mb_socket.grid(row=1, column=0, pady=(0, 12), sticky="w")

    # Chipset
    lbl_chipset = ctk.CTkLabel(mb_frame, text="Чипсет", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_chipset.grid(row=2, column=0, sticky="w", pady=(0, 4))

    mb_chipset = ctk.CTkEntry(mb_frame, placeholder_text="Чипсет",
                width=275, height=35, corner_radius=10,
                border_width=2, border_color="#00BFFF",
                text_color="#000000", fg_color="transparent",
                font=("Lato", 16),
                placeholder_text_color="#555555")
    mb_chipset.grid(row=3, column=0, pady=(0, 12), sticky="w")

    # Slots of RAM
    lbl_slots = ctk.CTkLabel(mb_frame, text="Кількість слотів ОЗП", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_slots.grid(row=4, column=0, sticky="w", pady=(0, 4))

    mb_slots = ctk.CTkComboBox(mb_frame, values=["2", "4", "8"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    mb_slots.grid(row=5, column=0, pady=(0, 12), sticky="w")

    # Formfactor
    lbl_form_factor = ctk.CTkLabel(mb_frame, text="Формфактор", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_form_factor.grid(row=6, column=0, sticky="w", pady=(0, 4))

    mb_form_factor = ctk.CTkComboBox(mb_frame, values=["ATX", "Micro-ATX", "Mini-ITX","E-ATX"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    mb_form_factor.grid(row=7, column=0, pady=(0, 12), sticky="w")

    # WIFI
    lbl_wifi = ctk.CTkLabel(mb_frame, text="Підтримка Wi-Fi", text_color="#000000",
                font=("Lato", 16, "bold"))
    lbl_wifi.grid(row=8, column=0, sticky="w", pady=(0, 4))

    mb_wifi = ctk.CTkComboBox(mb_frame, values=["Так", "Ні"],
                    width=170, height=35, corner_radius=8,
                    border_color="#00BFFF", button_color="#00BFFF",
                    text_color="#000000", fg_color="#FFFFFF",
                    font=("Lato", 16),
                    dropdown_font=("Lato", 14))
    mb_wifi.grid(row=9, column=0, pady=(0, 12), sticky="w")


    def create_product(category: str) -> None:
        from message import message_window
        cursor = None
        try:
            cursor = CONNECT.cursor()
            
            # Check required entry
            if (not entry_name_product.get() or not entry_name_model.get()):
                message_window(app, "Помилка!", "Заповніть усі поля!")
                return

            # Start transaction
            if not CONNECT.in_transaction:
                CONNECT.start_transaction()
            

            if category == "Процесор":
                clock_speed_cpu = f"{cpu_freq_from.get()}-{cpu_freq_to.get()}"
                # Check required entry
                if (not cpu_cores.get() or 
                    not cpu_threads.get() or 
                    not cpu_freq_from.get() or
                    not cpu_freq_to.get() or
                    not cpu_socket.get() or 
                    not cpu_cache.get()):
                    message_window(app, "Помилка!", "Заповніть характеристики")
                    return
                cursor.callproc('CreateCPU', (
                    global_state.current_employee_login,
                    category,
                    combobox_vendor.get(),
                    entry_name_product.get(),
                    entry_name_model.get(),
                    cpu_cores.get(),
                    cpu_threads.get(),
                    clock_speed_cpu,
                    cpu_socket.get(),
                    cpu_cache.get()
                ))
                
            elif category == "Відеокарта":
                # Check required entry
                if (not gpu_vram_entry.get() or 
                    not gpu_freq_entry.get() or 
                    not gpu_tech_entry.get() or 
                    not gpu_int_entry.get() or 
                    not gpu_tdp_entry.get()):
                    message_window(app, "Помилка!", "Заповніть характеристики!")
                    return

                cursor.callproc('CreateGPU', (
                    global_state.current_employee_login,
                    category,
                    combobox_vendor.get(),
                    entry_name_product.get(),
                    entry_name_model.get(),
                    gpu_vram_entry.get(),
                    gpu_freq_entry.get(),
                    gpu_tech_entry.get(),
                    gpu_int_entry.get(),
                    gpu_tdp_entry.get()
                ))
                
            elif category == "Материнська плата":
                # Check required entry
                if (not mb_socket.get() or 
                    not mb_chipset.get() or 
                    not mb_slots.get() or 
                    not mb_form_factor.get() or 
                    not mb_wifi.get()):
                    message_window(app, "Помилка!", "Заповніть характеристики!")
                    return
                cursor.callproc('CreateMotherboard', (
                    global_state.current_employee_login,
                    category,
                    combobox_vendor.get(),
                    entry_name_product.get(),
                    entry_name_model.get(),
                    mb_socket.get(),
                    mb_chipset.get(),
                    mb_slots.get(),
                    mb_form_factor.get(),
                    mb_wifi.get()
                ))
            else:
                return
            
            # Commit transaction
            CONNECT.commit()
            print(f"Товар '{entry_name_product.get()}' успішно додано!")
            message_window(app, "Успіх!", f"Товар {entry_name_product.get()} успішно додано!")
            
            # Очистка полів після успішного додавання
            entry_name_product.delete(0, 'end')
            entry_name_model.delete(0, 'end')
            
        except Exception as e:
            # Rollback
            try:
                CONNECT.rollback()
            except:
                pass
            print(f"Помилка при додаванні товару: {e}")
            message_window(app, "Помилка!", f"Такий товар вже існує!")
            
        finally:
            # Close cursor
            if cursor:
                try:
                    cursor.close()
                except:
                    pass


    
    # Button for add prod to DB
    frame_button_add = ctk.CTkFrame(master=frame_supply,fg_color="transparent",border_width=1)
    frame_button_add.place(
    relx=0.5,
    rely=1.0,
    anchor="s",   
    y=-20)

    button_add = ctk.CTkButton(master=frame_button_add,        
        text="ДОДАТИ ТОВАР У БД",
        width=230, 
        height=68,
        corner_radius=5,
        fg_color="#C3B1E1",
        hover_color="#A589D1",
        font=("Lato", 24, "bold"),
        text_color="#FFFFFF",
        command=lambda: create_product(combobox_category.get())
    )
    button_add.pack(fill="both")



    combobox_category.configure(command=lambda x:update_category_fields(combobox_category.get(),cpu_frame, gpu_frame, mb_frame))
 
if __name__ == "__main__":
    APP = ctk.CTk()
    Create_product_window(app=APP)
    APP.mainloop()

