from PIL import Image
from tkinter import ttk
import customtkinter as ctk
from DB_connector import CONNECT
import global_state # for get login 
from globalQuery import QUERY_SUPPLIER, QUERY_SUPPLY



current_products = []  # stores current table data for filtering

import re

# --- НОВІ ФУНКЦІЇ ДЛЯ СОРТУВАННЯ ТА ЛІВОЇ ПАНЕЛІ ---
def add_clear_button(parent_frame, command):
    btn = ctk.CTkButton(parent_frame, text="Очистити фільтри", 
                        fg_color="#FF3333", hover_color="#CC0000", text_color="white",
                        font=("Lato", 16, "bold"), height=40,
                        command=command) # Викликаємо функцію перезавантаження
    btn.pack(side="bottom", pady=(10, 20), fill="x", padx=20)

def parse_cpu_specs(spec_str):
    try:
        parts = spec_str.split(" / ")
        # 0: "16 ядер" -> 16
        cores = int(re.search(r'\d+', parts[0]).group())
        # 1: "24 потоків" -> 24
        threads = int(re.search(r'\d+', parts[1]).group())
        # 2: "3.4-5.4 Ггц" -> 5.4 (беремо макс частоту для спрощення фільтрації)
        freq_match = re.findall(r'\d+\.\d+', parts[2])
        max_freq = float(freq_match[-1]) if freq_match else 0.0
        # 3: "LGA1700"
        socket = parts[3].strip()
        # 4: "30 Мб" -> 30
        cache = int(re.search(r'\d+', parts[4]).group())
        
        return {
            "cores": cores,
            "threads": threads,
            "freq": max_freq,
            "socket": socket,
            "cache": cache
        }
    except Exception as e:
        print(f"Error parsing specs '{spec_str}': {e}")
        return None

def apply_advanced_cpu_filter(widgets, tree, all_products):
    global current_products
    
    # 1. Зчитуємо значення з віджетів
    try:        
        # Виробник (Vendor) - Checkboxes
        selected_vendors = []
        if widgets['vendor_amd'].get(): selected_vendors.append("AMD")
        if widgets['vendor_intel'].get(): selected_vendors.append("Intel")
        
        # Характеристики CPU
        sel_cores = widgets['cores'].get() # Combobox value or empty
        print(sel_cores)
        sel_threads = widgets['threads'].get()
        
        freq_min = float(widgets['freq_from'].get()) if widgets['freq_from'].get() else 0.0
        freq_max = float(widgets['freq_to'].get()) if widgets['freq_to'].get() else 10.0
        
        cache_min = float(widgets['cache_from'].get()) if widgets['cache_from'].get() else 0
        cache_max = float(widgets['cache_to'].get()) if widgets['cache_to'].get() else 1000
        
        # Сокети
        selected_sockets = []
        for sock_name, var in widgets['sockets'].items():
            if var.get(): selected_sockets.append(sock_name)

    except ValueError:
        # Якщо введено текст замість цифр, ігноруємо фільтрацію або чекаємо виправлення
        return

    filtered_list = []
    
    # 2. Проходимо по всіх товарах і фільтруємо
    for row in all_products:
        # row[4] = Category, row[5] = Vendor, row[8] = Cost, row[3] = Specs
        category = row[4]
        vendor = row[5]
        specs_str = row[3]

        # Базовий фільтр: Категорія має бути Процесор
        if category != "Процесор":
            continue
            
        # Фільтр виробника
        if selected_vendors and (vendor not in selected_vendors):
            continue
            
        # Розширений парсинг характеристик
        specs = parse_cpu_specs(specs_str)
        if not specs:
            continue
            
        # Фільтр ядер (якщо обрано конкретне значення)
        if sel_cores and str(specs['cores']) != sel_cores:
            continue
            
        # Фільтр потоків
        if sel_threads and str(specs['threads']) != sel_threads:
            continue
            
        # Фільтр частоти (попадання в діапазон)
        if not (freq_min <= specs['freq'] <= freq_max):
            continue
            
        # Фільтр кешу
        if not (cache_min <= specs['cache'] <= cache_max):
            continue
            
        # Фільтр сокету
        if selected_sockets and (specs['socket'] not in selected_sockets):
            continue
            
        filtered_list.append(row)

    # 3. Оновлюємо таблицю
    current_products = filtered_list.copy()
    tree.delete(*tree.get_children())
    for item in current_products:
        tree.insert("", "end", values=item)


def build_cpu_sidebar(parent_frame, tree, all_products, reset_command):
    widgets = {}
    
    def on_change(*args):
        apply_advanced_cpu_filter(widgets, tree, all_products)

    # --- СТВОРЮЄМО ГОЛОВНИЙ СКРОЛ-ФРЕЙМ ---
    # Це дозволить усьому контенту всередині parent_frame гортатися
    main_scroll = ctk.CTkScrollableFrame(
        parent_frame, 
        fg_color="transparent",
        scrollbar_button_color="#4A4A4A",
        scrollbar_button_hover_color="#666666"
    )
    main_scroll.pack(fill="both", expand=True)

    # --- ВИРОБНИК ---
    ctk.CTkLabel(main_scroll, text="Виробник", font=("Lato", 20, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['vendor_amd'] = ctk.CTkCheckBox(main_scroll, text="AMD", font=("Lato", 16), 
                                             text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_amd'].pack(anchor="w", padx=30, pady=2)
    widgets['vendor_intel'] = ctk.CTkCheckBox(main_scroll, text="Intel", font=("Lato", 16), 
                                               text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_intel'].pack(anchor="w", padx=30, pady=2)

    # --- ХАРАКТЕРИСТИКИ ---
    ctk.CTkLabel(main_scroll, text="Характеристики", font=("Lato", 24, "bold"), text_color="#FFFFFF").pack(pady=(20, 10))

    # Кількість ядер
    ctk.CTkLabel(main_scroll, text="Кількість ядер", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    widgets['cores'] = ctk.CTkComboBox(main_scroll, values=["", "2", "4", "6", "8", "12", "16", "24"], width=180, 
                                        fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                        button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['cores'].pack(pady=(0, 10))
    widgets['cores'].set("") 

    # Кількість потоків
    ctk.CTkLabel(main_scroll, text="Кількість потоків", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    widgets['threads'] = ctk.CTkComboBox(main_scroll, values=["", "4", "8", "12", "16", "24", "32"], width=180, 
                                          fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                          button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['threads'].pack(pady=(0, 10))
    widgets['threads'].set("")

    # Тактова частота
    ctk.CTkLabel(main_scroll, text="Тактова частота (GHz)", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    f_freq = ctk.CTkFrame(main_scroll, fg_color="transparent")
    f_freq.pack(pady=(0, 10))
    
    widgets['freq_from'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_from'].pack(side="left", padx=5)
    widgets['freq_from'].bind("<KeyRelease>", on_change)
    
    widgets['freq_to'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_to'].pack(side="left", padx=5)
    widgets['freq_to'].bind("<KeyRelease>", on_change)

    # Кеш
    ctk.CTkLabel(main_scroll, text="Об'єм кешу L3 (МБ)", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    f_cache = ctk.CTkFrame(main_scroll, fg_color="transparent")
    f_cache.pack(pady=(0, 10))
    
    widgets['cache_from'] = ctk.CTkEntry(f_cache, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['cache_from'].pack(side="left", padx=5)
    widgets['cache_from'].bind("<KeyRelease>", on_change)
    
    widgets['cache_to'] = ctk.CTkEntry(f_cache, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['cache_to'].pack(side="left", padx=5)
    widgets['cache_to'].bind("<KeyRelease>", on_change)

    # Сокет
    ctk.CTkLabel(main_scroll, text="Тип роз'єму", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20, pady=(5,5))
    socket_list = ["AM5", "AM4", "LGA1700"] 
    widgets['sockets'] = {}
    for sock in socket_list:
        chk = ctk.CTkCheckBox(main_scroll, text=sock, font=("Lato", 16), 
                               text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['sockets'][sock] = sock_chk = chk # Збереження у словник для фільтрації

    # --- КНОПКА ОЧИСТИТИ ---
    # Тепер вона знаходиться всередині скрол-зони в самому кінці
    add_clear_button(main_scroll, reset_command)


def parse_mb_specs(spec_str):
    try:
        parts = spec_str.split(" / ")
        if len(parts) < 5:
            return None
            
        # parts[0]: "AM5" -> "AM5"
        socket = parts[0].strip()
        
        # parts[1]: "B650" -> "B650"
        chipset = parts[1].strip()
        
        # parts[2]: "4 слотів ОЗП" -> беремо перше слово "4"
        slots = parts[2].strip().split()[0]
        
        # parts[3]: "ATX формфактор" -> беремо перше слово "ATX"
        # Увага: на скріншоті є "mATX", "ATX", "E-ATX"
        form_factor = parts[3].strip().split()[0]
        
        # parts[4]: "1 Wi-Fi" або "0 Wi-Fi" -> беремо перше слово "Так" або "Ні"
        wifi_val = parts[4].strip().split()[0]
        wifi = "Так" if wifi_val == "Так" else "Ні"
        
        return {
            "socket": socket,
            "chipset": chipset,
            "slots": slots,
            "form_factor": form_factor,
            "wifi": wifi
        }
    except Exception as e:
        print(f"Error parsing MB specs '{spec_str}': {e}")
        return None


def apply_advanced_mb_filter(widgets, tree, all_products):
    global current_products
    
    # 1. Зчитуємо значення з інтерфейсу
    try:
        # Виробник (ASUS, MSI, Gigabyte...)
        selected_vendors = [k for k, v in widgets['vendors'].items() if v.get()]
        
        # Сокети
        selected_sockets = [k for k, v in widgets['sockets'].items() if v.get()]
        
        # Чіпсети
        selected_chipsets = [k for k, v in widgets['chipsets'].items() if v.get()]
        
        # Слоти ОЗП (Dropdown)
        sel_slots = widgets['slots'].get()
        print("slots:   " + sel_slots)
        
        # Формфактор
        selected_ff = [k for k, v in widgets['ff'].items() if v.get()]
        
        # WiFi
        selected_wifi = [k for k, v in widgets['wifi'].items() if v.get()]
        print("SELECTED WIFI")
        print(selected_wifi)
        
    except ValueError:
        return


    filtered_list = []
    
    # 2. Фільтрація
    for row in all_products:
        category = row[4]
        vendor = row[5] # Наприклад "ASUS"
        specs_str = row[3]


        if category != "Материнська плата":
            continue
            
        # Фільтр виробника (нечутливий до регістру, про всяк випадок)
        if selected_vendors:
            # Якщо vendor в базі "ASUS", а ми шукаємо "Asus", приводимо до lower
            vendor_match = False
            for v_sel in selected_vendors:
                if v_sel.lower() == vendor.lower():
                    vendor_match = True
                    break
            if not vendor_match:
                continue
            
        specs = parse_mb_specs(specs_str)

        if not specs:
            print("not specs")
            continue
            
        # Socket
        if selected_sockets and (specs['socket'] not in selected_sockets):
            continue
            
        # Chipset (Точне співпадіння, бо ми взяли список з таблиці)
        if selected_chipsets and (specs['chipset'] not in selected_chipsets):
            continue

        # Створюємо умовний список для порівняння. Якщо "Усі" — фільтр не активний.
        if sel_slots and sel_slots != "Усі":
            if specs.get('slots') not in [sel_slots]:
                continue

        # Form Factor ("ATX", "mATX", "E-ATX")
        if selected_ff and (specs['form_factor'] not in selected_ff):
            continue
            
        # Wifi ("Так" або "Ні")
        if selected_wifi and (specs['wifi'] not in selected_wifi):
            continue

        filtered_list.append(row)

    # 3. Оновлення таблиці
    current_products = filtered_list.copy()
    tree.delete(*tree.get_children())
    for item in current_products:
        tree.insert("", "end", values=item)


def build_mb_sidebar(parent_frame, tree, all_products, reset_command):
    widgets = {}

    def on_change(*args):
        apply_advanced_mb_filter(widgets, tree, all_products)

    # --- СТВОРЮЄМО ГОЛОВНИЙ СКРОЛ-ФРЕЙМ ---
    # Він займає весь простір parent_frame
    main_scroll = ctk.CTkScrollableFrame(
        parent_frame, 
        fg_color="transparent", 
        label_text="", # Можна додати заголовок "Фільтри", якщо потрібно
        scrollbar_button_color="#4A4A4A", # Колір повзунка
        scrollbar_button_hover_color="#666666"
    )
    main_scroll.pack(fill="both", expand=True)
    
    # --- ВИРОБНИК ---
    ctk.CTkLabel(main_scroll, text="Виробник", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    vendor_list = ["ASUS", "MSI", "Gigabyte"]
    widgets['vendors'] = {}
    for v in vendor_list:
        chk = ctk.CTkCheckBox(main_scroll, text=v, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['vendors'][v] = chk

    # --- SOCKET ---
    ctk.CTkLabel(main_scroll, text="Сокет", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    socket_list = ["AM5", "AM4", "LGA1700"] 
    widgets['sockets'] = {}
    for sock in socket_list:
        chk = ctk.CTkCheckBox(main_scroll, text=sock, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['sockets'][sock] = chk

    # --- CHIPSET ---
    ctk.CTkLabel(main_scroll, text="Чіпсет", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    chipset_list = ["B650", "B550", "B660", "B760", "X670", "X670E", "Z690", "Z790"]
    widgets['chipsets'] = {}
    # Тепер тут не потрібен внутрішній скрол, просто виводимо список
    for chip in chipset_list:
        chk = ctk.CTkCheckBox(main_scroll, text=chip, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['chipsets'][chip] = chk

    # --- RAM SLOTS ---
    ctk.CTkLabel(main_scroll, text="Слоти ОЗП", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['slots'] = ctk.CTkComboBox(main_scroll, values=["Усі", "2", "4"], width=180, 
                                       fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                       button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['slots'].pack(pady=5)
    widgets['slots'].set("")

    # --- FORM FACTOR ---
    ctk.CTkLabel(main_scroll, text="Формфактор", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    ff_list = ["ATX", "Micro-ATX", "E-ATX"]
    widgets['ff'] = {}
    for ff in ff_list:
        chk = ctk.CTkCheckBox(main_scroll, text=ff, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['ff'][ff] = chk

    # --- WIFI ---
    ctk.CTkLabel(main_scroll, text="Наявність Wi-Fi", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['wifi'] = {}
    for status in ["Так", "Ні"]:
        chk = ctk.CTkCheckBox(main_scroll, text=status, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['wifi'][status] = chk

    # --- КНОПКА ОЧИСТИТИ ---
    # Додаємо кнопку очищення в кінець скрол-фрейму
    add_clear_button(main_scroll, reset_command)

def parse_gpu_specs(spec_str):
    try:
        parts = spec_str.split(" / ")
        # Перевірка на цілісність даних (має бути 5 частин)
        if len(parts) < 5:
            return None
            
        # 1. VRAM: "24 ГБ" -> 24
        vram_match = re.search(r'\d+', parts[0])
        vram = int(vram_match.group()) if vram_match else 0
        
        # 2. Частота: "2520 МГц" -> 2520
        freq_match = re.search(r'\d+', parts[1])
        freq = int(freq_match.group()) if freq_match else 0
        
        # 3. Технології: рядок
        tech = parts[2]
        
        # 4. TDP: "450 Вт" -> 450 (останній елемент)
        tdp_match = re.search(r'\d+', parts[4])
        tdp = int(tdp_match.group()) if tdp_match else 0
        
        return {
            "vram": vram,
            "freq": freq,
            "tech": tech,
            "tdp": tdp
        }
    except Exception as e:
        print(f"Error parsing GPU specs '{spec_str}': {e}")
        return None

def apply_advanced_gpu_filter(widgets, tree, all_products):
    global current_products
    
    try:
        
        # Виробник
        selected_vendors = []
        if widgets['vendor_nvidia'].get(): selected_vendors.append("NVIDIA")
        if widgets['vendor_amd'].get(): selected_vendors.append("AMD")
        
        # VRAM (Обсяг пам'яті)
        selected_vram = [int(k) for k, v in widgets['vram'].items() if v.get()]
        
        # Частота
        freq_min = float(widgets['freq_from'].get()) if widgets['freq_from'].get() else 0
        freq_max = float(widgets['freq_to'].get()) if widgets['freq_to'].get() else 10000
        
        # Технології
        # Якщо обрано DLSS3, то рядок характеристик має містити "DLSS3"
        req_tech = [k for k, v in widgets['tech'].items() if v.get()]
        
        # TDP
        tdp_min = float(widgets['tdp_from'].get()) if widgets['tdp_from'].get() else 0
        tdp_max = float(widgets['tdp_to'].get()) if widgets['tdp_to'].get() else 2000

    except ValueError:
        return

    filtered_list = []
    
    for row in all_products:
        category = row[4]
        vendor = row[5]
        specs_str = row[3]

        if category != "Відеокарта":
            continue
            
        if selected_vendors and (vendor not in selected_vendors):
            continue
            
        specs = parse_gpu_specs(specs_str)
        if not specs:
            continue
            
        # VRAM
        if selected_vram and (specs['vram'] not in selected_vram):
            continue
            
        # Frequency
        if not (freq_min <= specs['freq'] <= freq_max):
            continue
            
        # Tech (Логіка: якщо обрано чекбокс, ця технологія МАЄ бути в списку)
        if req_tech:
            has_tech = False
            for t in req_tech:
                if t in specs['tech']:
                    has_tech = True
                    break
            if not has_tech:
                continue

        # TDP
        if not (tdp_min <= specs['tdp'] <= tdp_max):
            continue
            
        filtered_list.append(row)

    current_products = filtered_list.copy()
    tree.delete(*tree.get_children())
    for item in current_products:
        tree.insert("", "end", values=item)


def build_gpu_sidebar(parent_frame, tree, all_products, reset_command):
    widgets = {}
    
    def on_change(*args):
        apply_advanced_gpu_filter(widgets, tree, all_products)

    # --- СТВОРЮЄМО ГОЛОВНИЙ СКРОЛ-ФРЕЙМ ---
    # Обгортка для всього контенту сайдбару
    main_scroll = ctk.CTkScrollableFrame(
        parent_frame, 
        fg_color="transparent",
        scrollbar_button_color="#4A4A4A",
        scrollbar_button_hover_color="#666666"
    )
    main_scroll.pack(fill="both", expand=True)

    # --- ВИРОБНИК ---
    ctk.CTkLabel(main_scroll, text="Виробник чіпа", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(10, 5))
    widgets['vendor_nvidia'] = ctk.CTkCheckBox(main_scroll, text="NVIDIA", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_nvidia'].pack(anchor="w", padx=30, pady=2)
    
    widgets['vendor_amd'] = ctk.CTkCheckBox(main_scroll, text="AMD", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_amd'].pack(anchor="w", padx=30, pady=2)

    # --- VRAM (Відеопам'ять) ---
    ctk.CTkLabel(main_scroll, text="Відеопам'ять (ГБ)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    vram_options = ["24", "16", "12", "10", "8", "6"]
    widgets['vram'] = {}
    f_vram = ctk.CTkFrame(main_scroll, fg_color="transparent")
    f_vram.pack(fill="x", padx=10)
    
    for i, v in enumerate(vram_options):
        chk = ctk.CTkCheckBox(f_vram, text=f"{v} ГБ", width=60, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        row = i // 2
        col = i % 2
        chk.grid(row=row, column=col, sticky="w", padx=10, pady=5)
        widgets['vram'][v] = chk

    # --- ЧАСТОТА ---
    ctk.CTkLabel(main_scroll, text="Частота (МГц)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    f_freq = ctk.CTkFrame(main_scroll, fg_color="transparent")
    f_freq.pack(pady=5)
    
    widgets['freq_from'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_from'].pack(side="left", padx=5)
    widgets['freq_from'].bind("<KeyRelease>", on_change)
    
    widgets['freq_to'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_to'].pack(side="left", padx=5)
    widgets['freq_to'].bind("<KeyRelease>", on_change)

    # --- ТЕХНОЛОГІЇ ---
    ctk.CTkLabel(main_scroll, text="Технології", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    tech_list = ["DLSS3", "DLSS2", "RayTracing"]
    widgets['tech'] = {}
    for t in tech_list:
        chk = ctk.CTkCheckBox(main_scroll, text=t, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['tech'][t] = chk

    # --- TDP ---
    ctk.CTkLabel(main_scroll, text="TDP (Вт)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    f_tdp = ctk.CTkFrame(main_scroll, fg_color="transparent")
    f_tdp.pack(pady=5)
    
    widgets['tdp_from'] = ctk.CTkEntry(f_tdp, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['tdp_from'].pack(side="left", padx=5)
    widgets['tdp_from'].bind("<KeyRelease>", on_change)
    
    widgets['tdp_to'] = ctk.CTkEntry(f_tdp, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['tdp_to'].pack(side="left", padx=5)
    widgets['tdp_to'].bind("<KeyRelease>", on_change)

    # --- КНОПКА ОЧИСТИТИ ---
    # Огортаємо кнопку очищення, щоб вона була в кінці списку, що прокручується
    add_clear_button(main_scroll, reset_command)


def update_left_panel(comb_category,category, left_frame, tree, all_products):
    """
    Очищає ліву панель і будує відповідні фільтри.
    """
    # 1. Видаляємо старі віджети (це і є очищення полів)
    for widget in left_frame.winfo_children():
        widget.destroy()
    
    # 2. Функція для повного скидання (передаємо її кнопці)
    def reset_all():
        global current_products
        # Повертаємо список до початкового стану
        current_products = all_products.copy()
        
        # Очищаємо таблицю і заповнюємо всіма продуктами
        tree.delete(*tree.get_children())
        for row in all_products:
            if row[4] == category:
                tree.insert("", "end", values=row)
            
        # Перебудовуємо панель (рекурсивний виклик, щоб очистити поля вводу)
        update_left_panel(comb_category,category, left_frame, tree, all_products)

    # 3. Будуємо нові панелі, передаючи функцію reset_all
    if category == "Процесор":
        build_cpu_sidebar(left_frame, tree, all_products, reset_all)
        
    elif category == "Відеокарта":
        build_gpu_sidebar(left_frame, tree, all_products, reset_all)
        
    elif category == "Материнська плата":
        build_mb_sidebar(left_frame, tree, all_products, reset_all)
        
    else:
        pass


# Function who filtered data in table by type category
def filter_by_type(combobox, tree, left_frame, all_products) -> None:
    global current_products

    # get choose
    choose = combobox.get()
    
    # --- НОВЕ: Оновлюємо ліву панель ---
    update_left_panel(combobox,choose, left_frame, tree, all_products)
    # -----------------------------------

    # remove all data in table, work faster than delete by row in for 
    tree.delete(*tree.get_children())

    # saved data who filtered 
    filtered = []

    # save the data source for the table as current data 
    # ВАЖЛИВО: Використовуємо all_products як базу, щоб скинути попередні фільтри
    sourse = all_products 

    if choose == "Усі":
        filtered = sourse.copy()
    else:
        filtered = [item for item in sourse if item[4] == choose]

    current_products = filtered.copy()

    # populate table with filtered data
    for row in tuple(current_products):
        tree.insert("", "end", values=row)



# Function who filtere data by entered text from entry search
def search_by_entry(entry_search, tree) -> None:
    global current_products

    cursor_tab = CONNECT.cursor()
    cursor_tab.execute(QUERY_SUPPLY) # exucutes an SQL query
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
def add_data_to_card(APP,id: ctk.CTkEntry,qnt: ctk.CTkEntry,
        price:ctk.CTkEntry,state:int,suppli:ctk.CTkComboBox,table: ttk.Treeview) -> None:
    from message import message_window
    global current_products
    product_id = id.get()
    quantity = qnt.get()
    price_prod = price.get()
    supplier = suppli.get()

    try:
        
        if not product_id or not quantity:
            message_window(APP, "Помилка!", "Заповніть  усі необхідні поля!")
            return
        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except:
            message_window(APP, "Помилка!", "Некоректні дані")
            return
        
        if quantity < 0:
            message_window(APP, "Помилка!", "Некоректні дані")
            return

        product_data = None
        for item in current_products:
            if int(item[0]) == product_id:
                product_data = item
                break

        if product_data is None:
            message_window(APP,"Помилка!","Товару з таким номером не існує!")
            print("Товар з таким ID не знайдено в current_products")
            return
        
        if quantity > 25:
            message_window(APP,"Помилка!","Велика кількість товару!")
            return

        # checking the product for duplicates
        for iid in table.get_children(): # iid have a unique id of row in table 
            row = table.item(iid)["values"]
            print(row)
            if int(row[0]) == product_id:  # if product exists
                old_price = float(row[5])
                print(old_price)
                if state == 1:
                    print(state)
                    new_quantity = int(row[4]) + quantity
                    new_row = [row[0], row[1], row[2], supplier, new_quantity, f"{old_price:.2f}",f"{old_price * new_quantity:.2f}"]
                    table.delete(iid)
                    table.insert("", "end", values=new_row)
                    return
                else:
                    if not price_prod:
                        message_window(APP, "Помилка!", "Введіть ціну постачі!")
                        return
                    try:
                        price_prod = float(price_prod)
                        if price_prod < 0:
                            message_window(APP, "Помилка!", "Некоректні дані")
                            return
                    except ValueError:
                        message_window(APP, "Помилка!", "Некоректні дані")
                        return
                    new_quantity = int(row[4]) + quantity
                    new_row = [row[0], row[1], row[2], supplier, new_quantity, f"{price_prod:.2f}",f"{price_prod * new_quantity:.2f}"]
                    table.delete(iid)
                    table.insert("", "end", values=new_row)
                    return

        #  if the product is not available we search for it in current_products
        for item in current_products:
            if int(item[0]) == product_id:
                if not price_prod:
                        message_window(APP, "Помилка!", "Введіть ціну постачі!")
                        return
                try:
                    price_prod = float(price_prod)
                    if price_prod < 0:
                        message_window(APP, "Помилка!", "Некоректні дані")
                        return
                except ValueError:
                    message_window(APP, "Помилка!", "Некоректні дані")
                    return

                new_row = [item[0],item[1],item[2],supplier,quantity,f"{price_prod:.2f}",f"{price_prod * quantity:.2f}"]
                table.insert("", "end", values=new_row)
                return
        print("Товар з таким ID не знайдено")
    except ValueError as e:
        print(f"Помилка: {e}")
    finally:
        id.delete(0, "end")
        qnt.delete(0, "end")
        price.delete(0, "end")     


# Function who clear basket
def clear_basket(table:ttk.Treeview) -> None:
    # clear table 
    table.delete(*table.get_children())


# Function who make supply product
def make_supply(APP,
              table_basket:ttk.Treeview, tree_table:ttk.Treeview) -> None:
    from message import message_window
    from collections import defaultdict
    global current_products

    basket = [table_basket.item(row)["values"] for row in table_basket.get_children()]

    if not basket:
        message_window(APP,"Помилка!","Кошик порожній, додайте товар!")
        raise Exception("Basket is empty")
    grouped_basket = defaultdict(list)
    for item in basket:
        supplier_name = str(item[3])
        print(supplier_name)
        print(type(grouped_basket))
        grouped_basket[supplier_name].append(item)
    print(f"grouped: {grouped_basket}")

    try:
        cursor_tab = CONNECT.cursor()
        # Start transaction
        CONNECT.start_transaction()
        
        for supplier, products in grouped_basket.items():
            cursor_tab.execute(f'''
                call CreateSupply(
                    '{1}',
                    '{supplier}', 
                    @supply_id
                )
            ''')

            cursor_tab.execute("SELECT @supply_id")
            current_supply_id = cursor_tab.fetchone()[0]

            for prod in products:
                curr_prod_name = prod[1]
                curr_prod_model = prod[2]
                curr_prod_count = int(prod[4])
                curr_prod_unit_price = float(prod[5])

                cursor_tab.execute(f'''
                call SupplyProduct(
                    '{current_supply_id}',
                    '{curr_prod_name}',
                    '{curr_prod_model}',
                    '{curr_prod_count}',
                    '{curr_prod_unit_price}'
                    )
                ''')
        CONNECT.commit()
        message_window(APP, "Успіх!", "Постачання оформлено успішно!")

    except Exception as e:
        CONNECT.rollback()
        print(f"Помилка: {e}")
        message_window(APP, "Помилка!", f"Сталася помилка при оформленні!")
        return 
    # clean basket
    table_basket.delete(*table_basket.get_children())
    
    # Update product table
    tree_table.delete(*tree_table.get_children())
    try:
        cursor_tab.execute(QUERY_SUPPLY)
        all_products = cursor_tab.fetchall()
        cursor_tab.close()
        CONNECT.commit()
        current_products.clear()
        for row in all_products:
            tree_table.insert("", "end", values=row)
            current_products.append(row)
    except Exception as e:
        print(f"Помилка оновлення таблиці: {e}")


def get_supplier_list() -> list[str]:
    cursor = CONNECT.cursor()
    cursor.execute(QUERY_SUPPLIER)

    suppliers = [row[0] for row in cursor.fetchall() if row[0] != '-']


    cursor.close()
    return suppliers


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


def show_entry(state:int, frame_entry:ctk.CTkFrame) -> None:
    if state == 1:
        frame_entry.grid_forget()
    elif state == 0:
        frame_entry.grid(row=0, column=2, padx=(0, 5), pady=9)
        
    


def Supply_window(*, app: ctk.CTk) -> None:
    global current_products

    app.geometry("1920x1080")
    app.title("Постачання товару")
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
        values=["Усі","Процесор","Відеокарта","Материнська плата"]
    )
    combobox_category.grid(row=1,column=0,padx=(25,0), pady=(19,0))


     #Frame for variable sort
    frame_var_sort = ctk.CTkFrame(master=frame_top_widget,width=200,height=90,fg_color="transparent")
    frame_var_sort.place(x=190,y=16)
    frame_var_sort.propagate(False)
    frame_var_sort.place_forget()

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
        values=["Від дешевих до дорогих", "Від дорогих до дешевих"]
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
        fg_color="#FFB030",
        hover_color="#FF9933",
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
    
    columns = ("id", "name", "model","specs","category","vendor","supplier","available_quantity")
    titles  = ["№","Назва","Модель","Характеристики","Тип категорії","Виробник","Постачальник","В наявності"]
    
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
    
    # # ------------------ 2. ПАНЕЛЬ ДОДАВАННЯ (Між таблицями) ------------------

    frame_controls_add = ctk.CTkFrame(master=frame_right_container, height=68, fg_color="transparent")
    frame_controls_add.pack(side="top", fill="x", padx=5, pady=(0, 5))
    frame_controls_add.propagate(False)
    frame_controls_add.columnconfigure(5, weight=1)
    

    # Frame: id
    frame_id = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_id.grid(row=0, column=0, padx=(5, 5), pady=9)
    entry_id = ctk.CTkEntry(
        master=frame_id, placeholder_text="Номер товару", width=165, height=50,
        fg_color="transparent", border_color="#00BFFF", border_width=2, corner_radius=10,
        font=("Lato", 16), placeholder_text_color="#7F7F7F", text_color="#000000"
    )
    entry_id.pack()

    # Frame: quantity
    frame_qty = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_qty.grid(row=0, column=1, padx=(0, 5), pady=9)

    entry_quantity = ctk.CTkEntry(
        master=frame_qty, placeholder_text="Кількість", width=165, height=50,
        fg_color="transparent", border_color="#00BFFF", border_width=2, corner_radius=10,
        font=("Lato", 16), placeholder_text_color="#7F7F7F", text_color="#000000",
    )
    entry_quantity.pack()

    # Frame: unit price
    frame_unit_price = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_unit_price.grid(row=0, column=2, padx=(0, 5), pady=9)

    entry_unit_price = ctk.CTkEntry(
        master=frame_unit_price, placeholder_text="Ціна за одиницю", width=165, height=50,
        fg_color="transparent", border_color="#00BFFF", border_width=2, corner_radius=10,
        font=("Lato", 16), placeholder_text_color="#7F7F7F", text_color="#000000",
    )
    entry_unit_price.pack()

    # Frame: supplier
    frame_supplier = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_supplier.grid(row=0, column=3, padx=(0, 5), pady=9)
    
    combobox_supplier = ctk.CTkComboBox(
        master=frame_supplier, width=165, height=50, corner_radius=5,
        text_color="#000000", font=("Lato", 16, "bold"),
        fg_color="#FFFFFF", button_color="#00BFFF", border_color="#00BFFF",
        values=get_supplier_list()
    )
    combobox_supplier.pack()

    # # Frame: button add
    frame_btn_add = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_btn_add.grid(row=0, column=4, padx=(0, 10), pady=9)

    button_add = ctk.CTkButton(
        master=frame_btn_add, text="Додати", width=165, height=50,
        corner_radius=5, fg_color="#00BFFF", hover_color="#009BCF",
        font=("Lato", 24, "bold"), text_color="#FFFFFF",
        command=lambda: on_add_click()
    )
    button_add.pack()

    # # Frame: clear basket
    frame_btn_clear = ctk.CTkFrame(master=frame_controls_add, fg_color="transparent")
    frame_btn_clear.grid(row=0, column=5, padx=(5, 5), sticky="e") 

    button_clear_basket = ctk.CTkButton(
        master=frame_btn_clear, text="Очистити кошик", width=193, height=39,
        corner_radius=5, fg_color="#FF3C00", hover_color="#E32600",
        font=("Lato", 16, "bold"), text_color="#FFFFFF",
        command=lambda: on_clear_click()
    )
    button_clear_basket.pack(pady=(14, 0))


    # ------------------ 3. ТАБЛИЦЯ КОШИКА (Нижня таблиця) ------------------
    frame_cart = ctk.CTkFrame(master=frame_right_container, fg_color="transparent", border_width=1, height=200)
    frame_cart.pack(side="top", fill="x", expand=False, padx=5, pady=(0, 5))
    
    frame_cart.grid_columnconfigure(0, weight=1)
    frame_cart.grid_rowconfigure(0, weight=1)

    # Columns for the cart
    cart_columns = ("id", "name", "model", "supplier","quantity", "price", "total")
    cart_titles = ["№", "Назва", "Модель", "Постачальник","Кількість", "Ціна", "Сума"]
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
    tree_cart.column("supplier", width=150, anchor="center")
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
    checkbox_is_add = ctk.CTkCheckBox(
        master=frame_check_box_sale,
        text="Товар вже у кошику",
        text_color="#000000",
        text_color_disabled="#E90000",
        font=("Lato", 16),
        fg_color="#00BFFF",    
        border_color="#00BFFF",
        border_width=3,
        corner_radius=5,
        hover_color="#0080C0",
        command=lambda:show_entry(checkbox_is_add.get(),frame_unit_price)
    )
    checkbox_is_add.pack(expand=True, anchor="center") 

    # Frame for button checkout
    frame_button_container = ctk.CTkFrame(
        master=frame_controls_checkout,
        height=68,
        fg_color="transparent"
    )
    frame_button_container.pack(side="right", fill="y", padx=(10, 0))

    button_checkout = ctk.CTkButton(
        master=frame_button_container,
        text="Завершити постачу",
        width=230,
        height=68,
        corner_radius=5,
        fg_color="#FFB030",
        hover_color="#FF9933",
        font=("Lato", 24, "bold"),
        text_color="#FFFFFF",
        command=lambda:on_supply_click()
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
    frame_sum.place(relx=0.75, rely=0.5, anchor="center")

    # Variable for save total sum
    sum_var = ctk.StringVar(value="Загальна сума: 0 ₴")
    # Entry for summary
    label_summary = ctk.CTkLabel(master=frame_sum,textvariable=sum_var,text_color="#000000",font=("Lato", 16, "bold"))
    label_summary.pack(expand=True)


    def on_add_click() -> None:
        add_data_to_card(app, entry_id, entry_quantity,entry_unit_price,checkbox_is_add.get(),combobox_supplier,tree_cart)
        total = get_summary_from_basket(tree_cart)
        sum_var.set(f"Загальна сума: {total} ₴")


    def on_clear_click() -> None:
        clear_basket(tree_cart)
        sum_var.set("Загальна сума: 0 ₴")


    def on_supply_click() -> None:
        total = get_summary_from_basket(tree_cart)
        try:
            make_supply(app, tree_cart, tree_table)
            sum_var.set("Загальна сума: 0 ₴")
        except Exception as e:
            print(f"Постачання скасовано: {e}")
            sum_var.set(f"Загальна сума: {total} ₴")        
            
    
    try:
        # Query for data in table
        cursor_tab = CONNECT.cursor(buffered=True)
        cursor_tab.execute(QUERY_SUPPLY) # exucutes an SQL query
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

        combobox_category.configure(
            command=lambda value: filter_by_type(
                combobox_category, 
                tree_table, 
                frame_left_widget, 
                all_products
            )
        )
    except:
        print("We have a problem with get data about product in Purchase Frame")
