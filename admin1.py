import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import re 
import os 
import shutil 

# ==============================================================================
# 0. CONFIGURATION & GLOBAL VARIABLES
# ==============================================================================
# ชื่อไฟล์ฐานข้อมูล
DB_NAME = "user_data.db"
# Path รูปภาพพื้นหลัง (ปรับให้เป็น path ที่ถูกต้อง)
PIC_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\" 
# Path สำหรับเก็บรูปโปรไฟล์ของผู้ใช้
PROFILE_PICS_DIR = "D:\\Project Nudee\\รูปโปรไฟล์ผู้ใช้\\"

# สร้างโฟลเดอร์สำหรับเก็บรูปโปรไฟล์ ถ้ายังไม่มี
os.makedirs(PROFILE_PICS_DIR, exist_ok=True)

# ชื่อไฟล์รูปภาพ
PIC_MAIN = "1.png"
PIC_LOGIN = "2.png"
PIC_REGISTER = "3.png"
PIC_TABLE_SELECT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\7 Table.png"
PIC_PROFILE_VIEW ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\5 profile.png"
PIC_PROFILE_EDIT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\6 edit profile.png"
PIC_ABOUT = "about.png" 
PIC_FORGOT_PASSWORD = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\4.png"

### START: เพิ่ม Path และ Credentials Admin ###
PIC_ADMIN_PANEL = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\admin.png"# ชื่อไฟล์รูปหน้าแอดมินที่คุณส่งมา
ADMIN_USERNAME = "admineiei"
ADMIN_PASSWORD = "12345678"
### END: เพิ่ม Path และ Credentials Admin ###

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

# Global Variables สำหรับรูปภาพที่ต้องใช้ซ้ำหลายหน้า
global bg_image_about
bg_image_about = None 
global bg_image_table_select
bg_image_table_select = None
global bg_image_forgot
bg_image_forgot = None

### START: เพิ่ม Global รูป Admin ###
global bg_image_admin_panel
bg_image_admin_panel = None
### END: เพิ่ม Global รูป Admin ###


# ******************************************************************************
# (ฟังก์ชัน Utility: load_and_resize_pic, create_db_table)
# ... โค้ดส่วนนี้เหมือนเดิม ...
# ******************************************************************************
def load_and_resize_pic(file_path, size):
    """โหลดและปรับขนาดรูปภาพให้เป็นวงกลม (จำลอง) หรือสี่เหลี่ยมตามขนาดที่ต้องการ"""
    if file_path and os.path.exists(file_path):
        try:
            img_pil = Image.open(file_path)
        except Exception as e:
            print(f"Error opening image {file_path}: {e}")
            img_pil = Image.new('RGB', (size, size), color = '#b8828b') # Placeholder
    else:
        # Placeholder สีเดียวเมื่อไม่มีรูปโปรไฟล์
        img_pil = Image.new('RGB', (size, size), color = '#b8828b') 
            
    img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk


def create_db_table():
    """สร้างฐานข้อมูลและตาราง user_account และ user_profile หากยังไม่มี"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 1. สร้างตาราง user_account
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_account (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT,
                surname TEXT,
                phone TEXT,
                birthday TEXT,
                email TEXT
            )
        """)
        
        # 2. สร้างตาราง user_profile (เก็บคะแนนและ path รูปโปรไฟล์)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                username TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0,
                profile_pic_path TEXT,
                FOREIGN KEY (username) REFERENCES user_account(username)
            )
        """)
        
        # 3. ตรวจสอบว่ามีคอลัมน์ profile_pic_path หรือไม่ ถ้าไม่มีให้เพิ่ม
        cursor.execute("PRAGMA table_info(user_profile)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'profile_pic_path' not in columns:
            try:
                cursor.execute("ALTER TABLE user_profile ADD COLUMN profile_pic_path TEXT")
            except sqlite3.OperationalError as e:
                # อาจเกิดขึ้นถ้ามีคนรันพร้อมกัน แต่ไม่เป็นไร
                print(f"Could not add column (likely already exists): {e}")

        conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถสร้างฐานข้อมูลได้: {e}")
    finally:
        if conn:
            conn.close()

# เรียกใช้ฟังก์ชันสร้างฐานข้อมูลเมื่อโปรแกรมเริ่มต้น
create_db_table()
# ------------------------------------


# ==============================================================================
# 1. NAVIGATION & UTILITY FUNCTIONS
# ... โค้ดส่วนนี้ (back_to_main_page, add_about_button) เหมือนเดิม ...
# ==============================================================================
def back_to_main_page(current_window):
    """ฟังก์ชันสำหรับกลับไปหน้าหลัก (root) และออกจากระบบ (ถ้ามี)"""
    global CURRENT_USER
    if CURRENT_USER:
        CURRENT_USER = None # Log out
    current_window.destroy()
    root.deiconify()

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
# ... โค้ดส่วนนี้ (get_user_data, update_user_profile) เหมือนเดิม ...
# ==============================================================================
def get_user_data(username):
    """ดึงข้อมูลผู้ใช้จากตาราง account และ profile"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.user_id, a.username, a.password, a.name, a.surname, a.phone, a.birthday, a.email, p.score, p.profile_pic_path
        FROM user_account a
        LEFT JOIN user_profile p ON a.username = p.username
        WHERE a.username = ?
    """, (username,))
    data = cursor.fetchone()
    conn.close()
    if data:
        # data format: (user_id, username, password, name, surname, phone, birthday, email, score, profile_pic_path)
        return dict(zip([
            "user_id", "username", "password", "name", "surname", "phone", "birthday", "email", "score", "pic_path"
        ], data))
    return None

def update_user_profile(old_username, new_data):
    """อัปเดตข้อมูลผู้ใช้ในตาราง account และ profile (รองรับการเปลี่ยน username)"""
    global CURRENT_USER
    new_username = new_data['username']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # 1. ตรวจสอบชื่อผู้ใช้ใหม่หากมีการเปลี่ยนแปลง
        if new_username != old_username:
            cursor.execute("SELECT username FROM user_account WHERE username = ?", (new_username,))
            if cursor.fetchone():
                messagebox.showerror("ผิดพลาด", f"ชื่อผู้ใช้ '{new_username}' ถูกใช้ไปแล้ว")
                return False
            
            cursor.execute("SELECT password FROM user_account WHERE username = ?", (old_username,))
            current_password = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE user_account SET username=?, password=?, name=?, surname=?, phone=?, birthday=?, email=? WHERE username=?
            """, (new_username, current_password, new_data['name'], new_data['surname'], new_data['phone'], new_data['birthday'], new_data['email'], old_username))
            
            cursor.execute("SELECT score FROM user_profile WHERE username = ?", (old_username,))
            profile_data = cursor.fetchone()
            score = profile_data[0] if profile_data else 0
            pic_path = new_data.get('pic_path', None)
            
            cursor.execute("DELETE FROM user_profile WHERE username = ?", (old_username,))
            
            cursor.execute("""
                INSERT INTO user_profile (username, score, profile_pic_path) VALUES (?, ?, ?)
            """, (new_username, score, pic_path))
            
            CURRENT_USER = new_username
            
        else:
            cursor.execute("""
                UPDATE user_account SET name=?, surname=?, phone=?, birthday=?, email=? WHERE username=?
            """, (new_data['name'], new_data['surname'], new_data['phone'], new_data['birthday'], new_data['email'], old_username))
            
            if 'pic_path' in new_data:
                cursor.execute("""
                    UPDATE user_profile SET profile_pic_path=? WHERE username=?
                """, (new_data['pic_path'], old_username))
                
                if cursor.rowcount == 0:
                    cursor.execute("""
                        INSERT INTO user_profile (username, score, profile_pic_path)
                        VALUES (?, ?, ?)
                    """, (old_username, 0, new_data['pic_path']))

        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback() 
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกข้อมูลได้: {e}")
        return False
    finally:
        conn.close()

# ==============================================================================
# 3. GUI WINDOW CREATION
# ==============================================================================

def create_toplevel_window(title):
    """ฟังก์ชันรวมสำหรับสร้างหน้าต่างย่อย (Toplevel) และซ่อนหน้าหลัก"""
    root.withdraw()
    new_window = tk.Toplevel(root)
    new_window.title(title)
    new_window.geometry("960x540")
    new_window.resizable(False, False)
    
    # ทำให้เมื่อปิดหน้าต่าง Toplevel ให้กลับไปหน้าหลัก (ยกเว้นหน้าที่ตั้งใจไปหน้าอื่น)
    new_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(new_window))
    
    return new_window

# ------------------------------------
# (หน้า 4: About Me)
# ... โค้ดส่วนนี้เหมือนเดิม ...
# ------------------------------------
def about_page():
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
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}")
        about_window.destroy()
        root.deiconify()

# ------------------------------------
# (หน้า 7: เลือกโต๊ะ)
# ... โค้ดส่วนนี้เหมือนเดิม ...
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
    def select_table(table_num):
        selected_table.set(table_num)
        print(f"เลือกโต๊ะ: {table_num}")
    table_coords = [(225, 65), (560, 65), (225, 270), (560, 270)]
    for i, (x, y) in enumerate(table_coords):
        tk.Button(table_window, text=f"โต๊ะ {i+1}", font=("UID SALMON 2019", 70), bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised", command=lambda num=i+1: select_table(num)).place(x=x, y=y, width=160 , height=150)
    back_button = tk.Button(table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50,"bold" ), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: back_to_main_page(table_window))
    back_button.place(x=315, y=460, width=140, height=49)
    next_button = tk.Button(table_window, text="ต่อไป", font=("UID SALMON 2019", 50,"bold" ), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: open_menu_page(table_window, selected_table.get()))
    next_button.place(x=490, y=460, width=140, height=49)
    size = 45
    profile_button_frame = tk.Frame(table_window, bg="white", bd=0, relief="flat")
    profile_button_frame.place(x=12, y=10, width=size, height=size) 
    user_data = get_user_data(CURRENT_USER)
    profile_pic_path = user_data.get('pic_path') if user_data else None
    def display_small_profile_pic(window, pic_path):
        global TABLE_PIC_REF
        pic_size = 45 
        img_tk = load_and_resize_pic(pic_path, pic_size)
        TABLE_PIC_REF['pic'] = img_tk 
        btn = tk.Button(window, image=img_tk, bd=0, relief="flat", command=lambda: profile_view_page(table_window))
        btn.place(x=0, y=0, width=pic_size, height=pic_size) 
    display_small_profile_pic(profile_button_frame, profile_pic_path)
    add_about_button(table_window) 

def open_menu_page(current_window, selected_table):
    if not selected_table or selected_table == 'None':
        messagebox.showwarning("ยังไม่ได้เลือก", "กรุณาเลือกโต๊ะก่อนดำเนินการต่อ")
        return
    current_window.destroy()
    messagebox.showinfo("ต่อไป", f"คุณเลือกโต๊ะ {selected_table} \n(จะนำไปยังหน้าเมนูอาหาร)")
    # --- !! Placeholder: ควรไปหน้าเมนูจริงๆ ---
    root.deiconify() 
    # --- !! Placeholder End ---

# ------------------------------------
# (หน้า 5: โปรไฟล์ View Mode)
# ... โค้ดส่วนนี้เหมือนเดิม ...
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
    display_profile_pic(profile_window, user_data.get('pic_path'))
    edit_button = tk.Button(profile_window, text="แก้ไข", font=("UID SALMON 2019", 35, "bold"), bg="#fffbf2", fg="#552c1f", bd=0, relief="flat", command=lambda: profile_edit_page(profile_window, user_data))
    edit_button.place(x=799, y=86, width=70, height=38)
    back_button = tk.Button(profile_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: table_selection_page(profile_window))
    back_button.place(x=300, y=440, width=150, height=70) 
    logout_button = tk.Button(profile_window, text="ออกจากระบบ", font=("UID SALMON 2019", 40, "bold"), bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat", command=lambda: back_to_main_page(profile_window))
    logout_button.place(x=525, y=440, width=150, height=70) 
    add_about_button(profile_window)

# ------------------------------------
# (หน้า 6: โปรไฟล์ Edit Mode)
# ... โค้ดส่วนนี้เหมือนเดิม ...
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
    current_pic_path = tk.StringVar(value=user_data.get('pic_path', ''))
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

# ------------------------------------
# Main Pages (Login/Register/Forgot Password)
# ------------------------------------

def open_next_page(current_window):
    current_window.destroy()
    table_selection_page()

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


### START: หน้าใหม่ (Admin Panel) ###
def admin_panel_page(prev_window):
    """ฟังก์ชันสำหรับหน้า 'แอดมิน'"""
    if prev_window:
        prev_window.destroy()
        
    admin_window = create_toplevel_window("Admin Panel")
    
    # ตั้งค่า protocol การปิดหน้าต่างใหม่ (ให้กลับไปหน้า main และ logout)
    admin_window.protocol("WM_DELETE_WINDOW", lambda: back_to_main_page(admin_window))

    global bg_image_admin_panel
    try:
        # โหลดรูปพื้นหลัง admin.jpg
        bg_image_admin_pil = Image.open(f"{PIC_ADMIN_PANEL}")
        bg_image_admin_pil = bg_image_admin_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_admin_panel = ImageTk.PhotoImage(bg_image_admin_pil)
        background_label_admin = tk.Label(admin_window, image=bg_image_admin_panel)
        background_label_admin.image = bg_image_admin_panel
        background_label_admin.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรูปภาพได้: {e}\n{PIC_PATH}{PIC_ADMIN_PANEL}")
        admin_window.destroy()
        root.deiconify()
        return

    # --- ปุ่ม Placeholder (ยังไม่ได้ใส่ command) ---
   # btn_font = ("UID SALMON 2019", 50, "bold") # ปรับ Font ตามรูป
    
    # 1. ปุ่มยอดขาย
    sales_button = tk.Button(admin_window, text="ยอดขาย", font= ("UID SALMON 2019", 70, "bold"), 
                             bg="#ffffff", fg="#552c1f", bd=0 , relief="groove")
    sales_button.place(relx=0.5, y=170, width=280, height=70, anchor=tk.CENTER)

    # 2. ปุ่มโต๊ะลูกค้า/ออเดอร์
    table_order_button = tk.Button(admin_window, text="โต๊ะลูกค้า/คำสั่งซื้อ", font= ("UID SALMON 2019", 45, "bold"), 
                                   bg="#ffffff", fg="#552c1f", bd=0, relief="groove")
    table_order_button.place(x=160, y=305, width=285 , height=85)

    # 3. ปุ่มเพิ่ม/แก้ไข/ลบ เมนู
    menu_button = tk.Button(admin_window, text="เพิ่ม/แก้ไข/ลบ เมนู", font= ("UID SALMON 2019", 45, "bold"),
                            bg="#ffffff", fg="#552c1f", bd=0, relief="groove", justify=tk.CENTER)
    menu_button.place(x=525, y=305, width=285, height=85)

    # --- ปุ่ม Logout ---
    logout_button = tk.Button(admin_window, text="ออกจากระบบ", font=("UID SALMON 2019", 30 , "bold"),
                             bg="#ff257d", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#ff257d", 
                             command=lambda: back_to_main_page(admin_window))
    logout_button.place(x=800, y=18, width=140, height=43) # ตำแหน่งมุมซ้ายบน (ตัวอย่าง)


    # ปุ่มผู้พัฒนา (About Me)
    add_about_button(admin_window)

### END: หน้าใหม่ (Admin Panel) ###


### START: แก้ไขหน้า Login ###
def login_page(prev_window=None): # เพิ่ม prev_window
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

    # *** แก้ไข Logic การ Login ***
    def local_verify_login():
        global CURRENT_USER
        user = username_entry.get()
        pwd = password_entry.get()
        
        # --- 1. ตรวจสอบว่าเป็น Admin หรือไม่ ---
        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            CURRENT_USER = ADMIN_USERNAME # ตั้งค่าผู้ใช้ปัจจุบันเป็น Admin
            messagebox.showinfo("Admin Login", "เข้าสู่ระบบแอดมินสำเร็จ!")
            admin_panel_page(login_window) # ไปหน้า Admin Panel
            return # ออกจากฟังก์ชัน ไม่ต้องเช็ค DB
            
        # --- 2. ถ้าไม่ใช่ Admin ให้ตรวจสอบในฐานข้อมูล (ลูกค้า) ---
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = ? AND password = ?", (user, pwd))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            CURRENT_USER = user # ตั้งค่าผู้ใช้ปัจจุบันเป็นลูกค้า
            messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ!")
            open_next_page(login_window) # ไปหน้าเลือกโต๊ะ
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3", 
                                 command=local_verify_login) # <<< เรียกฟังก์ชันที่แก้ไขแล้ว
    confirm_button.place(x=540, y=420, width=150, height=50)
    
    add_about_button(login_window)
### END: แก้ไขหน้า Login ###
    

### START: แก้ไขหน้า Register ###
def register_page(prev_window=None): # เพิ่ม prev_window
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

    # (โค้ดส่วนที่เหลือของหน้า Register เหมือนเดิม)
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
    email_entry = tk.Entry(register_window, font=("Arial", 24), bg="#ffebf6", bd=0, relief="flat")
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
### END: แก้ไขหน้า Register ###


# --- สร้างหน้าต่างหลัก ---
root = tk.Tk()
root.title("หนูดีส้มตำฟรุ้งฟริ้ง")
root.geometry("960x540")
root.resizable(False, False)

try:
    # แก้ไข Path ให้ถูกต้อง (ใช้ PIC_PATH)
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