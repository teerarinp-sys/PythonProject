import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import sqlite3
import re # สำหรับตรวจสอบรูปแบบ Email

# --- การตั้งค่าฐานข้อมูล SQLite ---
DB_NAME = "user_data.db"

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

def create_db_table():
    """สร้างฐานข้อมูลและตาราง user_account หากยังไม่มี และเพิ่มผู้ใช้เริ่มต้น"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # สร้างตาราง user_account (username ต้องไม่ซ้ำ)
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
        
        # เพิ่มผู้ใช้เริ่มต้น 'admin:123'
        try:
            cursor.execute("INSERT OR IGNORE INTO user_account (username, password, name) VALUES (?, ?, ?)", 
                           ('admin', '123', 'ผู้ดูแลระบบ'))
            conn.commit()
            print(">>> ข้อมูลผู้ใช้เริ่มต้น 'admin:123' ถูกตรวจสอบ/เพิ่มในฐานข้อมูลแล้ว")
        except sqlite3.IntegrityError:
             pass 
        
    except sqlite3.Error as e:
        messagebox.showerror("ข้อผิดพลาดฐานข้อมูล", f"ไม่สามารถสร้างฐานข้อมูลได้: {e}")

# เรียกใช้ฟังก์ชันสร้างฐานข้อมูลเมื่อโปรแกรมเริ่มต้น
create_db_table()
# ------------------------------------


# --- ส่วนของฟังก์ชัน ---

def back_to_main_page(current_window):
    """ฟังก์ชันสำหรับกลับไปหน้าหลัก"""
    current_window.destroy()
    root.deiconify()

def open_next_page(current_window):
    """ฟังก์ชันจำลอง: ไปยังหน้าถัดไปหลังจาก Login สำเร็จ (เช่น หน้าเมนูอาหาร)"""
    current_window.destroy()
    messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ! \n(จะนำไปยังหน้าเมนูอาหารในขั้นตอนถัดไป)")
    root.deiconify() 

def verify_login(login_window, username_entry, password_entry):
    """ฟังก์ชันสำหรับตรวจสอบข้อมูลการเข้าสู่ระบบกับฐานข้อมูล SQLite"""
    user = username_entry.get()
    pwd = password_entry.get()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # ตรวจสอบว่ามี username และ password ตรงกันหรือไม่
    cursor.execute("SELECT * FROM user_account WHERE username = ? AND password = ?", (user, pwd))
    record = cursor.fetchone()
    conn.close()
    
    if record:
        messagebox.showinfo("สำเร็จ", "เข้าสู่ระบบสำเร็จ!")
        open_next_page(login_window) # ไปหน้าถัดไป
    else:
        # แสดงข้อความเตือนตามที่ระบุในโจทย์
        messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        username_entry.delete(0, tk.END) # ล้างช่องกรอก
        password_entry.delete(0, tk.END)

def save_registration_data(register_window, username_entry, password_entry, name_entry, surname_entry, phone_entry, birthday_entry, email_entry):
    """ฟังก์ชันสำหรับบันทึกข้อมูลการสมัครสมาชิกไปยังฐานข้อมูล SQLite"""
    user = username_entry.get()
    pwd = password_entry.get()
    name = name_entry.get()
    surname = surname_entry.get()
    phone = phone_entry.get()
    bday = birthday_entry.get()
    email = email_entry.get()

    # ตรวจสอบว่ามีช่องว่างหรือไม่
    if not all([user, pwd, name, surname, phone, bday, email]):
        messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        return
    
    # ตรวจสอบรูปแบบ Email (อย่างง่าย)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # บันทึกข้อมูลลงในฐานข้อมูล
        cursor.execute("""
            INSERT INTO user_account (username, password, name, surname, phone, birthday, email) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user, pwd, name, surname, phone, bday, email))
        
        conn.commit()
        messagebox.showinfo("สำเร็จ", f"สมัครสมาชิกสำเร็จ! ชื่อผู้ใช้: {user} \nตอนนี้คุณสามารถเข้าสู่ระบบได้แล้ว")
        back_to_main_page(register_window)
        
    except sqlite3.IntegrityError:
        # ดักจับกรณี username ซ้ำ (UNIQUE constraint)
        messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้ (Username) นี้ถูกใช้ไปแล้ว")
        
    finally:
        conn.close()

# --- ฟังก์ชันรวมสำหรับสร้างปุ่มผู้พัฒนา ---
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


# --- หน้าจอที่ 4: ผู้พัฒนาโปรแกรม (About Me) ---
global bg_image_about
bg_image_about = None 

def about_page():
    """ฟังก์ชันสำหรับแสดงหน้า 'ผู้พัฒนาโปรแกรม' (About)"""
    root.withdraw()
    
    about_window = tk.Toplevel(root)
    about_window.title("หนูดีส้มตำฟรุ้งฟริ้ง - ผู้พัฒนาโปรแกรม")
    about_window.geometry("960x540")
    about_window.resizable(False, False)

    global bg_image_about
    # โหลดรูปภาพ about 
    try:
        # สมมติว่าไฟล์รูปภาพ 'about.png' ถูกบันทึกไว้ใน D:\ส้มตำฟรุ้งฟริ้ง\picnudee\
        bg_image_about_pil = Image.open("D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\about.png")
        bg_image_about_pil = bg_image_about_pil.resize((960, 540), Image.Resampling.LANCZOS)
        bg_image_about = ImageTk.PhotoImage(bg_image_about_pil)
        
        background_label_about = tk.Label(about_window, image=bg_image_about)
        background_label_about.image = bg_image_about # เก็บ reference
        background_label_about.place(x=0, y=0, relwidth=1, relheight=1)
        
        # เพิ่มปุ่ม 'ย้อนกลับ' บนรูปภาพ 
        back_button = tk.Button(about_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50 , "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="raised", 
                                 activebackground="#ffe0f1", 
                                 command=lambda: back_to_main_page(about_window))
        back_button.place(x=790, y=470, width=150, height=45) 
        
    except FileNotFoundError:
        print("ไม่พบไฟล์รูปภาพ 'about.png' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
        background_label_about = tk.Label(about_window, text="ไม่พบรูปภาพผู้พัฒนา", font=("Arial", 24))
        background_label_about.pack(expand=True, fill="both")
        
        # ถ้าหารูปไม่เจอ ให้สร้างปุ่มย้อนกลับแบบธรรมดา
        back_button = tk.Button(about_window, text="ย้อนกลับ", command=lambda: back_to_main_page(about_window))
        back_button.pack(pady=20)


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
    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3", 
                                 command=lambda: verify_login(login_window, username_entry, password_entry))
    confirm_button.place(x=540, y=420, width=150, height=50)
    
    # --- ปุ่มผู้พัฒนา (About Me) ในหน้า Login ---
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

    # อัปเดต command ให้เรียกใช้ save_registration_data พร้อมส่ง entry widgets เข้าไป
    confirm_button = tk.Button(register_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                                 bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                                 activebackground="#E3B2C3", 
                                 command=lambda: save_registration_data(register_window, username_entry, password_entry, name_entry, surname_entry, phone_entry, birthday_entry, email_entry))
    confirm_button.place(x=535, y=420, width=150, height=50)

    # --- ปุ่มผู้พัฒนา (About ) ในหน้า Register ---
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