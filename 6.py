import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import re 
import os 

# ==============================================================================
# 0. CONFIGURATION & GLOBAL VARIABLES
# ==============================================================================
# ชื่อไฟล์ฐานข้อมูล
DB_NAME = "user_data.db"
# Path รูปภาพ (ปรับให้เป็น path ที่ถูกต้อง)
PIC_PATH = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\" 
# ชื่อไฟล์รูปภาพ
PIC_MAIN = "1.png"
PIC_LOGIN = "2.png"
PIC_REGISTER = "3.png"
PIC_TABLE_SELECT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\7 Table.png" # PATH รูปภาพหน้าเลือกโต๊ะ
PIC_PROFILE_VIEW ="D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\5 profile.png"# PATH รูปภาพหน้าโปรไฟล์ (View)
PIC_PROFILE_EDIT = "D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\6 edit profile.png" # PATH รูปภาพหน้าโปรไฟล์ (Edit)
PIC_ABOUT = "about.png" 

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
CURRENT_USER = None # เก็บ username ของผู้ที่ล็อกอินอยู่
CURRENT_WINDOW = None # ใช้สำหรับเก็บ reference หน้าต่างปัจจุบัน (เพื่อความง่ายในการนำทาง)
PROFILE_PIC_REF = {} # ใช้เก็บ reference รูปโปรไฟล์เพื่อให้ไม่ถูก GC ลบ
TABLE_PIC_REF = {} # ใช้เก็บ reference รูปภาพโต๊ะ

# Global Variables สำหรับรูปภาพที่ต้องใช้ซ้ำหลายหน้า
global bg_image_about
bg_image_about = None 
global bg_image_table_select
bg_image_table_select = None


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
        
    except sqlite3.Error as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถสร้างฐานข้อมูลได้: {e}")

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
    """ดึงข้อมูลผู้ใช้จากตาราง account และ profile"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, p.score, p.profile_pic_path
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
            
            # 2. อัปเดตตาราง user_account (อัปเดตข้อมูลและชื่อผู้ใช้)
            # ดึงรหัสผ่านเดิมไว้ (เนื่องจากหน้านี้ไม่ให้แก้รหัสผ่าน)
            cursor.execute("SELECT password FROM user_account WHERE username = ?", (old_username,))
            current_password = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE user_account SET username=?, password=?, name=?, surname=?, phone=?, birthday=?, email=? WHERE username=?
            """, (new_username, current_password, new_data['name'], new_data['surname'], new_data['phone'], new_data['birthday'], new_data['email'], old_username))
            
            # 3. อัปเดตตาราง user_profile (ใช้วิธีลบแล้วสร้างใหม่เนื่องจาก username เป็น PRIMARY KEY)
            
            # ดึงข้อมูล profile เดิม
            cursor.execute("SELECT score FROM user_profile WHERE username = ?", (old_username,))
            profile_data = cursor.fetchone()
            score = profile_data[0] if profile_data else 0
            pic_path = new_data['pic_path']
            
            # ลบ profile เก่า
            cursor.execute("DELETE FROM user_profile WHERE username = ?", (old_username,))
            
            # สร้าง profile ใหม่ด้วย username ใหม่
            cursor.execute("""
                INSERT INTO user_profile (username, score, profile_pic_path) VALUES (?, ?, ?)
            """, (new_username, score, pic_path))
            
            # 4. อัปเดต Global User
            CURRENT_USER = new_username
            
        else:
            # หากไม่มีการเปลี่ยน username, อัปเดตเฉพาะข้อมูลอื่น ๆ
            cursor.execute("""
                UPDATE user_account SET name=?, surname=?, phone=?, birthday=?, email=? WHERE username=?
            """, (new_data['name'], new_data['surname'], new_data['phone'], new_data['birthday'], new_data['email'], old_username))
            
            if 'pic_path' in new_data:
                 cursor.execute("""
                     UPDATE user_profile SET profile_pic_path=? WHERE username=?
                 """, (new_data['pic_path'], old_username))

        conn.commit()
        return True
    except sqlite3.Error as e:
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
    return new_window

# ------------------------------------
# หน้า 4: About Me
# ------------------------------------
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
        
        back_button = tk.Button(about_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50 , "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised", 
                                 activebackground="#ffe0f1", 
                                 command=lambda: back_to_main_page(about_window))
        back_button.place(x=790, y=470, width=150, height=45) 
        
    except FileNotFoundError:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่พบไฟล์รูปภาพผู้พัฒนา")
        background_label_about = tk.Label(about_window, text="ไม่พบรูปภาพผู้พัฒนา", font=("Arial", 24))
        background_label_about.pack(expand=True, fill="both")
        
        back_button = tk.Button(about_window, text="ย้อนกลับ", command=lambda: back_to_main_page(about_window))
        back_button.pack(pady=20)

# ------------------------------------
# หน้า 7: เลือกโต๊ะ
# ------------------------------------
def table_selection_page():
    """ฟังก์ชันสำหรับหน้า 'เลือกโต๊ะ' (หน้าที่ 7)"""
    global CURRENT_WINDOW
    table_window = create_toplevel_window("หนูดีส้มตำฟรุ้งฟริ้ง - เลือกโต๊ะ")
    CURRENT_WINDOW = table_window # ตั้งค่าหน้าต่างปัจจุบัน

    global bg_image_table_select
    try:
        # พื้นหลัง
        bg_image_table_select_pil = Image.open(PIC_TABLE_SELECT)
        bg_image_table_select_pil = bg_image_table_select_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_table_select = ImageTk.PhotoImage(bg_image_table_select_pil)
        
        background_label_table = tk.Label(table_window, image=bg_image_table_select)
        background_label_table.image = bg_image_table_select
        background_label_table.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        tk.Label(table_window, text="ไม่พบรูปภาพพื้นหลัง (7.png)", font=("Arial", 24)).pack(expand=True)
        
    # โต๊ะ (จำลองการเลือก)
    selected_table = tk.StringVar(value=None)

    def select_table(table_num):
        selected_table.set(table_num)
        print(f"เลือกโต๊ะ: {table_num}")

    # สร้างปุ่มสำหรับโต๊ะ 4 ที่ (อ้างอิงตำแหน่งคร่าวๆ จากรูป)
    table_coords = [
        (225, 65), (560, 65),
        (225, 270), (560, 270)
    ]
    
    for i, (x, y) in enumerate(table_coords):
        tk.Button(table_window, text=f"โต๊ะ {i+1}", font=("UID SALMON 2019", 70), 
                  bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised",
                  command=lambda num=i+1: select_table(num)).place(x=x, y=y, width=160 , height=150)

    # ปุ่ม Navigation
    
    # ปุ่มย้อนกลับ (กลับไปหน้าหลัก/Login)
    back_button = tk.Button(table_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50,"bold" ),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             command=lambda: back_to_main_page(table_window))
    back_button.place(x=315, y=460, width=140, height=49)
    
    # ปุ่มต่อไป (ไปหน้าเมนู)
    next_button = tk.Button(table_window, text="ต่อไป", font=("UID SALMON 2019", 50,"bold" ),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             command=lambda: open_menu_page(table_window, selected_table.get()))
    next_button.place(x=490, y=460, width=140, height=49)
    
    # ปุ่มโปรไฟล์ (ซ้ายบน) - ต้องใช้รูปโปรไฟล์ที่บันทึกไว้
    profile_button_frame = tk.Frame(table_window, bg="white", bd=0)
    profile_button_frame.place(x=12, y=10, width=45, height=40) # กรอบสำหรับรูปโปรไฟล์

    user_data = get_user_data(CURRENT_USER)
    profile_pic_path = user_data.get('pic_path') if user_data else None
    
    # ฟังก์ชันสำหรับแสดงรูปโปรไฟล์ขนาดเล็ก (ใช้สำหรับปุ่ม)
    def display_small_profile_pic(window, pic_path):
        size = 50
        try:
            if pic_path and os.path.exists(pic_path):
                img_pil = Image.open(pic_path)
            else:
                img_pil = Image.new('RGB', (size, size), color = '#b8828b') # Placeholder สีเดียว
                
            img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            # เก็บ reference ไว้ใน global dictionary
            TABLE_PIC_REF['pic'] = img_tk 
            
            # สร้างปุ่มที่ใช้รูปภาพ
            btn = tk.Button(window, image=img_tk, bd=0, relief="flat",
                            command=lambda: profile_view_page(table_window))
            btn.place(x=0, y=0, width=size, height=size) 
            
        except Exception as e:
            print(f"Error loading small profile picture: {e}")
            tk.Button(window, text="P", command=lambda: profile_view_page(table_window), width=5, height=2).place(x=0, y=0)


    display_small_profile_pic(profile_button_frame, profile_pic_path)
    
    # ปุ่มผู้พัฒนา (ขวาบน)
    add_about_button(table_window) 

def open_menu_page(current_window, selected_table):
    """ฟังก์ชันจำลอง: ไปยังหน้าเมนูอาหาร"""
    if not selected_table or selected_table == 'None':
        messagebox.showwarning("ยังไม่ได้เลือก", "กรุณาเลือกโต๊ะก่อนดำเนินการต่อ")
        return
        
    current_window.destroy()
    messagebox.showinfo("ต่อไป", f"คุณเลือกโต๊ะ {selected_table} \n(จะนำไปยังหน้าเมนูอาหาร)")
    root.deiconify() # กลับหน้าหลักชั่วคราว


# ------------------------------------
# หน้า 5: โปรไฟล์ (View Mode)
# ------------------------------------
# ปรับปรุง: ต้องส่ง user_data ไปยังหน้า Edit ด้วย
def profile_view_page(prev_window, user_data=None): 
    """ฟังก์ชันสำหรับแสดงหน้า 'โปรไฟล์ลูกค้า' (หน้าที่ 5)"""
    global PROFILE_PIC_REF 
    
    # 1. ดึงข้อมูลผู้ใช้ (หากไม่ได้ส่ง user_data เข้ามา)
    if not user_data:
        user_data = get_user_data(CURRENT_USER)
        
    if not user_data:
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลผู้ใช้ กรุณาเข้าสู่ระบบใหม่")
        if prev_window:
             prev_window.deiconify() 
        else: 
             root.deiconify()
        return

    # 2. สร้างหน้าต่าง
    if prev_window:
        prev_window.withdraw()
        
    profile_window = tk.Toplevel(root)
    profile_window.title("หนูดีส้มตำฟรุ้งฟริ้ง - โปรไฟล์")
    profile_window.geometry("960x540")
    profile_window.resizable(False, False)

    # 3. พื้นหลัง
    try:
        bg_image_profile_pil = Image.open(PIC_PROFILE_VIEW)
        bg_image_profile_pil = bg_image_profile_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_profile = ImageTk.PhotoImage(bg_image_profile_pil)
        background_label_profile = tk.Label(profile_window, image=bg_image_profile)
        background_label_profile.image = bg_image_profile
        background_label_profile.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        tk.Label(profile_window, text="ไม่พบรูปภาพพื้นหลัง (5.png)", font=("Arial", 24)).pack(expand=True)

    # 4. ฟังก์ชันสำหรับแสดงรูปโปรไฟล์ (กรอบสีชมพู)
    def display_profile_pic(window, pic_path):
        x_pos, y_pos, size = 100, 135, 180 
        frame = tk.Frame(window, bg='white', width=size, height=size, bd=0)
        frame.place(x=x_pos, y=y_pos)
        
        try:
            if pic_path and os.path.exists(pic_path):
                img_pil = Image.open(pic_path)
            else:
                img_pil = Image.new('RGB', (size, size), color = 'pink') 
                
            img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            PROFILE_PIC_REF['pic_view'] = img_tk 
            
            pic_label = tk.Label(frame, image=img_tk, bd=0)
            pic_label.place(x=0, y=0, relwidth=1, relheight=1)
            return pic_label
        except Exception as e:
            print(f"Error loading profile picture: {e}")
            return tk.Label(frame, text="Load Error", fg="red").place(x=0, y=0, relwidth=1, relheight=1)

    # 5. แสดงข้อมูล (ตำแหน่งคร่าวๆ อ้างอิงจากรูป)
    font_style = ("Arial", 20)
    text_color = "#e37494" # สีชมพูอ่อน (อ้างอิงจากรูป)
    
    # ชื่อผู้ใช้
    tk.Label(profile_window, text=f"{user_data['username']}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=145, y=350, width=120 , height= 30)

    # ชื่อ-สกุล:
    name_full = f"{user_data['name']} {user_data['surname']}"
    tk.Label(profile_window, text=name_full, font=font_style, fg=text_color, bg="#ffe0f1").place(x=490, y=154, width=150 , height= 30)
    
    # เบอร์โทร:
    tk.Label(profile_window, text=f"{user_data['phone']}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=430, y=220, width=150 , height= 30)
    
    # วันเกิด:
    tk.Label(profile_window, text=f"{user_data['birthday']}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=410, y=280, width=165 , height= 30)
    
    # Email:
    tk.Label(profile_window, text=f"{user_data['email']}", font=font_style, fg=text_color, bg="#ffe0f1").place(x=410, y=330, width=300 , height= 30)

    # คะแนน:
    tk.Label(profile_window, text=f" {user_data['score']}", font=font_style, fg="#552c1f", bg="#ffe0f1").place(x=520, y=395, width=100 , height= 30)

    # แสดงรูปโปรไฟล์
    display_profile_pic(profile_window, user_data.get('pic_path'))

    # 6. ปุ่ม Navigation
    
    # ปุ่มแก้ไข (มุมขวาบน - อ้างอิงจากรูป)
    edit_button = tk.Button(profile_window, text="แก้ไข", font=("UID SALMON 2019", 35, "bold"),
                            bg="#fffbf2", fg="#552c1f", bd=0, relief="flat",
                            command=lambda: profile_edit_page(profile_window, user_data))
    edit_button.place(x=799, y=86, width=70, height=38)

    # ปุ่มย้อนกลับ (กลับไปหน้าเลือกโต๊ะ)
    back_button = tk.Button(profile_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             command=lambda: table_selection_page(profile_window)) # กลับไปหน้า 7
    back_button.place(x=300, y=440, width=150, height=70) 

    # ปุ่มออกจากระบบ
    logout_button = tk.Button(profile_window, text="ออกจากระบบ", font=("UID SALMON 2019", 40, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                               command=lambda: back_to_main_page(profile_window)) # กลับไปหน้าหลัก
    logout_button.place(x=525, y=440, width=150, height=70) 

    # ปุ่มผู้พัฒนา
    add_about_button(profile_window)


# ------------------------------------
# หน้า 6: โปรไฟล์ (Edit Mode) - ปรับปรุงการแก้ไข Username และลบ Password
# ------------------------------------
def profile_edit_page(prev_window, user_data):
    """ฟังก์ชันสำหรับหน้า 'แก้ไขโปรไฟล์ลูกค้า' (หน้าที่ 6)"""
    global PROFILE_PIC_REF
    
    prev_window.withdraw()
    edit_window = tk.Toplevel(root)
    edit_window.title("หนูดีส้มตำฟรุ้งฟริ้ง - แก้ไขโปรไฟล์")
    edit_window.geometry("960x540")
    edit_window.resizable(False, False)

    # พื้นหลัง
    try:
        bg_image_edit_pil = Image.open(PIC_PROFILE_EDIT)
        bg_image_edit_pil = bg_image_edit_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_edit = ImageTk.PhotoImage(bg_image_edit_pil)
        background_label_edit = tk.Label(edit_window, image=bg_image_edit)
        background_label_edit.image = bg_image_edit
        background_label_edit.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        tk.Label(edit_window, text="ไม่พบรูปภาพพื้นหลัง (6.png)", font=("Arial", 24)).pack(expand=True)
        
    # Variables สำหรับ Entry Fields
    username_var = tk.StringVar(value=user_data['username']) 
    name_var = tk.StringVar(value=user_data['name'])
    surname_var = tk.StringVar(value=user_data['surname'])
    phone_var = tk.StringVar(value=user_data['phone'])
    birthday_var = tk.StringVar(value=user_data['birthday'])
    email_var = tk.StringVar(value=user_data['email'])
    current_pic_path = tk.StringVar(value=user_data.get('pic_path', ''))
    
    # ฟังก์ชันแสดงรูปโปรไฟล์ (เหมือนหน้า View)
    def display_profile_pic(window, pic_path_var):
        x_pos, y_pos, size = 100, 130, 180
        pic_path = pic_path_var.get()
        
        frame = tk.Frame(window, bg='white', width=size, height=size, bd=0)
        frame.place(x=x_pos, y=y_pos)
        
        try:
            if pic_path and os.path.exists(pic_path):
                img_pil = Image.open(pic_path)
            else:
                img_pil = Image.new('RGB', (size, size), color = 'pink') 
                
            img_pil = img_pil.resize((size, size), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            PROFILE_PIC_REF['edit_pic'] = img_tk 
            
            pic_label = tk.Label(frame, image=img_tk, bd=0)
            pic_label.place(x=0, y=0, relwidth=1, relheight=1)
            return pic_label
        except Exception as e:
            print(f"Error loading profile picture: {e}")
            return tk.Label(frame, text="Load Error", fg="red").place(x=0, y=0, relwidth=1, relheight=1)

    # ฟังก์ชันสำหรับเลือกรูปโปรไฟล์
    def choose_profile_pic(pic_path_var, pic_label):
        file_path = filedialog.askopenfilename(title="เลือกรูปโปรไฟล์", 
                                               filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
        if file_path:
            pic_path_var.set(file_path)
            pic_label.destroy()
            display_profile_pic(edit_window, pic_path_var)

    # --- แสดง Entry Fields (ตำแหน่งคร่าวๆ อ้างอิงจากรูป) ---
    entry_font = ("Arial", 16)
    bg_color_entry = "#ffffff"
    bg_color_label = "#ffffff" 
    fg_color = "#552c1f"
    
    
    # 1. ชื่อ/นามสกุล (ตำแหน่งบรรทัดแรกของข้อมูล)
    # Entry ชื่อ
    tk.Entry(edit_window, textvariable=name_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=500, y=154, width=150, height=30)
    
    # Entry นามสกุล (วางติดกันทางขวาของชื่อ)
    tk.Entry(edit_window, textvariable=surname_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=690, y=154, width= 150, height=30)
    
    # 2. เบอร์โทร (ตำแหน่งบรรทัดที่สอง)
    tk.Entry(edit_window, textvariable=phone_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=450, y=220, width=150, height=30)
    
    # 3. วันเกิด (ตำแหน่งบรรทัดที่สาม)
    tk.Entry(edit_window, textvariable=birthday_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=430, y=280, width=130 , height= 30)
    
    # 4. Email (ตำแหน่งบรรทัดที่สี่)
    tk.Entry(edit_window, textvariable=email_var, font=entry_font, bg=bg_color_entry, bd=0).place(x=430, y=330, width=190, height=30)
    
    # 5. ชื่อผู้ใช้ (Entry ใต้รูปโปรไฟล์ - อนุญาตให้แก้ไข)
    username_entry = tk.Entry(edit_window, textvariable=username_var, font=entry_font, bg=bg_color_entry, bd=0)
    username_entry.place(x=170, y=350, width=100, height=30)
    

    # แสดงรูปโปรไฟล์ปัจจุบัน และปุ่มเปลี่ยน
    pic_label = display_profile_pic(edit_window, current_pic_path)
    
    # ปุ่ม 'เปลี่ยน' รูปโปรไฟล์
    change_pic_button = tk.Button(edit_window, text="เปลี่ยน", font=("UID SALMON 2019", 16, "bold"),
                                   bg="#ffffff", fg="#552c1f", bd=0, relief="flat",
                                   command=lambda: choose_profile_pic(current_pic_path, pic_label))
    change_pic_button.place(x=143, y=314, width=90, height=17)
    
    # ฟังก์ชันสำหรับบันทึก
    def save_changes():
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_var.get()):
            messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
            return
            
        new_data = {
            'username': username_var.get(), # ส่ง username ใหม่
            'name': name_var.get(),
            'surname': surname_var.get(),
            'phone': phone_var.get(),
            'birthday': birthday_var.get(),
            'email': email_var.get(),
            'pic_path': current_pic_path.get()
        }
        
        if update_user_profile(user_data['username'], new_data):
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            
            # ต้องส่ง user_data ที่อัปเดตแล้วไปหน้า view
            updated_user_data = get_user_data(CURRENT_USER) 
            profile_view_page(edit_window, updated_user_data) 

    # ปุ่ม Navigation
    
    # ปุ่มย้อนกลับ (ยกเลิกการแก้ไข)
    back_button = tk.Button(edit_window, text="ย้อนกลับ", font=("UID SALMON 2019", 40, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             command=lambda: profile_view_page(edit_window, user_data)) # กลับไปหน้า 5
    back_button.place(x=300, y=440, width=150, height=70) 

    # ปุ่มบันทึก
    save_button = tk.Button(edit_window, text="บันทึก", font=("UID SALMON 2019", 40, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             command=save_changes)
    save_button.place(x=525, y=440, width=150, height=70) 

    # ปุ่มผู้พัฒนา
    add_about_button(edit_window)


# ------------------------------------
# Main Pages (Login/Register) - อัปเดต open_next_page
# ------------------------------------

def open_next_page(current_window):
    """เปลี่ยนจากหน้า Login/Register ไปหน้าเลือกโต๊ะ (หน้าที่ 7)"""
    current_window.destroy()
    table_selection_page() # ไปหน้าเลือกโต๊ะ


# --- หน้าจอที่ 2: เข้าสู่ระบบ (Login) ---
def login_page():
    """ฟังก์ชันสำหรับหน้า 'เข้าสู่ระบบ'"""
    root.withdraw()
    
    login_window = tk.Toplevel(root)
    login_window.title("หนูดีส้มตำฟรุ้งฟริ้ง - เข้าสู่ระบบ")
    login_window.geometry("960x540")
    login_window.resizable(False, False)

    # กำหนดรูปภาพพื้นหลังสำหรับหน้า 'เข้าสู่ระบบ'
    try:
        bg_image_login_pil = Image.open("D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\2.png")
        bg_image_login_pil = bg_image_login_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_login = ImageTk.PhotoImage(bg_image_login_pil)
        background_label_login = tk.Label(login_window, image=bg_image_login)
        background_label_login.image = bg_image_login
        background_label_login.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("ไม่พบไฟล์รูปภาพ '2.png' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
        background_label_login = tk.Label(login_window, text="ไม่พบรูปภาพพื้นหลัง", font=("Arial", 24))
        background_label_login.pack(expand=True, fill="both")

    # สร้างช่องกรอกข้อมูล 'ชื่อผู้ใช้'
    username_entry = tk.Entry(login_window, font=("Arial", 28,"bold"),bg ="#fffbf2", bd=0, relief="flat")
    username_entry.place(x=315, y=240, width=320, height=45)
    
    # สร้างช่องกรอกข้อมูล 'รหัสผ่าน'
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 28,"bold"),bg ="#fffbf2" , bd=0, relief="flat")
    password_entry.place(x=315, y=320, width=320, height=45)

    # สร้างปุ่ม 'ย้อนกลับ'
    back_button = tk.Button(login_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#E3B2C3", command=lambda: back_to_main_page(login_window))
    back_button.place(x=280, y=420, width=150, height=50)

    # สร้างปุ่ม 'ยืนยัน'
    def local_verify_login():
        global CURRENT_USER
        user = username_entry.get()
        pwd = password_entry.get()
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = ? AND password = ?", (user, pwd))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            CURRENT_USER = user # บันทึกผู้ใช้ที่ล็อกอินสำเร็จ
            messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ!")
            open_next_page(login_window) # ไปหน้าเลือกโต๊ะ (หน้าที่ 7)
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3", 
                                 command=local_verify_login)
    confirm_button.place(x=540, y=420, width=150, height=50)
    
    # ปุ่มผู้พัฒนา (About Me)
    add_about_button(login_window)
    

# --- หน้าจอที่ 3: สมัครสมาชิก (Register) ---
def register_page():
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก'"""
    root.withdraw()
    
    register_window = tk.Toplevel(root)
    register_window.title("หนูดีส้มตำฟรุ้งฟริ้ง - สมัครสมาชิก")
    register_window.geometry("960x540")
    register_window.resizable(False, False)

    # กำหนดรูปภาพพื้นหลังสำหรับหน้า 'สมัครสมาชิก'
    try:
        bg_image_register_pil = Image.open("D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\3.png")
        bg_image_register_pil = bg_image_register_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_register = ImageTk.PhotoImage(bg_image_register_pil)
        background_label_register = tk.Label(register_window, image=bg_image_register)
        background_label_register.image = bg_image_register # เก็บ reference
        background_label_register.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("ไม่พบไฟล์รูปภาพ '3.png' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
        background_label_register = tk.Label(register_window, text="ไม่พบรูปภาพพื้นหลัง", font=("Arial", 24))
        background_label_register.pack(expand=True, fill="both")

    # สร้างช่องกรอกข้อมูลต่างๆ
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

    # สร้างปุ่ม 'ย้อนกลับ' และ 'ยืนยัน'
    back_button = tk.Button(register_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                             bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                             activebackground="#E3B2C3", command=lambda: back_to_main_page(register_window))
    back_button.place(x=285, y=420, width=150, height=50)

    def local_save_registration_data():
        user = username_entry.get()
        pwd = password_entry.get()
        name = name_entry.get()
        surname = surname_entry.get()
        phone = phone_entry.get()
        bday = birthday_entry.get()
        email = email_entry.get()

        if not all([user, pwd, name, surname, phone, bday, email]):
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        try:
            # บันทึกข้อมูล account
            cursor.execute("""
                INSERT INTO user_account (username, password, name, surname, phone, birthday, email) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user, pwd, name, surname, phone, bday, email))
            
            # บันทึกข้อมูล profile (คะแนนเริ่มต้น 0)
            cursor.execute("""
                INSERT INTO user_profile (username, score) VALUES (?, ?)
            """, (user, 0))
            
            conn.commit()
            messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ชื่อผู้ใช้: {user} \nตอนนี้คุณสามารถเข้าสู่ระบบได้แล้ว")
            back_to_main_page(register_window)
            
        except sqlite3.IntegrityError:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) นี้ถูกใช้ไปแล้ว")
            
        finally:
            conn.close()

    confirm_button = tk.Button(register_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3", 
                                 command=local_save_registration_data)
    confirm_button.place(x=535, y=420, width=150, height=50)

    # ปุ่มผู้พัฒนา (About ) ในหน้า Register ---
    add_about_button(register_window)


# --- สร้างหน้าต่างหลัก ---
root = tk.Tk()
root.title("หนูดีส้มตำฟรุ้งฟริ้ง")
root.geometry("960x540")
root.resizable(False, False)

# กำหนดรูปภาพพื้นหลัง
try:
    bg_image_pil = Image.open("D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\1.png")
    bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image_pil)
    background_label = tk.Label(root, image=bg_image)
    background_label.image = bg_image # เก็บ reference
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("ไม่พบไฟล์รูปภาพ '1.png' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
    background_label = tk.Label(root, text="ไม่พบรูปภาพพื้นหลัง", font=("Arial", 24))
    background_label.pack(expand=True, fill="both")

# สร้างปุ่ม 'เข้าสู่ระบบ'
login_button = tk.Button(root, text="เข้าสู่ระบบ", font=("UID SALMON 2019", 50, "bold"),
                         bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                         activebackground="#ffabcf", command=login_page)
login_button.place(x=685, y=235, width=180, height=85)

# สร้างปุ่ม 'สมัครสมาชิก'
register_button = tk.Button(root, text="สมัครสมาชิก", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffabcf", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#ffabcf", command=register_page)
register_button.place(x=685, y=343, width=180, height=85)

# --- ปุ่มผู้พัฒนา (About ) ในหน้าหลัก ---
add_about_button(root)


# เริ่มต้นการทำงานของโปรแกรม
root.mainloop()