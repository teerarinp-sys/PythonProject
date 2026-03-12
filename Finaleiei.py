import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog, ttk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5  # (A5 เหมาะกับใบเสร็จมากกว่า A4)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import webbrowser
import sqlite3
import re
import os
import shutil
import math
import platform 
from datetime import datetime
from PIL import Image, ImageTk
from datetime import datetime, timedelta


# ==============================================================================
# 0. CONFIGURATION & GLOBAL VARIABLES
# =============================================================================

# ชื่อไฟล์ฐานข้อมูล
DB_NAME = "user_data.db"
PIC_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\"
PROFILE_PICS_DIR = "D:\\Project Nudee\\รูปโปรไฟล์ผู้ใช้\\"
MENU_PICS_DIR = "D:\\Project Nudee\\รูปเมนูอาหาร\\"
SLIP_PICS_DIR = "D:\\Project Nudee\\สลิปโอนเงิน\\"
PIC_CHECKOUT_PAGE ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\payment summary.png" 
PIC_PAYMENT_PAGE ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\pay.png"
PIC_ADMIN_SALES ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\Sales.png"

os.makedirs(PROFILE_PICS_DIR, exist_ok=True)
os.makedirs(MENU_PICS_DIR, exist_ok=True)
os.makedirs(SLIP_PICS_DIR, exist_ok=True)



# ชื่อไฟล์รูปภาพ
PIC_MAIN = "1.png"
PIC_LOGIN = "2.png"
PIC_REGISTER = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\3.png"
PIC_TABLE_SELECT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\7 Table.png"
PIC_PROFILE_VIEW ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\5 profile.png"
PIC_PROFILE_EDIT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\6 edit profile.png"
PIC_ABOUT = "about.png"
PIC_FORGOT_PASSWORD = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\4.png"
PIC_ADMIN_PANEL = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin.png"
PIC_ADMIN_TABLE_VIEW = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin table.png"
PIC_ADMIN_MANAGE_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin menu.png" 
PIC_ADMIN_ADD_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\add menu 6.png" 
PIC_ADMIN_EDIT_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\edit menu 7.png" 
PIC_ADMIN_STATUS_VIEW = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\Stock.png"
PIC_ADMIN_MANAGE_ORDER = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\edit table.png"
PIC_ADMIN_ORDERS_VIEW = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\order.png" 
global bg_image_admin_orders_view
bg_image_admin_orders_view = None
global bg_image_admin_manage_order
bg_image_admin_manage_order = None
PIC_MENU_PLACEHOLDER = "placeholder.png" 
PIC_CUSTOMER_MENU = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\9 menu.png"
PIC_CART_PAGE = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\basket.png"
PIC_CHECKOUT_PAGE ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\payment summary.png" 

ADMIN_USERNAME = "admineiei"
ADMIN_PASSWORD = "12345678"

VAT_RATE = 0.07 


ABOUT_BTN_CONFIG = {
    'text': "•••",
    'font': ("Arial", 30 , "bold"), 
    'bg': "#ff88bd",
    'fg': "#552c1f",
    'bd': 0,
    'relief': "ridge",
    'activebackground': "#E3B2C3",
    'x': 1203, 
    'y': 655, 
    'width': 50, 
    'height': 40 
}

CURRENT_USER = None
CURRENT_WINDOW = None
PROFILE_PIC_REF = {}
TABLE_PIC_REF = {}
MENU_ITEM_PIC_REFS = {} 
MENU_FORM_PIC_REF = {} 
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
global bg_image_admin_sales
bg_image_admin_sales = None
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
global TABLE_DISPLAY_REF
TABLE_DISPLAY_REF = {}




# ==============================================================================
# FUNCTION: RIGHT CLICK MENU (CUT/COPY/PASTE)
# ==============================================================================
def add_right_click_menu(widget):
    """เพิ่มเมนูคลิกขวา (ตัด/คัดลอก/วาง) ให้กับช่องกรอกข้อความ"""
    menu = tk.Menu(widget, tearoff=0, font=("Arial", 12))
    menu.add_command(label="ตัด (Cut)", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="คัดลอก (Copy)", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="วาง (Paste)", command=lambda: widget.event_generate("<<Paste>>"))

    def show_menu(event):
        widget.focus_set()
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    widget.bind("<Button-3>", show_menu)
    widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))
    widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))

# ******************************************************************************
# ฟังก์ชัน Utility: load_and_resize_pic, create_db_table
# ******************************************************************************
def load_and_resize_pic(file_path, size, is_menu_item=False): 
    """โหลดและปรับขนาดรูปภาพ"""
    default_color = '#d3d3d3' if is_menu_item else '#b8828b' 
    if file_path and os.path.exists(file_path):
        try:
            
            img_pil = Image.open(file_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening image {file_path}: {e}")
            img_pil = Image.new('RGB', (size, size), color=default_color) 
    else:
        
        img_pil = Image.new('RGB', (size, size), color=default_color)

    
    img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk


def create_db_table():
    """สร้างฐานข้อมูลและตารางต่างๆ (ปรับปรุงใหม่)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT, 
                surname TEXT, 
                phone TEXT, 
                birthday TEXT, 
                email TEXT,
                score INTEGER DEFAULT 0,       -- รวม score มาไว้ที่นี่
                profile_pic_path TEXT          -- รวม path รูปมาไว้ที่นี่
            )""")

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image_path TEXT,
                is_available INTEGER NOT NULL DEFAULT 1,
                is_recommended INTEGER NOT NULL DEFAULT 0 
            )""")

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number INTEGER NOT NULL,
                order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                subtotal REAL,                 -- ยอดก่อนหักส่วนลด (เพิ่มใหม่)
                discount_amount REAL DEFAULT 0,-- มูลค่าส่วนลด (เพิ่มใหม่)
                points_used INTEGER DEFAULT 0, -- แต้มที่ใช้ (เพิ่มใหม่)
                total_amount REAL,             -- ยอดสุทธิ (จ่ายจริง)
                status TEXT DEFAULT 'pending',
                slip_image_path TEXT,
                customer_username TEXT,
                FOREIGN KEY (customer_username) REFERENCES users(username)
            )""")

        
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
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถสร้างฐานข้อมูลได้: {e}")
    finally:
        if conn: conn.close()

create_db_table()

# ==============================================================================
# 1. NAVIGATION & UTILITY FUNCTIONS
# ==============================================================================
def back_to_main_page(current_window):
    """ฟังก์ชันสำหรับกลับไปหน้าหลัก (root) และออกจากระบบ (ถ้ามี)"""
    global CURRENT_USER
    if CURRENT_USER:
        CURRENT_USER = None 
    current_window.destroy()
    root.deiconify()

def about_page():
    """ฟังก์ชันสำหรับแสดงหน้า 'ผู้พัฒนาโปรแกรม' (About Me)"""
    about_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - ผู้พัฒนาโปรแกรม")
    global bg_image_about
    try:
        bg_image_about_pil = Image.open(f"{PIC_PATH}{PIC_ABOUT}")
        bg_image_about_pil = bg_image_about_pil.resize((1280, 720), Image.Resampling.LANCZOS) # <<< ใช้ขนาด 1280x720
        bg_image_about = ImageTk.PhotoImage(bg_image_about_pil)
        background_label_about = tk.Label(about_window, image=bg_image_about)
        background_label_about.image = bg_image_about
        background_label_about.place(x=0, y=0, relwidth=1, relheight=1)
        back_button = tk.Button(about_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50 , "bold"), bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid", activebackground="#ffe0f1", command=lambda: back_to_main_page(about_window))
        back_button.place(x=1080, y=640, width=170, height=60) # <<< ปรับตำแหน่ง/ขนาด
        
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพ About Page ได้: {e}")
        about_window.destroy()
        root.deiconify() 

def add_small_profile_button(parent_window, x=15, y=15, size=60):
    """
    สร้างปุ่มโปรไฟล์จิ๋ว (ฉบับแก้ไข: ป้องกันปุ่มหาย)
    """
    try:
        
        profile_frame = tk.Frame(parent_window, bg="white", bd=0, relief="flat")
        profile_frame.place(x=x, y=y, width=size, height=size)

        user_data = None
        pic_path = None
        
        if CURRENT_USER:
            user_data = get_user_data(CURRENT_USER)
            if user_data:
                pic_path = user_data.get('profile_pic_path')

        img_tk = None
        try:
            img_tk = load_and_resize_pic(pic_path, size)
        except Exception as e:
            print(f"Error loading profile pic: {e}")
            img_pil = Image.new('RGB', (size, size), color='#d3d3d3')
            img_tk = ImageTk.PhotoImage(img_pil)

        profile_btn = tk.Button(
            profile_frame,
            image=img_tk,
            bd=0,
            relief="flat",
            command=lambda: profile_view_page(parent_window)
        )
        
        profile_btn.image = img_tk 
        
        profile_btn.place(x=0, y=0, width=size, height=size)
        
    except Exception as e:
        print(f"Critical Error creating profile button: {e}")

# ==============================================================================
# 2. DATABASE LOGIC
# ==============================================================================

def get_user_data(username):
    """ ดึงข้อมูลผู้ใช้จากตาราง users (ตารางใหม่) """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_record = cursor.fetchone()
        if user_record:
            return dict(user_record)
        return None
    except Exception as e:
        print(f"Error get_user_data: {e}")
        return None
    finally:
        if conn: conn.close()
def update_user_profile(old_username, new_data):
    """ อัปเดตข้อมูลผู้ใช้ในตาราง users (แก้ไขแล้ว) """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        
        cursor.execute("""
            UPDATE users
            SET username = ?, name = ?, surname = ?, phone = ?, birthday = ?, email = ?, profile_pic_path = ?
            WHERE username = ?
        """, (new_data['username'], new_data['name'], new_data['surname'],
              new_data['phone'], new_data['birthday'], new_data['email'],
              new_data['pic_path'], old_username))

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
        if conn: conn.close()



def get_menu_items_from_db(category):
    """ดึงรายการเมนูจากฐานข้อมูลตามหมวดหมู่"""
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu_items WHERE category = ? ORDER BY is_available DESC, item_id ASC", (category,))
        
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
        messagebox.showerror("Database Error", f"Could not update profile: {e}")
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

def get_all_table_statuses():
    """
    (ฟังก์ชันใหม่) ดึงสถานะโต๊ะทั้งหมด
    คืนค่าเป็น Set ของเบอร์โต๊ะที่ "ไม่ว่าง" (pending หรือ paid)
    """
    occupied_tables = set()
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT table_number 
            FROM orders 
            WHERE status = 'pending' OR status = 'paid' OR status = 'served'
        """)
        rows = cursor.fetchall()
        for row in rows:
            occupied_tables.add(row[0])
    except Exception as e:
        print(f"Error get_all_table_statuses: {e}")
    finally:
        if conn: conn.close()
    return occupied_tables

def get_active_order_for_table(table_num):
    """
    (ฟังก์ชันใหม่) ดึงข้อมูลออเดอร์ล่าสุดที่ยัง "ไม่เสร็จ" (paid หรือ pending) ของโต๊ะนั้น
    """
    order_data = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM orders 
            WHERE table_number = ? AND (status = 'paid' OR status = 'pending'OR status = 'served')
            ORDER BY order_time DESC 
            LIMIT 1
        """, (table_num,))
        row = cursor.fetchone()
        if row:
            order_data = dict(row)
    except Exception as e:
        print(f"Error get_active_order_for_table: {e}")
    finally:
        if conn: conn.close()
    return order_data

def get_order_details_from_db(order_id):
    """
    (ฟังก์ชันใหม่) ดึงรายการอาหารทั้งหมดในออเดอร์ (join กับ menu_items)
    """
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT od.*, mi.name 
            FROM order_details od
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE od.order_id = ?
        """, (order_id,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not fetch order details: {e}")
    finally:
        if conn: conn.close()
    return items
def get_all_paid_items_for_table(table_num):
    """
    (แก้ไขล่าสุด) ดึงเฉพาะรายการที่ 'กำลังดำเนินการ' (Paid/Pending) ของโต๊ะนั้น
    *ตัดรายการที่ 'เสร็จสิ้นแล้ว' (Completed) ออกไป* เพื่อให้เห็นเฉพาะลูกค้าคนปัจจุบัน
    """
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT od.*, mi.name, o.order_id, o.slip_image_path, o.order_time, o.status, o.subtotal, o.discount_amount
            FROM order_details od
            JOIN orders o ON od.order_id = o.order_id
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE o.table_number = ? AND (o.status = 'paid' OR o.status = 'pending'OR o.status = 'served')
            ORDER BY o.order_id DESC
        """, (table_num,))
        
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching all items: {e}")
    finally:
        if conn: conn.close()
    return items

def db_complete_order(order_id):
    """
    (ฟังก์ชันใหม่) "เสร็จสิ้นรายการ" - เปลี่ยนสถานะออเดอร์เป็น 'completed'
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = 'completed' WHERE order_id = ?", (order_id,))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not complete order: {e}")
        return False
    finally:
        if conn: conn.close()

def get_all_paid_orders():
    """
    (ฟังก์ชันใหม่) ดึงออเดอร์ทั้งหมดที่ 'paid' (รอแอดมินยืนยัน)
    เรียงตามโต๊ะ แล้วตามเวลา
    """
    orders = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM orders 
            WHERE status = 'paid' 
            ORDER BY order_time ASC  -- ASC = เรียงจากเก่าไปใหม่ (ออเดอร์แรกขึ้นก่อน)
        """)
        rows = cursor.fetchall()
        orders = [dict(row) for row in rows]
    except Exception as e:
        print(f"Error get_all_paid_orders: {e}")
    finally:
        if conn: conn.close()
    return orders

def copy_slip_image(source_path, order_id):
    """คัดลอกรูปภาพสลิปไปยังโฟลเดอร์และคืนค่า Path ใหม่"""
    if not source_path or not os.path.exists(source_path):
        return None
    try:
        _, extension = os.path.splitext(source_path)
        new_filename = f"order_{order_id}{extension}"
        dest_path = os.path.join(SLIP_PICS_DIR, new_filename)

        shutil.copy(source_path, dest_path)
        return dest_path
    except Exception as e:
        messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกสลิปได้: {e}")
        return None
    
def db_mark_order_as_served(order_id):
    """เปลี่ยนสถานะเป็น 'served' (ทำเสร็จแล้ว แต่ลูกค้ายังนั่งอยู่)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = 'served' WHERE order_id = ?", (order_id,))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("Database Error", f"อัปเดตสถานะไม่สำเร็จ: {e}")
        return False
    finally:
        if conn: conn.close()

# ==============================================================================
# 5. PDF GENERATION (ReportLab implementation)
# ==============================================================================
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os
import webbrowser
from datetime import datetime

LOGO_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\logo.png" 
FONT_TH_PATH = "D:\\Windows\\Fonts\\Tahoma.ttf"  
FONT_NAME = "Tahoma" 

def generate_receipt_pdf(order_data, order_details_list, total_before_vat, vat_amount, grand_total):
    """
    สร้างไฟล์ PDF ใบเสร็จรับเงิน
    """
    if not os.path.exists(FONT_TH_PATH):
        messagebox.showerror("Font Error", f"ไม่พบไฟล์ฟอนต์ที่: {FONT_TH_PATH}")
        return

    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_TH_PATH))
    except Exception as e:
        messagebox.showerror("Font Error", f"ไม่สามารถลงทะเบียนฟอนต์ได้: {e}")
        return

    try:
        order_id = order_data['order_id']
        table_num = order_data['table_number']
        order_time_str = order_data['order_time']
        
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(downloads_path):
             downloads_path = os.path.expanduser('~') 
        pdf_filename = os.path.join(downloads_path, f"Receipt_NU{order_id:05d}.pdf")

        pdf = canvas.Canvas(pdf_filename, pagesize=A4)
        width, height = A4 
        margin_x = 1.5*cm
        current_y = height - 2*cm
        
        pdf.setFont(FONT_NAME, 20)
        pdf.drawCentredString(width / 2.0, current_y, "หนูดีส้มตำฟรุ้งฟริ้ง")
        current_y -= 0.8*cm
        pdf.setFont(FONT_NAME, 14)
        pdf.drawCentredString(width / 2.0, current_y, "ใบเสร็จรับเงิน")
        current_y -= 1.0*cm

        pdf.setFont(FONT_NAME, 12)
        pdf.drawString(margin_x, current_y, f"เลขที่: NU{order_id:05d}")
        pdf.drawRightString(width - margin_x, current_y, datetime.now().strftime(f"พิมพ์เมื่อ: %d/%m/{datetime.now().year + 543} %H:%M"))
        current_y -= 0.6*cm
        
        try:
            dt_obj = datetime.strptime(order_time_str, "%Y-%m-%d %H:%M:%S")
            display_time = dt_obj.strftime(f"%d/%m/{dt_obj.year + 543} %H:%M")
        except:
            display_time = order_time_str
            
        pdf.drawString(margin_x, current_y, f"โต๊ะ: {table_num}")
        pdf.drawString(margin_x + 4*cm, current_y, f"เวลาสั่ง: {display_time}")
        current_y -= 1.0*cm
        pdf.line(margin_x, current_y, width - margin_x, current_y)
        current_y -= 0.6*cm
        col_x = [margin_x, margin_x + 2*cm, margin_x + 10*cm, width - margin_x - 3*cm, width - margin_x]
        
        pdf.setFont(FONT_NAME, 12)
        pdf.drawString(col_x[0], current_y, "รายการอาหาร")
        pdf.drawString(col_x[2], current_y, "ราคา/หน่วย")
        pdf.drawString(col_x[3], current_y, "จำนวน")
        pdf.drawRightString(col_x[4], current_y, "รวม")
        
        current_y -= 0.3*cm
        pdf.line(margin_x, current_y, width - margin_x, current_y)
        current_y -= 0.3*cm

        for item in order_details_list:
            item_total = item['price_per_item'] * item['quantity']
            
            if current_y < 4*cm:
                pdf.showPage()
                current_y = height - 2*cm
                pdf.setFont(FONT_NAME, 12)
                pdf.drawString(margin_x, current_y, "รายการอาหาร (ต่อ)")
                current_y -= 1.0*cm
            
            pdf.drawString(col_x[0], current_y, item['name'])
            pdf.drawRightString(col_x[2], current_y, f"{item['price_per_item']:,.2f} บ.")
            pdf.drawRightString(col_x[3], current_y, f"x {item['quantity']}")
            pdf.drawRightString(col_x[4], current_y, f"{item_total:,.2f} บ.")
            current_y -= 0.7*cm
            
        pdf.line(margin_x, current_y, width - margin_x, current_y)
        current_y -= 0.8*cm
        pdf.setFont(FONT_NAME, 12)
        pdf.drawString(width - 6*cm, current_y, "มูลค่าสินค้า (ก่อนภาษี):")
        pdf.drawRightString(width - margin_x, current_y, f"{total_before_vat:,.2f} บ.")
        current_y -= 0.6*cm
        pdf.drawString(width - 6*cm, current_y, f"ภาษีมูลค่าเพิ่ม ({VAT_RATE*100:.0f}%):")
        pdf.drawRightString(width - margin_x, current_y, f"{vat_amount:,.2f} บ.")
        current_y -= 0.6*cm
        pdf.line(width - 6.5*cm, current_y, width - margin_x, current_y)
        current_y -= 0.3*cm
        pdf.setFont(FONT_NAME, 14)
        pdf.drawString(width - 6*cm, current_y, "รวมทั้งสิ้น:")
        pdf.drawRightString(width - margin_x, current_y, f"฿ {grand_total:,.2f}")
        current_y -= 0.8*cm
        pdf.line(width - 6.5*cm, current_y, width - margin_x, current_y)
        pdf.setFont(FONT_NAME, 10)
        pdf.drawCentredString(width / 2.0, 1*cm, "ขอบคุณที่ใช้บริการค่ะ")
        pdf.save()
        messagebox.showinfo("สำเร็จ", f"สร้างใบเสร็จเรียบร้อย! บันทึกที่: {pdf_filename}")
        webbrowser.open(f"file:///{pdf_filename}")
        
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        messagebox.showerror("PDF Error", f"ไม่สามารถสร้างไฟล์ PDF ได้: {e}")

def get_order_details_for_receipt(order_id):
    """ดึงข้อมูลออเดอร์และรายการสินค้าสำหรับใช้ในใบเสร็จ"""
    order_data = {}
    order_details_list = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order_data = dict(cursor.fetchone())
        cursor.execute("""
            SELECT od.*, mi.name 
            FROM order_details od
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE od.order_id = ?
        """, (order_id,))
        order_details_list = [dict(row) for row in cursor.fetchall()]
        
        return order_data, order_details_list
    except Exception as e:
        print(f"Error fetching receipt data: {e}")
        messagebox.showerror("DB Error", "ไม่สามารถดึงข้อมูลออเดอร์เพื่อสร้างใบเสร็จได้")
        return None, None
    finally:
        if conn: conn.close()

def confirm_payment(order_id, slip_source_path, all_windows, table_num):
    """(ฟังก์ชันใหม่) ยืนยันการชำระเงิน, อัปโหลดสลิป, และปิดหน้าต่าง"""
    
    final_slip_path = None
    if slip_source_path:
        final_slip_path = copy_slip_image(slip_source_path, order_id)
        if final_slip_path is None:
            messagebox.showwarning("ผิดพลาด", "ไม่สามารถบันทึกสลิปได้ กรุณาลองใหม่")
            return
    else:
        messagebox.showwarning("ยังไม่เสร็จสิ้น", "กรุณาแนบสลิปหลักฐานการโอนเงินก่อนกดยืนยันค่ะ")
        return 

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE orders 
            SET status = 'paid', slip_image_path = ?
            WHERE order_id = ?
        """, (final_slip_path, order_id))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ไม่สามารถยืนยันออเดอร์ได้: {e}")
        return
    finally:
        conn.close() 
    try:
        order_data, order_details_list = get_order_details_for_receipt(order_id)
        if order_data and order_details_list:
            generate_receipt_pdf(order_data, order_details_list, table_num)
            messagebox.showinfo("สำเร็จ", "ยืนยันการชำระเงินเรียบร้อย!")
    except Exception as e:
        print(f"PDF Error: {e}")
        messagebox.showinfo("สำเร็จ", "ชำระเงินเรียบร้อย (แต่สร้างใบเสร็จขัดข้อง)")

    for window in all_windows:
        if window:
            try:
                window.destroy()
            except:
                pass
                
    global CURRENT_ORDER, CURRENT_REDEMPTION
    CURRENT_ORDER.clear()
    CURRENT_REDEMPTION.clear()
    customer_menu_page(table_num)

# ==============================================================================
# 3. GUI WINDOW CREATION
# ==============================================================================

def create_toplevel_window(title):
    """ฟังก์ชันรวมสำหรับสร้างหน้าต่างย่อย (Toplevel) และซ่อนหน้าหลัก"""
    root.withdraw()
    new_window = tk.Toplevel(root)
    new_window.title(title)
    new_window.geometry("1280x720") 
    new_window.resizable(True, True) 
    new_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(new_window))
    return new_window

def about_page():
    """ฟังก์ชันสำหรับแสดงหน้า 'ผู้พัฒนาโปรแกรม' (About Me)"""
    about_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - ผู้พัฒนาโปรแกรม")
    global bg_image_about
    try:
        bg_image_about_pil = Image.open(f"{PIC_PATH}{PIC_ABOUT}")
        bg_image_about_pil = bg_image_about_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_about = ImageTk.PhotoImage(bg_image_about_pil)
        background_label_about = tk.Label(about_window, image=bg_image_about)
        background_label_about.image = bg_image_about
        background_label_about.place(x=0, y=0, relwidth=1, relheight=1)
        back_button = tk.Button(about_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50 , "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised", activebackground="#ffe0f1", command=lambda: back_to_main_page(about_window))
        back_button.place(x=1050, y=650, width=200, height=65) 
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพ About Page ได้: {e}")
        about_window.destroy()
        root.deiconify() 


def add_small_profile_button(parent_window, x=15, y=15, size=60): 
    """
    สร้างปุ่มโปรไฟล์จิ๋วบนหน้าต่างที่กำหนด
    เมื่อกดจะไปที่หน้า profile_view_page
    """

    profile_frame = tk.Frame(parent_window, bg="white", bd=0, relief="flat")
    profile_frame.place(x=x, y=y, width=size, height=size)
    user_data = get_user_data(CURRENT_USER)
    pic_path = user_data.get('profile_pic_path') if user_data else None
    img_tk = load_and_resize_pic(pic_path, size)
    profile_btn = tk.Button(
        profile_frame,
        image=img_tk,
        bd=0,
        relief="flat",
        command=lambda: profile_view_page(parent_window)
    )
    
    profile_btn.image = img_tk 
    
    profile_btn.place(x=0, y=0, width=size, height=size)

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


def add_table_display(parent_window, table_num, x=99, y=15, width=55, height=55):
    """
    สร้างกรอบแสดงหมายเลขโต๊ะเท่านั้น และจัดชิดขวาของกรอบ (ใช้ place + anchor='e')
    """

    table_frame = tk.Frame(parent_window, bg="#ffe0f1", 
                            highlightbackground="#552c1f", 
                            highlightthickness=0)
    table_frame.place(x=x, y=y, width=width, height=height)

    tk.Label(table_frame, 
             text=f"{table_num}", 
             font=("UID SALMON 2019", 45, "bold"), 
             bg="#ffe0f1", 
             fg="#552c1f"
            ).place(relx=0.96, rely=0.5, anchor='e') 
    
def table_selection_page(prev_window=None):
    if prev_window: prev_window.destroy()
    global CURRENT_WINDOW
    table_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - เลือกโต๊ะ")
    CURRENT_WINDOW = table_window
    global bg_image_table_select
    try:
        bg_image_table_select_pil = Image.open(PIC_TABLE_SELECT)
        bg_image_table_select_pil = bg_image_table_select_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
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
    occupied_tables = get_all_table_statuses()

    def select_table(table_num):
        selected_table.set(table_num)
        print(f"เลือกโต๊ะ: {table_num}")
        for num, btn in table_buttons.items():

            if num in occupied_tables:
                continue 
            if num != table_num:
                btn.config(bg=original_button_bg, relief="raised")
            else:
                btn.config(bg=selected_button_bg, relief="sunken")

    button_width = 200 
    button_height = 200
    y1 = 80 
    y2 = 350 
    total_width_needed = (4 * button_width) + (3 * 45) 
    start_x = (1280 - total_width_needed) / 2 
    start_x = 172 
    x_gap = 45 

    table_coords = [
        (start_x, y1), (start_x + 1*(button_width + x_gap), y1), (start_x + 2*(button_width + x_gap), y1), (start_x + 3*(button_width + x_gap), y1),  
        (start_x, y2), (start_x + 1*(button_width + x_gap), y2), (start_x + 2*(button_width + x_gap), y2), (start_x + 3*(button_width + x_gap), y2)
    ]

    for i, (x, y) in enumerate(table_coords):
        table_num = i + 1 
        
        btn_state = "normal"
        btn_bg = original_button_bg
        
        if table_num in occupied_tables:
            btn_state = "disabled"
            btn_bg = "#cccccc"
        
        btn = tk.Button(table_window, text=f"โต๊ะ {table_num}", font=("UID SALMON 2019", 90), 
                         bg=btn_bg, fg="#552c1f", bd=2 , relief="solid", 
                         state=btn_state,
                         command=lambda num=table_num: select_table(num))
        
        btn.place(x=x, y=y, width=button_width , height=button_height) 
        table_buttons[table_num] = btn 
        status_icon_text = "❌" if table_num in occupied_tables else "✓"
        status_icon_bg = "#ff4d4d" if table_num in occupied_tables else "#bfffcb"
        status_icon_fg = "white" if table_num in occupied_tables else "#006b2c"
        
        status_icon_label = tk.Label(table_window, text=status_icon_text, 
                                     font=("Arial", 30, "bold"), 
                                     bg=status_icon_bg, fg=status_icon_fg, 
                                     bd=2, relief="solid")
        status_icon_label.place(x=x + button_width - 45, y=y + 5, width=40, height=40)

    back_button = tk.Button(table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 60,"bold" ), bg="#ffe0f1", fg="#552c1f",  bd=2 , relief="solid", command=lambda: back_to_main_page(table_window))
    back_button.place(relx=0.42, rely=0.88, anchor="e", width=250, height=80) 
    
    next_button = tk.Button(table_window, text="ต่อไป", font=("UID SALMON 2019", 60,"bold" ), bg="#ffe0f1", fg="#552c1f",  bd=2 , relief="solid", command=lambda: open_menu_page(table_window, selected_table.get()))
    next_button.place(relx=0.58, rely=0.88, anchor="w", width=250, height=80) 
    add_small_profile_button(table_window)

    add_about_button(table_window) 
    
def open_menu_page(current_window, selected_table):
    if not selected_table or selected_table == 'None':
        messagebox.showwarning("ยังไม่ได้เลือก", "กรุณาเลือกโต๊ะก่อนดำเนินการต่อ")
        return
    
    current_window.destroy()
    customer_menu_page(selected_table) 

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
        bg_image_profile_pil = bg_image_profile_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
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
        x_pos, y_pos, size = 130, 180, 240 
        frame = tk.Frame(window, bg='white', width=size, height=size, bd=0)
        frame.place(x=x_pos, y=y_pos)
        img_tk = load_and_resize_pic(pic_path, size)
        PROFILE_PIC_REF['pic_view'] = img_tk
        pic_label = tk.Label(frame, image=img_tk, bd=0)
        pic_label.place(x=0, y=0, relwidth=1, relheight=1)
        return pic_label

    font_style = ("Arial", 20)
    text_color = "#e37494"
    
    tk.Label(profile_window, text=f"{user_data.get('username', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=185, y=470, width=160 , height= 40)
    
    name_full = f"{user_data.get('name', '-')} {user_data.get('surname', '-')}"
    tk.Label(profile_window, text=name_full, font=font_style, fg=text_color, bg="#ffe0f1").place(x=635, y=210, width=400 , height= 40)
    
    tk.Label(profile_window, text=f"{user_data.get('phone', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=570, y=300, width=200 , height= 40)
    
    tk.Label(profile_window, text=f"{user_data.get('birthday', '-')}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=540, y=380, width=220 , height= 40)
    
    tk.Label(profile_window, text=f"{user_data.get('email', '-')}", font=("Arial", 20), fg=text_color, bg="#ffe0f1").place(x=540, y=440, width=400 , height= 40) 
    
    tk.Label(profile_window, text=f" {user_data.get('score', 0)}", font=font_style, fg="#552c1f", bg="#ffe0f1").place(x=680, y=520, width=130 , height= 40)
    
    display_profile_pic(profile_window, user_data.get('profile_pic_path')) 
    
    edit_button = tk.Button(profile_window, text="แก้ไข", font=("UID SALMON 2019", 45, "bold"), bg="#fffbf2", fg="#552c1f", bd=0, relief="flat", command=lambda: profile_edit_page(profile_window, user_data))
    edit_button.place(x=1060, y=115, width=100, height=50) 
    
    back_button = tk.Button(profile_window, text="ย้อนกลับ", font=("UID SALMON 2019", 55, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: table_selection_page(profile_window))
    back_button.place(x=400, y=600, width=180, height=80) 
    
    logout_button = tk.Button(profile_window, text="ออกจากระบบ", font=("UID SALMON 2019", 55, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: back_to_main_page(profile_window))
    logout_button.place(x=705, y=600, width=195, height=80) 
    
    add_about_button(profile_window)

def profile_edit_page(prev_window, user_data):
    global PROFILE_PIC_REF
    prev_window.destroy()
    edit_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - แก้ไขโปรไฟล์")
    try:
        bg_image_edit_pil = Image.open(PIC_PROFILE_EDIT)
        bg_image_edit_pil = bg_image_edit_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
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
    current_pic_path = tk.StringVar(value=user_data.get('profile_pic_path', '')) 
    pic_label_ref = None
    pic_frame_ref = None
    
    def display_profile_pic(window, pic_path_var):
        nonlocal pic_label_ref, pic_frame_ref
        x_pos, y_pos, size = 130, 175, 240 
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
                
    entry_font = ("Arial", 20) 
    bg_color_entry = "#ffffff"
    
    tk.Entry(edit_window, textvariable=name_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=660, y=210, width=200, height=40) 
    tk.Entry(edit_window, textvariable=surname_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=940, y=210, width= 200, height=40) 
    tk.Entry(edit_window, textvariable=phone_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=590, y=300, width=200, height=40) 
    tk.Entry(edit_window, textvariable=birthday_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=570, y=375, width=170 , height= 40) 
    tk.Entry(edit_window, textvariable=email_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=570, y=440, width=250, height=40) 
    
    username_entry = tk.Entry(edit_window, textvariable=username_var, font=entry_font, bg=bg_color_entry, bd=0)
    username_entry.place(x=210, y=470, width=130, height=40) 
    
    display_profile_pic(edit_window, current_pic_path)
    
    change_pic_button = tk.Button(edit_window, text="เปลี่ยน", font=("UID SALMON 2019", 20, "bold"), 
                                  bg="#ffffff", fg="#552c1f", bd=0, relief="flat",
                                  command=choose_profile_pic)
    change_pic_button.place(x=175, y=420, width=120, height=30) 

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

    back_button = tk.Button(edit_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: profile_view_page(edit_window, user_data))
    back_button.place(x=400, y=600, width=180, height=80) 
    
    save_button = tk.Button(edit_window, text="บันทึก", font=("UID SALMON 2019", 50, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=save_changes)
    save_button.place(x=695, y=600, width=180, height=80) 
    add_about_button(edit_window)


def add_item_to_order(item, table_num):
    """เพิ่มสินค้าลงในตะกร้า (CURRENT_ORDER)"""
    global CURRENT_ORDER
    item_id = item['item_id']
    
    if item_id in CURRENT_ORDER:
        CURRENT_ORDER[item_id]['quantity'] += 1
    else:
        CURRENT_ORDER[item_id] = {
            'name': item['name'],
            'price': item['price'],
            'quantity': 1,
            'item_id': item_id 
        }
    
    
    messagebox.showinfo("เพิ่มรายการ", f"เพิ่ม '{item['name']}' 1 รายการ ลงในตะกร้าแล้ว")
    print(f"โต๊ะ {table_num} ตะกร้าปัจจุบัน: {CURRENT_ORDER}") 

def submit_order(menu_window, cart_window, checkout_window, table_num):
    """บันทึกออเดอร์ลงฐานข้อมูล (พร้อมระบบคะแนนสะสม - แก้ไขแล้ว)"""
    global CURRENT_ORDER, CURRENT_USER, CURRENT_REDEMPTION
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        subtotal = 0
        for item in CURRENT_ORDER.values():
            subtotal += item['price'] * item['quantity']
        
        points_used = CURRENT_REDEMPTION.get('points_used', 0)
        discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)
        grand_total = subtotal - discount_amount
        

        cursor.execute("""
            INSERT INTO orders (table_number, subtotal, discount_amount, points_used, total_amount, customer_username, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (table_num, subtotal, discount_amount, points_used, grand_total, CURRENT_USER))
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
            cursor.execute("UPDATE users SET score = score - ? WHERE username = ?", (points_used, CURRENT_USER))

        points_earned = int(grand_total // 100) 
        if points_earned > 0:
            cursor.execute("UPDATE users SET score = score + ? WHERE username = ?", (points_earned, CURRENT_USER))
        conn.commit()        
        payment_page(menu_window, cart_window, checkout_window, new_order_id, grand_total, table_num)        
        CURRENT_ORDER.clear()
        CURRENT_REDEMPTION.clear()        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ไม่สามารถบันทึกออเดอร์ได้: {e}")
    finally:
        if conn: conn.close()
global slip_photo_tk
slip_photo_tk = None

def payment_page(menu_window, cart_window, checkout_window, order_id, final_total, table_num):
    """(ฟังก์ชันใหม่) แสดงหน้าชำระเงิน QR Code และแนบสลิป"""
    
    if checkout_window:
        checkout_window.destroy() 

    global bg_image_payment_page
    
    payment_window = create_toplevel_window(f"หนูดีส้มตำฟรุ้งฟริ้ง - ยืนยันออเดอร์ #{order_id}")
    payment_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - ยืนยันออเดอร์ #{order_id}")
    
    payment_window.resizable(True, True)

    slip_path_var = tk.StringVar(value="") 

    def go_back_to_checkout():
        """ย้อนกลับไปหน้าสรุปยอด (ออเดอร์ยัง pending)"""
        payment_window.destroy()
        if checkout_window:
            checkout_window.deiconify() 
    payment_window.protocol("WM_DELETE_WINDOW", go_back_to_checkout)

    try:
        bg_image_pil = Image.open(PIC_PAYMENT_PAGE)
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_payment_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(payment_window, image=bg_image_payment_page)
        background_label.image = bg_image_payment_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_PAYMENT_PAGE}")
        payment_window.config(bg="#ffd7e8")

    total_frame = tk.Frame(payment_window, bg="#fff0f5", bd=2, relief="solid")
    total_frame.place(relx=0.72, rely=0.25, anchor="center", width=400, height=120) 
    total_label = tk.Label(total_frame, text=f"ราคารวมทั้งสิ้น\n{final_total:,.2f} บาท",
                             font=("Arial", 30, "bold"), bg="#fff0f5", fg="#552c1f") 
    total_label.pack(pady=5)
    
    def choose_slip(event): 
        global slip_photo_tk
        
        source_path = filedialog.askopenfilename(
            title="เลือกไฟล์สลิป",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            slip_path_var.set(source_path)
            
            try:
                slip_image_pil = Image.open(source_path)
                frame_width = 400
                frame_height = 400
                original_w, original_h = slip_image_pil.size
                ratio = min(frame_width / original_w, frame_height / original_h)
                new_w = int(original_w * ratio)
                new_h = int(original_h * ratio)
                slip_image_pil = slip_image_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
                slip_photo_tk = ImageTk.PhotoImage(slip_image_pil)
                
                
                slip_label_display.config(image=slip_photo_tk, text="") 
                slip_label_display.image = slip_photo_tk 
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดไฟล์สลิปได้: {e}")
                slip_path_var.set("")
                slip_label_display.config(image="", text="ไฟล์สลิปไม่ถูกต้อง", font=("Arial", 25))
                slip_photo_tk = None

        else:
            slip_path_var.set("")
            slip_label_display.config(image="", text="แนบหลักฐานการโอน", font=("Arial", 25, "bold")) 
            slip_photo_tk = None

    slip_label_display = tk.Label(payment_window, 
                                     text="แนบหลักฐานการโอน", 
                                     font=("Arial", 25, "bold"), 
                                     bg="#fff0f5", 
                                     fg="#552c1f", 
                                     bd=2, 
                                     relief="solid",
                                     wraplength=350,
                                     justify="center")

    slip_label_display.bind("<Button-1>", choose_slip) 
    slip_label_display.place(relx=0.72, rely=0.58, anchor="center", width=400, height=400) 
    confirm_btn = tk.Button(payment_window, text="ยืนยันชำระเงิน", font=("UID SALMON 2019", 45, "bold"),
                             bg="#bfffcb", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: confirm_payment(order_id, slip_path_var.get(), [menu_window, cart_window, checkout_window, payment_window], table_num))
    confirm_btn.place(relx=0.5, rely=0.93, anchor="center", width=380, height=80)
    
    back_btn = tk.Button(payment_window, text="ย้อนกลับ", font=("UID SALMON 2019", 45, "bold"),
                          bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                          command=go_back_to_checkout)
    back_btn.place(relx=0.10, rely=0.93, anchor="center", width=200, height=80) 
    add_small_profile_button(payment_window)
    add_table_display(payment_window, table_num)
    add_about_button(payment_window)

def cart_page(prev_window, table_num):
    """แสดงหน้าตะกร้าสินค้า (พร้อมระบบแลกคะแนน)"""
    if prev_window:
        prev_window.withdraw() 

    global bg_image_cart_page, CURRENT_ORDER, CURRENT_REDEMPTION
    
    cart_window = create_toplevel_window(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {table_num} - ตะกร้า")
    cart_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {table_num} - ตะกร้า")

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
    try:
        bg_image_pil = Image.open(PIC_CART_PAGE)
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_cart_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(cart_window, image=bg_image_cart_page)
        background_label.image = bg_image_cart_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CART_PAGE}")
        cart_window.config(bg="#ffd7e8")
    
    list_frame_bg = tk.Frame(cart_window, bg="#fff0f5", bd=2, relief="solid")
    list_frame_bg.place(relx=0.5, rely=0.48, anchor="center", width=1040, height=400)
    list_canvas = tk.Canvas(list_frame_bg, bg="#fff0f5", bd=0, highlightthickness=0)
    list_scrollbar = ttk.Scrollbar(list_frame_bg, orient="vertical", command=list_canvas.yview)
    list_scrollable_frame = tk.Frame(list_canvas, bg="#fff0f5")
    list_scrollable_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    def _on_mousewheel_cart(event):
        if platform.system() == 'Windows':
            delta = int(-1*(event.delta/120))
        elif event.num == 4: 
            delta = -1
        elif event.num == 5: 
            delta = 1
        else:
            delta = event.delta
        
        list_canvas.yview_scroll(delta, "units")

    list_canvas.bind_all("<MouseWheel>", _on_mousewheel_cart)
    
    list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw", width=1010) 
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
        for widget in list_scrollable_frame.winfo_children():
            widget.destroy()
        row_font = ("Arial", 18) 
        total_price = 0
        header_frame = tk.Frame(list_scrollable_frame, bg="#ffc1e0")
        header_frame.grid_columnconfigure(0, weight=3, minsize=400) # เมนู
        header_frame.grid_columnconfigure(1, weight=1, minsize=150) # ราคา/หน่วย
        header_frame.grid_columnconfigure(2, weight=1, minsize=200) # จำนวน
        header_frame.grid_columnconfigure(3, weight=2, minsize=250) # รวม
        
        header_font = ("Arial", 18, "bold")
        header_fg = "#552c1f"
        tk.Label(header_frame, text="เมนู", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5) 
        tk.Label(header_frame, text="ราคา/หน่วย", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=5) 
        tk.Label(header_frame, text="จำนวน", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="center").grid(row=0, column=2, padx=10, pady=5) 
        tk.Label(header_frame, text="รวม", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=5) 
        header_frame.pack(fill="x", pady=(0, 10))
        if not CURRENT_ORDER:
            tk.Label(list_scrollable_frame, text="ตะกร้าของคุณว่าง", font=("Arial", 25, "bold"), bg="#fff0f5", fg="#552c1f").pack(pady=80) 
        for item_id, item_data in CURRENT_ORDER.items():
            item_total = item_data['price'] * item_data['quantity']
            total_price += item_total
            row_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
            row_frame.grid_columnconfigure(0, weight=3, minsize=400) 
            row_frame.grid_columnconfigure(1, weight=1, minsize=150) 
            row_frame.grid_columnconfigure(2, weight=1, minsize=200) 
            row_frame.grid_columnconfigure(3, weight=2, minsize=250) 
            
            tk.Label(row_frame, text=item_data['name'], font=row_font, bg="#fff0f5", fg="#552c1f", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=8) 
            tk.Label(row_frame, text=f"{item_data['price']:,.2f} บ.", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=8) 
            
            control_frame = tk.Frame(row_frame, bg="#fff0f5")
            minus_btn = tk.Button(control_frame, text="—", font=("Arial", 22, "bold"), bg="#ffc1e0", fg="#552c1f", bd=0, relief="solid", width=3, 
                                 command=lambda i=item_id: update_cart_quantity_internal(i, -1))
            minus_btn.pack(side="left", padx=5)
            tk.Label(control_frame, text=f"{item_data['quantity']}", font=row_font, bg="#fff0f5", fg="#552c1f", width=3).pack(side="left", padx=5) 
            plus_btn = tk.Button(control_frame, text="+", font=("Arial", 22, "bold"), bg="#bfffcb", fg="#552c1f", bd=0, relief="solid", width=3, 
                                command=lambda i=item_id: update_cart_quantity_internal(i, 1))
            plus_btn.pack(side="left", padx=5)
            control_frame.grid(row=0, column=2, padx=10, pady=8, sticky="") 
            
            tk.Label(row_frame, text=f"{item_total:,.2f} บาท", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=8) 
            row_frame.pack(fill="x")
            
        redeem_frame = tk.Frame(list_scrollable_frame, bg="#fff8fa", bd=1, relief="solid")
        redeem_frame.pack(fill="x", pady=20, padx=15) 
        redeem_frame.grid_columnconfigure(0, weight=2)
        redeem_frame.grid_columnconfigure(1, weight=1)
        redeem_frame.grid_columnconfigure(2, weight=1)
        redeem_frame.grid_columnconfigure(3, weight=3)
        
        user_data = get_user_data(CURRENT_USER)
        current_score = user_data.get('score', 0)
        tk.Label(redeem_frame, text=f"คุณมี {current_score} คะแนน", font=("Arial", 18, "bold"), bg="#fff8fa", fg="#552c1f").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        points_entry = tk.Entry(redeem_frame, textvariable=points_to_use_var, font=("Arial", 18), width=10, justify="center") 
        points_entry.grid(row=0, column=1, padx=10, pady=10) 
        redeem_btn = tk.Button(redeem_frame, text="ใช้คะแนน", font=("Arial", 16, "bold"), bg="#fff0b1", fg="#552c1f", 
                              command=lambda: apply_points(total_price, current_score))
        redeem_btn.grid(row=0, column=2, padx=10, pady=10) 
        tk.Label(redeem_frame, text="(ทุก 10 คะแนน = 25 บ.)", font=("Arial", 14), bg="#fff8fa", fg="#552c1f").grid(row=0, column=3, padx=5, pady=10, sticky="e") 
        total_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
        total_frame.pack(fill="x", side="bottom", pady=25) 
        total_font = ("Arial", 25, "bold") 
        if total_price > 0:
            discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)
            final_total = total_price - discount_amount
            tk.Label(total_frame, text=f"รวม {total_price:,.2f} บาท", font=total_font, bg="#fff0f5", fg="#552c1f", anchor="e").pack(fill="x", padx=30)
            if discount_amount > 0:
                tk.Label(total_frame, text=f"ส่วนลดคะแนน -{discount_amount:,.2f} บาท", font=("Arial", 20, "bold"), bg="#fff0f5", fg="green", anchor="e").pack(fill="x", padx=30) 
                tk.Label(total_frame, text=f"ยอดสุทธิ {final_total:,.2f} บาท", font=total_font, bg="#fff0f5", fg="#552c1f", anchor="e").pack(fill="x", padx=30)
                
        list_scrollable_frame.update_idletasks()
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    back_btn = tk.Button(cart_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), 
                          bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                          command=go_back_to_menu)
    back_btn.place(relx=0.42, rely=0.88, anchor="e", width=250, height=80) 

    submit_btn = tk.Button(cart_window, text="ส่งคำสั่งซื้อ", font=("UID SALMON 2019", 50, "bold"), 
                            bg="#bfffcb", fg="#552c1f", bd=1 , relief="solid",
                            command=lambda: checkout_summary_page(prev_window, cart_window, table_num))

    submit_btn.place(relx=0.58, rely=0.88, anchor="w", width=250, height=80) 
    add_small_profile_button(cart_window)
    add_table_display(cart_window, table_num)
    add_about_button(cart_window)
    refresh_cart_display()

def checkout_summary_page(menu_window, cart_window, table_num):
    """(ฟังก์ชันใหม่) แสดงหน้าสรุปยอด (รูป 165551.png)"""
    
    if cart_window:
        cart_window.withdraw() 

    global bg_image_checkout_page, CURRENT_ORDER, CURRENT_REDEMPTION
    
    checkout_window = tk.Toplevel(root)
    checkout_window.title(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {table_num} - สรุปยอด")
    checkout_window.geometry("1280x720") # <<< แก้ไขขนาดจอ
    checkout_window.resizable(True, True)

    def go_back_to_cart():
        """ย้อนกลับไปหน้าตะกร้า"""
        checkout_window.destroy()
        if cart_window:
            cart_window.deiconify()

    checkout_window.protocol("WM_DELETE_WINDOW", go_back_to_cart)


    try:
        bg_image_pil = Image.open(PIC_CHECKOUT_PAGE) 
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_checkout_page = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(checkout_window, image=bg_image_checkout_page)
        background_label.image = bg_image_checkout_page
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CHECKOUT_PAGE}")
        checkout_window.config(bg="#ffd7e8")
    
    list_frame_bg = tk.Frame(checkout_window, bg="#fff0f5", bd=2, relief="solid")
    list_frame_bg.place(relx=0.5, rely=0.48, anchor="center", width=1040, height=400) 
    list_canvas = tk.Canvas(list_frame_bg, bg="#fff0f5", bd=0, highlightthickness=0)
    list_scrollbar = ttk.Scrollbar(list_frame_bg, orient="vertical", command=list_canvas.yview)
    list_scrollable_frame = tk.Frame(list_canvas, bg="#fff0f5")

    list_scrollable_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    def _on_mousewheel_checkout(event):
        if platform.system() == 'Windows':
            delta = int(-1*(event.delta/120))
        elif event.num == 4:  
            delta = -1
        elif event.num == 5: 
            delta = 1
        else:
            delta = event.delta
        list_canvas.yview_scroll(delta, "units")

    list_canvas.bind_all("<MouseWheel>", _on_mousewheel_checkout)

    list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw", width=1010) 
    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    list_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    list_scrollbar.pack(side="right", fill="y")

    row_font = ("Arial", 18) 
    total_price = 0
    
    header_frame = tk.Frame(list_scrollable_frame, bg="#ffc1e0")
    header_frame.grid_columnconfigure(0, weight=3, minsize=400) 
    header_frame.grid_columnconfigure(1, weight=1, minsize=150)
    header_frame.grid_columnconfigure(2, weight=1, minsize=200)
    header_frame.grid_columnconfigure(3, weight=2, minsize=250)
    header_font = ("Arial", 18, "bold") 
    header_fg = "#552c1f"
    tk.Label(header_frame, text="เมนู", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    tk.Label(header_frame, text="ราคา/หน่วย", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=5)
    tk.Label(header_frame, text="จำนวน", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="center").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(header_frame, text="รวม", font=header_font, bg="#ffc1e0", fg=header_fg, anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=5)
    header_frame.pack(fill="x", pady=(0, 10))
    
    for item_id, item_data in CURRENT_ORDER.items():
        item_total = item_data['price'] * item_data['quantity']
        total_price += item_total
        
        row_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
        row_frame.grid_columnconfigure(0, weight=3, minsize=400)
        row_frame.grid_columnconfigure(1, weight=1, minsize=150)
        row_frame.grid_columnconfigure(2, weight=1, minsize=200)
        row_frame.grid_columnconfigure(3, weight=2, minsize=250)
        
        # คอลัมน์ 1: ชื่อ
        tk.Label(row_frame, text=item_data['name'], font=row_font, bg="#fff0f5", fg="#552c1f", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5) 
        # คอลัมน์ 2: ราคา
        tk.Label(row_frame, text=f"{item_data['price']:,.2f} บ.", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=5) 
        # คอลัมน์ 3: จำนวน
        tk.Label(row_frame, text=f"x {item_data['quantity']}", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="center").grid(row=0, column=2, padx=10, pady=5) 
        # คอลัมน์ 4: ราคารวม
        tk.Label(row_frame, text=f"{item_total:,.2f} บาท", font=row_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=3, sticky="e", padx=20, pady=5) 
        
        row_frame.pack(fill="x", pady=2)
        
        ttk.Separator(list_scrollable_frame, orient='horizontal').pack(fill='x', padx=10)

    # --- สรุปยอดรวม (ดึงจาก Global) ---
    summary_frame = tk.Frame(list_scrollable_frame, bg="#fff0f5")
    summary_frame.pack(fill="x", side="bottom", pady=20, padx=30) 
    
    # คำนวณ VAT (แบบรวมในราคา)
    discount_amount = CURRENT_REDEMPTION.get('discount_amount', 0)
    grand_total = total_price - discount_amount
    total_before_vat = grand_total / (1 + VAT_RATE)
    vat_amount = grand_total - total_before_vat
    summary_font = ("Arial", 25, "bold") 
    summary_font_small = ("Arial", 20, "bold") 
    detail_font = ("Arial", 16) 

    #  รวมเป็นเงิน (ก่อนส่วนลด)
    tk.Label(summary_frame, text="รวมเป็นเงิน", font=summary_font_small, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    tk.Label(summary_frame, text=f"{total_price:,.2f} บาท", font=summary_font_small, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=3)

    #  ส่วนลด
    tk.Label(summary_frame, text="ส่วนลด", font=summary_font_small, bg="#fff0f5", fg="green", anchor="e").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    tk.Label(summary_frame, text=f"-{discount_amount:,.2f} บาท", font=summary_font_small, bg="#fff0f5", fg="green", anchor="e").grid(row=1, column=1, sticky="e", padx=5, pady=3)
    
    #  ยอดก่อน VAT (ตัวเล็ก)
    tk.Label(summary_frame, text="มูลค่าสินค้า (ก่อนภาษี)", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    tk.Label(summary_frame, text=f"{total_before_vat:,.2f} บาท", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=2, column=1, sticky="e", padx=5, pady=3)

    #  VAT (ตัวเล็ก)
    tk.Label(summary_frame, text=f"ภาษีมูลค่าเพิ่ม ({int(VAT_RATE*100)}%)", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=3, column=0, sticky="e", padx=5, pady=3)
    tk.Label(summary_frame, text=f"{vat_amount:,.2f} บาท", font=detail_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=3, column=1, sticky="e", padx=5, pady=3)
    
    ttk.Separator(summary_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=8)

      # ยอดสุทธิ 
    tk.Label(summary_frame, text="รวมทั้งสิ้น", font=summary_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=5, column=0, sticky="e", padx=5)
    tk.Label(summary_frame, text=f"{grand_total:,.2f} บาท", font=summary_font, bg="#fff0f5", fg="#552c1f", anchor="e").grid(row=5, column=1, sticky="e", padx=5)

    summary_frame.grid_columnconfigure(0, weight=1) 
    back_btn = tk.Button(checkout_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                          bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                          command=go_back_to_cart)
    back_btn.place(relx=0.42, rely=0.88, anchor="e", width=250, height=80) 

    submit_btn = tk.Button(checkout_window, text="ชำระเงิน", font=("UID SALMON 2019", 50, "bold"),
                            bg="#bfffcb", fg="#552c1f", bd=1 , relief="solid",
                            command=lambda: submit_order(menu_window, cart_window, checkout_window, table_num))
    submit_btn.place(relx=0.58, rely=0.88, anchor="w", width=250, height=80) 

    add_small_profile_button(checkout_window)
    add_table_display(checkout_window, table_num)
    add_about_button(checkout_window)

def customer_menu_page(selected_table):
    """ฟังก์ชันสำหรับหน้าเมนูอาหารของลูกค้า"""
    menu_window = create_toplevel_window(f"หนูดีส้มตำฟรุ้งฟริ้ง - โต๊ะ {selected_table} - เมนู")
    menu_window.protocol("WM_DELETE_WINDOW", lambda: table_selection_page(menu_window))

    global bg_image_customer_menu
    try:
        image_path_to_load = PIC_CUSTOMER_MENU 
        bg_image_manage_pil = Image.open(image_path_to_load)
        bg_image_manage_pil = bg_image_manage_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_customer_menu = ImageTk.PhotoImage(bg_image_manage_pil)
        background_label = tk.Label(menu_window, image=bg_image_customer_menu)
        background_label.image = bg_image_customer_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_CUSTOMER_MENU}")
        menu_window.config(bg="#ffd7e8") 
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
    cart_button.place(x=1160, y=20, width=80, height=60) 

    add_table_display(menu_window, selected_table)
    
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
            elif platform.system() == 'Windows': delta = int(-1*(event.delta/120)) 
            else: delta = event.delta
            
            canvas.yview_scroll(delta, "units")
        except Exception as e:
            pass

    menu_window.bind("<MouseWheel>", _on_mousewheel_menu)
    menu_window.bind("<Button-4>", _on_mousewheel_menu)
    menu_window.bind("<Button-5>", _on_mousewheel_menu)

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1160) 
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(x=50, y=195, width=1180, height=400) 
    scrollbar.place(x=1230, y=195, height=400) 

    def display_customer_menu_items(category):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        MENU_ITEM_PIC_REFS.clear()

        filtered_items = get_menu_items_from_db(category) 

        row_num = 0
        col_num = 0
        card_width = 380 
        col_count = 3 

        if not filtered_items:
            tk.Label(scrollable_frame, text="ไม่มีรายการเมนูในหมวดหมู่นี้",
                          font=("Arial", 25), bg="#fff0f5").grid(row=0, column=0, columnspan=col_count, pady=40) 

        for item in filtered_items:
            outer_card = tk.Frame(scrollable_frame, bg="#fff0f5", padx=8, pady=8) 
            card = tk.Frame(outer_card, bg="white", bd=1, relief="solid", padx=8, pady=8) 

            img_size = 150 
            img_label = tk.Label(card, bg='#d3d3d3', width=img_size//10, height=img_size//20) 
            try:
                img_placeholder_path = os.path.join(PIC_PATH, PIC_MENU_PLACEHOLDER)
                img_path = item['image_path'] or img_placeholder_path
                if not os.path.exists(img_path): img_path = None
                if img_path:
                    img = load_and_resize_pic(img_path, img_size, is_menu_item=True)
                    img_label.config(image=img, width=img_size, height=img_size, bg='white')
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
                status_fg = "#006b2c"
            else:
                status_text = "สินค้าหมด"
                status_bg = "#cccccc"
                status_fg = "#666666"
            status_label = tk.Label(status_frame, text=status_text, 
                font=("Arial", 12, "bold"), bg=status_bg, fg=status_fg, 
                padx=8, pady=4 
            )
            status_label.pack(side="left")
            if item.get('is_recommended', 0) == 1:
                rec_label = tk.Label(status_frame, text="⭐ แนะนำ",
                    font=("Arial", 12, "bold"), bg="#fff0b1", fg="#552c1f", 
                    padx=8, pady=4 
                )
                rec_label.pack(side="left", padx=8) 
            status_frame.pack(fill="x", padx=0, pady=(0, 5)) 

            tk.Label(card, text=item['name'], font=("Arial", 20, "bold"), bg="white", anchor="w").pack(fill="x") 
            tk.Label(card, text=item.get('description', ''), font=("Arial", 14), bg="white", anchor="nw", wraplength=card_width-40, justify="left", height=2).pack(fill="x") 
            tk.Label(card, text=f"ราคา {item['price']:,.2f} บาท", font=("Arial", 18, "bold"), bg="white", anchor="w").pack(fill="x", pady=(0, 5)) 

            add_btn_frame = tk.Frame(card, bg="white")
            add_btn = tk.Button(add_btn_frame, font=("Arial", 16, "bold"), width=15) 
            
            if item.get('is_available', 1) == 1: 
                add_btn.config(
                    text="เพิ่ม",
                    bg="#a0e0b0",
                    fg="#552c1f",
                    state="normal",
                    command=lambda i=item: add_item_to_order(i, selected_table)
                )
            else: 
                add_btn.config(
                    text="สินค้าหมด",
                    bg="#cccccc", 
                    fg="#552c1f",
                    state="disabled"
                )
            
            add_btn.pack(pady=10) 
            add_btn_frame.pack(fill="x")

            card.pack(fill="both", expand=True)
            outer_card.grid(row=row_num, column=col_num, padx=15, pady=15, sticky="nsew")

            col_num += 1
            if col_num >= col_count:
                col_num = 0
                row_num += 1

        for i in range(col_count):
            scrollable_frame.grid_columnconfigure(i, weight=1, minsize=card_width + 15) 

        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)
    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    category_buttons = {}
    tab_frame = tk.Frame(menu_window, bg="#fff0f5", bd=0)
    tab_frame.place(x=50, y=125, height=65, width=1150) 
    current_category = tk.StringVar(value=categories[0]) 

    def select_category(category):
        current_category.set(category)
        display_customer_menu_items(category) 
        for cat, btn in category_buttons.items():
            if cat == category:
                btn.config(bg="#ffc1e0", relief="sunken")
            else:
                btn.config(bg="#ffe0f1", relief="raised") 

    for i, cat in enumerate(categories):
        btn = tk.Button(tab_frame, text=cat, font=("Arial", 25, "bold"), 
                         bg="#ffe0f1", fg="#552c1f", relief="raised", bd=1,
                         activebackground="#ffc1e0",
                         command=lambda c=cat: select_category(c))
        btn.pack(side="left", fill="both", expand=True, padx=5, pady=5) 
        category_buttons[cat] = btn

    def confirm_back_and_clear_cart():
        global CURRENT_ORDER, CURRENT_REDEMPTION 
        if CURRENT_ORDER: 
            if messagebox.askyesno("ยืนยัน", "หากย้อนกลับ รายการในตะกร้าจะถูกล้างทั้งหมด\nคุณต้องการย้อนกลับใช่หรือไม่?"):
               CURRENT_ORDER.clear() 
               CURRENT_REDEMPTION.clear() 
               table_selection_page(menu_window)
        else:
                table_selection_page(menu_window) 

    back_button = tk.Button(menu_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=2 , relief="solid",
                             command=confirm_back_and_clear_cart) 
    back_button.place(x=50, y=620, width=200, height=80)
    add_small_profile_button(menu_window)
    add_about_button(menu_window)
    add_table_display(menu_window, selected_table)
    select_category(categories[0])

def forgot_password_page(prev_window):
    if prev_window:
        prev_window.destroy()
        
    forgot_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - รหัสผ่านใหม่")
    
    global bg_image_forgot
    try:
        bg_image_forgot_pil = Image.open(PIC_FORGOT_PASSWORD)
        bg_image_forgot_pil = bg_image_forgot_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_forgot = ImageTk.PhotoImage(bg_image_forgot_pil)
        background_label_forgot = tk.Label(forgot_window, image=bg_image_forgot)
        background_label_forgot.image = bg_image_forgot
        background_label_forgot.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        forgot_window.destroy()
        root.deiconify()
        return
        
    contact_var = tk.StringVar()
    new_pass_var = tk.StringVar()
    confirm_pass_var = tk.StringVar()
    verified_contact = tk.StringVar(value="") # ตัวแปรเก็บค่าเบอร์/อีเมลที่ผ่านการตรวจสอบแล้ว
    
    entry_font = ("Arial", 25) 
    
    contact_entry = tk.Entry(forgot_window, textvariable=contact_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat")
    contact_entry.place(x=350, y=260, width=480, height=45) 
    
    new_pass_entry = tk.Entry(forgot_window, textvariable=new_pass_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat", show="*", state='disabled')
    new_pass_entry.place(x=350, y=370, width=580, height=45) 
    
    confirm_pass_entry = tk.Entry(forgot_window, textvariable=confirm_pass_var, font=entry_font, bg="#fffbf2", bd=0, relief="flat", show="*", state='disabled')
    confirm_pass_entry.place(x=350, y=470, width=580, height=45) 

    def handle_check():
        contact = contact_var.get()
        if not contact:
            messagebox.showwarning("ว่าง", "กรุณากรอกเบอร์โทรหรือ Email")
            return
            
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE email = ? OR phone = ?", (contact, contact))
            record = cursor.fetchone()
            conn.close()
            
            if record:
                messagebox.showinfo("สำเร็จ", "พบข้อมูลบัญชี! กรุณาตั้งรหัสผ่านใหม่")
                new_pass_entry.config(state='normal')
                confirm_pass_entry.config(state='normal')
                save_button.config(state='normal')
                verified_contact.set(contact) 
            else:
                messagebox.showerror("ไม่พบ", "ไม่พบข้อมูลในระบบ")
                new_pass_entry.config(state='disabled')
                confirm_pass_entry.config(state='disabled')
                save_button.config(state='disabled')
                verified_contact.set("")
        except Exception as e:
            messagebox.showerror("Database Error", f"เกิดข้อผิดพลาด: {e}")
            
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
        if len(new_pass) < 8:
            messagebox.showerror("ไม่ปลอดภัย", "รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE email = ? OR phone = ?", (new_pass, contact, contact))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("สำเร็จ", "เปลี่ยนรหัสผ่านเรียบร้อยแล้ว")
            login_page(forgot_window) 
            
        except sqlite3.Error as e:
            messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถอัปเดตรหัสผ่านได้: {e}")
            
    check_button = tk.Button(forgot_window, text="ตรวจสอบ", font=("UID SALMON 2019", 30 ), 
                             bg="#bfffcb", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#bfffcb",
                             command=handle_check)
    check_button.place(x=848, y=255, width=95 , height=45) 
    
    back_button = tk.Button(forgot_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#ffe0f1",
                             command=lambda: login_page(forgot_window))
    back_button.place(x=390, y=560, width=180, height=70) 
    
    save_button = tk.Button(forgot_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#ffe0f1",
                             command=handle_save_new_password,
                             state='disabled')
    save_button.place(x=724, y=560, width=180, height=70) 
    
    add_about_button(forgot_window)

def open_next_page(current_window):
    current_window.destroy()
    table_selection_page()

def login_page(prev_window=None):
    """ฟังก์ชันสำหรับหน้า 'เข้าสู่ระบบ' (แก้ไขแล้ว)"""

    if prev_window:
        prev_window.destroy()

    login_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - เข้าสู่ระบบ")
    login_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(login_window))

    try:
        bg_image_login_pil = Image.open(f"{PIC_PATH}{PIC_LOGIN}")
        bg_image_login_pil = bg_image_login_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_login = ImageTk.PhotoImage(bg_image_login_pil)
        background_label_login = tk.Label(login_window, image=bg_image_login)
        background_label_login.image = bg_image_login
        background_label_login.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        login_window.destroy()
        root.deiconify()
        return

    username_entry = tk.Entry(login_window, font=("Arial", 35,"bold"),bg ="#fffbf2", bd=0, relief="flat")
    username_entry.place(x=420, y=320, width=480, height=60)

    password_entry = tk.Entry(login_window, show="*", font=("Arial", 35,"bold"),bg ="#fffbf2" , bd=0, relief="flat")
    password_entry.place(x=420, y=430, width=410, height=60)

    forgot_btn = tk.Button(login_window, text="ลืมรหัส", font=("Arial", 25, "bold"),
                            bg="#daf1ff", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#daf1ff",
                            command=lambda: forgot_password_page(login_window))
    forgot_btn.place(x=850, y=432, width=110, height=50)


    back_button = tk.Button(login_window, text="ย้อนกลับ", font=("UID SALMON 2019", 60, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#E3B2C3", command=lambda: back_to_main_page(login_window))
    back_button.place(x=380, y=555, width=200, height=80) 

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

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
        
        record = cursor.fetchone()
        conn.close()

        if record:
            CURRENT_USER = user
            messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ!")
            open_next_page(login_window)
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 60, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3",
                                 command=local_verify_login)
    confirm_button.place(x=720, y=555, width=200, height=80)

    add_about_button(login_window)

def register_page(prev_window=None):
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก' (แก้ไขแล้ว)"""
    if prev_window:
        prev_window.destroy()

    register_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - สมัครสมาชิก")
    register_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(register_window))

    try:
        bg_image_register_pil = Image.open(PIC_REGISTER) 
        bg_image_register_pil = bg_image_register_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_register = ImageTk.PhotoImage(bg_image_register_pil)
        background_label_register = tk.Label(register_window, image=bg_image_register)
        background_label_register.image = bg_image_register
        background_label_register.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        register_window.destroy()
        root.deiconify()
        return

    current_pic_path = tk.StringVar(value=None)
    pic_label_ref = None
    pic_frame_ref = None


    def display_profile_pic_register(window, pic_path_var):
        nonlocal pic_label_ref, pic_frame_ref
        x_pos, y_pos, size = 80, 240, 150 
        
        pic_path = pic_path_var.get()
        if pic_frame_ref:
            pic_frame_ref.destroy()
        

        frame = tk.Frame(window, bg='white', width=size, height=size, bd=1, relief="solid")
        frame.place(x=x_pos, y=y_pos)
        pic_frame_ref = frame
        

        img_tk = load_and_resize_pic(pic_path, size)
        PROFILE_PIC_REF['register_pic'] = img_tk 
        
        pic_label = tk.Label(frame, image=img_tk, bd=0, bg="white")
        pic_label.place(x=0, y=0, relwidth=1, relheight=1)
        pic_label_ref = pic_label
        return pic_label

    def choose_profile_pic_register():
        source_path = filedialog.askopenfilename(
            title="เลือกรูปโปรไฟล์",
            filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        )
        if source_path:
            current_pic_path.set(source_path) 
            display_profile_pic_register(register_window, current_pic_path)


    display_profile_pic_register(register_window, current_pic_path) 
    
    change_pic_button = tk.Button(register_window, text="เลือกรูป", font=("Arial", 16, "bold"),
                                  bg="#ffe0f1", fg="#552c1f", bd=1, relief="solid",
                                  command=choose_profile_pic_register)
    change_pic_button.place(x=105, y=400, width=100, height=40) 

    entry_font = ("Arial", 20) 
    
    # ช่องกรอกข้อมูล
    username_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    username_entry.place(x=325, y=260, width=320, height=40)
    
    password_entry = tk.Entry(register_window, show="*", font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    password_entry.place(x=705, y=260, width=320, height=40)
    
    name_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    name_entry.place(x=325, y=340, width=320, height=40)
    
    surname_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    surname_entry.place(x=705, y=340, width=320, height=40)
    
    phone_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    phone_entry.place(x=325, y=420, width=320, height=40)
    
    birthday_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    birthday_entry.place(x=705, y=420, width=320, height=40)
    
    email_entry = tk.Entry(register_window, font=entry_font, bg="#fcecf3", bd=0, relief="flat")
    email_entry.place(x=515, y=500, width=320, height=40)
    
    back_button = tk.Button(register_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                              bg="#ffe0f1", fg="#552c1f", bd=1, relief="solid",
                              activebackground="#E3B2C3", command=lambda: back_to_main_page(register_window))
    back_button.place(x=320, y=580, width=180, height=70)

    # ฟังก์ชันบันทึกข้อมูล
    # ฟังก์ชันบันทึกข้อมูล (พร้อมเงื่อนไขตรวจสอบเข้มข้น)
    def local_save_registration_data():
        user, pwd, name, surname, phone, bday, email = username_entry.get(), password_entry.get(), name_entry.get(), surname_entry.get(), phone_entry.get(), birthday_entry.get(), email_entry.get()
        
        # 1. เช็คห้ามเว้นว่าง
        if not all([user, pwd, name, surname, phone, bday, email]):
            messagebox.showerror("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return

        # 2. เช็คเบอร์โทรศัพท์ (ตัวเลขล้วน 10 หลัก)
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("เบอร์โทรผิดพลาด", "เบอร์โทรศัพท์ต้องเป็นตัวเลข 10 หลักเท่านั้น\n(ห้ามใส่ขีด หรือตัวอักษร)")
            return

        # 3. เช็คอีเมล (ต้องมี @ และ .นามสกุล)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("อีเมลผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง\n(ตัวอย่างที่ถูก: user@example.com)")
            return

        # 4. เช็คชื่อผู้ใช้ (Username)
        # - ขั้นต่ำ 8 ตัว
        # - มีพิมพ์ใหญ่ >= 1
        # - เฉพาะ A-Z, a-z, 0-9
        if len(user) < 8:
            messagebox.showerror("ชื่อผู้ใช้ผิดพลาด", "ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            return
        if not any(c.isupper() for c in user):
            messagebox.showerror("ชื่อผู้ใช้ผิดพลาด", "ชื่อผู้ใช้ต้องมี 'ตัวพิมพ์ใหญ่' อย่างน้อย 1 ตัว")
            return
        if not re.match(r"^[A-Za-z0-9]+$", user):
            messagebox.showerror("ชื่อผู้ใช้ผิดพลาด", "ชื่อผู้ใช้ต้องประกอบด้วยตัวอักษรภาษาอังกฤษ (A-Z, a-z) และตัวเลข (0-9) เท่านั้น\n(ห้ามใช้อักขระพิเศษหรือภาษาไทย)")
            return

        # 5. เช็ครหัสผ่าน (Password)
        # - ขั้นต่ำ 8 ตัว
        # - พิมพ์เล็ก >= 1, พิมพ์ใหญ่ >= 1, ตัวเลข >= 1, อักขระพิเศษ >= 1
        if len(pwd) < 8:
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            return
        if not any(c.islower() for c in pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมี 'ตัวพิมพ์เล็ก' อย่างน้อย 1 ตัว")
            return
        if not any(c.isupper() for c in pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมี 'ตัวพิมพ์ใหญ่' อย่างน้อย 1 ตัว")
            return
        if not any(c.isdigit() for c in pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมี 'ตัวเลข' อย่างน้อย 1 ตัว")
            return
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            messagebox.showerror("รหัสผ่านไม่ปลอดภัย", "รหัสผ่านต้องมี 'อักขระพิเศษ' อย่างน้อย 1 ตัว\n(เช่น ! @ # $ % & *)")
            return
            
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            source_path = current_pic_path.get()
            final_pic_path = None

            if source_path: 
                try:
                    _, extension = os.path.splitext(source_path)
                    new_filename = f"{user}{extension}" 
                    dest_path = os.path.join(PROFILE_PICS_DIR, new_filename)
                    shutil.copy(source_path, dest_path)
                    final_pic_path = dest_path 
                except Exception as e:
                    messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกรูปภาพได้: {e}")
                    conn.close()
                    return 

            cursor.execute("""
                INSERT INTO users (username, password, name, surname, phone, birthday, email, score, profile_pic_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (user, pwd, name, surname, phone, bday, email, final_pic_path))
            
            conn.commit()
            messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ชื่อผู้ใช้: {user}")
            back_to_main_page(register_window)
            
        except sqlite3.IntegrityError:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) นี้ถูกใช้ไปแล้ว")
        except sqlite3.Error as e:
            messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถบันทึกได้: {e}")
        finally:
            if conn: conn.close()

    confirm_button = tk.Button(register_window, text="ยืนยัน", font=("UID SALMON 2019", 40, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=1, relief="solid",
                                 activebackground="#E3B2C3",
                                 command=local_save_registration_data)
    confirm_button.place(x=700, y=580, width=180, height=70)

    add_about_button(register_window)

# ==============================================================================
# 5. PDF GENERATION (หน้าใบเสร็จ)
# ==============================================================================

FONT_TH_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\THSarabunNew.ttf" 
FONT_NAME = "THSarabunNew" 
LOGO_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\logo.png" 

def _draw_receipt_table_header(pdf, width, height, FONT_NAME):
    """(Helper) วาดหัวตารางสำหรับหน้าใหม่"""
    
    current_y = height - 2*cm 
    pdf.setFont(FONT_NAME, 12)
    margin_left = 1.5*cm
    margin_right = width - 1.5*cm
    
    pdf.line(margin_left, current_y, margin_right, current_y)
    current_y -= 0.6*cm
    

    pdf.drawString(margin_left, current_y, "รายการอาหาร (Item)")
    pdf.drawRightString(margin_right - 4*cm, current_y, "ราคา (Price)")
    pdf.drawRightString(margin_right - 2*cm, current_y, "จำนวน (Qty)")
    pdf.drawRightString(margin_right, current_y, "รวม (Total)")
    
    current_y -= 0.3*cm
    pdf.line(margin_left, current_y, margin_right, current_y)
    
    return current_y 

def get_order_details_for_receipt(order_id):
    """(Helper) ดึงข้อมูลออเดอร์และรายการสินค้าสำหรับใช้ในใบเสร็จ"""
    order_data = {}
    order_details_list = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order_data_raw = cursor.fetchone()
        if not order_data_raw:
            messagebox.showerror("ผิดพลาด", "ไม่พบข้อมูลออเดอร์ (NU{order_id})")
            return None, None
        order_data = dict(order_data_raw)

        cursor.execute("""
            SELECT od.*, mi.name 
            FROM order_details od
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE od.order_id = ?
        """, (order_id,))
        order_details_list = [dict(row) for row in cursor.fetchall()]
        
        return order_data, order_details_list
    except Exception as e:
        print(f"Error fetching receipt data: {e}")
        messagebox.showerror("DB Error", "ไม่สามารถดึงข้อมูลออเดอร์เพื่อสร้างใบเสร็จได้")
        return None, None
    finally:
        if conn: conn.close()


def generate_receipt_pdf(order_data, order_details_list, table_num):
    """
    สร้างไฟล์ PDF ใบเสร็จแบบสลิปยาว (Thermal Slip)
    """
    
    if not os.path.exists(FONT_TH_PATH):
        messagebox.showerror("Font Error", f"ไม่พบไฟล์ฟอนต์ที่: {FONT_TH_PATH}")
        return

    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_TH_PATH))
    except Exception as e:
        pass 

    try:
        order_id = order_data['order_id']
        grand_total = order_data['total_amount']
        
        total_before_vat = grand_total / (1 + VAT_RATE)
        vat_amount = grand_total - total_before_vat


        page_width = 8 * cm 
        header_height = 6.0 * cm  
        info_height = 2.5 * cm    
        item_height = 0.8 * cm    
        footer_height = 4.0 * cm  
        total_height = header_height + info_height + (len(order_details_list) * item_height) + footer_height
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(downloads_path): downloads_path = os.path.expanduser('~') 
        pdf_filename = os.path.join(downloads_path, f"Slip_NU{order_id:05d}.pdf")
        pdf = canvas.Canvas(pdf_filename, pagesize=(page_width, total_height))
        
 
        current_y = total_height - 0.5 * cm 
        center_x = page_width / 2.0
        left_x = 0.5 * cm
        right_x = page_width - 0.5 * cm

        if os.path.exists(LOGO_PATH):
            try:
               
                logo_size = 2.0 * cm
                pdf.drawImage(LOGO_PATH, center_x - (logo_size/2), current_y - logo_size, 
                              width=logo_size, height=logo_size, mask='auto')
                current_y -= (logo_size + 0.5 * cm)
            except:
                pass

        pdf.setFont(FONT_NAME, 16) 
        pdf.drawCentredString(center_x, current_y, "หนูดีส้มตำฟรุ้งฟริ้ง")
        current_y -= 0.6 * cm
        
        pdf.setFont(FONT_NAME, 10) 
        pdf.drawCentredString(center_x, current_y, "24/8 อ.เมือง จ.ขอนแก่น")
        current_y -= 0.4 * cm
        pdf.drawCentredString(center_x, current_y, "โทร. 095-664-8495")
        current_y -= 0.8 * cm
        pdf.drawCentredString(center_x, current_y, "เลขผู้เสียภาษี 1246810121433") 
        current_y -= 0.8 * cm  


        pdf.setLineWidth(0.5)
        pdf.setDash(1, 2) 
        pdf.line(left_x, current_y, right_x, current_y)
        current_y -= 0.5 * cm
        pdf.setDash([]) 

        pdf.setFont(FONT_NAME, 10)
        try:
            dt_obj = datetime.strptime(order_data['order_time'], '%Y-%m-%d %H:%M:%S')
            date_str = dt_obj.strftime(f"%d/%m/%y %H:%M")
        except:
            date_str = str(order_data['order_time'])
            
        pdf.drawString(left_x, current_y, f"โต๊ะ: {table_num}")
        pdf.drawRightString(right_x, current_y, date_str)
        current_y -= 0.5 * cm
        pdf.drawString(left_x, current_y, f"บิลเลขที่: #{order_id:05d}")
        customer_name = order_data.get('customer_username', '-')
        pdf.drawRightString(right_x, current_y, f"คุณ: {customer_name}")
        current_y -= 0.6 * cm
        pdf.line(left_x, current_y, right_x, current_y)
        current_y -= 0.5 * cm

        pdf.setFont(FONT_NAME, 10)
        
        for item in order_details_list:
            item_name = item['name']
            qty = item['quantity']
            total_price = item['price_per_item'] * qty

            if len(item_name) > 15:
                item_name = item_name[:13] + ".."
            pdf.drawString(left_x, current_y, item_name)
            pdf.drawRightString(right_x - 2.0 * cm, current_y, f"{qty} x {item['price_per_item']:.0f}")
            pdf.drawRightString(right_x, current_y, f"{total_price:,.2f}")
            
            current_y -= item_height 

        current_y -= 0.2 * cm
        pdf.line(left_x, current_y, right_x, current_y)
        current_y -= 0.6 * cm

        pdf.setFont(FONT_NAME, 10)
        
        pdf.drawString(left_x, current_y, "ยอดรวม:")
        pdf.drawRightString(right_x, current_y, f"{grand_total:,.2f}")
        current_y -= 0.5 * cm
        
        discount = order_data.get('discount_amount', 0)
        if discount > 0:
            pdf.drawString(left_x, current_y, "ส่วนลด:")
            pdf.drawRightString(right_x, current_y, f"-{discount:,.2f}")
            current_y -= 0.5 * cm

        pdf.setFont(FONT_NAME, 8)
        pdf.drawString(left_x, current_y, f"VAT 7% ({total_before_vat:,.2f}):")
        pdf.drawRightString(right_x, current_y, f"{vat_amount:,.2f}")
        current_y -= 0.8 * cm

        pdf.setFont(FONT_NAME, 14)
        pdf.drawString(left_x, current_y, "รวมทั้งสิ้น")
        pdf.drawRightString(right_x, current_y, f"{grand_total:,.2f}")
        current_y -= 0.2 * cm
        
        pdf.line(left_x, current_y, right_x, current_y)
        current_y -= 0.1 * cm
        pdf.line(left_x, current_y, right_x, current_y)
        
        current_y -= 1.0 * cm
        
        pdf.setFont(FONT_NAME, 10)
        pdf.drawCentredString(center_x, current_y, "ขอบคุณที่อุดหนุนค่ะ")
        current_y -= 0.5 * cm
        pdf.drawCentredString(center_x, current_y, "*** Thank You ***")

        pdf.save()
        
        messagebox.showinfo("สำเร็จ", f"พิมพ์ใบเสร็จเรียบร้อย!\n{pdf_filename}")
        webbrowser.open(f"file:///{pdf_filename}")

    except Exception as e:
        print(f"Error PDF: {e}")
        messagebox.showerror("PDF Error", f"สร้างใบเสร็จไม่สำเร็จ: {e}")

def admin_orders_page(prev_window):
    """
    (!! แก้ไข !!)
    หน้าสำหรับแสดงรายการ "คำสั่งซื้อ" (status='paid')
    (เพิ่มปุ่ม 'เสร็จสิ้น' และฟังก์ชัน refresh)
    """
    if prev_window:
        prev_window.destroy()

    orders_window = create_toplevel_window("Admin - คำสั่งซื้อลูกค้า")
    orders_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(orders_window))

    global bg_image_admin_orders_view
    try:
        
        bg_image_pil = Image.open(PIC_ADMIN_ORDERS_VIEW) 
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_admin_orders_view = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(orders_window, image=bg_image_admin_orders_view)
        background_label.image = bg_image_admin_orders_view
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_ORDERS_VIEW}")
        orders_window.config(bg="#fff5f5") 
        time_label = tk.Label(orders_window, text="", font=("Arial", 16, "bold"),
                              bg="#ffe0f1", fg="#552c1f", bd=1, relief="solid")

        time_label.place(x=1050, y=20, width=210, height=40)

        def update_clock():
            try:

                now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                time_label.config(text=now_str)
                time_label.after(1000, update_clock)
            except Exception as e:
                pass 

        update_clock()

    list_frame_bg = tk.Frame(orders_window, bg="white", 
                             highlightbackground="black", highlightthickness=2)
    list_frame_bg.place(x=120, y=190, width=1040, height=450)
    
    list_canvas = tk.Canvas(list_frame_bg, bg="white", bd=0, highlightthickness=0)
    list_scrollbar = ttk.Scrollbar(list_frame_bg, orient="vertical", command=list_canvas.yview)
    list_scrollable_frame = tk.Frame(list_canvas, bg="white")
    
    list_scrollable_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw", width=1010)
    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    list_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    list_scrollbar.pack(side="right", fill="y")

    def refresh_orders_list():
        for widget in list_scrollable_frame.winfo_children():
            widget.destroy()

        all_paid_orders = get_all_paid_orders()
        
        if not all_paid_orders:
            tk.Label(list_scrollable_frame, text="ไม่มีคำสั่งซื้อที่รอตรวจสอบ", 
                     font=("Arial", 25, "bold"), bg="white", fg="#552c1f").pack(pady=150, padx=100)
            return 
        current_table = -1
        item_font = ("Arial", 16)
        header_font = ("Arial", 18, "bold")
        table_font = ("Arial", 22, "bold")
        
        for order in all_paid_orders:
            order_id = order['order_id']
            table_num = order['table_number']
            
            if table_num != current_table:
                current_table = table_num
                tk.Label(list_scrollable_frame, text=f"โต๊ะ {table_num}", 
                         font=table_font, bg="white", fg="#552c1f", anchor="w").pack(fill="x", padx=10, pady=(20, 5))
            
            order_header_frame = tk.Frame(list_scrollable_frame, bg="white")
            
            order_label_text = f"คำสั่งซื้อ # {order_id:05d}"
            tk.Label(order_header_frame, text=order_label_text, 
                     font=header_font, bg="white", fg="#552c1f", anchor="w").pack(side="left", padx=10)
            
            status_label = tk.Label(order_header_frame, text="ชำระเงินแล้ว", 
                                    font=("Arial", 16, "bold"), bg="#bfffcb", fg="#006b2c", bd=1, relief="solid")
            status_label.pack(side="left", padx=10)

            complete_btn = tk.Button(order_header_frame, text="เสร็จสิ้น", 
                                     font=("Arial", 16, "bold"), bg="#c4e6fa", fg="#552c1f", 
                                     bd=1, relief="solid",
                                     
                                     command=lambda oid=order_id: on_complete_click(oid))
            complete_btn.pack(side="right", padx=10)
            order_header_frame.pack(fill="x")
            order_items = get_order_details_from_db(order_id)
            
            for item in order_items:
                item_total = item['price_per_item'] * item['quantity']
                
                row_frame = tk.Frame(list_scrollable_frame, bg="white")
                
                tk.Label(row_frame, text=item['name'], font=item_font, bg="white", fg="black", anchor="w").grid(row=0, column=0, sticky="w", padx=(40, 0))
                tk.Label(row_frame, text=f"{item['price_per_item']:,.2f} บ.", font=item_font, bg="white", fg="black", anchor="e").grid(row=0, column=1, sticky="e", padx=10)
                tk.Label(row_frame, text=f"x {item['quantity']}", font=item_font, bg="white", fg="black", anchor="e").grid(row=0, column=2, sticky="e", padx=10)
                tk.Label(row_frame, text=f"{item_total:,.2f} บาท", font=item_font, bg="white", fg="black", anchor="e").grid(row=0, column=3, sticky="e", padx=20)
                
                row_frame.grid_columnconfigure(0, weight=4) 
                row_frame.grid_columnconfigure(1, weight=2)
                row_frame.grid_columnconfigure(2, weight=1)
                row_frame.grid_columnconfigure(3, weight=2)
                row_frame.pack(fill="x")

            ttk.Separator(list_scrollable_frame, orient='horizontal').pack(fill='x', pady=10, padx=10)

    def on_complete_click(order_id_to_complete):

        if messagebox.askyesno("ยืนยัน", f"ทำรายการ #{order_id_to_complete:05d} เสร็จแล้วใช่หรือไม่?\n(รายการจะหายไปจากหน้านี้ แต่โต๊ะจะยังไม่ว่าง)"):
            

            if db_mark_order_as_served(order_id_to_complete):
                messagebox.showinfo("สำเร็จ", "บันทึกสถานะ 'ปิดออเดอร์' เรียบร้อย")
                refresh_orders_list() 
            else:
                messagebox.showerror("ผิดพลาด", "ไม่สามารถบันทึกสถานะได้")

    refresh_orders_list()


    back_button = tk.Button(orders_window, text="ย้อนกลับ", font=("UID SALMON 2019", 30, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                            command=lambda: admin_panel_page(orders_window))
    back_button.place(x=60, y=650, width=200, height=60)

    add_about_button(orders_window)

def admin_sales_page(prev_window):
    """(ฟังก์ชันใหม่) แสดงหน้าสรุปยอดขาย (Sales Report)"""
    if prev_window:
        prev_window.destroy()

    sales_window = create_toplevel_window("Admin - ยอดขาย")
    sales_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(sales_window))

    global bg_image_admin_sales
    try:
        bg_image_pil = Image.open(PIC_ADMIN_SALES)
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_admin_sales = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(sales_window, image=bg_image_admin_sales)
        background_label.image = bg_image_admin_sales
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_SALES}")
        sales_window.config(bg="#fff5f5") 
    day_var = tk.StringVar(value="ทั้งหมด")
    month_var = tk.StringVar(value="ทั้งหมด")
    year_var = tk.StringVar(value="ทั้งหมด")
    mode_var = tk.StringVar(value="รายวัน") 
    category_var = tk.StringVar(value="ส้มตำ") 
    filter_frame = tk.Frame(sales_window, bg="#ffa5c8", bd=0) 
    filter_frame.place(x=50, y=140, width=1180, height=60)

    days = ["ทั้งหมด"] + [str(d) for d in range(1, 32)]
    months = ["ทั้งหมด"] + [str(m) for m in range(1, 13)]
    current_year = datetime.now().year
    years = ["ทั้งหมด"] + [str(y) for y in range(current_year, current_year - 5, -1)]
    
    combo_font = ("Arial", 16)
    
    day_label = tk.Label(filter_frame, text="วัน", font=combo_font, bg="#ffffff")
    day_label.pack(side="left", padx=(10,0))
    day_combo = ttk.Combobox(filter_frame, textvariable=day_var, values=days, font=combo_font, state="readonly", width=4)
    day_combo.pack(side="left", padx=(5,15))

    month_label = tk.Label(filter_frame, text="เดือน", font=combo_font, bg="#ffffff")
    month_label.pack(side="left", padx=(10,0))
    month_combo = ttk.Combobox(filter_frame, textvariable=month_var, values=months, font=combo_font, state="readonly", width=4)
    month_combo.pack(side="left", padx=(5,15))

    year_label = tk.Label(filter_frame, text="ปี", font=combo_font, bg="#ffffff")
    year_label.pack(side="left", padx=(10,0))
    year_combo = ttk.Combobox(filter_frame, textvariable=year_var, values=years, font=combo_font, state="readonly", width=6)
    year_combo.pack(side="left", padx=(5,15))


    modes = ['รายวัน', 'รายเดือน', 'รายปี']
    mode_label = tk.Label(filter_frame, text="เลือกโหมด", font=combo_font, bg="#fff0b1") 
    mode_label.pack(side="left", padx=(30,0))
    mode_combo = ttk.Combobox(filter_frame, textvariable=mode_var, values=modes, font=combo_font, state="readonly", width=8)
    mode_combo.pack(side="left", padx=5)
    categories = ['ทั้งหมด', 'ส้มตำ', 'ย่าง/ทอด', 'ต้ม/ลาบ', 'เครื่องดื่ม', 'อื่นๆ']
    category_label = tk.Label(filter_frame, text="หมวดหมู่", font=combo_font, bg="#c4e6fa") 
    category_label.pack(side="left", padx=(30,0))
    category_combo = ttk.Combobox(filter_frame, textvariable=category_var, values=categories, font=combo_font, state="readonly", width=10)
    category_combo.pack(side="left", padx=5)

    tree_frame = tk.Frame(sales_window, bg="white")
    tree_frame.place(x=50, y=200, width=1180, height=355)

    tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
    tree = ttk.Treeview(tree_frame, columns=("item", "quantity", "revenue"), show="headings", yscrollcommand=tree_scroll_y.set)
    tree_scroll_y.config(command=tree.yview)

    tree.heading("item", text="รายการ")
    tree.heading("quantity", text="จำนวนขาย")
    tree.heading("revenue", text="รายได้รวม")

    tree.column("item", width=700, anchor="w") 
    tree.column("quantity", width=220, anchor="center") 
    tree.column("revenue", width=220, anchor="e") 

    tree_scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"), background="#ffc1e0", foreground="#552c1f")
    style.configure("Treeview", font=("Arial", 18), rowheight=35) 
    style.map("Treeview", background=[('selected', '#ffe0f1')], foreground=[('selected', 'black')])
    summary_frame = tk.Frame(sales_window, bg="#ffa5c8")
    summary_frame.place(x=50, y=555, width=1180, height=50)

    total_qty_label = tk.Label(summary_frame, text="จำนวนรวม:", font=("Arial", 18, "bold"), bg="#fff0f5", fg="#552c1f")
    total_qty_label.pack(side="left", padx=20)
    total_qty_value = tk.Label(summary_frame, text="0", font=("Arial", 18, "bold"), bg="#fff0f5", fg="#552c1f")
    total_qty_value.pack(side="left", padx=5)
    
    total_rev_label = tk.Label(summary_frame, text="รายได้รวม:", font=("Arial", 18, "bold"), bg="#fff0f5", fg="#552c1f")
    total_rev_label.pack(side="left", padx=(100, 5))
    total_rev_value = tk.Label(summary_frame, text="0.00 บาท", font=("Arial", 18, "bold"), bg="#fff0f5", fg="#552c1f")
    total_rev_value.pack(side="left", padx=5)

    # --- 5. ฟังก์ชันสำหรับ Logic ---
    
    def update_filter_state(*args):
        """(Logic) เปิด/ปิด ฟิลเตอร์วัน/เดือน ตามโหมด"""
        mode = mode_var.get()
        if mode == "รายวัน":
            day_combo.config(state="readonly")
            month_combo.config(state="readonly")
            year_combo.config(state="readonly")
        elif mode == "รายเดือน":
            day_combo.config(state="disabled")
            day_var.set("ทั้งหมด")
            month_combo.config(state="readonly")
            year_combo.config(state="readonly")
        elif mode == "รายปี":
            day_combo.config(state="disabled")
            month_combo.config(state="disabled")
            day_var.set("ทั้งหมด") 
            month_var.set("ทั้งหมด") 
            year_combo.config(state="readonly")
            

    mode_var.trace_add("write", update_filter_state)
    
    def fetch_sales_data():
        """(Logic) ดึงข้อมูลจาก DB ตามฟิลเตอร์"""
        
        tree.delete(*tree.get_children())
        total_qty_value.config(text="0")
        total_rev_value.config(text="0.00 บาท")
        
        base_query = """
            SELECT 
                mi.name, 
                SUM(od.quantity) as TotalQuantity, 
                SUM(od.quantity * od.price_per_item) as TotalRevenue
            FROM order_details od
            JOIN orders o ON od.order_id = o.order_id
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE o.status = 'completed' 
        """
        params = []
        
        mode = mode_var.get()
        day = day_var.get()
        month = month_var.get()
        year = year_var.get()
        category = category_var.get()
        
        if category != "ทั้งหมด":
            base_query += " AND mi.category = ?"
            params.append(category)

        if year != "ทั้งหมด":
            base_query += " AND strftime('%Y', o.order_time) = ?"
            params.append(year)
        
        if (mode == "รายวัน" or mode == "รายเดือน") and month != "ทั้งหมด":
            base_query += " AND strftime('%m', o.order_time) = ?"
            params.append(month.zfill(2)) 
            
        if mode == "รายวัน" and day != "ทั้งหมด":
            base_query += " AND strftime('%d', o.order_time) = ?"
            params.append(day.zfill(2))

        base_query += " GROUP BY mi.name ORDER BY TotalRevenue DESC"
        
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(base_query, params)
            rows = cursor.fetchall()
            conn.close()
            
            total_qty = 0
            total_rev = 0
            
            if not rows:
                messagebox.showinfo("ไม่พบข้อมูล", "ไม่พบยอดขายตามเงื่อนไขที่เลือก")
                return

            for row in rows:
                tree.insert("", "end", values=(
                    row["name"], 
                    row["TotalQuantity"],
                    f"{row['TotalRevenue']:,.2f}"
                ))
                total_qty += row["TotalQuantity"]
                total_rev += row["TotalRevenue"]
            
            total_qty_value.config(text=f"{total_qty}")
            total_rev_value.config(text=f"{total_rev:,.2f} บาท")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"ไม่สามารถดึงข้อมูลยอดขายได้: {e}")

    show_button = tk.Button(filter_frame, text="แสดงผล", font=("Arial", 16, "bold"),
                            bg="#ffc1e0", fg="#552c1f", bd=1, relief="solid",
                            command=fetch_sales_data) 
    show_button.pack(side="right", padx=10, ipady=5) 

    back_button = tk.Button(sales_window, text="ย้อนกลับ", font=("UID SALMON 2019", 45, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                            command=lambda: admin_panel_page(sales_window))
    back_button.place(x=60, y=640, width=200, height=70) 
    update_filter_state() 
    add_about_button(sales_window)

def admin_panel_page(prev_window):
    """ฟังก์ชันสำหรับหน้า 'แอดมิน' (เวอร์ชันใหม่ 2x2)"""
    if prev_window:
        prev_window.destroy()

    admin_window = create_toplevel_window("Admin Panel")
    admin_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(admin_window))

    global bg_image_admin_panel 
    try:
        bg_image_admin_pil = Image.open(PIC_ADMIN_PANEL) 
        
        bg_image_admin_pil = bg_image_admin_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        
        bg_image_admin_panel = ImageTk.PhotoImage(bg_image_admin_pil)
        background_label_admin = tk.Label(admin_window, image=bg_image_admin_panel)
        background_label_admin.image = bg_image_admin_panel
        
        background_label_admin.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}\n{PIC_ADMIN_PANEL}") 
        admin_window.destroy()
        root.deiconify()
        return

    btn_font = ("UID SALMON 2019", 70, "bold") 
    btn_bg = "#ffffff"
    btn_fg = "#552c1f"
    btn_relief = "groove"
    btn_bd = 0
    
    btn_width = 350 # 
    btn_height = 100 

    # 1. ยอดขาย 
    sales_button = tk.Button(admin_window, text="ยอดขาย", font=btn_font,
                             bg=btn_bg, fg=btn_fg, bd=btn_bd, relief=btn_relief,
                             command=lambda: admin_sales_page(admin_window)) # <<< (!! แก้ไขตรงนี้ !!)
    sales_button.place(relx=0.32, rely=0.40, anchor="center", width=btn_width, height=btn_height)

    # 2. คำสั่งซื้อ 
    orders_button = tk.Button(admin_window, text="คำสั่งซื้อ", font=btn_font,
                              bg=btn_bg, fg=btn_fg, bd=btn_bd, relief=btn_relief,
                              command=lambda: admin_orders_page(admin_window)) 
    orders_button.place(relx=0.70, rely=0.40, anchor="center", width=btn_width, height=btn_height) 

    # 3. โต๊ะลูกค้า 
    table_button = tk.Button(admin_window, text="โต๊ะลูกค้า", font=btn_font,
                              bg=btn_bg, fg=btn_fg, bd=btn_bd, relief=btn_relief,
                              command=lambda: admin_table_view_page(admin_window)) 
    table_button.place(relx=0.32, rely=0.66, anchor="center", width=btn_width, height=btn_height) 

    # 4. เมนู 
    menu_button = tk.Button(admin_window, text="เพิ่ม/แก้ไข/ลบ เมนู", font= ("UID SALMON 2019", 50, "bold"),
                             bg=btn_bg, fg=btn_fg, bd=btn_bd, relief=btn_relief, justify=tk.CENTER,
                             command=lambda: admin_manage_menu_page(admin_window)) 

    menu_button.place(relx=0.70, rely=0.66, anchor="center", width=btn_width, height=btn_height) 



    logout_button = tk.Button(admin_window, text="ออกจากระบบ", font=("UID SALMON 2019", 45 , "bold"),
                              bg="#ff257d", fg="#552c1f", bd=0, relief="flat",
                              activebackground="#ff257d",
                              command=lambda: back_to_main_page(admin_window))

    logout_button.place(relx=0.91, rely=0.07, anchor="center", width=183, height=55) 

    add_about_button(admin_window)


# (แสดงเลขโต๊ะ) 
# ==============================================================================
# 1. ฟังก์ชันดึงข้อมูล (Database Logic)
# ==============================================================================
def get_all_paid_items_for_table(table_num):
    """
    แก้ไข: ดึงเฉพาะรายการที่ 'กำลังดำเนินการ' (Paid/Pending) 
    ตัดรายการที่ 'เสร็จสิ้นแล้ว' (Completed) ออกไป เพื่อไม่ให้เห็นข้อมูลลูกค้าเก่า
    """
    items = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT od.*, mi.name, o.order_id, o.slip_image_path, o.order_time, o.status, o.subtotal, o.discount_amount
            FROM order_details od
            JOIN orders o ON od.order_id = o.order_id
            JOIN menu_items mi ON od.item_id = mi.item_id
            WHERE o.table_number = ? AND (o.status = 'paid' OR o.status = 'pending')
            ORDER BY o.order_id DESC
        """, (table_num,))
        
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching all items: {e}")
    finally:
        if conn: conn.close()
    return items

# ==============================================================================
# 2. ฟังก์ชันหน้าจัดการโต๊ะ (UI Logic) 
# ==============================================================================
def admin_manage_order_page(prev_window, order_data):
    """
    (Layout V.7 - Border Fix & Final Position)
    - เส้นกรอบคลุมทั้งหัวข้อและเนื้อหา
    - ป้ายโต๊ะมีกรอบดำ ย้ายไปข้างแอดมิน
    - ปุ่มเขียวกลางล่าง, แถบชมพูซ้ายล่าง
    """
    if not order_data:
        messagebox.showerror("ผิดพลาด", "ไม่พบข้อมูลออเดอร์")
        return
        
    if prev_window:
        prev_window.destroy()

    table_num = order_data['table_number']
    
    manage_window = create_toplevel_window(f"Admin - จัดการโต๊ะ {table_num}")
    manage_window.protocol("WM_DELETE_WINDOW", lambda: admin_table_view_page(manage_window))

    global bg_image_admin_manage_order
    try:
        bg_image_pil = Image.open(PIC_ADMIN_MANAGE_ORDER) 
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_admin_manage_order = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(manage_window, image=bg_image_admin_manage_order)
        background_label.image = bg_image_admin_manage_order
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background Error: {e}")
        manage_window.config(bg="#fff5f5")
    table_badge = tk.Label(manage_window, 
                           text=f"โต๊ะ {table_num}", 
                           font=("UID SALMON 2019", 35, "bold"), 
                           bg="#ffe0f1", 
                           fg="#552c1f",
                           highlightbackground="black", 
                           highlightthickness=1,        
                           bd=0)                        
    
    table_badge.place(x=230, y=25, width=120, height=70)


    main_frame = tk.Frame(manage_window, bg="white", highlightbackground="#552c1f", highlightthickness=2)
    main_frame.place(x=60, y=130, width=1160, height=480) 

    canvas = tk.Canvas(main_frame, bg="white", bd=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_content = tk.Frame(canvas, bg="white")

    scrollable_content.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    def _on_mousewheel(event):
        if platform.system() == 'Windows':
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            canvas.yview_scroll(event.delta, "units")
            
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.create_window((0, 0), window=scrollable_content, anchor="nw", width=1130)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scrollbar.pack(side="right", fill="y")


    all_items = get_all_paid_items_for_table(table_num)

    orders_grouped = {}
    order_ids_ordered = [] 
    
    for item in all_items:
        oid = item['order_id']
        if oid not in orders_grouped:
            orders_grouped[oid] = {
                'items': [],
                'slip': item['slip_image_path'],
                'time': item['order_time'],
                'status': item['status'],
                'discount': item.get('discount_amount', 0)
            }
            order_ids_ordered.append(oid)
        orders_grouped[oid]['items'].append(item)


    grand_total_all_orders = 0
    
    if not orders_grouped:
        tk.Label(scrollable_content, text="ยังไม่มีรายการสั่งซื้อ", font=("Arial", 20), bg="white", fg="#aaa").pack(pady=100)

    for oid in order_ids_ordered:
        data = orders_grouped[oid]
        block_frame = tk.Frame(scrollable_content, bg="white", 
                               highlightbackground="black", highlightthickness=1)
        block_frame.pack(fill="x", pady=15, padx=10)
        try:
            time_str_db = str(data['time']) 
            
            try:
                dt_obj = datetime.strptime(time_str_db, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                dt_obj = datetime.strptime(time_str_db, '%Y-%m-%d %H:%M:%S')

            dt_obj = dt_obj + timedelta(hours=7)

            thai_year = dt_obj.year + 543
            time_str = dt_obj.strftime(f'%d/%m/{thai_year} %H:%M:%S')

        except Exception as e:
            print(f"Time Error for Order {oid}: {e}") 
            time_str = data['time'] 

        header_frame = tk.Frame(block_frame, bg="#ffc1e0", height=40)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                 text=f" รายการสั่งซื้อ #{oid}  (เวลา: {time_str})", 
                 font=("Arial", 16, "bold"), 
                 bg="#ffc1e0", fg="#552c1f", anchor="w").pack(fill="x", padx=10, pady=5)
        content_frame = tk.Frame(block_frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(content_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)
        
        headers = ["เมนู", "ราคา", "จำนวน", "รวม"]
        col_widths = [25, 10, 8, 10]
        aligns = ["w", "e", "c", "e"]
        
        for idx, h_text in enumerate(headers):
            tk.Label(left_panel, text=h_text, font=("Arial", 14, "bold"), bg="white", fg="#552c1f",
                     width=col_widths[idx], anchor=aligns[idx]).grid(row=0, column=idx, pady=(0, 5))
        
        tk.Frame(left_panel, bg="#ddd", height=2).grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)

        subtotal = 0
        current_row = 2
        for item in data['items']:
            total_item = item['price_per_item'] * item['quantity']
            subtotal += total_item
            
            tk.Label(left_panel, text=item['name'], font=("Arial", 14), bg="white", anchor="w").grid(row=current_row, column=0, sticky="w")
            tk.Label(left_panel, text=f"{item['price_per_item']:.0f}", font=("Arial", 14), bg="white", anchor="e").grid(row=current_row, column=1, sticky="e")
            tk.Label(left_panel, text=f"x{item['quantity']}", font=("Arial", 14), bg="white", anchor="c").grid(row=current_row, column=2)
            tk.Label(left_panel, text=f"{total_item:,.0f}", font=("Arial", 14), bg="white", anchor="e").grid(row=current_row, column=3, sticky="e")
            current_row += 1
        
        tk.Frame(left_panel, bg="#552c1f", height=1).grid(row=current_row, column=0, columnspan=4, sticky="ew", pady=10)
        current_row += 1
        
        discount = data['discount']
        final_subtotal = subtotal - discount
        grand_total_all_orders += final_subtotal
        
        total_label_text = f"ยอดรวมรอบนี้:  {final_subtotal:,.2f} บาท"
        tk.Label(left_panel, text=total_label_text, font=("Arial", 18, "bold"), bg="white", fg="#552c1f", anchor="e")\
            .grid(row=current_row, column=0, columnspan=4, sticky="e")

       
        right_panel = tk.Frame(content_frame, bg="white", width=250)
        right_panel.pack(side="right", padx=(20, 0), fill="y")
        
        slip_path = data['slip']
        if slip_path and os.path.exists(slip_path):
            try:
                pil_img = Image.open(slip_path)
                target_height = 200
                ratio = target_height / float(pil_img.size[1])
                target_width = int(float(pil_img.size[0]) * float(ratio))
                
                pil_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                
                img_lbl = tk.Label(right_panel, image=tk_img, bg="white", bd=1, relief="solid")
                img_lbl.image = tk_img
                img_lbl.pack()
                
                tk.Button(right_panel, text="🔍 ขยายรูป", font=("Arial", 10), bg="#eee",
                          command=lambda p=slip_path: webbrowser.open(p)).pack(fill="x", pady=2)
            except Exception as e:
                tk.Label(right_panel, text="รูปเสียหาย", bg="#eee", width=15, height=5).pack()
        else:
            tk.Label(right_panel, text="ไม่มีรูปสลิป", bg="#f0f0f0", fg="#888", width=20, height=8).pack()


 
    footer_frame = tk.Frame(manage_window, bg="#ffe0f1", bd=0)
    footer_frame.place(x=0, y=620, width=450, height=100) 
    
    tk.Label(footer_frame, text=f"ยอดรวมสุทธิ: {grand_total_all_orders:,.2f} บ.", 
             font=("UID SALMON 2019", 35, "bold"), bg="#ffe0f1", fg="#552c1f").place(relx=0.5, rely=0.5, anchor="center")


    def finish_all_transactions():
        if messagebox.askyesno("ยืนยัน", f"ต้องการปิดโต๊ะ {table_num} และเคลียร์ยอดเงินทั้งหมดหรือไม่?"):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE orders 
                    SET status = 'completed' 
                    WHERE table_number = ? AND (status = 'paid' OR status = 'pending'OR status = 'served')
                """, (table_num,))
                conn.commit()
                conn.close()
                messagebox.showinfo("สำเร็จ", "ปิดโต๊ะเรียบร้อย")
                admin_table_view_page(manage_window) 
            except Exception as e:
                messagebox.showerror("ผิดพลาด", f"ปิดงานไม่สำเร็จ: {e}")

    btn_finish = tk.Button(manage_window, text="เสร็จสิ้นการทำรายการ", font=("UID SALMON 2019", 35, "bold"),
                           bg="#bfffcb", fg="#552c1f", bd=1, relief="solid",
                           command=finish_all_transactions)
    btn_finish.place(relx=0.5, y=660, anchor="center", width=380, height=80)
    
 
    btn_back = tk.Button(manage_window, text="ย้อนกลับ", font=("UID SALMON 2019", 30, "bold"),
                         bg="#ffe0f1", fg="#552c1f", bd=1, relief="solid",
                         command=lambda: admin_table_view_page(manage_window))
    btn_back.place(x=980, y=630, width=180, height=70)

    add_about_button(manage_window)

def admin_table_view_page(prev_window):
    """ฟังก์ชันสำหรับหน้าแสดงโต๊ะสำหรับ Admin (พร้อมระบบ Auto-Refresh)"""
    if prev_window:
        prev_window.destroy()

    admin_table_window = create_toplevel_window("Admin - Table View")
    admin_table_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(admin_table_window))

    global bg_image_admin_table_view
    try:
        bg_image_admin_table_pil = Image.open(PIC_ADMIN_TABLE_VIEW) 
        bg_image_admin_table_pil = bg_image_admin_table_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_admin_table_view = ImageTk.PhotoImage(bg_image_admin_table_pil)
        background_label_admin_table = tk.Label(admin_table_window, image=bg_image_admin_table_view)
        background_label_admin_table.image = bg_image_admin_table_view
        background_label_admin_table.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        admin_table_window.config(bg="#fff5f5") 
    table_widgets = {} 

    def view_table_order(table_num):
        order_data = get_active_order_for_table(table_num)
        if order_data:
            admin_manage_order_page(admin_table_window, order_data)
        else:
            messagebox.showinfo("โต๊ะว่าง", f"โต๊ะ {table_num} ยังไม่มีออเดอร์")

    button_width = 200 
    button_height = 200
    y1 = 150
    y2 = 370 
    
    total_width_needed = (4 * button_width) + (3 * 45)
    start_x = 172
    x_gap = 45

    table_coords_admin = [
        (start_x, y1), (start_x + 1*(button_width + x_gap), y1), (start_x + 2*(button_width + x_gap), y1), (start_x + 3*(button_width + x_gap), y1),  
        (start_x, y2), (start_x + 1*(button_width + x_gap), y2), (start_x + 2*(button_width + x_gap), y2), (start_x + 3*(button_width + x_gap), y2)
    ]

    for i, (x, y) in enumerate(table_coords_admin):
        table_num = i + 1
        btn = tk.Button(admin_table_window, text=f"โต๊ะ {table_num}", font=("UID SALMON 2019", 90), 
                          bg="#ffe0f1", fg="#552c1f", bd=2 , relief="solid", 
                          justify=tk.CENTER,
                          command=lambda num=table_num: view_table_order(num))
        btn.place(x=x, y=y, width=button_width, height=button_height) 
        status_icon_label = tk.Label(admin_table_window, text="?", 
                                     font=("Arial", 30, "bold"), 
                                     bg="#cccccc", fg="white", 
                                     bd=2, relief="solid")
        status_icon_label.place(x=x + button_width - 45, y=y + 5, width=40, height=40)

        table_widgets[table_num] = {
            'btn': btn,
            'icon': status_icon_label
        }

    def update_table_status_realtime():
        try:
            occupied_tables = get_all_table_statuses()
            
            for t_num, widgets in table_widgets.items():
                btn = widgets['btn']
                icon = widgets['icon']
                
                if t_num in occupied_tables:
                    btn.config(bg="#ffb3d1") 
                    icon.config(text="!", bg="#ff4d4d", fg="white") 
                else:
                    btn.config(bg="#ffe0f1") 
                    icon.config(text="✓", bg="#bfffcb", fg="#006b2c") 
            
           
            admin_table_window.after(2000, update_table_status_realtime)
            
        except Exception as e:
            print(f"Error updating admin tables: {e}")

    
    update_table_status_realtime()
    back_button = tk.Button(admin_table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_panel_page(admin_table_window))
    back_button.place(x=60, y=640, width=220, height=70) 
    
    add_about_button(admin_table_window)
def admin_add_menu_page(prev_window, category_from_manage=None):
    """ฟังก์ชันสำหรับหน้าเพิ่มเมนู"""
    if prev_window:
        prev_window.destroy()

    add_window = create_toplevel_window("Admin - เพิ่มเมนู")
    add_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(add_window, category_from_manage))

    global bg_image_admin_add_menu
    try:
        bg_image_add_pil = Image.open(PIC_ADMIN_ADD_MENU)
        bg_image_add_pil = bg_image_add_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_admin_add_menu = ImageTk.PhotoImage(bg_image_add_pil)
        background_label = tk.Label(add_window, image=bg_image_admin_add_menu)
        background_label.image = bg_image_admin_add_menu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}")
        add_window.config(bg="#fff0f5")

    name_var = tk.StringVar()
    description_var = tk.StringVar()
    price_var = tk.StringVar()
    category_var = tk.StringVar()
    image_source_path_var = tk.StringVar()

    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    if category_from_manage and category_from_manage in categories:
        category_var.set(category_from_manage)
    else:
        category_var.set(categories[0])

    
    img_size = 200 
    img_frame = tk.Frame(add_window, bg="white", bd=1, relief="solid")
    img_frame.place(x=170, y=250, width=img_size, height=img_size)

    img_label = tk.Label(img_frame, bg="#d3d3d3", text="No Image", font=("Arial", 16))
    img_label.place(relwidth=1, relheight=1)

    def display_menu_pic(pic_path):
        global MENU_FORM_PIC_REF
        img_tk = load_and_resize_pic(pic_path, img_size-2, is_menu_item=True)
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

    entry_font = ("Arial", 25) 
    bg_color = "#ffffff"

   
    name_entry = tk.Entry(add_window, textvariable=name_var, font=entry_font, bd=2, bg=bg_color)
    name_entry.place(x=590, y=240, width=450, height=45) 
    add_right_click_menu(name_entry)

    price_entry = tk.Entry(add_window, textvariable=price_var, font=entry_font, bd=2, bg=bg_color)
    price_entry.place(x=600, y=320, width=450, height=45) 
    add_right_click_menu(price_entry) 

    
    description_entry = tk.Entry(add_window, textvariable=description_var, font=entry_font, bd=2, bg=bg_color)
    description_entry.place(x=660, y=390, width=450, height=45) 
    add_right_click_menu(description_entry) 

    category_menu = ttk.Combobox(add_window, textvariable=category_var,
                                    values=categories, state="readonly", font=entry_font)
    category_menu.place(x=670, y=470, width=450, height=45) 

    add_pic_button = tk.Button(add_window, text="เพิ่มรูป", font=("Arial", 20, "bold"),
                                  bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                                  command=choose_image)
    add_pic_button.place(x=185, y=470, width=170, height=50)

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
            admin_manage_menu_page(add_window, category)

    save_button = tk.Button(add_window, text="เสร็จสิ้น", font=("UID SALMON 2019", 50, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                             command=save_item)
    save_button.place(x=550, y=600, width=180, height=70) 
    
    back_button = tk.Button(add_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_manage_menu_page(add_window, category_var.get()))
    back_button.place(x=60, y=640, width=220, height=70) 

    add_about_button(add_window)

def admin_edit_menu_page(prev_window, item_data):
    """ฟังก์ชันสำหรับหน้าแก้ไขเมนู (แก้ไขเพิ่มคลิกขวา)"""
    if prev_window:
        prev_window.destroy()

    edit_window = create_toplevel_window("Admin - แก้ไขเมนู")
    edit_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(edit_window, item_data.get('category'))) 

    global bg_image_admin_edit_menu 
    
    try:
        bg_image_edit_pil = Image.open(PIC_ADMIN_EDIT_MENU)
        bg_image_edit_pil = bg_image_edit_pil.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image_edit = ImageTk.PhotoImage(bg_image_edit_pil)
        background_label = tk.Label(edit_window, image=bg_image_edit)
        background_label.image = bg_image_edit
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_EDIT_MENU}")
        edit_window.config(bg="#fff0f5")

    item_id = item_data['item_id']
    original_image_path = item_data.get('image_path')
    
    current_recommend_status_var = tk.IntVar(value=item_data.get('is_recommended', 0))

    name_var = tk.StringVar(value=item_data.get('name', ''))
    description_var = tk.StringVar(value=item_data.get('description', ''))
    price_var = tk.StringVar(value=f"{item_data.get('price', 0.0):,.2f}")
    category_var = tk.StringVar(value=item_data.get('category', ''))
    image_path_var = tk.StringVar(value=original_image_path)

    categories = ["ส้มตำ", "ย่าง/ทอด", "ต้ม/ลาบ", "เครื่องดื่ม", "อื่นๆ"]
    if category_var.get() not in categories:
          category_var.set(categories[0])

    img_size = 200 
    img_frame = tk.Frame(edit_window, bg="white", bd=1, relief="solid")
    img_frame.place(x=170, y=250, width=img_size, height=img_size) 
    
    img_label = tk.Label(img_frame, bg="#d3d3d3", text="No Image", font=("Arial", 16)) 
    img_label.place(relwidth=1, relheight=1)

    def display_menu_pic(pic_path):
        global MENU_FORM_PIC_REF
        img_tk = load_and_resize_pic(pic_path, img_size-2, is_menu_item=True)
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

    entry_font = ("Arial", 25) 
    bg_color = "#ffffff"

    #  (1) ช่องชื่อ 
    name_entry = tk.Entry(edit_window, textvariable=name_var, font=entry_font, bd=2, bg=bg_color)
    name_entry.place(x=590, y=240, width=320, height=45) 
    add_right_click_menu(name_entry) 
    
    #  (2) ช่องราคา 
    price_entry = tk.Entry(edit_window, textvariable=price_var, font=entry_font, bd=2, bg=bg_color)
    price_entry.place(x=600, y=320, width=320, height=45) 
    add_right_click_menu(price_entry) 
    
    #  (3) ช่องคำอธิบาย 
    description_entry = tk.Entry(edit_window, textvariable=description_var, font=entry_font, bd=2, bg=bg_color)
    description_entry.place(x=660, y=390, width=450, height=45) 
    add_right_click_menu(description_entry) 
    
    category_menu = ttk.Combobox(edit_window, textvariable=category_var,
                                    values=categories, state="readonly", font=entry_font)
    category_menu.place(x=670, y=470, width=450, height=45) 

    add_pic_button = tk.Button(edit_window, text="เปลี่ยนรูป", font=("Arial", 20, "bold"), 
                                  bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                                  command=choose_image)
    add_pic_button.place(x=185, y=470, width=170, height=50) 

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

    save_button = tk.Button(edit_window, text="เสร็จสิ้น", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="solid",
                             command=save_item)
    save_button.place(x=550, y=600, width=180, height=70) 
    
    back_button = tk.Button(edit_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_manage_menu_page(edit_window, category_var.get()))
    back_button.place(x=60, y=640, width=220, height=70) 
    
    recommend_button = tk.Button(edit_window, font=("Arial", 18, "bold"), 
                                  fg="#552c1f", bd=1 , relief="solid")
    recommend_button.place(x=910, y=240, width=200, height=45) 

    def update_recommend_button_style():
        if current_recommend_status_var.get() == 0:
            rec_text = "⭐ เพิ่ม 'แนะนำ'"
            rec_bg = "#fff0b1" 
        else:
            rec_text = "⭐ ลบ 'แนะนำ'"
            rec_bg = "#ffc1e0" 
        recommend_button.config(text=rec_text, bg=rec_bg)

    def toggle_recommend():
        current_status = current_recommend_status_var.get()
        new_status = 1 if current_status == 0 else 0 
        
        if db_set_recommend_status(item_id, new_status):
            current_recommend_status_var.set(new_status)
            update_recommend_button_style()
        else:
            messagebox.showerror("ผิดพลาด", "ไม่สามารถอัปเดตสถานะ 'แนะนำ' ได้")

    recommend_button.config(command=toggle_recommend) 
    update_recommend_button_style() 

    add_about_button(edit_window)
def admin_status_view_page(prev_window):
    """ฟังก์ชันสำหรับหน้าแสดงสถานะสินค้า (ตามรูป 003602.png)"""
    if prev_window:
        prev_window.destroy()

    status_window = create_toplevel_window("Admin - สถานะสินค้า")
    status_window.protocol("WM_DELETE_WINDOW", lambda: admin_manage_menu_page(status_window))

    global bg_image_admin_status_view
    try:
        bg_image_pil = Image.open(PIC_ADMIN_STATUS_VIEW) 
        bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        bg_image_admin_status_view = ImageTk.PhotoImage(bg_image_pil)
        background_label = tk.Label(status_window, image=bg_image_admin_status_view)
        background_label.image = bg_image_admin_status_view
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปพื้นหลังได้: {e}\n{PIC_ADMIN_STATUS_VIEW}")
        status_window.config(bg="#ffd7e8") 
    list_width = 450 
    list_height = 400 
    list_x1 = 150 
    list_x2 = 680 
    
    list_canvas_instock = tk.Canvas(status_window, bg="#ffffff", bd=0, highlightthickness=0)
    list_scrollbar_instock = ttk.Scrollbar(status_window, orient="vertical", command=list_canvas_instock.yview)
    list_scrollable_frame_instock = tk.Frame(list_canvas_instock, bg="#ffffff")

    list_scrollable_frame_instock.bind(
        "<Configure>",
        lambda e: list_canvas_instock.configure(scrollregion=list_canvas_instock.bbox("all"))
    )
    
    list_canvas_instock.create_window((0, 0), window=list_scrollable_frame_instock, anchor="nw", width=list_width-17)
    list_canvas_instock.configure(yscrollcommand=list_scrollbar_instock.set)
    list_canvas_instock.place(x=list_x1, y=200, width=list_width-17, height=list_height) 
    list_scrollbar_instock.place(x=list_x1+list_width-17, y=200, height=list_height) 
    
    
    list_canvas_outofstock = tk.Canvas(status_window, bg="#ffffff", bd=0, highlightthickness=0)
    list_scrollbar_outofstock = ttk.Scrollbar(status_window, orient="vertical", command=list_canvas_outofstock.yview)
    list_scrollable_frame_outofstock = tk.Frame(list_canvas_outofstock, bg="#ffffff")

    list_scrollable_frame_outofstock.bind(
        "<Configure>",
        lambda e: list_canvas_outofstock.configure(scrollregion=list_canvas_outofstock.bbox("all"))
    )

    list_canvas_outofstock.create_window((0, 0), window=list_scrollable_frame_outofstock, anchor="nw", width=list_width-17)
    list_canvas_outofstock.configure(yscrollcommand=list_scrollbar_outofstock.set)
    list_canvas_outofstock.place(x=list_x2, y=200, width=list_width-17, height=list_height) 
    list_scrollbar_outofstock.place(x=list_x2+list_width-17, y=200, height=list_height) 
    def _on_mousewheel_status(event):
        try:
            delta = 0
            if event.num == 4: delta = -1
            elif event.num == 5: delta = 1
            elif platform.system() == 'Windows': delta = int(-1*(event.delta/120))
            else: delta = event.delta

            mouse_x_in_window = event.x_root - status_window.winfo_rootx()
            window_center_x = 1280 / 2
            
            if mouse_x_in_window < window_center_x:
                 list_canvas_instock.yview_scroll(delta, "units")
            elif mouse_x_in_window > list_x2 - 100: 
                 list_canvas_outofstock.yview_scroll(delta, "units")

        except Exception as e:
            pass
    status_window.bind_all("<MouseWheel>", _on_mousewheel_status)
    status_window.bind_all("<Button-4>", _on_mousewheel_status) 
    status_window.bind_all("<Button-5>", _on_mousewheel_status) 
    
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
            tk.Label(target_frame, text="ไม่มีรายการ", font=("Arial", 18), bg="white").pack(pady=20) 
            return
        
        new_status_on_click = 0 if is_available == 1 else 1 

        current_category = ""
        for item in items:
            if item['category'] != current_category:
                current_category = item['category']
                tk.Label(
                    target_frame, 
                    text=f"   {current_category}   ",
                    font=("Arial", 16, "bold"), 
                    bg="#ffc1e0",
                    fg="#552c1f",
                    anchor="w"
                ).pack(fill="x", pady=(15, 5), padx=8) 

            item_btn = tk.Button(
                target_frame,
                text=f"🍴 {item['name']}",
                font=("Arial", 16), 
                bg="#fff8fa",
                fg="#552c1f",
                anchor="w",
                bd=1,
                relief="solid",
                activebackground="#ffe0f1",
                activeforeground="#552c1f",
                justify="left",
                wraplength=list_width-40, 
                command=lambda i=item['item_id'], ns=new_status_on_click: toggle_status_internal(i, ns)
            )
            item_btn.pack(fill="x", padx=15, pady=3) 
            
        target_frame.update_idletasks()
        target_canvas.configure(scrollregion=target_canvas.bbox("all"))

    def refresh_status_display():
        """(ฟังก์ชันภายใน) เรียกวาดใหม่ทั้ง 2 รายการ"""
        populate_list(list_scrollable_frame_instock, list_canvas_instock, is_available=1)
        populate_list(list_scrollable_frame_outofstock, list_canvas_outofstock, is_available=0)

    
    back_button = tk.Button(status_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_manage_menu_page(status_window))
    back_button.place(x=60, y=640, width=220, height=70) 

    add_about_button(status_window)
    
    refresh_status_display()
def admin_manage_menu_page(prev_window, default_category=None): 
    """ฟังก์ชันสำหรับหน้าจัดการเมนู"""
    if prev_window:
        prev_window.destroy()

    manage_menu_window = create_toplevel_window("Admin - จัดการเมนู")
    manage_menu_window.protocol("WM_DELETE_WINDOW", lambda: admin_panel_page(manage_menu_window))

    global bg_image_admin_manage_menu
    try:
        bg_image_manage_pil = Image.open(PIC_ADMIN_MANAGE_MENU) 
        bg_image_manage_pil = bg_image_manage_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
        
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
        if platform.system() == 'Windows':
            delta = int(-1*(event.delta/120))
        elif event.num == 4: 
            delta = -1
        elif event.num == 5: 
            delta = 1
        else:
            delta = event.delta
        
        canvas.yview_scroll(delta, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel) 

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1160) 
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.place(x=50, y=190, width=1180, height=450) 
    scrollbar.place(x=1230, y=190, height=450) 

    def display_menu_items(category):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        MENU_ITEM_PIC_REFS.clear()
        
        filtered_items = get_menu_items_from_db(category) 

        row_num = 0
        col_num = 0
        card_width = 380 
        col_count = 3 
        img_size = 150 

        if not filtered_items: 
            tk.Label(scrollable_frame, text="ไม่มีรายการเมนูในหมวดหมู่นี้",
                          font=("Arial", 25), bg="#fff0f5").grid(row=0, column=0, columnspan=col_count, pady=40) 

        for item in filtered_items:
            outer_card = tk.Frame(scrollable_frame, bg="#fff0f5", padx=8, pady=8) 
            card = tk.Frame(outer_card, bg="white", bd=1, relief="solid", padx=8, pady=8) 

            img_label = tk.Label(card, bg='#d3d3d3', width=img_size//10, height=img_size//20)
            try:
                img_placeholder_path = os.path.join(PIC_PATH, PIC_MENU_PLACEHOLDER)
                img_path = item['image_path'] or img_placeholder_path
                if not os.path.exists(img_path):
                    img_path = None 
                if img_path:
                    img = load_and_resize_pic(img_path, img_size, is_menu_item=True)
                    img_label.config(image=img, width=img_size, height=img_size, bg='white')
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
                font=("Arial", 12, "bold"), bg=status_bg, fg=status_fg, 
                padx=8, pady=4 
            )
            status_label.pack(side="left")
            
            if item.get('is_recommended', 0) == 1:
                rec_label = tk.Label(status_frame, text="⭐ แนะนำ",
                    font=("Arial", 12, "bold"), bg="#fff0b1", fg="#552c1f", 
                    padx=8, pady=4 
                )
                rec_label.pack(side="left", padx=8) 
            
            status_frame.pack(fill="x", padx=0, pady=(0, 5)) 
            
            tk.Label(card, text=item['name'], font=("Arial", 20, "bold"), bg="white", anchor="w").pack(fill="x") 
            tk.Label(card, text=item.get('description', ''), font=("Arial", 14), bg="white", anchor="nw", wraplength=card_width-40, justify="left", height=2).pack(fill="x") 
            tk.Label(card, text=f"ราคา {item['price']:,.2f} บาท", font=("Arial", 18, "bold"), bg="white", anchor="w").pack(fill="x", pady=(0, 5)) 

            btn_frame = tk.Frame(card, bg="white")
            edit_btn = tk.Button(btn_frame, text="แก้ไข", font=("Arial", 18, "bold"), bg="#c4e6fa", fg="black", width=8, 
                                 command=lambda i=item: admin_edit_menu_page(manage_menu_window, i))
            del_btn = tk.Button(btn_frame, text="ลบ", font=("Arial", 18, "bold"), bg="#ff7bb5", fg="black", width=8, 
                                 command=lambda i=item: delete_menu_item(i)) 
            edit_btn.pack(side="left", padx=15) 
            del_btn.pack(side="right", padx=15) 
            btn_frame.pack(fill="x", pady=(0, 10)) 

            card.pack(fill="both", expand=True)
            outer_card.grid(row=row_num, column=col_num, padx=15, pady=15, sticky="nsew") 

            col_num += 1
            if col_num >= col_count:
                col_num = 0
                row_num += 1

        for i in range(col_count):
            scrollable_frame.grid_columnconfigure(i, weight=1, minsize=card_width + 15) 
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
    tab_frame.place(x=50, y=125, height=65, width=950)

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
        btn = tk.Button(tab_frame, text=cat, font=("Arial", 25, "bold"), 
                         bg="#ffe0f1", fg="#552c1f", relief="raised", bd=1,
                         activebackground="#ffc1e0",
                         command=lambda c=cat: select_category(c))
        btn.pack(side="left", fill="both", expand=True, padx=5, pady=5) 
        category_buttons[cat] = btn
    
    button_frame = tk.Frame(manage_menu_window, bg="#fff0f5", bd=0) 
    button_frame.place(x=1010, y=125, width=220, height=65) 
    add_button = tk.Button(button_frame, text="เพิ่มเมนู", font=("Arial", 16, "bold"), 
                           bg="#fff0b1", fg="#552c1f", relief="raised", bd=1,
                           command=lambda: admin_add_menu_page(manage_menu_window, current_category.get())) 
    add_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
    status_page_button = tk.Button(button_frame, text="สถานะ", font=("Arial", 16, "bold"), 
                                   bg="#bfffcb", fg="#552c1f", relief="raised", bd=1,
                                   command=lambda: admin_status_view_page(manage_menu_window))
    status_page_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)

    back_button = tk.Button(manage_menu_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"), 
                             bg="#ffe0f1", fg="#552c1f", bd=1 , relief="solid",
                             command=lambda: admin_panel_page(manage_menu_window))
    back_button.place(x=60, y=640, width=220, height=70) 

    if default_category and default_category in categories:
        select_category(default_category)
    else:
        select_category(categories[0]) 

root = tk.Tk()
root.title("หนูดีส้มตำฟรุ้งฟริ้ง")
root.geometry("1280x720") 
root.resizable(True, True) 

try:
    bg_image_pil = Image.open(f"{PIC_PATH}{PIC_MAIN}")
    bg_image_pil = bg_image_pil.resize((1280, 720), Image.Resampling.LANCZOS) 
    bg_image = ImageTk.PhotoImage(bg_image_pil)
    background_label = tk.Label(root, image=bg_image)
    background_label.image = bg_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"ไม่สามารถโหลดรูปภาพหลัก ({PIC_PATH}{PIC_MAIN}) ได้: {e}")
    root.destroy()
    exit()

login_button = tk.Button(root, text="เข้าสู่ระบบ", font=("UID SALMON 2019", 60, "bold"), 
                          bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                          activebackground="#ffabcf",
                          command=login_page)
login_button.place(x=920, y=318, width=235, height=100) 

register_button = tk.Button(root, text="สมัครสมาชิก", font=("UID SALMON 2019", 60, "bold"), 
                             bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#ffabcf",
                             command=register_page)
register_button.place(x=920, y=458, width=235, height=100) 

add_about_button(root)
root.mainloop()