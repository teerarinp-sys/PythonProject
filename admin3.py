import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog, ttk # เพิ่ม ttk สำหรับ Scrollbar
from PIL import Image, ImageTk
import sqlite3
import re
import os
import shutil
import math

# ==============================================================================
# 0. CONFIGURATION & GLOBAL VARIABLES
# ==============================================================================
# ชื่อไฟล์ฐานข้อมูล
DB_NAME = "user_data.db"
# Path รูปภาพพื้นหลัง (ปรับให้เป็น path ที่ถูกต้อง)
PIC_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\"
# Path สำหรับเก็บรูปโปรไฟล์ของผู้ใช้
PROFILE_PICS_DIR = "D:\\Project Nudee\\รูปโปรไฟล์ผู้ใช้\\"
### START: เพิ่มใหม่ ###
# Path สำหรับเก็บรูปเมนูอาหาร
MENU_PICS_DIR = "D:\\Project Nudee\\รูปเมนูอาหาร\\"
# Path สำหรับเก็บสลิปที่ลูกค้าอัปโหลด
SLIP_PICS_DIR = "D:\\Project Nudee\\สลิปโอนเงิน\\"
PIC_CHECKOUT_PAGE ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\payment summary.png"  # <<< รูปสรุปยอด
#รูปหน้าชำระเงิน
PIC_PAYMENT_PAGE ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\pay.png"

# สร้างโฟลเดอร์สำหรับเก็บรูปโปรไฟล์ และ รูปเมนู ถ้ายังไม่มี
os.makedirs(PROFILE_PICS_DIR, exist_ok=True)
os.makedirs(MENU_PICS_DIR, exist_ok=True)
os.makedirs(SLIP_PICS_DIR, exist_ok=True)
### END: เพิ่มใหม่ ###


# ชื่อไฟล์รูปภาพ
PIC_MAIN = "1.png"
PIC_LOGIN = "2.png"
PIC_REGISTER = "3.png"
PIC_TABLE_SELECT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\7 Table.png"
PIC_PROFILE_VIEW ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\5 profile.png"
PIC_PROFILE_EDIT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\6 edit profile.png"
PIC_ABOUT = "about.png"
PIC_FORGOT_PASSWORD = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\4.png"
PIC_ADMIN_PANEL = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin.png"
PIC_ADMIN_TABLE_VIEW = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin table.png"
PIC_ADMIN_MANAGE_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin menu.png" # พื้นหลังหน้าจัดการเมนู
PIC_ADMIN_ADD_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\add menu 6.png" # รูปจากที่คุณอัปโหลด
PIC_ADMIN_EDIT_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\edit menu 7.png" # รูปจากที่คุณอัปโหลด
PIC_ADMIN_STATUS_VIEW = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\Stock.png"
PIC_MENU_PLACEHOLDER = "placeholder.png" # รูป Placeholder เมนู
# --- !! เพิ่ม Path รูปพื้นหลังหน้าเมนูลูกค้า !! ---
PIC_CUSTOMER_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\9 menu.png" 
PIC_CART_PAGE = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\basket.png"

ADMIN_USERNAME = "admineiei"
ADMIN_PASSWORD = "12345678"

# VVV เพิ่มบรรทัดนี้ VVV
VAT_RATE = 0.07  # 7%

# กำหนดค่าสำหรับปุ่มผู้พัฒนา (About Me)
ABOUT_BTN_CONFIG = {
    'text': "•••",
    'font': ("Arial", 23 , "bold"),
    'bg': "#ff88bd",
    'fg': "#552c1f",
    'bd': 0,
    'relief': "ridge",
    'activebackground': "#E3B2C3",
    'x': 901,
    'y': 490,
    'width': 40,
    'height': 30
}

# Global Variables สำหรับการจัดการสถานะและรูปภาพโปรไฟล์
CURRENT_USER = None
CURRENT_WINDOW = None
PROFILE_PIC_REF = {}
TABLE_PIC_REF = {}
MENU_ITEM_PIC_REFS = {} # เก็บ reference รูปเมนู
MENU_FORM_PIC_REF = {} # เก็บ reference รูปเมนูในหน้า Add/Edit
# Global Variable สำหรับเก็บตะกร้าสินค้าชั่วคราว
CURRENT_ORDER = {} 
CURRENT_REDEMPTION = {} 
global bg_image_about
bg_image_about = None
global bg_image_table_select
bg_image_table_select = None
global bg_image_forgot
bg_image_forgot = None
global bg_image_admin_panel
bg_image_admin_panel = None
global bg_image_admin_table_view
bg_image_admin_table_view = None
global bg_image_admin_manage_menu
bg_image_admin_manage_menu = None

### START: เพิ่มใหม่ ###
global bg_image_admin_add_menu
bg_image_admin_add_menu = None
global bg_image_admin_edit_menu
bg_image_admin_edit_menu = None
global bg_image_admin_status_view
bg_image_admin_status_view = None
global bg_image_checkout_page
bg_image_checkout_page = None
global bg_image_cart_page
bg_image_cart_page = None
global bg_image_payment_page
bg_image_payment_page = None
global bg_image_customer_menu 
bg_image_customer_menu = None
### END: เพิ่มใหม่ ###


# ******************************************************************************
# ฟังก์ชัน Utility: load_and_resize_pic, create_db_table
# ******************************************************************************
def load_and_resize_pic(file_path, size, is_menu_item=False): # เพิ่ม is_menu_item
    """โหลดและปรับขนาดรูปภาพ"""
    default_color = '#d3d3d3' if is_menu_item else '#b8828b' # สีเทาสำหรับเมนู
    if file_path and os.path.exists(file_path):
        try:
            # ใช้ convert("RGBA") เพื่อรองรับ PNG ที่โปร่งใส
            img_pil = Image.open(file_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening image {file_path}: {e}")
            img_pil = Image.new('RGB', (size, size), color=default_color) # Placeholder
    else:
        # Placeholder สีเดียว
        img_pil = Image.new('RGB', (size, size), color=default_color)

    # ปรับขนาดให้พอดีกรอบ (อาจบิดเบี้ยวถ้าอัตราส่วนไม่เท่ากัน)
    img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk

def create_db_table():
    """สร้างฐานข้อมูลและตารางต่างๆ หากยังไม่มี"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 1. ตาราง user_account (เหมือนเดิม)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_account (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
                name TEXT, surname TEXT, phone TEXT, birthday TEXT, email TEXT
            )""")

        # 2. ตาราง user_profile (เหมือนเดิม)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                username TEXT PRIMARY KEY, score INTEGER DEFAULT 0,
                profile_pic_path TEXT,
                FOREIGN KEY (username) REFERENCES user_account(username)
            )""")
        cursor.execute("PRAGMA table_info(user_profile)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'profile_pic_path' not in columns:
            try: cursor.execute("ALTER TABLE user_profile ADD COLUMN profile_pic_path TEXT")
            except: pass 

        # --- 3. ตาราง Menu Items (!! แก้ไข !!) ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image_path TEXT,
                is_available INTEGER NOT NULL DEFAULT 1,
                is_recommended INTEGER NOT NULL DEFAULT 0 -- <<< (!! 1. เพิ่มบรรทัดนี้ !!)
            )""")

        cursor.execute("PRAGMA table_info(menu_items)")
        columns_menu = [info[1] for info in cursor.fetchall()]
        
        # (เพิ่ม is_available ถ้ายังไม่มี)
        if 'is_available' not in columns_menu:
            try:
                cursor.execute("ALTER TABLE menu_items ADD COLUMN is_available INTEGER NOT NULL DEFAULT 1")
                print("Added 'is_available' column to menu_items")
            except Exception as e:
                print(f"Could not add 'is_available' column: {e}")
        
        # --- (!! 2. เพิ่มโค้ด ALTER TABLE สำหรับ is_recommended !!) ---
        if 'is_recommended' not in columns_menu:
            try:
                cursor.execute("ALTER TABLE menu_items ADD COLUMN is_recommended INTEGER NOT NULL DEFAULT 0")
                print("Added 'is_recommended' column to menu_items")
            except Exception as e:
                print(f"Could not add 'is_recommended' column: {e}")
        # --- (!! สิ้นสุดส่วนที่เพิ่ม !!) ---

        # 4. ตาราง Orders (เหมือนเดิม)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number INTEGER NOT NULL,
                order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                slip_image_path TEXT,
                customer_username TEXT,
                FOREIGN KEY (customer_username) REFERENCES user_account(username)
            )""")

        # 5. ตาราง Order Details (เหมือนเดิม)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_details (
                detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_item REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
            )""")

        conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถสร้าง/อัปเดตฐานข้อมูลได้: {e}")
    finally:
        if conn: conn.close()

# เรียกใช้ฟังก์ชันสร้างฐานข้อมูลเมื่อโปรแกรมเริ่มต้น
create_db_table()
# ------------------------------------


# ==============================================================================
# 1. NAVIGATION & UTILITY FUNCTIONS
# ==============================================================================
def back_to_main_page(current_window):
    """ฟังก์ชันสำหรับกลับไปหน้าหลัก (root) และออกจากระบบ (ถ้ามี)"""
    global CURRENT_USER
    if CURRENT_USER:
        CURRENT_USER = None # Log out
    current_window.destroy()
    root.deiconify()

# *** ย้ายนิยาม about_page มาไว้ก่อน add_about_button ***
def about_page():
    """ฟังก์ชันสำหรับแสดงหน้า 'ผู้พัฒนาโปรแกรม' (About Me)"""
    about_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - ผู้พัฒนาโปรแกรม")
    global bg_image_about
    try:
        bg_image_about_pil = Image.open(f"{PIC_PATH}{PIC_ABOUT}")
        bg_image_about_pil = bg_image_about_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_about = ImageTk.PhotoImage(bg_image_about_pil)
        background_label_about = tk.Label(about_window, image=bg_image_about)
        background_label_about.image = bg_image_about
        background_label_about.place(x=0, y=0, relwidth=1, relheight=1)
        back_button = tk.Button(about_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50 , "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised", activebackground="#ffe0f1", command=lambda: back_to_main_page(about_window))
        back_button.place(x=790, y=470, width=150, height=45)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพ About Page ได้: {e}")
        about_window.destroy()
        root.deiconify() # กลับหน้าหลักถ้าโหลดรูปไม่ได้

### START: เพิ่มใหม่ (ฟังก์ชันสร้างปุ่มโปรไฟล์จิ๋ว) ###
def add_small_profile_button(parent_window, x=12, y=10, size=45):
    """
    สร้างปุ่มโปรไฟล์จิ๋วบนหน้าต่างที่กำหนด
    เมื่อกดจะไปที่หน้า profile_view_page
    """
    # 1. สร้างกรอบสำหรับปุ่ม
    profile_frame = tk.Frame(parent_window, bg="white", bd=0, relief="flat")
    profile_frame.place(x=x, y=y, width=size, height=size)

    # 2. ดึงข้อมูลผู้ใช้และ Path รูป
    user_data = get_user_data(CURRENT_USER)
    pic_path = user_data.get('profile_pic_path') if user_data else None

    # 3. โหลดรูปภาพ
    img_tk = load_and_resize_pic(pic_path, size)

    # 4. สร้างปุ่ม
    profile_btn = tk.Button(
        profile_frame,
        image=img_tk,
        bd=0,
        relief="flat",
        # (สำคัญ) ส่ง parent_window ไปด้วย เพื่อให้รู้ว่าต้องกลับมาหน้าไหน
        command=lambda: profile_view_page(parent_window) 
    )
    
    # 5. (สำคัญมาก) เก็บ reference ของรูปภาพไว้กับตัวปุ่ม
    profile_btn.image = img_tk 
    
    profile_btn.place(x=0, y=0, width=size, height=size)
### END: เพิ่มใหม่ ###

def add_about_button(parent_window):
    """เพิ่มปุ่มผู้พัฒนา (•••) ลงในหน้าต่างที่กำหนด"""
    about_button = tk.Button(parent_window,
                             text=ABOUT_BTN_CONFIG['text'],
                             font=ABOUT_BTN_CONFIG['font'],
                             bg=ABOUT_BTN_CONFIG['bg'],
                             fg=ABOUT_BTN_CONFIG['fg'],
                             bd=ABOUT_BTN_CONFIG['bd'],
                             relief=ABOUT_BTN_CONFIG['relief'],
                             activebackground=ABOUT_BTN_CONFIG['activebackground'],
                             command=about_page)
    about_button.place(x=ABOUT_BTN_CONFIG['x'],
                       y=ABOUT_BTN_CONFIG['y'],
                       width=ABOUT_BTN_CONFIG['width'],
                       height=ABOUT_BTN_CONFIG['height'])

# ==============================================================================
# 2. DATABASE LOGIC
# ==============================================================================

def get_user_data(username):
    """ ดึงข้อมูลผู้ใช้จาก DB """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.*, p.score, p.profile_pic_path
            FROM user_account a
            LEFT JOIN user_profile p ON a.username = p.username
            WHERE a.username = ?
        """, (username,))
        user_record = cursor.fetchone()
        if user_record:
            return dict(user_record)
        return None
    except Exception as e:
        print(f"Error get_user_data: {e}")
        return None
    finally:
        conn.close()

def update_user_profile(old_username, new_data):
    """ อัปเดตข้อมูลผู้ใช้ใน DB """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE user_account
            SET username = ?, name = ?, surname = ?, phone = ?, birthday = ?, email = ?
            WHERE username = ?
        """, (new_data['username'], new_data['name'], new_data['surname'],
              new_data['phone'], new_data['birthday'], new_data['email'],
              old_username))

        cursor.execute("""
            UPDATE user_profile
            SET username = ?, profile_pic_path = ?
            WHERE username = ?
        """, (new_data['username'], new_data['pic_path'], old_username))

        conn.commit()

        global CURRENT_USER
        if old_username != new_data['username']:
             CURRENT_USER = new_data['username']

        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) ใหม่นี้ถูกใช้ไปแล้ว")
        return False
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not update profile: {e}")
        return False
    finally:
        conn.close()


def get_menu_items_from_db(category):
    """ดึงรายการเมนูจากฐานข้อมูลตามหมวดหมู่"""
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # ---!! แก้ไขบรรทัดนี้ !! ---
        # (เรียงตาม is_available (1 มาก่อน 0) แล้วค่อยเรียงตาม item_id (ใหม่มาก่อนเก่า))
        cursor.execute("SELECT * FROM menu_items WHERE category = ? ORDER BY is_available DESC, item_id DESC", (category,))
        
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch menu items: {e}")
    return items


def copy_menu_image(source_path, item_name):
    """คัดลอกรูปภาพเมนูไปยังโฟลเดอร์และคืนค่า Path ใหม่"""
    if not source_path or not os.path.exists(source_path):
        return None
    try:
        _, extension = os.path.splitext(source_path)
        clean_name = re.sub(r'[\\/*?:"<>|]', "", item_name)
        new_filename = f"{clean_name}{extension}"
        dest_path = os.path.join(MENU_PICS_DIR, new_filename)

        counter = 1
        while os.path.exists(dest_path):
            new_filename = f"{clean_name}_{counter}{extension}"
            dest_path = os.path.join(MENU_PICS_DIR, new_filename)
            counter += 1

        shutil.copy(source_path, dest_path)
        return dest_path
    except Exception as e:
        messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกรูปภาพได้: {e}")
        return None

def db_add_menu_item(name, price, category, image_path, description=""):
    """เพิ่มเมนูใหม่ลงในฐานข้อมูล"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO menu_items (name, description, price, category, image_path)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, price, category, image_path))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("ข้อผิดพลาด", "ชื่อเมนูนี้มีอยู่แล้วในระบบ")
        return False
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถเพิ่มรายการได้: {e}")
        return False
    finally:
        if conn: conn.close()

def db_update_menu_item(item_id, name, price, category, image_path, description=""):
    """อัปเดตข้อมูลเมนูในฐานข้อมูล"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE menu_items
            SET name = ?, description = ?, price = ?, category = ?, image_path = ?
            WHERE item_id = ?
        """, (name, description, price, category, image_path, item_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("ข้อผิดพลาด", "ชื่อเมนูนี้ซ้ำกับรายการอื่น")
        return False
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถอัปเดตรายการได้: {e}")
        return False
    finally:
        if conn: conn.close()

def db_delete_menu_item(item_id):
    """ลบเมนูออกจากฐานข้อมูล"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE item_id = ?", (item_id,))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถลบรายการได้: {e}")
        return False
    finally:
        if conn: conn.close()

def db_update_item_availability(item_id, is_available):
    """อัปเดตสถานะสินค้า (1=มี, 0=หมด)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE menu_items
            SET is_available = ?
            WHERE item_id = ?
        """, (is_available, item_id))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถอัปเดตสถานะได้: {e}")
        return False
    finally:
        if conn: conn.close()

def get_menu_items_by_status_from_db(is_available):
    """ดึงรายการเมนูทั้งหมดตามสถานะ (1=มี, 0=หมด)"""
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # ดึงข้อมูลโดยกรองตามสถานะ และเรียงตามหมวดหมู่/ชื่อ
        cursor.execute("SELECT * FROM menu_items WHERE is_available = ? ORDER BY category, name", (is_available,))
        
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch menu items: {e}")
    return items

def get_recommended_items_from_db():
    """ดึงเฉพาะรายการเมนูที่ติดดาว (is_recommended = 1)"""
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # --- (!! แก้ไข !!) ลบ (1,) ที่ไม่จำเป็นซึ่งทำให้เกิด Error ออก ---
        cursor.execute("SELECT * FROM menu_items WHERE is_recommended = 1 ORDER BY is_available DESC, name")
        
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch recommended items: {e}")
    return items

def db_set_recommend_status(item_id, status):
    """อัปเดตสถานะ "แนะนำ" (1=ใช่, 0=ไม่ใช่)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE menu_items
            SET is_recommended = ?
            WHERE item_id = ?
        """, (status, item_id))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถอัปเดตสถานะแนะนำได้: {e}")
        return False
    finally:
        if conn: conn.close()

def copy_slip_image(source_path, order_id):
    """คัดลอกรูปภาพสลิปไปยังโฟลเดอร์และคืนค่า Path ใหม่"""
    if not source_path or not os.path.exists(source_path):
        return None
    try:
        _, extension = os.path.splitext(source_path)
        new_filename = f"order_{order_id}{extension}"
        dest_path = os.path.join(SLIP_PICS_DIR, new_filename)

        # (ถ้ามีไฟล์ซ้ำ ให้เขียนทับไปเลย)
        shutil.copy(source_path, dest_path)
        return dest_path
    except Exception as e:
        messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกสลิปได้: {e}")
        return None
    
def confirm_payment(order_id, slip_source_path, all_windows):
    """(ฟังก์ชันใหม่) ยืนยันการชำระเงิน, อัปโหลดสลิป, และปิดหน้าต่าง"""
    
    final_slip_path = None
    if slip_source_path:
        # 1. คัดลอกสลิปไปเก็บ
        final_slip_path = copy_slip_image(slip_source_path, order_id)
        if final_slip_path is None:
            messagebox.showwarning("ผิดพลาด", "ไม่สามารถบันทึกสลิปได้ กรุณาลองใหม่")
            return
    else:
        # (ถ้าไม่แนบสลิป ก็อนุญาตให้ยืนยันได้)
        pass 

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 2. อัปเดตสถานะออเดอร์
        cursor.execute("""
            UPDATE orders 
            SET status = 'paid', slip_image_path = ?
            WHERE order_id = ?
        """, (final_slip_path, order_id))
        conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ไม่สามารถยืนยันออเดอร์ได้: {e}")
        if conn: conn.close()
        return
    finally:
        if conn: conn.close()

    # 3. แจ้งเตือนและปิดทุกอย่าง
    messagebox.showinfo("สำเร็จ", "ยืนยันการชำระเงินเรียบร้อย!\nขอบคุณที่ใช้บริการค่ะ")
    
    # (ปิดหน้าต่างทั้งหมด: payment, cart, menu)
    for window in all_windows:
        if window:
            try:
                window.destroy()
            except:
                pass
                
    table_selection_page(None) # กลับไปหน้าเลือกโต๊ะ

# ==============================================================================
# 3. GUI WINDOW CREATION
# ==============================================================================

def create_toplevel_window(title):
    """ฟังก์ชันรวมสำหรับสร้างหน้าต่างย่อย (Toplevel) และซ่อนหน้าหลัก"""
    root.withdraw()
    new_window = tk.Toplevel(root)
    new_window.title(title)
    new_window.geometry("960x540")
    new_window.resizable(True, True) # <<< แก้ไขให้ขยายได้

    new_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(new_window))

    return new_window
# ------------------------------------
# (หน้า 7: เลือกโต๊ะ - ลูกค้า)
# ------------------------------------
def table_selection_page(prev_window=None):
    if prev_window: prev_window.destroy()
    global CURRENT_WINDOW
    table_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - เลือกโต๊ะ")
    CURRENT_WINDOW = table_window
    global bg_image_table_select
    try:
        bg_image_table_select_pil = Image.open(PIC_TABLE_SELECT)
        bg_image_table_select_pil = bg_image_table_select_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_table_select = ImageTk.PhotoImage(bg_image_table_select_pil)
        background_label_table = tk.Label(table_window, image=bg_image_table_select)
        background_label_table.image = bg_image_table_select
        background_label_table.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        table_window.destroy()
        root.deiconify()
        return

    selected_table = tk.StringVar(value=None)
    table_buttons = {} 
    original_button_bg = "#ffe0f1"
    selected_button_bg = "#ffb3d1"

    def select_table(table_num):
        selected_table.set(table_num)
        print(f"เลือกโต๊ะ: {table_num}")
        for num, btn in table_buttons.items():
            if num != table_num:
                btn.config(bg=original_button_bg, relief="raised")
            else:
                btn.config(bg=selected_button_bg, relief="sunken")

    button_width = 160
    button_height = 150
    y1 = 60
    y2 = 270 
    
    table_coords = [
        (115, y1), (305, y1), (495, y1), (685, y1),  # แถว 1: โต๊ะ 1-4
        (115, y2), (305, y2), (495, y2), (685, y2)   # แถว 2: โต๊ะ 5-8
    ]

    for i, (x, y) in enumerate(table_coords):
        table_num = i + 1 
        btn = tk.Button(table_window, text=f"โต๊ะ {table_num}", font=("UID SALMON 2019", 70),
                        bg=original_button_bg, fg="#552c1f",  bd=2 , relief="solid", 
                        command=lambda num=table_num: select_table(num))
        btn.place(x=x, y=y, width=button_width , height=button_height) 
        table_buttons[table_num] = btn 

    back_button = tk.Button(table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50,"bold" ), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: back_to_main_page(table_window))
    back_button.place(x=315, y=460, width=140, height=49)
    next_button = tk.Button(table_window, text="ต่อไป", font=("UID SALMON 2019", 50,"bold" ), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: open_menu_page(table_window, selected_table.get()))
    next_button.place(x=490, y=460, width=140, height=49)
    
    ### START: เรียกใช้ฟังก์ชันแสดงรูปจิ๋ว ###
    add_small_profile_button(table_window)
    ### END: เรียกใช้ฟังก์ชันแสดงรูปจิ๋ว ###

    add_about_button(table_window) # <<< (!!!) ลบอันที่ซ้ำออกแล้ว (!!!)
    
### START: แก้ไข ฟังก์ชัน open_menu_page ###
def open_menu_page(current_window, selected_table):
    if not selected_table or selected_table == 'None':
        messagebox.showwarning("ยังไม่ได้เลือก", "กรุณาเลือกโต๊ะก่อนดำเนินการต่อ")
        return
    current_window.destroy()
    customer_menu_page(selected_table) # <<< เรียกหน้าเมนูของลูกค้า
### END: แก้ไข ฟังก์ชัน open_menu_page ###

# ------------------------------------
# (หน้า 5: โปรไฟล์ View Mode)
# ------------------------------------
def profile_view_page(prev_window, user_data=None):
    global PROFILE_PIC_REF
    if not user_data:
        if CURRENT_USER: user_data = get_user_data(CURRENT_USER)
        else:
             messagebox.showerror("ข้อผิดพลาด", "ไม่พบเซสชันผู้ใช้ กรุณาเข้าสู่ระบบใหม่")
             if prev_window: prev_window.destroy()
             root.deiconify()
             return
    if not user_data:
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลผู้ใช้ กรุณาเข้าสู่ระบบใหม่")
        if prev_window: prev_window.destroy()
        root.deiconify()
        return
    if prev_window: prev_window.destroy()
    profile_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - โปรไฟล์")
    try:
        bg_image_profile_pil = Image.open(PIC_PROFILE_VIEW)
        bg_image_profile_pil = bg_image_profile_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_profile = ImageTk.PhotoImage(bg_image_profile_pil)
        background_label_profile = tk.Label(profile_window, image=bg_image_profile)
        background_label_profile.image = bg_image_profile
        background_label_profile.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        profile_window.destroy()
        root.deiconify()
        return
    def display_profile_pic(window, pic_path):
        x_pos, y_pos, size = 100, 135, 180
        frame = tk.Frame(window, bg='white', width=size, height=size, bd=0)
        frame.place(x=x_pos, y=y_pos)
        img_tk = load_and_resize_pic(pic_path, size)
        PROFILE_PIC_REF['pic_view'] = img_tk
        pic_label = tk.Label(frame, image=img_tk, bd=0)
        pic_label.place(x=0, y=0, relwidth=1, relheight=1)
        return pic_label
    font_style = ("Arial", 20)
    text_color = "#e37494"
    tk.Label(profile_window, text=f"{user_data.get('username', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=145, y=350, width=120 , height= 30)
    name_full = f"{user_data.get('name', '-')} {user_data.get('surname', '-')}"
    tk.Label(profile_window, text=name_full, font=font_style, fg=text_color, bg="#ffe0f1").place(x=490, y=154, width=150 , height= 30)
    tk.Label(profile_window, text=f"{user_data.get('phone', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=430, y=220, width=150 , height= 30)
    tk.Label(profile_window, text=f"{user_data.get('birthday', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=410, y=280, width=165 , height= 30)
    tk.Label(profile_window, text=f"{user_data.get('email', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=410, y=330, width=300 , height= 30)
    tk.Label(profile_window, text=f" {user_data.get('score', 0)}", font=font_style, fg="#552c1f", bg="#ffe0f1").place(x=520, y=395, width=100 , height= 30)
    display_profile_pic(profile_window, user_data.get('profile_pic_path')) # <<< แก้ไข Key
    edit_button = tk.Button(profile_window, text="แก้ไข", font=("UID SALMON 2019", 35, "bold"), bg="#fffbf2", fg="#552c1f", bd=0, relief="flat", command=lambda: profile_edit_page(profile_window, user_data))
    edit_button.place(x=799, y=86, width=70, height=38)
    back_button = tk.Button(profile_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: table_selection_page(profile_window))
    back_button.place(x=300, y=440, width=150, height=70)
    logout_button = tk.Button(profile_window, text="ออกจากระบบ", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: back_to_main_page(profile_window))
    logout_button.place(x=525, y=440, width=150, height=70)
    add_about_button(profile_window)

# ------------------------------------
# (หน้า 6: โปรไฟล์ Edit Mode)
# ------------------------------------
def profile_edit_page(prev_window, user_data):
    global PROFILE_PIC_REF
    prev_window.destroy()
    edit_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - แก้ไขโปรไฟล์")
    try:
        bg_image_edit_pil = Image.open(PIC_PROFILE_EDIT)
        bg_image_edit_pil = bg_image_edit_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_edit = ImageTk.PhotoImage(bg_image_edit_pil)
        background_label_edit = tk.Label(edit_window, image=bg_image_edit)
        background_label_edit.image = bg_image_edit
        background_label_edit.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        edit_window.destroy()
        root.deiconify()
        return
    username_var = tk.StringVar(value=user_data.get('username', ''))
    name_var = tk.StringVar(value=user_data.get('name', ''))
    surname_var = tk.StringVar(value=user_data.get('surname', ''))
    phone_var = tk.StringVar(value=user_data.get('phone', ''))
    birthday_var = tk.StringVar(value=user_data.get('birthday', ''))
    email_var = tk.StringVar(value=user_data.get('email', ''))
    current_pic_path = tk.StringVar(value=user_data.get('profile_pic_path', '')) # <<< แก้ไข Key
    pic_label_ref = None
    pic_frame_ref = None
    def display_profile_pic(window, pic_path_var):
        nonlocal pic_label_ref, pic_frame_ref
        x_pos, y_pos, size = 100, 130, 180
        pic_path = pic_path_var.get()
        if pic_frame_ref:
            pic_frame_ref.destroy()
        frame = tk.Frame(window, bg='white', width=size, height=size, bd=0)
        frame.place(x=x_pos, y=y_pos)
        pic_frame_ref = frame
        img_tk = load_and_resize_pic(pic_path, size)
        PROFILE_PIC_REF['edit_pic'] = img_tk
        pic_label = tk.Label(frame, image=img_tk, bd=0)
        pic_label.place(x=0, y=0, relwidth=1, relheight=1)
        pic_label_ref = pic_label
        return pic_label
    def choose_profile_pic():
        source_path = filedialog.askopenfilename(
            title="เลือกรูปโปรไฟล์",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            try:
                _, extension = os.path.splitext(source_path)
                username = user_data['username']
                new_filename = f"{username}{extension}"
                dest_path = os.path.join(PROFILE_PICS_DIR, new_filename)
                shutil.copy(source_path, dest_path)
                current_pic_path.set(dest_path)
                display_profile_pic(edit_window, current_pic_path)
            except Exception as e:
                messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกรูปภาพได้: {e}")
    entry_font = ("Arial", 16)
    bg_color_entry = "#ffffff"
    tk.Entry(edit_window, textvariable=name_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=500, y=154, width=150, height=30)
    tk.Entry(edit_window, textvariable=surname_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=690, y=154, width= 150, height=30)
    tk.Entry(edit_window, textvariable=phone_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=450, y=220, width=150, height=30)
    tk.Entry(edit_window, textvariable=birthday_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=430, y=280, width=130 , height= 30)
    tk.Entry(edit_window, textvariable=email_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=430, y=330, width=190, height=30)
    username_entry = tk.Entry(edit_window, textvariable=username_var, font=entry_font, bg=bg_color_entry, bd=0)
    username_entry.place(x=170, y=350, width=100, height=30)
    display_profile_pic(edit_window, current_pic_path)
    change_pic_button = tk.Button(edit_window, text="เปลี่ยน", font=("UID SALMON 2019", 16, "bold"),
                                  bg="#ffffff", fg="#552c1f", bd=0, relief="flat",
                                  command=choose_profile_pic)
    change_pic_button.place(x=143, y=314, width=90, height=17)
    def save_changes():
        email = email_var.get()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
            return
        new_username = username_var.get()
        if not new_username:
            messagebox.showerror("ผิดพลาด", "กรุณากรอกชื่อผู้ใช้")
            return
        new_data = {
            'username': new_username, 'name': name_var.get(), 'surname': surname_var.get(),
            'phone': phone_var.get(), 'birthday': birthday_var.get(), 'email': email,
            'pic_path': current_pic_path.get()
        }
        if update_user_profile(user_data['username'], new_data):
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            updated_user_data = get_user_data(CURRENT_USER)
            profile_view_page(edit_window, updated_user_data)
    back_button = tk.Button(edit_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: profile_view_page(edit_window, user_data))
    back_button.place(x=300, y=440, width=150, height=70)
    save_button = tk.Button(edit_window, text="บันทึก", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=save_changes)
    save_button.place(x=525, y=440, width=150, height=70)
    add_about_button(edit_window)

# (!!!) โค้ดที่วางผิดที่ ถูกย้ายออกจากตรงนี้แล้ว (!!!)

### START: เพิ่มใหม่ (Placeholder สำหรับเพิ่มรายการอาหาร) ###
def add_item_to_order(item, table_num):
    """เพิ่มสินค้าลงในตะกร้า (CURRENT_ORDER)"""
    global CURRENT_ORDER
    item_id = item['item_id']
    
    if item_id in CURRENT_ORDER:
        # ถ้ามีอยู่แล้ว, เพิ่มจำนวน
        CURRENT_ORDER[item_id]['quantity'] += 1
    else:
        # ถ้ายังไม่มี, เพิ่มใหม่
        CURRENT_ORDER[item_id] = {
            'name': item['name'],
            'price': item['price'],
            'quantity': 1
        }
            
    # แสดงข้อความยืนยัน
    messagebox.showinfo("เพิ่มรายการ", f"เพิ่ม '{item['name']}' 1 รายการ ลงในตะกร้าแล้ว")
    print(f"โต๊ะ {table_num} ตะกร้าปัจจุบัน: {CURRENT_ORDER}") # (สำหรับ Debug)
### END: เพิ่มใหม่ ###

### START: (ระบบหน้าตะกร้าสินค้า) ###
def submit_order(menu_window, cart_window, checkout_window, table_num):
    """บันทึกออเดอร์ลงฐานข้อมูล (พร้อมระบบคะแนนสะสม)"""
    global CURRENT_ORDER, CURRENT_USER, CURRENT_REDEMPTION
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        total_amount = 0
        for item in CURRENT_ORDER.values():
            total_amount += item['price'] * item['quantity']
        
        points_used = CURRENT_REDEMPTION.get('points_used', 0)
        discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)
        
        # VVV --- (แก้ไข) ยอดรวมสุทธิ คือยอดนี้เลย (แบบ VAT Inclusive) --- VVV
        grand_total = total_amount - discount_amount
        # ^^^ -------------------------------------------------------- ^^^
        
        cursor.execute("""
            INSERT INTO orders (table_number, total_amount, customer_username, status)
            VALUES (?, ?, ?, 'pending')
        """, (table_num, grand_total, CURRENT_USER)) # <-- (ยอดนี้ถูกต้องแล้ว)
        
        new_order_id = cursor.lastrowid

        order_details_data = []
        for item_id, item_data in CURRENT_ORDER.items():
            order_details_data.append((
                new_order_id,
                item_id,
                item_data['quantity'],
                item_data['price']
            ))
        
        cursor.executemany("""
            INSERT INTO order_details (order_id, item_id, quantity, price_per_item)
            VALUES (?, ?, ?, ?)
        """, order_details_data)

        if points_used > 0:
            cursor.execute("UPDATE user_profile SET score = score - ? WHERE username = ?", (points_used, CURRENT_USER))

        # (แก้ไข: คำนวณคะแนนจากยอด grand_total)
        points_earned = int(grand_total // 100) 
        if points_earned > 0:
            cursor.execute("UPDATE user_profile SET score = score + ? WHERE username = ?", (points_earned, CURRENT_USER))

        conn.commit()
        
        # --- (!! แก้ไข !!) ---
        # 1. เปิดหน้าชำระเงิน
        payment_page(menu_window, cart_window, checkout_window, new_order_id, grand_total) # <-- (ยอดนี้ถูกต้องแล้ว)
        
        # 2. ล้างตะกร้า
        CURRENT_ORDER.clear()
        CURRENT_REDEMPTION.clear()
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ไม่สามารถบันทึกออเดอร์ได้: {e}")
    finally:
        if conn: conn.close()

global slip_photo_tk
slip_photo_tk = None

def payment_page(menu_window, cart_window, checkout_window, order_id, final_total):
    """(ฟังก์ชันใหม่) แสดงหน้าชำระเงิน QR Code และแนบสลิป"""
    
    if checkout_window:
        checkout_window.withdraw() # ซ่อนหน้าสรุปยอด

    global bg_image_payment_page
    
    payment_window = tk.Toplevel(root)
    payment_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - ยืนยันออเดอร์ #{order_id}")
    payment_window.geometry("960x540")
    payment_window.resizable(True, True)

    slip_path_var = tk.StringVar(value="") 

    def go_back_to_checkout():
        """ย้อนกลับไปหน้าสรุปยอด (ออเดอร์ยัง pending)"""
        payment_window.destroy()
        if checkout_window:
            checkout_window.deiconify() # เปิดหน้าสรุปยอดที่ซ่อนไว้

    payment_window.protocol("WM_DELETE_WINDOW", go_back_to_checkout)

    # (โค้ดโหลดพื้นหลัง เหมือนเดิม)
    try:
        bg_image_pil = Image.open(PIC_PAYMENT_PAGE)
        bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_payment_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(payment_window, image=bg_image_payment_page)
        background_label.image = bg_image_payment_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_PAYMENT_PAGE}")
        payment_window.config(bg="#ffd7e8")

    # --- (!! NEW !!) แสดงยอดรวม (ในกรอบชมพูตามดีไซน์) ---
    total_frame = tk.Frame(payment_window, bg="#fff0f5", bd=2, relief="solid")
    # (ปรับพิกัดและขนาดตามรูป 015816.png)
    total_frame.place(x=550, y=160, width=350, height=80) 
    
    total_label = tk.Label(total_frame, text=f"ราคารวมทั้งสิ้น\n{final_total:.2f} บาท",
                            font=("Arial", 24, "bold"), bg="#fff0f5", fg="#552c1f")
    total_label.pack(pady=5)
    
    
# --- (!! 1. ฟังก์ชันสำหรับปุ่มแนบสลิป/แสดงสลิป !!) ---
   # --- (!! NEW !!) ฟังก์ชันสำหรับปุ่มแนบสลิป/แสดงสลิป !!) ---
    def choose_slip(event): # ต้องมี event เพราะเราผูกกับ bind
        global slip_photo_tk
        
        source_path = filedialog.askopenfilename(
            title="เลือกไฟล์สลิป",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            slip_path_var.set(source_path)
            
            try:
                # 1. โหลดรูปภาพด้วย PIL
                slip_image_pil = Image.open(source_path)
                
                # VVVV --- NEW: ปรับขนาดตามสัดส่วน (Proportional Resize) --- VVVV
                # พื้นที่แสดงผล: 350x180 (หัก padding)
                frame_width = 350
                frame_height = 250
                original_w, original_h = slip_image_pil.size
                
                # คำนวณอัตราส่วนการย่อให้พอดีกรอบ
                ratio = min(frame_width / original_w, frame_height / original_h)
                
                new_w = int(original_w * ratio)
                new_h = int(original_h * ratio)

                slip_image_pil = slip_image_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
                # ^^^^ ------------------------------------------------------ ^^^^
                
                # 3. แปลงเป็น PhotoImage ของ Tkinter
                slip_photo_tk = ImageTk.PhotoImage(slip_image_pil)
                
                # 4. แสดงรูปภาพใน Label ที่เตรียมไว้ (และลบข้อความเก่าออก)
                slip_label_display.config(image=slip_photo_tk, text="") 
                slip_label_display.image = slip_photo_tk # (สำคัญ: เก็บ reference)
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดไฟล์สลิปได้: {e}")
                slip_path_var.set("")
                slip_label_display.config(image="", text="ไฟล์สลิปไม่ถูกต้อง", font=("Arial", 16))
                slip_photo_tk = None

        else:
            slip_path_var.set("")
            slip_label_display.config(image="", text="แนบหลักฐานการโอน", font=("Arial", 20, "bold")) 
            slip_photo_tk = None


    # --- (!! 2. Label ขนาดใหญ่ที่ทำหน้าที่เป็นปุ่มและช่องแสดงผล !!) ---
    slip_label_display = tk.Label(payment_window, 
                                  text="แนบหลักฐานการโอน", 
                                  font=("Arial", 20, "bold"),
                                  bg="#fff0f5", 
                                  fg="#552c1f", 
                                  bd=2, 
                                  relief="solid",
                                  wraplength=330,
                                  justify="center")
    
    # *** ทำให้ Label นี้ "คลิกได้" โดยผูกกับฟังก์ชัน choose_slip ***
    slip_label_display.bind("<Button-1>", choose_slip) 
    
    # (ปรับพิกัด x, y, width, height)
    slip_label_display.place(x=550, y=260, width=350, height=250)

def cart_page(prev_window, table_num):
    """แสดงหน้าตะกร้าสินค้า (พร้อมระบบแลกคะแนน)"""
    if prev_window:
        prev_window.withdraw() 

    global bg_image_cart_page, CURRENT_ORDER, CURRENT_REDEMPTION
    
    cart_window = tk.Toplevel(root)
    cart_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {table_num} - ตะกร้า")
    cart_window.geometry("960x540")
    cart_window.resizable(True, True)

    def go_back_to_menu():
        global CURRENT_REDEMPTION
        CURRENT_REDEMPTION.clear() 
        cart_window.destroy()
        if prev_window:
            prev_window.deiconify()
        else:
            customer_menu_page(table_num) 

    cart_window.protocol("WM_DELETE_WINDOW", go_back_to_menu)

    # (โค้ดโหลดพื้นหลัง เหมือนเดิม)
    try:
        bg_image_pil = Image.open(PIC_CART_PAGE)
        bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_cart_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(cart_window, image=bg_image_cart_page)
        background_label.image = bg_image_cart_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CART_PAGE}")
        cart_window.config(bg="#ffd7e8")
    
    # (โค้ดสร้าง Canvas, Scrollbar, Frames เหมือนเดิม)
    list_frame_bg = tk.Frame(cart_window, bg="#fff0f5", bd=2, relief="solid")
    list_frame_bg.place(x=90, y=140, width=780, height=300)
    list_canvas = tk.Canvas(list_frame_bg, bg="#fff0f5", bd=0, highlightthickness=0)
    list_scrollbar = ttk.Scrollbar(list_frame_bg, orient="vertical", command=list_canvas.yview)
    list_scrollable_frame = tk.Frame(list_canvas, bg="#fff0f5")
    list_scrollable_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    def _on_mousewheel_cart(event):
        if os.name == 'nt' or os.name == 'posix':
             list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    list_canvas.bind_all("<MouseWheel>", _on_mousewheel_cart)
    list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw", width=740)
    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    list_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    list_scrollbar.pack(side="right", fill="y")
    total_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
    points_to_use_var = tk.StringVar(value="0")

    def update_cart_quantity_internal(item_id, change):
        global CURRENT_ORDER
        if item_id in CURRENT_ORDER:
            CURRENT_ORDER[item_id]['quantity'] += change
            if CURRENT_ORDER[item_id]['quantity'] <= 0:
                del CURRENT_ORDER[item_id]
        refresh_cart_display()

    def apply_points(total_price, current_score):
        global CURRENT_REDEMPTION
        try:
            points_to_use = int(points_to_use_var.get())
        except ValueError:
            messagebox.showwarning("ผิดพลาด", "กรุณากรอกคะแนนเป็นตัวเลข")
            points_to_use_var.set("0")
            return
        if points_to_use < 0:
            messagebox.showwarning("ผิดพลาด", "ไม่สามารถใช้คะแนนติดลบได้")
            points_to_use_var.set("0")
            return
        if points_to_use > current_score:
            messagebox.showwarning("คะแนนไม่พอ", f"คุณมีคะแนนสะสมเพียง {current_score} คะแนน")
            points_to_use_var.set(str(current_score))
            return
        if points_to_use % 10 != 0:
            messagebox.showwarning("เงื่อนไข", "กรุณาใช้คะแนนทีละ 10 คะแนน\n(เช่น 10, 20, 30, ...)")
            return
        discount_amount = (points_to_use / 10) * 25
        if discount_amount > total_price:
            messagebox.showwarning("ส่วนลดเกิน", f"ส่วนลด ({discount_amount} บ.) มากกว่ายอดรวม ({total_price} บ.)\nระบบจะใช้ส่วนลดสูงสุดเท่าที่ทำได้")
            max_discount_groups = int(total_price // 25) 
            points_to_use = max_discount_groups * 10
            discount_amount = max_discount_groups * 25
            points_to_use_var.set(str(points_to_use))
        CURRENT_REDEMPTION['points_used'] = points_to_use
        CURRENT_REDEMPTION['discount_amount'] = discount_amount
        refresh_cart_display()

    def refresh_cart_display():
        # (โค้ด refresh_cart_display ทั้งหมด เหมือนเดิมเป๊ะ)
        for widget in list_scrollable_frame.winfo_children():
            widget.destroy()
        row_font = ("Arial", 16)
        total_price = 0
        header_frame = tk.Frame(list_scrollable_frame, bg="#ffc1e0")
        header_frame.grid_columnconfigure(0, weight=3, minsize=250)
        header_frame.grid_columnconfigure(1, weight=1, minsize=100)
        header_frame.grid_columnconfigure(2, weight=1, minsize=120)
        header_frame.grid_columnconfigure(3, weight=2, minsize=150)
        header_font = ("Arial", 16, "bold")
        header_fg = "#552c1f"
        tk.Label(header_frame, text="เมนู", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(header_frame, text="ราคา/หน่วย", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=5)
        tk.Label(header_frame, text="จำนวน", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="center").grid(row=0, column=2, padx=10, pady=5)
        tk.Label(header_frame, text="รวม", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=5)
        header_frame.pack(fill="x", pady=(0, 5))
        if not CURRENT_ORDER:
            tk.Label(list_scrollable_frame, text="ตะกร้าของคุณว่าง", font=("Arial", 20, "bold"), bg="#fff0f5", fg="#552c1f").pack(pady=50)
        for item_id, item_data in CURRENT_ORDER.items():
            item_total = item_data['price'] * item_data['quantity']
            total_price += item_total
            row_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
            row_frame.grid_columnconfigure(0, weight=3, minsize=250)
            row_frame.grid_columnconfigure(1, weight=1, minsize=100)
            row_frame.grid_columnconfigure(2, weight=1, minsize=120)
            row_frame.grid_columnconfigure(3, weight=2, minsize=150)
            tk.Label(row_frame, text=item_data['name'], font=row_font, bg="#fff0f5", fg="#552c1f", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=2)
            tk.Label(row_frame, text=f"{item_data['price']:.2f} บ.", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=2)
            control_frame = tk.Frame(row_frame, bg="#fff0f5")
            minus_btn = tk.Button(control_frame, text="-", font=("Arial", 16, "bold"), bg="#ffc1e0", fg="#552c1f", bd=0, relief="solid", width=2,
                                command=lambda i=item_id: update_cart_quantity_internal(i, -1))
            minus_btn.pack(side="left", padx=5)
            tk.Label(control_frame, text=f"{item_data['quantity']}", font=row_font, bg="#fff0f5", fg="#552c1f", width=2).pack(side="left", padx=5)
            plus_btn = tk.Button(control_frame, text="+", font=("Arial", 16, "bold"), bg="#bfffcb", fg="#552c1f", bd=0, relief="solid", width=2,
                               command=lambda i=item_id: update_cart_quantity_internal(i, 1))
            plus_btn.pack(side="left", padx=5)
            control_frame.grid(row=0, column=2, padx=10, pady=2) 
            tk.Label(row_frame, text=f"{item_total:.2f} บาท", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=2)
            row_frame.pack(fill="x")
        redeem_frame = tk.Frame(list_scrollable_frame, bg="#fff8fa", bd=1, relief="solid")
        redeem_frame.pack(fill="x", pady=10, padx=10)
        user_data = get_user_data(CURRENT_USER)
        current_score = user_data.get('score', 0)
        tk.Label(redeem_frame, text=f"คุณมี {current_score} คะแนน", font=("Arial", 14, "bold"), bg="#fff8fa", fg="#552c1f").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        points_entry = tk.Entry(redeem_frame, textvariable=points_to_use_var, font=("Arial", 14), width=8, justify="center")
        points_entry.grid(row=0, column=1, padx=10, pady=5)
        redeem_btn = tk.Button(redeem_frame, text="ใช้คะแนน", font=("Arial", 12, "bold"), bg="#fff0b1", fg="#552c1f",
                             command=lambda: apply_points(total_price, current_score))
        redeem_btn.grid(row=0, column=2, padx=10, pady=5)
        tk.Label(redeem_frame, text="(ทุก 10 คะแนน = 25 บ.)", font=("Arial", 10), bg="#fff8fa", fg="#552c1f").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        redeem_frame.grid_columnconfigure(3, weight=1)
        total_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
        total_frame.pack(fill="x", side="bottom", pady=10) 
        total_font = ("Arial", 20, "bold")
        if total_price > 0:
            discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)
            final_total = total_price - discount_amount
            tk.Label(total_frame, text=f"รวม {total_price:.2f} บาท", font=total_font, bg="#fff0f5", fg="#552c1f", anchor="e").pack(fill="x", padx=20)
            if discount_amount > 0:
                tk.Label(total_frame, text=f"ส่วนลดคะแนน -{discount_amount:.2f} บาท", font=("Arial", 16, "bold"), bg="#fff0f5", fg="green", anchor="e").pack(fill="x", padx=20)
                tk.Label(total_frame, text=f"ยอดสุทธิ {final_total:.2f} บาท", font=total_font, bg="#fff0f5", fg="#552c1f", anchor="e").pack(fill="x", padx=20)
        list_scrollable_frame.update_idletasks()
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    # --- ปุ่ม ย้อนกลับ / สั่งซื้อ ---
    back_btn = tk.Button(cart_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                         bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                         command=go_back_to_menu)
    back_btn.place(x=290, y=460, width=150, height=60)

    # --- (!! 1. แก้ไขปุ่ม "ส่งคำสั่งซื้อ" !!) ---
    submit_btn = tk.Button(cart_window, text="ส่งคำสั่งซื้อ", font=("UID SALMON 2019", 40, "bold"),
                           bg="#bfffcb", fg="#552c1f", bd=1 , relief="solid",
                           # (เปลี่ยน command ให้ไปหน้า checkout_summary_page)
                           command=lambda: checkout_summary_page(prev_window, cart_window, table_num))
    submit_btn.place(x=510, y=460, width=150, height=60)

    add_about_button(cart_window)
    refresh_cart_display()

def checkout_summary_page(menu_window, cart_window, table_num):
    """(ฟังก์ชันใหม่) แสดงหน้าสรุปยอด (รูป 165551.png)"""
    
    if cart_window:
        cart_window.withdraw() # ซ่อนหน้าตะกร้า

    global bg_image_checkout_page, CURRENT_ORDER, CURRENT_REDEMPTION
    
    checkout_window = tk.Toplevel(root)
    checkout_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {table_num} - สรุปยอด")
    checkout_window.geometry("960x540")
    checkout_window.resizable(True, True)

    def go_back_to_cart():
        """ย้อนกลับไปหน้าตะกร้า"""
        checkout_window.destroy()
        if cart_window:
            cart_window.deiconify()

    checkout_window.protocol("WM_DELETE_WINDOW", go_back_to_cart)

    # --- โหลดพื้นหลัง ---
    try:
        bg_image_pil = Image.open(PIC_CHECKOUT_PAGE) # <<< ใช้รูปใหม่
        bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_checkout_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(checkout_window, image=bg_image_checkout_page)
        background_label.image = bg_image_checkout_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CHECKOUT_PAGE}")
        checkout_window.config(bg="#ffd7e8")
    
    # --- สร้างกรอบสำหรับรายการสินค้า (คล้ายๆ ตะกร้า) ---
    list_frame_bg = tk.Frame(checkout_window, bg="#fff0f5", bd=2, relief="solid")
    list_frame_bg.place(x=90, y=140, width=780, height=300) # (ปรับพิกัดตามดีไซน์)
    
    list_canvas = tk.Canvas(list_frame_bg, bg="#fff0f5", bd=0, highlightthickness=0)
    list_scrollbar = ttk.Scrollbar(list_frame_bg, orient="vertical", command=list_canvas.yview)
    list_scrollable_frame = tk.Frame(list_canvas, bg="#fff0f5")

    list_scrollable_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    def _on_mousewheel_checkout(event):
         list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    list_canvas.bind_all("<MouseWheel>", _on_mousewheel_checkout)

    list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw", width=740)
    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    list_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    list_scrollbar.pack(side="right", fill="y")

    # --- วาดรายการสินค้า (แบบไม่มีปุ่ม +/-) ---
    row_font = ("Arial", 16)
    total_price = 0
    
    for item_id, item_data in CURRENT_ORDER.items():
        item_total = item_data['price'] * item_data['quantity']
        total_price += item_total
        
        row_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
        row_frame.grid_columnconfigure(0, weight=3, minsize=250)
        row_frame.grid_columnconfigure(1, weight=1, minsize=100)
        row_frame.grid_columnconfigure(2, weight=1, minsize=120)
        row_frame.grid_columnconfigure(3, weight=2, minsize=150)
        
        # คอลัมน์ 1: ชื่อ
        tk.Label(row_frame, text=item_data['name'], font=row_font, bg="#fff0f5", fg="#552c1f", anchor="w").grid(row=0, column=0, sticky="w", padx=10)
        # คอลัมน์ 2: ราคา
        tk.Label(row_frame, text=f"{item_data['price']:.2f} บ.", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        # คอลัมน์ 3: จำนวน
        tk.Label(row_frame, text=f"x {item_data['quantity']}", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="center").grid(row=0, column=2, padx=10)
        # คอลัมน์ 4: ราคารวม
        tk.Label(row_frame, text=f"{item_total:.2f} บาท", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=3, sticky="e", padx=20)
        
        row_frame.pack(fill="x", pady=2)
        
        # เพิ่มเส้นประ (ถ้าต้องการ)
        ttk.Separator(list_scrollable_frame, orient='horizontal').pack(fill='x', padx=10)

    # --- สรุปยอดรวม (ดึงจาก Global) ---
# --- สรุปยอดรวม (ดึงจาก Global) ---
    summary_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
    summary_frame.pack(fill="x", side="bottom", pady=20, padx=20)

    # VVV --- คำนวณ VAT (แบบรวมในราคาแล้ว) --- VVV
    discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)

    # grand_total คือยอดที่ลูกค้าต้องจ่ายจริง (ราคารวม - ส่วนลด)
    grand_total = total_price - discount_amount

# คำนวณย้อนกลับ
    total_before_vat = grand_total / (1 + VAT_RATE)
    vat_amount = grand_total - total_before_vat
    # ^^^ --------------------------------- ^^^

    summary_font = ("Arial", 18, "bold")
    summary_font_small = ("Arial", 16, "bold")
    detail_font = ("Arial", 12) # (ฟอนต์ตัวเล็กสำหรับรายละเอียด)

    # แถว 0: รวมเป็นเงิน (ก่อนส่วนลด)
    tk.Label(summary_frame, text="รวมเป็นเงิน", font=summary_font_small, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"{total_price:.2f} บาท", font=summary_font_small, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5)

    # แถว 1: ส่วนลด
    tk.Label(summary_frame, text="ส่วนลด", font=summary_font_small, bg="#fff0f5", fg="green", anchor="e").grid(row=1, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"-{discount_amount:.2f} บาท", font=summary_font_small, bg="#fff0f5", fg="green", anchor="e").grid(row=1, column=1, sticky="e", padx=5)
    
    # แถว 2: ยอดก่อน VAT (ตัวเล็ก)
    tk.Label(summary_frame, text="มูลค่าสินค้า (ก่อนภาษี)", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=2, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"{total_before_vat:.2f} บาท", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=2, column=1, sticky="e", padx=5)

    # แถว 3: VAT (ตัวเล็ก)
    tk.Label(summary_frame, text=f"ภาษีมูลค่าเพิ่ม ({int(VAT_RATE*100)}%)", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=3, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"{vat_amount:.2f} บาท", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=3, column=1, sticky="e", padx=5)
    
    # (เพิ่มเส้นคั่น)
    ttk.Separator(summary_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)

     # แถว 5: ยอดสุทธิ (ตัวใหญ่)
    tk.Label(summary_frame, text="รวมทั้งสิ้น", font=summary_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=5, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"{grand_total:.2f} บาท", font=summary_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=5, column=1, sticky="e", padx=5)

    summary_frame.grid_columnconfigure(0, weight=1) # ให้คอลัมน์ชิดขวา
    # --- ปุ่ม ย้อนกลับ / ชำระเงิน ---
    back_btn = tk.Button(checkout_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                         bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                         command=go_back_to_cart)
    back_btn.place(x=290, y=460, width=150, height=60)

    submit_btn = tk.Button(checkout_window, text="ชำระเงิน", font=("UID SALMON 2019", 40, "bold"),
                           bg="#bfffcb", fg="#552c1f", bd=1 , relief="solid",
                           # --- (!! 2. แก้ไข !!) เรียก submit_order จากหน้านี้ ---
                           command=lambda: submit_order(menu_window, cart_window, checkout_window, table_num))
    submit_btn.place(x=510, y=460, width=150, height=60)

    add_about_button(checkout_window)

### START: เพิ่มใหม่ (หน้าเมนูสำหรับลูกค้า) ###
def customer_menu_page(selected_table):
    """ฟังก์ชันสำหรับหน้าเมนูอาหารของลูกค้า"""
    menu_window = create_toplevel_window(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {selected_table} - เมนู")
    menu_window.protocol("WM_DELETE_WINDOW", lambda: table_selection_page(menu_window))

    global bg_image_customer_menu
    try:
        image_path_to_load = PIC_CUSTOMER_MENU 
        bg_image_manage_pil = Image.open(image_path_to_load)
        bg_image_manage_pil = bg_image_manage_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_customer_menu = ImageTk.PhotoImage(bg_image_manage_pil)
        background_label = tk.Label(menu_window, image=bg_image_customer_menu)
        background_label.image = bg_image_customer_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CUSTOMER_MENU}")
        menu_window.config(bg="#ffd7e8") # Fallback

    table_label_font = ("UID SALMON 2019",35 , "bold")
    table_label_bg = "#ffe0f1" 
    table_label_fg = "#552c1f" 

    table_display_label = tk.Label(menu_window, text=f" {selected_table}",
                                     font=table_label_font,
                                     bg=table_label_bg,
                                     fg=table_label_fg,
                                     padx=10, pady=5)
    table_display_label.place(x=123, y=15, width=35 , height=30) 

    cart_button_font = ("Arial", 30, "bold") 
    cart_button_bg = "#fd75af"        
    cart_button_fg = "#552c1f"        
    
    cart_button = tk.Button(
        menu_window, 
        text="🛒", 
        font=cart_button_font,
        bg=cart_button_bg,
        fg=cart_button_fg,
        bd=1, 
        relief="solid" ,
        activebackground="#fd75af",
        command=lambda: cart_page(menu_window, selected_table)
    )
    cart_button.place(x=870, y=15, width=66, height=51) 

    canvas = tk.Canvas(menu_window, bg="#ffd7e8", highlightthickness=1,highlightbackground="black", bd=0)
    scrollbar = ttk.Scrollbar(menu_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffd7e8")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    def _on_mousewheel_menu(event):
        try:
            delta = 0
            if event.num == 4: delta = -1
            elif event.num == 5: delta = 1
            elif os.name == 'nt': delta = int(-1*(event.delta/120))
            else: delta = event.delta
            
            canvas.yview_scroll(delta, "units")
        except Exception as e:
            pass

    menu_window.bind("<MouseWheel>", _on_mousewheel_menu)
    menu_window.bind("<Button-4>", _on_mousewheel_menu)
    menu_window.bind("<Button-5>", _on_mousewheel_menu)

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=860)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(x=40, y=145, width=880, height=320)
    scrollbar.place(x=920, y=145, height=320)

    # --- (!! แก้ไขฟังก์ชันนี้ !!) ---
    def display_customer_menu_items(category):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        MENU_ITEM_PIC_REFS.clear()

        # --- (!! 1. ลบ if...else ที่เช็ค "⭐ แนะนำ" ออก !!) ---
        filtered_items = get_menu_items_from_db(category) 

        row_num = 0
        col_num = 0
        card_width = 270

        if not filtered_items:
            tk.Label(scrollable_frame, text="ไม่มีรายการเมนูในหมวดหมู่นี้",
                         font=("Arial", 20), bg="#fff0f5").grid(row=0, column=0, columnspan=3, pady=20)

        for item in filtered_items:
            outer_card = tk.Frame(scrollable_frame, bg="#fff0f5", padx=5, pady=5)
            card = tk.Frame(outer_card, bg="white", bd=1, relief="solid", padx=5, pady=5)

            img_label = tk.Label(card, bg='#d3d3d3', width=20, height=8)
            try:
                img_placeholder_path = os.path.join(PIC_PATH, PIC_MENU_PLACEHOLDER)
                img_path = item['image_path'] or img_placeholder_path
                if not os.path.exists(img_path): img_path = None
                if img_path:
                    img = load_and_resize_pic(img_path, 120, is_menu_item=True)
                    img_label.config(image=img, width=120, height=120, bg='white')
                    img_label.image = img
                    MENU_ITEM_PIC_REFS[item['item_id']] = img
                else:
                    img_label.config(text="No Image", fg="black")
            except Exception as img_err:
                print(f"Error loading image for {item['name']}: {img_err}")
                img_label.config(text="Load Error", fg="red")
            img_label.pack(pady=(0, 5))
            
            # (โค้ดป้ายแท็กยังอยู่เหมือนเดิม)
            status_frame = tk.Frame(card, bg="white")
            if item.get('is_available', 1) == 1:
                status_text = "มีสินค้า"
                status_bg = "#a0e0b0"
                status_fg = "#006b2c"
            else:
                status_text = "สินค้าหมด"
                status_bg = "#cccccc"
                status_fg = "#666666"
            status_label = tk.Label(status_frame, text=status_text, 
                font=("Arial", 10, "bold"), bg=status_bg, fg=status_fg,
                padx=5, pady=2
            )
            status_label.pack(side="left")
            if item.get('is_recommended', 0) == 1:
                rec_label = tk.Label(status_frame, text="⭐ แนะนำ",
                    font=("Arial", 10, "bold"), bg="#fff0b1", fg="#552c1f",
                    padx=5, pady=2
                )
                rec_label.pack(side="left", padx=5)
            status_frame.pack(fill="x", padx=0, pady=(0, 5))

            tk.Label(card, text=item['name'], font=("Arial", 15, "bold"), bg="white", anchor="w").pack(fill="x")
            tk.Label(card, text=item.get('description', ''), font=("Arial", 12), bg="white", anchor="nw", wraplength=card_width-30, justify="left", height=3).pack(fill="x")
            tk.Label(card, text=f"ราคา {item['price']:.2f} บาท", font=("Arial", 15, "bold"), bg="white", anchor="w").pack(fill="x", pady=(5, 5))

            add_btn_frame = tk.Frame(card, bg="white")
            add_btn = tk.Button(add_btn_frame, font=("Arial", 12, "bold"), width=10)
            
            if item.get('is_available', 1) == 1: # ถ้ามีของ
                add_btn.config(
                    text="เพิ่ม",
                    bg="#a0e0b0",
                    fg="#552c1f",
                    state="normal",
                    command=lambda i=item: add_item_to_order(i, selected_table)
                )
            else: # ถ้าของหมด
                add_btn.config(
                    text="สินค้าหมด",
                    bg="#cccccc", 
                    fg="#552c1f",
                    state="disabled"
                )
            
            add_btn.pack(pady=5)
            add_btn_frame.pack(fill="x")

            card.pack(fill="both", expand=True)
            outer_card.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="nsew")

            col_num += 1
            if col_num >= 3:
                col_num = 0
                row_num += 1

        for i in range(3):
           scrollable_frame.grid_columnconfigure(i, weight=1, minsize=card_width + 10)

        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)

    # --- (!! 2. แก้ไข !!) ลบ "⭐ แนะนำ" ออกจาก categories ---
    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    category_buttons = {}
    tab_frame = tk.Frame(menu_window, bg="#fff0f5", bd=0)
    tab_frame.place(x=40, y=90, height=45, width=750) 

    current_category = tk.StringVar(value=categories[0]) 

    def select_category(category):
        current_category.set(category)
        display_customer_menu_items(category) 
        for cat, btn in category_buttons.items():
            if cat == category:
                btn.config(bg="#ffc1e0", relief="sunken") # สีเข้ม
            else:
                btn.config(bg="#ffe0f1", relief="raised") # สีอ่อน

    for i, cat in enumerate(categories):
        btn = tk.Button(tab_frame, text=cat, font=("Arial", 20, "bold"),
                        bg="#ffe0f1", fg="#552c1f", relief="raised", bd=1,
                        activebackground="#ffc1e0",
                        command=lambda c=cat: select_category(c))
        btn.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        category_buttons[cat] = btn

    def confirm_back_and_clear_cart():
        global CURRENT_ORDER, CURRENT_REDEMPTION # <<< เพิ่ม
        if CURRENT_ORDER: # ถ้าในตะกร้ามีของ
            if messagebox.askyesno("ยืนยัน", "หากย้อนกลับ รายการในตะกร้าจะถูกล้างทั้งหมด\nคุณต้องการย้อนกลับใช่หรือไม่?"):
               CURRENT_ORDER.clear() # ล้างตะกร้า
               CURRENT_REDEMPTION.clear() # <<< เพิ่มบรรทัดนี้
               table_selection_page(menu_window)
        else:
                table_selection_page(menu_window) # ถ้าตะกร้าว่าง ก็กลับได้เลย

    back_button = tk.Button(menu_window, text="ย้อนกลับ", font=("UID SALMON 2019", 45, "bold"), 
                            bg="#ffe0f1", fg="#552c1f", bd=2 , relief="solid",
                            command=confirm_back_and_clear_cart) 
    back_button.place(x=744, y=470, width=140, height=50) 

    add_small_profile_button(menu_window)
    add_about_button(menu_window)

    # (โค้ดนี้ถูกต้องแล้ว มันจะเลือก "ส้มตำ" เป็นค่าเริ่มต้น)
    select_category(categories[0])
# ------------------------------------
# Main Pages (Login/Register/Forgot Password)
# ------------------------------------

# (หน้า Forgot Password - เหมือนเดิม)
def forgot_password_page(prev_window):
    if prev_window:
        prev_window.destroy()
    forgot_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - รหัสผ่านใหม่")
    verified_contact = tk.StringVar(value="")
    global bg_image_forgot
    try:
        bg_image_forgot_pil = Image.open(PIC_FORGOT_PASSWORD)
        bg_image_forgot_pil = bg_image_forgot_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_forgot = ImageTk.PhotoImage(bg_image_forgot_pil)
        background_label_forgot = tk.Label(forgot_window, image=bg_image_forgot)
        background_label_forgot.image = bg_image_forgot
        background_label_forgot.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}\n{PIC_FORGOT_PASSWORD}")
        forgot_window.destroy()
        root.deiconify()
        return
    contact_var = tk.StringVar()
    new_pass_var = tk.StringVar()
    confirm_pass_var = tk.StringVar()
    entry_font = ("Arial", 20)
    contact_entry = tk.Entry(forgot_window, textvariable=contact_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat")
    contact_entry.place(x=263, y=193, width=360, height=35)
    new_pass_entry = tk.Entry(forgot_window, textvariable=new_pass_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat", show="*", state='disabled')
    new_pass_entry.place(x=260, y=280, width=440, height=35)
    confirm_pass_entry = tk.Entry(forgot_window, textvariable=confirm_pass_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat", show="*", state='disabled')
    confirm_pass_entry.place(x=260, y=355, width=440, height=35)
    def handle_check():
        contact = contact_var.get()
        if not contact:
            messagebox.showwarning("ว่าง", "กรุณากรอกเบอร์โทรหรือ Email")
            return
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM user_account WHERE email = ? OR phone = ?", (contact, contact))
        record = cursor.fetchone()
        conn.close()
        if record:
            messagebox.showinfo("สำเร็จ", "แก้รหัสผ่าน! กรุณาตั้งรหัสผ่านใหม่")
            new_pass_entry.config(state='normal')
            confirm_pass_entry.config(state='normal')
            save_button.config(state='normal')
            verified_contact.set(contact)
        else:
            messagebox.showerror("ไม่พบ", "ไม่พบบัญชีของคุณ")
            new_pass_entry.config(state='disabled')
            confirm_pass_entry.config(state='disabled')
            save_button.config(state='disabled')
            verified_contact.set("")
    def handle_save_new_password():
        contact = verified_contact.get()
        new_pass = new_pass_var.get()
        confirm_pass = confirm_pass_var.get()
        if not contact:
            messagebox.showerror("ผิดพลาด", "กรุณากด 'ตรวจสอบ' บัญชีก่อน")
            return
        if not new_pass or not confirm_pass:
            messagebox.showwarning("ว่าง", "กรุณากรอกรหัสผ่านใหม่ทั้งสองช่อง")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("ผิดพลาด", "รหัสผ่านใหม่ไม่ตรงกัน")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE user_account SET password = ? WHERE email = ? OR phone = ?", (new_pass, contact, contact))
            conn.commit()
            conn.close()
            messagebox.showinfo("สำเร็จ", "เปลี่ยนรหัสผ่านเรียบร้อยแล้ว")
            login_page(forgot_window)
        except sqlite3.Error as e:
            messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถอัปเดตรหัสผ่านได้: {e}")
    check_button = tk.Button(forgot_window, text="ตรวจสอบ", font=("UID SALMON 2019", 25 ),
                             bg="#bfffcb", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#bfffcb",
                             command=handle_check)
    check_button.place(x=638, y=190, width=72 , height=33)
    back_button = tk.Button(forgot_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#ffe0f1",
                            command=lambda: login_page(forgot_window))
    back_button.place(x=280, y=420, width=150, height=50)
    save_button = tk.Button(forgot_window, text="ยืนยัน", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#ffe0f1",
                            command=handle_save_new_password,
                            state='disabled')
    save_button.place(x=540, y=420, width=150, height=50)
    add_about_button(forgot_window)

# (!!!) ย้าย open_next_page มาไว้ตรงนี้ (!!!)
def open_next_page(current_window):
    current_window.destroy()
    table_selection_page() # ไปหน้าเลือกโต๊ะ

### START: (หน้า Login) ###
def login_page(prev_window=None):
    """ฟังก์ชันสำหรับหน้า 'เข้าสู่ระบบ'"""

    if prev_window:
        prev_window.destroy()

    login_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - เข้าสู่ระบบ")
    login_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(login_window))

    try:
        bg_image_login_pil = Image.open(f"{PIC_PATH}{PIC_LOGIN}")
        bg_image_login_pil = bg_image_login_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_login = ImageTk.PhotoImage(bg_image_login_pil)
        background_label_login = tk.Label(login_window, image=bg_image_login)
        background_label_login.image = bg_image_login
        background_label_login.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        login_window.destroy()
        root.deiconify()
        return

    username_entry = tk.Entry(login_window, font=("Arial", 28,"bold"),bg ="#fffbf2", bd=0, relief="flat")
    username_entry.place(x=315, y=240, width=320, height=45)

    password_entry = tk.Entry(login_window, show="*", font=("Arial", 28,"bold"),bg ="#fffbf2" , bd=0, relief="flat")
    password_entry.place(x=315, y=320, width=300, height=45)

    forgot_btn = tk.Button(login_window, text="ลืมรหัส", font=("Arial", 20, "bold"),
                           bg="#daf1ff", fg="#552c1f", bd=0, relief="flat",
                           activebackground="#daf1ff",
                           command=lambda: forgot_password_page(login_window))
    forgot_btn.place(x=638, y=325, width=82, height=35)


    back_button = tk.Button(login_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#E3B2C3", command=lambda: back_to_main_page(login_window))
    back_button.place(x=280, y=420, width=150, height=50)

    # *** Logic การ Login ***
    def local_verify_login():
        global CURRENT_USER
        user = username_entry.get()
        pwd = password_entry.get()

        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            CURRENT_USER = ADMIN_USERNAME
            messagebox.showinfo("Admin Login", "เข้าสู่ระบบแอดมินสำเร็จ!")
            admin_panel_page(login_window)
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = ? AND password = ?", (user, pwd))
        record = cursor.fetchone()
        conn.close()

        if record:
            CURRENT_USER = user
            messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ!")
            open_next_page(login_window) # <<< เรียกใช้ฟังก์ชันที่ย้ายมา
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                               activebackground="#E3B2C3",
                               command=local_verify_login)
    confirm_button.place(x=540, y=420, width=150, height=50)

    add_about_button(login_window)
### END: (หน้า Login) ###


### START: (หน้า Register) ###
def register_page(prev_window=None):
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก'"""
    if prev_window:
        prev_window.destroy()

    register_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - สมัครสมาชิก")
    register_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(register_window))

    try:
        bg_image_register_pil = Image.open(f"{PIC_PATH}{PIC_REGISTER}")
        bg_image_register_pil = bg_image_register_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_register = ImageTk.PhotoImage(bg_image_register_pil)
        background_label_register = tk.Label(register_window, image=bg_image_register)
        background_label_register.image = bg_image_register
        background_label_register.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        register_window.destroy()
        root.deiconify()
        return

    username_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    username_entry.place(x=165, y=170, width=270, height=30)
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    password_entry.place(x=520, y=170, width=270, height=30)
    name_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    name_entry.place(x=165, y=235, width=270, height=30)
    surname_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    surname_entry.place(x=520, y=235, width=270, height=30)
    phone_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    phone_entry.place(x=165, y=300, width=270, height=30)
    birthday_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    birthday_entry.place(x=520, y=300, width=270, height=30)
    email_entry = tk.Entry(register_window, font=("Arial", 20), bg="#ffebf6", bd=0, relief="flat")
    email_entry.place(x=340, y=370, width=270, height=30)
    back_button = tk.Button(register_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#E3B2C3", command=lambda: back_to_main_page(register_window))
    back_button.place(x=285, y=420, width=150, height=50)

    def local_save_registration_data():
        user, pwd, name, surname, phone, bday, email = username_entry.get(), password_entry.get(), name_entry.get(), surname_entry.get(), phone_entry.get(), birthday_entry.get(), email_entry.get()
        if not all([user, pwd, name, surname, phone, bday, email]):
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
            return

        ### START: เพิ่มโค้ดตรวจสอบรหัสผ่าน ###
        if len(pwd) < 8:
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            password_entry.delete(0, tk.END)
            return
        special_chars = "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?~`"
        if not any(char in special_chars for char in pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมีอักขระพิเศษอย่างน้อย 1 ตัว\nเช่น !, @, #, $, %")
            password_entry.delete(0, tk.END)
            return
        ### END: เพิ่มโค้ดตรวจสอบรหัสผ่าน ###

        ### START: เพิ่มโค้ดตรวจสอบเบอร์โทรศัพท์ ###
        if not phone.isdigit():
            messagebox.showerror("ผิดพลาด", "เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
            phone_entry.delete(0, tk.END)
            return
        if len(phone) != 10:
            messagebox.showerror("ผิดพลาด", "เบอร์โทรศัพท์ต้องมี 10 หลักพอดี")
            phone_entry.delete(0, tk.END)
            return
        ### END: เพิ่มโค้ดตรวจสอบเบอร์โทรศัพท์ ###

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user_account (username, password, name, surname, phone, birthday, email) VALUES (?, ?, ?, ?, ?, ?, ?)", (user, pwd, name, surname, phone, bday, email))
            cursor.execute("INSERT INTO user_profile (username, score, profile_pic_path) VALUES (?, ?, ?)", (user, 0, None))
            conn.commit()
            messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ชื่อผู้ใช้: {user} \nตอนนี้คุณสามารถเข้าสู่ระบบได้แล้ว")
            back_to_main_page(register_window)
        except sqlite3.IntegrityError:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) นี้ถูกใช้ไปแล้ว")
        except sqlite3.Error as e:
            messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถบันทึกได้: {e}")
        finally:
            conn.close()

    confirm_button = tk.Button(register_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                               activebackground="#E3B2C3",
                               command=local_save_registration_data)
    confirm_button.place(x=535, y=420, width=150, height=50)

    add_about_button(register_window)
### END: (หน้า Register) ###

### START: (Admin Panel) ###
def admin_panel_page(prev_window):
    """ฟังก์ชันสำหรับหน้า 'แอดมิน'"""
    if prev_window:
        prev_window.destroy()

    admin_window = create_toplevel_window("Admin Panel")
    admin_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(admin_window))

    global bg_image_admin_panel
    try:
        bg_image_admin_pil = Image.open(PIC_ADMIN_PANEL)
        bg_image_admin_pil = bg_image_admin_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_panel = ImageTk.PhotoImage(bg_image_admin_pil)
        background_label_admin = tk.Label(admin_window, image=bg_image_admin_panel)
        background_label_admin.image = bg_image_admin_panel
        background_label_admin.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}\n{PIC_ADMIN_PANEL}")
        admin_window.destroy()
        root.deiconify()
        return

    btn_font = ("UID SALMON 2019", 50, "bold") 

    sales_button = tk.Button(admin_window, text="ยอดขาย", font= btn_font,
                             bg="#ffffff", fg="#552c1f", bd=0 , relief="groove",
                             command=lambda: messagebox.showinfo("Info", "ฟังก์ชันยอดขาย (ยังไม่เสร็จ)"))
    sales_button.place(relx=0.5, y=170, width=280, height=70, anchor=tk.CENTER)

    table_order_button = tk.Button(admin_window, text="โต๊ะลูกค้า/คำสั่งซื้อ", font=("UID SALMON 2019", 40, "bold"),
                                   bg="#ffffff", fg="#552c1f", bd=0, relief="groove",
                                   command=lambda: admin_table_view_page(admin_window))
    table_order_button.place(x=160, y=305, width=285 , height=85)

    menu_button = tk.Button(admin_window, text="เพิ่ม/แก้ไข/ลบ เมนู", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffffff", fg="#552c1f", bd=0, relief="groove", justify=tk.CENTER,
                            command=lambda: admin_manage_menu_page(admin_window))
    menu_button.place(x=525, y=305, width=285, height=85)

    logout_button = tk.Button(admin_window, text="ออกจากระบบ", font=("UID SALMON 2019", 30 , "bold"),
                              bg="#ff257d", fg="#552c1f", bd=0, relief="flat",
                              activebackground="#ff257d",
                              command=lambda: back_to_main_page(admin_window))
    logout_button.place(x=800, y=18, width=140, height=43)

    add_about_button(admin_window)

### END: (Admin Panel) ###

### START: (Admin Table View) ###
def admin_table_view_page(prev_window):
    """ฟังก์ชันสำหรับหน้าแสดงโต๊ะสำหรับ Admin"""
    if prev_window:
        prev_window.destroy()

    admin_table_window = create_toplevel_window("Admin - Table View")
    admin_table_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(admin_table_window))

    global bg_image_admin_table_view
    try:
        bg_image_admin_table_pil = Image.open(PIC_ADMIN_TABLE_VIEW)
        bg_image_admin_table_pil = bg_image_admin_table_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_table_view = ImageTk.PhotoImage(bg_image_admin_table_pil)
        background_label_admin_table = tk.Label(admin_table_window, image=bg_image_admin_table_view)
        background_label_admin_table.image = bg_image_admin_table_view
        background_label_admin_table.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}\n{PIC_ADMIN_TABLE_VIEW}")
        admin_table_window.destroy()
        admin_panel_page(None)
        return

    table_buttons = {}

    def view_table_order(current_window, table_number):
        messagebox.showinfo("ดูออเดอร์", f"ดูออเดอร์โต๊ะ {table_number}\n(ยังไม่ได้ทำ)")

    button_width = 160
    button_height = 150
    y1 = 80 
    y2 = 290 
    
    table_coords_admin = [
        (115, y1), (305, y1), (495, y1), (685, y1),  # แถว 1: โต๊ะ 1-4
        (115, y2), (305, y2), (495, y2), (685, y2)   # แถว 2: โต๊ะ 5-8
    ]

    for i, (x, y) in enumerate(table_coords_admin):
        table_num = i + 1
        btn = tk.Button(admin_table_window, text=f"โต๊ะ {table_num}", font=("UID SALMON 2019", 70), 
                        bg="#ffe0f1", fg="#552c1f", bd=2 , relief="solid", 
                        justify=tk.CENTER,
                        command=lambda num=table_num: view_table_order(admin_table_window, num))
        btn.place(x=x, y=y, width=button_width, height=button_height) 
        table_buttons[table_num] = btn

    back_button = tk.Button(admin_table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 45, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="groove",
                            command=lambda: admin_panel_page(admin_table_window))
    back_button.place(x=744, y=468, width=140, height=60) 

    add_about_button(admin_table_window) 

### END: (Admin Table View) ###

### START: เพิ่มใหม่ (หน้า Add Menu) ###
def admin_add_menu_page(prev_window, category_from_manage=None): # <<< 1. เพิ่ม category_from_manage
    """ฟังก์ชันสำหรับหน้าเพิ่มเมนู (ตามไฟล์ 29.png)"""
    if prev_window:
        prev_window.destroy()

    add_window = create_toplevel_window("Admin - เพิ่มเมนู")
    # (เราจะใช้ category_from_manage ตอนกดย้อนกลับ)
    add_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(add_window, category_from_manage)) 

    global bg_image_admin_add_menu
    try:
        bg_image_add_pil = Image.open(PIC_ADMIN_ADD_MENU)
        bg_image_add_pil = bg_image_add_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_add_menu = ImageTk.PhotoImage(bg_image_add_pil)
        background_label = tk.Label(add_window, image=bg_image_admin_add_menu)
        background_label.image = bg_image_admin_add_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_ADD_MENU}")
        add_window.config(bg="#fff0f5") # Fallback

    name_var = tk.StringVar()
    description_var = tk.StringVar()
    price_var = tk.StringVar()
    category_var = tk.StringVar()
    image_source_path_var = tk.StringVar()

    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    
    # ---!! (2. แก้ไข) ตั้งค่าเริ่มต้นตามหมวดหมู่ที่ส่งมา !! ---
    if category_from_manage and category_from_manage in categories:
        category_var.set(category_from_manage)
    else:
        category_var.set(categories[0]) # ถ้าไม่มี ให้ใช้ "ส้มตำ" เป็นค่าเริ่มต้น

    img_frame = tk.Frame(add_window, bg="white", bd=1, relief="solid")
    img_frame.place(x=140, y=190, width=150, height=150)

    img_label = tk.Label(img_frame, bg="#d3d3d3", text="No Image", font=("Arial", 12))
    img_label.place(relwidth=1, relheight=1)

    def display_menu_pic(pic_path):
        global MENU_FORM_PIC_REF
        img_tk = load_and_resize_pic(pic_path, 148, is_menu_item=True)
        MENU_FORM_PIC_REF['pic'] = img_tk
        img_label.config(image=img_tk, text="")
        img_label.image = img_tk

    def choose_image():
        source_path = filedialog.askopenfilename(
            title="เลือกรูปเมนู",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            image_source_path_var.set(source_path)
            display_menu_pic(source_path)

    entry_font = ("Arial", 20)
    bg_color = "#ffffff"

    name_entry = tk.Entry(add_window, textvariable=name_var, font=entry_font, bd=2, bg=bg_color)
    name_entry.place(x=440, y=185, width=340, height=30)
    price_entry = tk.Entry(add_window, textvariable=price_var, font=entry_font, bd=2, bg=bg_color)
    price_entry.place(x=450, y=240, width=340, height=30) 
    description_entry = tk.Entry(add_window, textvariable=description_var, font=entry_font, bd=2, bg=bg_color)
    description_entry.place(x=500, y=290, width=340, height=30) 
    category_menu = ttk.Combobox(add_window, textvariable=category_var,
                                 values=categories, state="readonly", font=entry_font)
    category_menu.place(x=510, y=350, width=340, height=30) 

    add_pic_button = tk.Button(add_window, text="เพิ่มรูป", font=("Arial", 15, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                               command=choose_image)
    add_pic_button.place(x=165, y=355, width=105, height=40)

    def save_item():
        name = name_var.get()
        description = description_var.get()
        price_str = price_var.get()
        category = category_var.get()
        source_img_path = image_source_path_var.get()

        if not name or not price_str or not category:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก ชื่อ, ราคา และหมวดหมู่")
            return
        try:
            price = float(price_str)
            if price < 0: raise ValueError
        except ValueError:
            messagebox.showwarning("ข้อมูลผิดพลาด", "ราคาต้องเป็นตัวเลขเท่านั้น")
            return
        
        final_image_path = None
        if source_img_path:
            final_image_path = copy_menu_image(source_img_path, name)
            if final_image_path is None:
                messagebox.showerror("ผิดพลาด", "ไม่สามารถบันทึกรูปภาพได้")
                return
        
        if db_add_menu_item(name, price, category, final_image_path, description=description):
            messagebox.showinfo("สำเร็จ", "เพิ่มเมนูเรียบร้อยแล้ว")
            # ---!! (3. แก้ไข) ส่งหมวดหมู่ที่เพิ่งบันทึกกลับไป !! ---
            admin_manage_menu_page(add_window, category)

    save_button = tk.Button(add_window, text="เสร็จสิ้น", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                            command=save_item)
    save_button.place(x=430, y=460, width=100, height=40)
    
    back_button = tk.Button(add_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                            # ---!! (4. แก้ไข) ส่งหมวดหมู่ปัจจุบันกลับไป !! ---
                            command=lambda: admin_manage_menu_page(add_window, category_var.get()))
    back_button.place(x=765, y=480, width=100, height=40)

    add_about_button(add_window)

### END: เพิ่มใหม่ (หน้า Add Menu) ###

### START: เพิ่มใหม่ (หน้า Edit Menu) ###
def admin_edit_menu_page(prev_window, item_data):
    """ฟังก์ชันสำหรับหน้าแก้ไขเมนู (ตามไฟล์ 28.png)"""
    if prev_window:
        prev_window.destroy()

    edit_window = create_toplevel_window("Admin - แก้ไขเมนู")
    edit_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(edit_window, item_data.get('category'))) 

    global bg_image_admin_edit_menu 
    
    try:
        bg_image_edit_pil = Image.open(PIC_ADMIN_EDIT_MENU)
        bg_image_edit_pil = bg_image_edit_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_edit_menu = ImageTk.PhotoImage(bg_image_edit_pil)
        background_label = tk.Label(edit_window, image=bg_image_admin_edit_menu)
        background_label.image = bg_image_admin_edit_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_EDIT_MENU}")
        edit_window.config(bg="#fff0f5") # Fallback

    item_id = item_data['item_id']
    original_image_path = item_data.get('image_path')
    
    # --- (!! 1. เปลี่ยนเป็น tk.IntVar !!) ---
    # ใช้ tk.IntVar เพื่อให้เราอัปเดตค่านี้และให้ปุ่มรับรู้ได้
    current_recommend_status_var = tk.IntVar(value=item_data.get('is_recommended', 0))

    name_var = tk.StringVar(value=item_data.get('name', ''))
    description_var = tk.StringVar(value=item_data.get('description', ''))
    price_var = tk.StringVar(value=f"{item_data.get('price', 0.0):.2f}")
    category_var = tk.StringVar(value=item_data.get('category', ''))
    image_path_var = tk.StringVar(value=original_image_path)

    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    if category_var.get() not in categories:
         category_var.set(categories[0])

    img_frame = tk.Frame(edit_window, bg="white", bd=1, relief="solid")
    img_frame.place(x=140, y=190, width=150, height=150)
    img_label = tk.Label(img_frame, bg="#d3d3d3", text="No Image", font=("Arial", 12))
    img_label.place(relwidth=1, relheight=1)

    def display_menu_pic(pic_path):
        global MENU_FORM_PIC_REF
        img_tk = load_and_resize_pic(pic_path, 148, is_menu_item=True)
        MENU_FORM_PIC_REF['pic'] = img_tk
        img_label.config(image=img_tk, text="")
        img_label.image = img_tk

    display_menu_pic(original_image_path)

    def choose_image():
        source_path = filedialog.askopenfilename(
            title="เลือกรูปเมนูใหม่",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            image_path_var.set(source_path)
            display_menu_pic(source_path)

    entry_font = ("Arial", 18)
    bg_color = "#ffffff"

    name_entry = tk.Entry(edit_window, textvariable=name_var, font=entry_font, bd=2, bg=bg_color)
    name_entry.place(x=440, y=185, width=250, height=30)
    price_entry = tk.Entry(edit_window, textvariable=price_var, font=entry_font, bd=2, bg=bg_color)
    price_entry.place(x=450, y=240, width=250, height=30) 
    description_entry = tk.Entry(edit_window, textvariable=description_var, font=entry_font, bd=2, bg=bg_color)
    description_entry.place(x=500, y=290, width=340, height=30) 
    category_menu = ttk.Combobox(edit_window, textvariable=category_var,
                                 values=categories, state="readonly", font=entry_font)
    category_menu.place(x=510, y=350, width=340, height=30) 

    add_pic_button = tk.Button(edit_window, text="เปลี่ยนรูป", font=("Arial", 12, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                               command=choose_image)
    add_pic_button.place(x=165, y=355, width=100, height=30)

    def save_item():
        name = name_var.get()
        description = description_var.get()
        price_str = price_var.get()
        category = category_var.get() 
        current_img_path_var = image_path_var.get()

        if not name or not price_str or not category:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก ชื่อ, ราคา และหมวดหมู่")
            return
        try:
            price = float(price_str)
            if price < 0: raise ValueError
        except ValueError:
            messagebox.showwarning("ข้อมูลผิดพลาด", "ราคาต้องเป็นตัวเลขเท่านั้น")
            return

        final_image_path = original_image_path
        if current_img_path_var != original_image_path and os.path.exists(current_img_path_var):
            final_image_path = copy_menu_image(current_img_path_var, name)
            if final_image_path is None:
                messagebox.showerror("ผิดพลาด", "ไม่สามารถบันทึกรูปภาพใหม่ได้")
                return
        
        if db_update_menu_item(item_id, name, price, category, final_image_path, description=description):
            messagebox.showinfo("สำเร็จ", "อัปเดตเมนูเรียบร้อยแล้ว")
            admin_manage_menu_page(edit_window, category)

    save_button = tk.Button(edit_window, text="เสร็จสิ้น", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                            command=save_item)
    save_button.place(x=430, y=460, width=100, height=40)
    
    back_button = tk.Button(edit_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                            command=lambda: admin_manage_menu_page(edit_window, category_var.get()))
    back_button.place(x=765, y=480, width=100, height=40)
    
    # --- (!! 2. สร้างปุ่มแนะนำก่อน !!) ---
    recommend_button = tk.Button(edit_window, font=("Arial", 14, "bold"),
                                  fg="#552c1f", bd=1 , relief="solid")
    recommend_button.place(x=730, y=160, width=150, height=40)

    # --- (!! 3. สร้างฟังก์ชันที่อัปเดตปุ่ม !!) ---
    def update_recommend_button_style():
        """(ฟังก์ชันภายใน) อัปเดตสีและข้อความของปุ่มแนะนำ"""
        if current_recommend_status_var.get() == 0:
            rec_text = "⭐ เพิ่ม 'แนะนำ'"
            rec_bg = "#fff0b1" # สีเหลือง
        else:
            rec_text = "⭐ ลบ 'แนะนำ'"
            rec_bg = "#ffc1e0" # สีชมพู
        recommend_button.config(text=rec_text, bg=rec_bg)

    # --- (!! 4. สร้างฟังก์ชัน toggle ที่เรียกใช้ฟังก์ชันอัปเดต !!) ---
    def toggle_recommend():
        current_status = current_recommend_status_var.get()
        new_status = 1 if current_status == 0 else 0 
        
        if db_set_recommend_status(item_id, new_status):
            # อัปเดตตัวแปรในหน้านี้
            current_recommend_status_var.set(new_status)
            # อัปเดตปุ่ม (สี/ข้อความ)
            update_recommend_button_style()
            # (ไม่ต้องเด้งไปหน้าอื่น)
        else:
            messagebox.showerror("ผิดพลาด", "ไม่สามารถอัปเดตสถานะ 'แนะนำ' ได้")

    # --- (!! 5. ผูก command และเรียกใช้ครั้งแรก !!) ---
    recommend_button.config(command=toggle_recommend) # ผูกคำสั่ง
    update_recommend_button_style() # เรียกใช้เพื่อตั้งค่าเริ่มต้น

    add_about_button(edit_window)

### END: เพิ่มใหม่ (หน้า Edit Menu) ###

### START: เพิ่มใหม่ (หน้าดูสถานะสินค้า) ###
def admin_status_view_page(prev_window):
    """ฟังก์ชันสำหรับหน้าแสดงสถานะสินค้า (ตามรูป 003602.png)"""
    if prev_window:
        prev_window.destroy()

    status_window = create_toplevel_window("Admin - สถานะสินค้า")
    status_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(status_window))

    global bg_image_admin_status_view
    try:
        bg_image_pil = Image.open(PIC_ADMIN_STATUS_VIEW) 
        bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_status_view = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(status_window, image=bg_image_admin_status_view)
        background_label.image = bg_image_admin_status_view
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_STATUS_VIEW}")
        status_window.config(bg="#ffd7e8") # Fallback

    # --- กรอบซ้าย: มีสินค้า (is_available = 1) ---
    list_canvas_instock = tk.Canvas(status_window, bg="#ffffff", bd=0, highlightthickness=0)
    list_scrollbar_instock = ttk.Scrollbar(status_window, orient="vertical", command=list_canvas_instock.yview)
    list_scrollable_frame_instock = tk.Frame(list_canvas_instock, bg="#ffffff")

    list_scrollable_frame_instock.bind(
        "<Configure>",
        lambda e: list_canvas_instock.configure(scrollregion=list_canvas_instock.bbox("all"))
    )
    # --- (!! ลบ _on_mousewheel_instock เก่าทิ้ง !!) ---
    
    list_canvas_instock.create_window((0, 0), window=list_scrollable_frame_instock, anchor="nw", width=340-17)
    list_canvas_instock.configure(yscrollcommand=list_scrollbar_instock.set)
    list_canvas_instock.place(x=115, y=175, width=340-17, height=270)
    list_scrollbar_instock.place(x=115+340-17, y=175, height=270)
    
    # --- กรอบขวา: สินค้าหมด (is_available = 0) ---
    list_canvas_outofstock = tk.Canvas(status_window, bg="#ffffff", bd=0, highlightthickness=0)
    list_scrollbar_outofstock = ttk.Scrollbar(status_window, orient="vertical", command=list_canvas_outofstock.yview)
    list_scrollable_frame_outofstock = tk.Frame(list_canvas_outofstock, bg="#ffffff")

    list_scrollable_frame_outofstock.bind(
        "<Configure>",
        lambda e: list_canvas_outofstock.configure(scrollregion=list_canvas_outofstock.bbox("all"))
    )
    # --- (!! ลบ _on_mousewheel_outofstock เก่าทิ้ง !!) ---

    list_canvas_outofstock.create_window((0, 0), window=list_scrollable_frame_outofstock, anchor="nw", width=340-17)
    list_canvas_outofstock.configure(yscrollcommand=list_scrollbar_outofstock.set)
    list_canvas_outofstock.place(x=505, y=175, width=340-17, height=270)
    list_scrollbar_outofstock.place(x=505+340-17, y=175, height=270)

    # --- (!! NEW !!) ฟังก์ชัน Mousewheel อัจฉริยะ (อันเดียว) ---
    def _on_mousewheel_status(event):
        try:
            # คำนวณหาค่า delta (Windows/Mac/Linux ใช้ไม่เหมือนกัน)
            delta = 0
            if event.num == 4: # Linux scroll up
                delta = -1
            elif event.num == 5: # Linux scroll down
                delta = 1
            elif os.name == 'nt': # Windows
                delta = int(-1*(event.delta/120))
            else: # macOS
                delta = event.delta

            # คำนวณตำแหน่ง x ของเมาส์ที่สัมพันธ์กับหน้าต่าง
            mouse_x_in_window = event.x_root - status_window.winfo_rootx()
            window_center_x = 480 # (960 / 2)
            
            if mouse_x_in_window < window_center_x:
                # ถ้าอยู่ซ้าย -> เลื่อนกรอบซ้าย
                list_canvas_instock.yview_scroll(delta, "units")
            else:
                # ถ้าอยู่ขวา -> เลื่อนกรอบขวา
                list_canvas_outofstock.yview_scroll(delta, "units")
        except Exception as e:
            # (กัน error ตอนหน้าต่างกำลังปิด)
            pass

    # --- (!! NEW !!) ผูก (bind) ฟังก์ชันนี้แค่ครั้งเดียว ---
    status_window.bind_all("<MouseWheel>", _on_mousewheel_status)
    status_window.bind_all("<Button-4>", _on_mousewheel_status) # (สำหรับ Linux scroll up)
    status_window.bind_all("<Button-5>", _on_mousewheel_status) # (สำหรับ Linux scroll down)
    
    # --- (โค้ดส่วนที่เหลือเหมือนเดิม) ---
    
    def toggle_status_internal(item_id, new_status):
        """อัปเดตสถานะและเรียก refresh"""
        if db_update_item_availability(item_id, new_status):
            refresh_status_display()
        else:
            messagebox.showerror("ผิดพลาด", "ไม่สามารถอัปเดตสถานะได้")

    def populate_list(target_frame, target_canvas, is_available):
        """(ฟังก์ชันภายใน) วาดรายการลงในกรอบที่กำหนด"""
        
        for widget in target_frame.winfo_children():
            widget.destroy()

        items = get_menu_items_by_status_from_db(is_available)
        
        if not items:
            tk.Label(target_frame, text="ไม่มีรายการ", font=("Arial", 14), bg="white").pack(pady=10)
            return
        
        new_status_on_click = 0 if is_available == 1 else 1 

        current_category = ""
        for item in items:
            if item['category'] != current_category:
                current_category = item['category']
                tk.Label(
                    target_frame, 
                    text=f"   {current_category}   ",
                    font=("Arial", 12, "bold"), 
                    bg="#ffc1e0",
                    fg="#552c1f",
                    anchor="w"
                ).pack(fill="x", pady=(10, 2), padx=5)

            item_btn = tk.Button(
                target_frame,
                text=f"🍴 {item['name']}",
                font=("Arial", 12),
                bg="#fff8fa",
                fg="#552c1f",
                anchor="w",
                bd=1,
                relief="solid",
                activebackground="#ffe0f1",
                activeforeground="#552c1f",
                justify="left",
                wraplength=340-40,
                command=lambda i=item['item_id'], ns=new_status_on_click: toggle_status_internal(i, ns)
            )
            item_btn.pack(fill="x", padx=10, pady=2)
            
        target_frame.update_idletasks()
        target_canvas.configure(scrollregion=target_canvas.bbox("all"))

    def refresh_status_display():
        """(ฟังก์ชันภายใน) เรียกวาดใหม่ทั้ง 2 รายการ"""
        populate_list(list_scrollable_frame_instock, list_canvas_instock, is_available=1)
        populate_list(list_scrollable_frame_outofstock, list_canvas_outofstock, is_available=0)

    # --- ปุ่มย้อนกลับ ---
    back_button = tk.Button(status_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_manage_menu_page(status_window))
    back_button.place(x=690, y=470, width=150, height=50)

    add_about_button(status_window)
    
    refresh_status_display()
    ### end: เพิ่มใหม่ (หน้าดูสถานะสินค้า) ###

### START: แก้ไขหน้า (Admin Manage Menu) ###
def admin_manage_menu_page(prev_window, default_category=None): # <<< 1. เพิ่ม default_category
    """ฟังก์ชันสำหรับหน้าจัดการเมนู"""
    if prev_window:
        prev_window.destroy()

    manage_menu_window = create_toplevel_window("Admin - จัดการเมนู")
    manage_menu_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(manage_menu_window))

    global bg_image_admin_manage_menu
    try:
        bg_image_manage_pil = Image.open(PIC_ADMIN_MANAGE_MENU) 
        bg_image_manage_pil = bg_image_manage_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_manage_menu = ImageTk.PhotoImage(bg_image_manage_pil)
        background_label = tk.Label(manage_menu_window, image=bg_image_admin_manage_menu)
        background_label.image = bg_image_admin_manage_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_MANAGE_MENU}")
        manage_menu_window.config(bg="#ffd7e8")

    canvas = tk.Canvas(manage_menu_window, bg="#ffd7e8", highlightthickness=1,highlightbackground="black", bd=0)
    scrollbar = ttk.Scrollbar(manage_menu_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffd7e8")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    def _on_mousewheel(event):
        if os.name == 'nt' or os.name == 'posix':
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=860) 
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.place(x=40, y=180, width=880, height=285) 
    scrollbar.place(x=920, y=180, height=285)

    def display_menu_items(category):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        MENU_ITEM_PIC_REFS.clear()
        
        filtered_items = get_menu_items_from_db(category) 

        row_num = 0
        col_num = 0
        card_width = 270
        card_height = 250 

        if not filtered_items: 
            tk.Label(scrollable_frame, text="ไม่มีรายการเมนูในหมวดหมู่นี้",
                         font=("Arial", 20), bg="#fff0f5").grid(row=0, column=0, columnspan=3, pady=20)

        for item in filtered_items:
            outer_card = tk.Frame(scrollable_frame, bg="#fff0f5", padx=5, pady=5)
            card = tk.Frame(outer_card, bg="white", bd=1, relief="solid", padx=5, pady=5)

            img_label = tk.Label(card, bg='#d3d3d3', width=20, height=8)
            try:
                img_placeholder_path = os.path.join(PIC_PATH, PIC_MENU_PLACEHOLDER)
                img_path = item['image_path'] or img_placeholder_path
                if not os.path.exists(img_path):
                    img_path = None 
                if img_path:
                    img = load_and_resize_pic(img_path, 120, is_menu_item=True)
                    img_label.config(image=img, width=120, height=120, bg='white')
                    img_label.image = img
                    MENU_ITEM_PIC_REFS[item['item_id']] = img
                else:
                    img_label.config(text="No Image", fg="black")
            except Exception as img_err:
                print(f"Error loading image for {item['name']}: {img_err}")
                img_label.config(text="Load Error", fg="red")
            img_label.pack(pady=(0, 5))
            
            status_frame = tk.Frame(card, bg="white")
            if item.get('is_available', 1) == 1:
                status_text = "มีสินค้า"
                status_bg = "#a0e0b0"
                status_fg = "#552c1f"
            else:
                status_text = "สินค้าหมด"
                status_bg = "#cccccc"
                status_fg = "#552c1f"
            status_label = tk.Label(status_frame, text=status_text, 
                font=("Arial", 10, "bold"), bg=status_bg, fg=status_fg,
                padx=5, pady=2
            )
            status_label.pack(side="left")
            
            if item.get('is_recommended', 0) == 1:
                rec_label = tk.Label(status_frame, text="⭐ แนะนำ",
                    font=("Arial", 10, "bold"), bg="#fff0b1", fg="#552c1f",
                    padx=5, pady=2
                )
                rec_label.pack(side="left", padx=5)
            
            status_frame.pack(fill="x", padx=0, pady=(0, 5))
            
            tk.Label(card, text=item['name'], font=("Arial", 15, "bold"), bg="white", anchor="w").pack(fill="x")
            tk.Label(card, text=item.get('description', ''), font=("Arial", 12), bg="white", anchor="nw", wraplength=card_width-30, justify="left", height=3).pack(fill="x")
            tk.Label(card, text=f"ราคา {item['price']:.2f} บาท", font=("Arial", 14, "bold"), bg="white", anchor="w").pack(fill="x", pady=(5, 5))

            btn_frame = tk.Frame(card, bg="white")
            edit_btn = tk.Button(btn_frame, text="แก้ไข", font=("Arial", 15, "bold"), bg="#c4e6fa", fg="black", width=7,
                                  command=lambda i=item: admin_edit_menu_page(manage_menu_window, i))
            del_btn = tk.Button(btn_frame, text="ลบ", font=("Arial", 15, "bold"), bg="#ff7bb5", fg="black", width=7,
                                  command=lambda i=item: delete_menu_item(i)) 
            edit_btn.pack(side="left", padx=10)
            del_btn.pack(side="right", padx=10)
            btn_frame.pack(fill="x", pady=(0, 5))

            card.pack(fill="both", expand=True)
            outer_card.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="nsew")

            col_num += 1
            if col_num >= 3:
                col_num = 0
                row_num += 1

        for i in range(3):
           scrollable_frame.grid_columnconfigure(i, weight=1, minsize=card_width + 10)
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)

    def delete_menu_item(item):
        if messagebox.askyesno("ยืนยันการลบ", f"คุณต้องการลบ '{item['name']}' ใช่หรือไม่?"):
            if db_delete_menu_item(item['item_id']): 
                messagebox.showinfo("ลบเมนู", f"ลบเมนู '{item['name']}' สำเร็จ")
                display_menu_items(current_category.get())

    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    category_buttons = {}
    tab_frame = tk.Frame(manage_menu_window, bg="#fff0f5", bd=0)
    tab_frame.place(x=40, y=135, height=45, width=750)

    current_category = tk.StringVar(value=categories[0]) 

    def select_category(category):
        current_category.set(category)
        display_menu_items(category)
        for cat, btn in category_buttons.items():
            if cat == category:
                btn.config(bg="#ffc1e0", relief="sunken") 
            else:
                btn.config(bg="#ffe0f1", relief="raised")

    for i, cat in enumerate(categories):
        btn = tk.Button(tab_frame, text=cat, font=("Arial", 16, "bold"),
                        bg="#ffe0f1", fg="#552c1f", relief="raised", bd=1,
                        activebackground="#ffc1e0",
                        command=lambda c=cat: select_category(c))
        btn.pack(side="left", fill="both", expand=True, padx=2, pady=2)
    
    add_button = tk.Button(manage_menu_window, text="เพิ่มเมนู", font=("Arial", 20, "bold"),
                           bg="#fff0b1", fg="#552c1f", relief="raised", bd=0,
                           # ---!! (2. แก้ไข) ส่งหมวดหมู่ปัจจุบันไป !! ---
                           command=lambda: admin_add_menu_page(manage_menu_window, current_category.get())) 
    add_button.place(x=810, y=90, width=110, height=45) 

    status_page_button = tk.Button(manage_menu_window, text="สถานะสินค้า", font=("Arial", 16, "bold"),
                           bg="#bfffcb", fg="#552c1f", relief="raised", bd=1,
                           command=lambda: admin_status_view_page(manage_menu_window))
    status_page_button.place(x=810, y=140, width=110, height=40) 

    back_button = tk.Button(manage_menu_window, text="ย้อนกลับ", font=("UID SALMON 2019", 45, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_panel_page(manage_menu_window))
    back_button.place(x=744, y=470, width=140, height=50)

    add_about_button(manage_menu_window)

    # ---!! (3. แก้ไข) เช็คว่ามี default_category ส่งมาหรือไม่ !! ---
    if default_category and default_category in categories:
        select_category(default_category)
    else:
        select_category(categories[0]) # ถ้าไม่ ให้ใช้ "ส้มตำ"

### END: แก้ไขหน้า (Admin Manage Menu) ###

### START: (หน้า Register) ###
def register_page(prev_window=None): 
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก'"""
    if prev_window:
        prev_window.destroy()

    register_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - สมัครสมาชิก")
    register_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(register_window))

    try:
        bg_image_register_pil = Image.open(f"{PIC_PATH}{PIC_REGISTER}")
        bg_image_register_pil = bg_image_register_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_register = ImageTk.PhotoImage(bg_image_register_pil)
        background_label_register = tk.Label(register_window, image=bg_image_register)
        background_label_register.image = bg_image_register
        background_label_register.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        register_window.destroy()
        root.deiconify()
        return

    username_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    username_entry.place(x=165, y=170, width=270, height=30)
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    password_entry.place(x=520, y=170, width=270, height=30)
    name_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    name_entry.place(x=165, y=235, width=270, height=30)
    surname_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    surname_entry.place(x=520, y=235, width=270, height=30)
    phone_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    phone_entry.place(x=165, y=300, width=270, height=30)
    birthday_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
    birthday_entry.place(x=520, y=300, width=270, height=30)
    email_entry = tk.Entry(register_window, font=("Arial", 20), bg="#ffebf6", bd=0, relief="flat")
    email_entry.place(x=340, y=370, width=270, height=30)
    back_button = tk.Button(register_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#E3B2C3", command=lambda: back_to_main_page(register_window))
    back_button.place(x=285, y=420, width=150, height=50)

    def local_save_registration_data():
        user, pwd, name, surname, phone, bday, email = username_entry.get(), password_entry.get(), name_entry.get(), surname_entry.get(), phone_entry.get(), birthday_entry.get(), email_entry.get()
        if not all([user, pwd, name, surname, phone, bday, email]):
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
            return

        ### START: เพิ่มโค้ดตรวจสอบรหัสผ่าน ###
        if len(pwd) < 8:
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            password_entry.delete(0, tk.END)
            return
        special_chars = "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?~`"
        if not any(char in special_chars for char in pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมีอักขระพิเศษอย่างน้อย 1 ตัว\nเช่น !, @, #, $, %")
            password_entry.delete(0, tk.END)
            return
        ### END: เพิ่มโค้ดตรวจสอบรหัสผ่าน ###

        ### START: เพิ่มโค้ดตรวจสอบเบอร์โทรศัพท์ ###
        if not phone.isdigit():
            messagebox.showerror("ผิดพลาด", "เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
            phone_entry.delete(0, tk.END)
            return
        if len(phone) != 10:
            messagebox.showerror("ผิดพลาด", "เบอร์โทรศัพท์ต้องมี 10 หลักพอดี")
            phone_entry.delete(0, tk.END)
            return
        ### END: เพิ่มโค้ดตรวจสอบเบอร์โทรศัพท์ ###

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user_account (username, password, name, surname, phone, birthday, email) VALUES (?, ?, ?, ?, ?, ?, ?)", (user, pwd, name, surname, phone, bday, email))
            cursor.execute("INSERT INTO user_profile (username, score, profile_pic_path) VALUES (?, ?, ?)", (user, 0, None))
            conn.commit()
            messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ชื่อผู้ใช้: {user} \nตอนนี้คุณสามารถเข้าสู่ระบบได้แล้ว")
            back_to_main_page(register_window)
        except sqlite3.IntegrityError:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) นี้ถูกใช้ไปแล้ว")
        except sqlite3.Error as e:
            messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถบันทึกได้: {e}")
        finally:
            conn.close()

    confirm_button = tk.Button(register_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                               activebackground="#E3B2C3",
                               command=local_save_registration_data)
    confirm_button.place(x=535, y=420, width=150, height=50)

    add_about_button(register_window)
### END: (หน้า Register) ###

# --- สร้างหน้าต่างหลัก ---
root = tk.Tk()
root.title("หนูดีส้มตำฟรุ้งฟริ้ง")
root.geometry("960x540")
root.resizable(True, True) # <<< แก้ไขให้ขยายได้

try:
    bg_image_pil = Image.open(f"{PIC_PATH}{PIC_MAIN}")
    bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image_pil)
    background_label = tk.Label(root, image=bg_image)
    background_label.image = bg_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"ไม่สามารถโหลดรูปภาพหลัก ({PIC_PATH}{PIC_MAIN}) ได้: {e}")
    root.destroy()
    exit()

# (ปุ่มหน้าหลักไม่เปลี่ยนแปลง)
login_button = tk.Button(root, text="เข้าสู่ระบบ", font=("UID SALMON 2019", 50, "bold"),
                         bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                         activebackground="#ffabcf",
                         command=login_page)
login_button.place(x=685, y=235, width=180, height=85)

register_button = tk.Button(root, text="สมัครสมาชิก", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#ffabcf",
                            command=register_page)
register_button.place(x=685, y=343, width=180, height=85)

add_about_button(root)
root.mainloop()