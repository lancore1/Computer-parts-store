from PIL import Image
from tkinter import ttk
import customtkinter as ctk
from DB_connector import CONNECT
from Main_Frame import *
import global_state 
import globalQuery

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
        # Ціна
        p_min = float(widgets['price_from'].get()) if widgets['price_from'].get() else 0
        p_max = float(widgets['price_to'].get()) if widgets['price_to'].get() else 1000000
        
        # Виробник (Vendor) - Checkboxes
        selected_vendors = []
        if widgets['vendor_amd'].get(): selected_vendors.append("AMD")
        if widgets['vendor_intel'].get(): selected_vendors.append("Intel")
        
        # Характеристики CPU
        sel_cores = widgets['cores'].get() # Combobox value or empty
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
        cost = float(row[8])
        specs_str = row[3]

        # Базовий фільтр: Категорія має бути Процесор
        if category != "Процесор":
            continue
            
        # Фільтр ціни
        if not (p_min <= cost <= p_max):
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

    # --- ЦІНА ---
    ctk.CTkLabel(parent_frame, text="Ціна, грн", font=("Lato", 20, "bold"), text_color="#FFFFFF").pack(pady=(20, 5))
    f_price = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_price.pack(pady=5)
    
    widgets['price_from'] = ctk.CTkEntry(f_price, width=80, placeholder_text="Від: 100", 
                                         fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_from'].pack(side="left", padx=5)
    widgets['price_from'].bind("<KeyRelease>", on_change)
    
    widgets['price_to'] = ctk.CTkEntry(f_price, width=80, placeholder_text="До: 100000", 
                                       fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_to'].pack(side="left", padx=5)
    widgets['price_to'].bind("<KeyRelease>", on_change)

    # --- ВИРОБНИК ---
    ctk.CTkLabel(parent_frame, text="Виробник", font=("Lato", 20, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['vendor_amd'] = ctk.CTkCheckBox(parent_frame, text="AMD", font=("Lato", 16), 
                                            text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_amd'].pack(anchor="w", padx=30, pady=2)
    widgets['vendor_intel'] = ctk.CTkCheckBox(parent_frame, text="Intel", font=("Lato", 16), 
                                              text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_intel'].pack(anchor="w", padx=30, pady=2)

    # --- ХАРАКТЕРИСТИКИ ---
    ctk.CTkLabel(parent_frame, text="Характеристики", font=("Lato", 24, "bold"), text_color="#FFFFFF").pack(pady=(20, 10))

    # Кількість ядер
    ctk.CTkLabel(parent_frame, text="Кількість ядер", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    widgets['cores'] = ctk.CTkComboBox(parent_frame, values=["", "2", "4", "6", "8", "12", "16", "24"], width=180, 
                                       fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                       button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['cores'].pack(pady=(0, 10))
    widgets['cores'].set("") 

    # Кількість потоків
    ctk.CTkLabel(parent_frame, text="Кількість потоків", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    widgets['threads'] = ctk.CTkComboBox(parent_frame, values=["", "4", "8", "12", "16", "24", "32"], width=180, 
                                         fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                         button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['threads'].pack(pady=(0, 10))
    widgets['threads'].set("")

    # Тактова частота
    ctk.CTkLabel(parent_frame, text="Тактова частота (GHz)", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    f_freq = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_freq.pack(pady=(0, 10))
    
    widgets['freq_from'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_from'].pack(side="left", padx=5)
    widgets['freq_from'].bind("<KeyRelease>", on_change)
    
    widgets['freq_to'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_to'].pack(side="left", padx=5)
    widgets['freq_to'].bind("<KeyRelease>", on_change)

    # Кеш
    ctk.CTkLabel(parent_frame, text="Об'єм кешу L3 (МБ)", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
    f_cache = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_cache.pack(pady=(0, 10))
    
    widgets['cache_from'] = ctk.CTkEntry(f_cache, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['cache_from'].pack(side="left", padx=5)
    widgets['cache_from'].bind("<KeyRelease>", on_change)
    
    widgets['cache_to'] = ctk.CTkEntry(f_cache, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['cache_to'].pack(side="left", padx=5)
    widgets['cache_to'].bind("<KeyRelease>", on_change)

    # Сокет
    ctk.CTkLabel(parent_frame, text="Тип роз'єму", font=("Lato", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20, pady=(5,5))
    socket_list = ["AM5", "AM4", "LGA1700"] 
    widgets['sockets'] = {}
    for sock in socket_list:
        chk = ctk.CTkCheckBox(parent_frame, text=sock, font=("Lato", 16), 
                              text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['sockets'][sock] = chk

    add_clear_button(parent_frame, reset_command)

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
        
        # parts[4]: "1 Wi-Fi" або "0 Wi-Fi" -> беремо перше слово "1" або "0"
        wifi_val = parts[4].strip().split()[0]
        wifi = "Так" if wifi_val == "1" else "Ні"
        
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
        # Ціна
        p_min = float(widgets['price_from'].get()) if widgets['price_from'].get() else 0
        p_max = float(widgets['price_to'].get()) if widgets['price_to'].get() else 1000000
        
        # Виробник (ASUS, MSI, Gigabyte...)
        selected_vendors = [k for k, v in widgets['vendors'].items() if v.get()]
        
        # Сокети
        selected_sockets = [k for k, v in widgets['sockets'].items() if v.get()]
        
        # Чіпсети
        selected_chipsets = [k for k, v in widgets['chipsets'].items() if v.get()]
        
        # Слоти ОЗП (Dropdown)
        sel_slots = widgets['slots'].get()
        
        # Формфактор
        selected_ff = [k for k, v in widgets['ff'].items() if v.get()]
        
        # WiFi
        selected_wifi = [k for k, v in widgets['wifi'].items() if v.get()]
        
    except ValueError:
        return

    filtered_list = []
    
    # 2. Фільтрація
    for row in all_products:
        category = row[4]
        vendor = row[5] # Наприклад "ASUS"
        cost = float(row[8])
        specs_str = row[3]

        if category != "Материнська плата":
            continue
            
        if not (p_min <= cost <= p_max):
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
            continue
            
        # Socket
        if selected_sockets and (specs['socket'] not in selected_sockets):
            continue
            
        # Chipset (Точне співпадіння, бо ми взяли список з таблиці)
        if selected_chipsets and (specs['chipset'] not in selected_chipsets):
            continue

        # Slots (Рядкове порівняння "2", "4")
        if sel_slots and specs['slots'] != sel_slots:
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

    # --- ЦІНА ---
    ctk.CTkLabel(parent_frame, text="Ціна, грн", font=("Lato", 20, "bold"), text_color="#FFFFFF").pack(pady=(10, 5))
    f_price = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_price.pack(pady=5)
    widgets['price_from'] = ctk.CTkEntry(f_price, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_from'].pack(side="left", padx=5)
    widgets['price_from'].bind("<KeyRelease>", on_change)
    widgets['price_to'] = ctk.CTkEntry(f_price, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_to'].pack(side="left", padx=5)
    widgets['price_to'].bind("<KeyRelease>", on_change)

    # --- ВИРОБНИК ---
    ctk.CTkLabel(parent_frame, text="Виробник", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(10, 5))
    vendor_list = ["ASUS", "MSI", "Gigabyte"]
    widgets['vendors'] = {}
    for v in vendor_list:
        chk = ctk.CTkCheckBox(parent_frame, text=v, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['vendors'][v] = chk

    # --- SOCKET ---
    ctk.CTkLabel(parent_frame, text="Сокет", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    socket_list = ["AM5", "AM4", "LGA1700"] 
    widgets['sockets'] = {}
    for sock in socket_list:
        chk = ctk.CTkCheckBox(parent_frame, text=sock, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['sockets'][sock] = chk

# --- CHIPSET ---
    ctk.CTkLabel(parent_frame, text="Чіпсет", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(5, 2))
    chipset_list = ["B650", "B550", "B660", "B760", "X670", "X670E", "Z690", "Z790"]
    widgets['chipsets'] = {}
    chipset_container = ctk.CTkFrame(parent_frame, height=140, fg_color="transparent")
    chipset_container.pack(fill="x", padx=10, pady=2)
    chipset_container.pack_propagate(False) 
    f_chipsets = ctk.CTkScrollableFrame(chipset_container, fg_color="transparent") 
    f_chipsets.pack(fill="both", expand=True)
    for chip in chipset_list:
        chk = ctk.CTkCheckBox(f_chipsets, text=chip, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=5, pady=1)
        widgets['chipsets'][chip] = chk


    # --- RAM SLOTS ---
    ctk.CTkLabel(parent_frame, text="Слоти ОЗП", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['slots'] = ctk.CTkComboBox(parent_frame, values=["", "2", "4"], width=180, 
                                       fg_color="#FFFFFF", text_color="#000000", dropdown_fg_color="#FFFFFF", dropdown_text_color="#000000", 
                                       button_color="#FFFFFF", button_hover_color="#E0E0E0", border_width=0, command=on_change)
    widgets['slots'].pack(pady=5)
    widgets['slots'].set("")

    # --- FORM FACTOR ---
    ctk.CTkLabel(parent_frame, text="Формфактор", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    ff_list = ["ATX", "mATX", "E-ATX"]
    widgets['ff'] = {}
    for ff in ff_list:
        chk = ctk.CTkCheckBox(parent_frame, text=ff, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['ff'][ff] = chk

    # --- WIFI ---
    ctk.CTkLabel(parent_frame, text="Наявність Wi-Fi", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    widgets['wifi'] = {}
    chk_yes = ctk.CTkCheckBox(parent_frame, text="Так", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    chk_yes.pack(anchor="w", padx=30, pady=2)
    widgets['wifi']['Так'] = chk_yes
    chk_no = ctk.CTkCheckBox(parent_frame, text="Ні", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    chk_no.pack(anchor="w", padx=30, pady=2)
    widgets['wifi']['Ні'] = chk_no

    add_clear_button(parent_frame, reset_command)

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
        # Ціна
        p_min = float(widgets['price_from'].get()) if widgets['price_from'].get() else 0
        p_max = float(widgets['price_to'].get()) if widgets['price_to'].get() else 1000000
        
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
        cost = float(row[8])
        specs_str = row[3]

        if category != "Відеокарта":
            continue
            
        if not (p_min <= cost <= p_max):
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

    # --- ЦІНА ---
    ctk.CTkLabel(parent_frame, text="Ціна, грн", font=("Lato", 20, "bold"), text_color="#FFFFFF").pack(pady=(10, 5))
    f_price = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_price.pack(pady=5)
    widgets['price_from'] = ctk.CTkEntry(f_price, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_from'].pack(side="left", padx=5)
    widgets['price_from'].bind("<KeyRelease>", on_change)
    widgets['price_to'] = ctk.CTkEntry(f_price, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['price_to'].pack(side="left", padx=5)
    widgets['price_to'].bind("<KeyRelease>", on_change)

    # --- ВИРОБНИК ---
    ctk.CTkLabel(parent_frame, text="Виробник чіпа", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(10, 5))
    widgets['vendor_nvidia'] = ctk.CTkCheckBox(parent_frame, text="NVIDIA", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_nvidia'].pack(anchor="w", padx=30, pady=2)
    widgets['vendor_amd'] = ctk.CTkCheckBox(parent_frame, text="AMD", text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
    widgets['vendor_amd'].pack(anchor="w", padx=30, pady=2)

    # --- VRAM ---
    ctk.CTkLabel(parent_frame, text="Відеопам'ять (ГБ)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    vram_options = ["24", "16", "12", "10", "8", "6"]
    widgets['vram'] = {}
    f_vram = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_vram.pack(fill="x", padx=10)
    for i, v in enumerate(vram_options):
        chk = ctk.CTkCheckBox(f_vram, text=f"{v} ГБ", width=60, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        row = i // 2
        col = i % 2
        chk.grid(row=row, column=col, sticky="w", padx=10, pady=5)
        widgets['vram'][v] = chk

    # --- ЧАСТОТА ---
    ctk.CTkLabel(parent_frame, text="Частота (МГц)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    f_freq = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_freq.pack(pady=5)
    widgets['freq_from'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_from'].pack(side="left", padx=5)
    widgets['freq_from'].bind("<KeyRelease>", on_change)
    widgets['freq_to'] = ctk.CTkEntry(f_freq, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['freq_to'].pack(side="left", padx=5)
    widgets['freq_to'].bind("<KeyRelease>", on_change)

    # --- ТЕХНОЛОГІЇ ---
    ctk.CTkLabel(parent_frame, text="Технології", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    tech_list = ["DLSS3", "DLSS2", "RayTracing"]
    widgets['tech'] = {}
    for t in tech_list:
        chk = ctk.CTkCheckBox(parent_frame, text=t, text_color="#FFFFFF", fg_color="#FFFFFF", checkmark_color="#00BFFF", border_color="white", command=on_change)
        chk.pack(anchor="w", padx=30, pady=2)
        widgets['tech'][t] = chk

    # --- TDP ---
    ctk.CTkLabel(parent_frame, text="TDP (Вт)", font=("Lato", 18, "bold"), text_color="#FFFFFF").pack(pady=(15, 5))
    f_tdp = ctk.CTkFrame(parent_frame, fg_color="transparent")
    f_tdp.pack(pady=5)
    widgets['tdp_from'] = ctk.CTkEntry(f_tdp, width=80, placeholder_text="Від", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['tdp_from'].pack(side="left", padx=5)
    widgets['tdp_from'].bind("<KeyRelease>", on_change)
    widgets['tdp_to'] = ctk.CTkEntry(f_tdp, width=80, placeholder_text="До", fg_color="#FFFFFF", text_color="#000000", border_width=0)
    widgets['tdp_to'].pack(side="left", padx=5)
    widgets['tdp_to'].bind("<KeyRelease>", on_change)

    add_clear_button(parent_frame, reset_command)


def update_left_panel(category, left_frame, tree, all_products):
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
            tree.insert("", "end", values=row)
            
        # Перебудовуємо панель (рекурсивний виклик, щоб очистити поля вводу)
        update_left_panel(category, left_frame, tree, all_products)

    # 3. Будуємо нові панелі, передаючи функцію reset_all
    if category == "Процесор":
        build_cpu_sidebar(left_frame, tree, all_products, reset_all)
        
    elif category == "Відеокарта":
        build_gpu_sidebar(left_frame, tree, all_products, reset_all)
        
    elif category == "Материнська плата":
        build_mb_sidebar(left_frame, tree, all_products, reset_all)
        
    else:
        pass


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
# Змінена версія для інтеграції з sidebar
def filter_by_type(combobox, tree, left_frame, all_products) -> None:
    global current_products

    # get choose
    choose = combobox.get()
    
    # --- НОВЕ: Оновлюємо ліву панель ---
    update_left_panel(choose, left_frame, tree, all_products)
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
def search_by_entry(entry_search, tree, all_products) -> None:
    global current_products

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

# Function who open purchase frame
def open_purchase(APP) -> None:
    from Purchase_Frame import Purchase_window
    try:
        for widget in APP.winfo_children():
            widget.destroy()
        Purchase_window(app=APP)
    except:
        print("We have a problem with rework window")
    
def open_supply(APP) -> None:
    from CreateProduct_Frame import Create_product_window
    try:
        for widget in APP.winfo_children():
            widget.destroy()
        Create_product_window(app=APP)
    except:
        print("We have a problem with rework window")

    
def Main_window(*, app: ctk.CTk) -> None:
    global current_products

    app.geometry("1920x1080")
    app.title("Головне меню")
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
        # command=lambda value: filter_by_type(combobox_category,tree_table)
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
        command=lambda: search_by_entry(entry_search,tree_table,all_products)

    )
    button_search.place(relx=0.90, rely=0.5, anchor="center")
    # add hotkey for button search on press "ENTER"
    app.bind("<Return>", lambda event: button_search.invoke())

    # Frame for all buttons
    frame_buttons_sale_supply = ctk.CTkFrame(master=frame_top_widget, fg_color="transparent")
    frame_buttons_sale_supply.place(relx=0.725, rely=0.5, anchor="w")

    # Configure frame
    frame_buttons_sale_supply.columnconfigure(0, weight=1)
    frame_buttons_sale_supply.columnconfigure(1, weight=1)

    # Frame for sale button
    frame_sale_container = ctk.CTkFrame(master=frame_buttons_sale_supply, fg_color="transparent")
    frame_sale_container.grid(row=0, column=0, columnspan=2, pady=(0, 5)) 

    button_sale = ctk.CTkButton(
        master=frame_sale_container,
        text="Продаж",
        width=250,
        height=39,
        corner_radius=5,
        fg_color="#34D399",
        hover_color="#2ECC71",
        font=("Lato", 14, "bold"),
        image=ctk.CTkImage(light_image=Image.open("images/sale.png"), size=(20, 20)),
        compound="right",
        command=lambda: open_purchase(APP=app)
    )
    button_sale.pack()


    # Frame for add button
    frame_add_container = ctk.CTkFrame(master=frame_buttons_sale_supply, fg_color="transparent")
    frame_add_container.grid(row=1, column=1, padx=(5, 0))

    button_create_prod = ctk.CTkButton(
        master=frame_add_container,
        text="Додавання",
        width=115, # Робимо її ширшою, оскільки вона одна в рядку
        height=39,
        corner_radius=5,
        fg_color="#FF3C00",
        hover_color="#E32600",
        font=("Lato", 14, "bold"),
        image=ctk.CTkImage(light_image=Image.open("images/add_prod.png"), size=(20, 20)),
        compound="right"
    )
    button_create_prod.pack()


    # Frame for supply button
    frame_supply_container = ctk.CTkFrame(master=frame_buttons_sale_supply, fg_color="transparent")
    frame_supply_container.grid(row=1, column=0, padx=(0, 0))

    button_supply = ctk.CTkButton(
        master=frame_supply_container,
        text="Постачання",
        width=115,
        height=39,
        corner_radius=5,
        fg_color="#FFB030",
        hover_color="#FF9933",
        font=("Lato", 14, "bold"),
        image=ctk.CTkImage(light_image=Image.open("images/supply.png"), size=(20, 20)),
        compound="right",
        command=lambda: open_supply(APP=app)
    )
    button_supply.pack()

    
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


    # Frame table for product
    frame_table = ctk.CTkFrame(master=app, fg_color="transparent", border_width=1)
    frame_table.pack(side="right", padx=(220,0),pady=(110,0),fill="both", expand=True)
    # allow frame scaling
    frame_table.grid_rowconfigure(0, weight=1) 
    frame_table.grid_columnconfigure(0, weight=1) 
    
    columns = ("id", "name", "model","specs","category","vendor","supplier","available_quantity","cost")
    titles  = ["№","Назва","Модель","Характеристики","Тип категорії","Виробник","Постачальник","В наявності","Ціна товару"]
    # Table for product
    tree_table = ttk.Treeview(master=frame_table,columns=columns, show="headings")
    # add a title to each column
    for col, title in zip(columns, titles):
        tree_table.heading(col, text=title)
    
    tree_table.grid(row=0, column=0, sticky="nsew", padx=(5,0), pady=(5,10))
    
    # Scrollbar for table by Y
    scrollbar_y = ctk.CTkScrollbar(frame_table, orientation="vertical",command=tree_table.yview,height=1)
    scrollbar_y.grid(row=0, column=1, sticky="ns", padx=(0,5), pady=(5,10))

    # Configure scroll bar for table by Y
    tree_table.configure(yscrollcommand=scrollbar_y.set)

    # Style for table
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
            
        # --- НОВЕ: Перепризначаємо команду комбобоксу, тепер коли у нас є всі змінні ---
        combobox_category.configure(
            command=lambda value: filter_by_type(
                combobox_category, 
                tree_table, 
                frame_left_widget, 
                all_products
            )
        )
        # ------------------------------------------------------------------------------

    except:
        print("We have a problem with get data about product in Main_Frame")
