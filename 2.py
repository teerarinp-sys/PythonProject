import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# --- ส่วนของฟังก์ชัน ---
def login_page():
    """ฟังก์ชันสำหรับหน้า 'เข้าสู่ระบบ'"""
    # ซ่อนหน้าต่างหลัก
    root.withdraw()
    
    # สร้างหน้าต่างสำหรับ 'เข้าสู่ระบบ'
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
        print("ไม่พบไฟล์รูปภาพ '2.jpg' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
        background_label_login = tk.Label(login_window, text="ไม่พบรูปภาพพื้นหลัง", font=("Arial", 24))
        background_label_login.pack(expand=True, fill="both")

    # สร้างช่องกรอกข้อมูล 'ชื่อผู้ใช้'
    username_entry = tk.Entry(login_window, font=("Arial", 16),bg ="#fffbf2", bd=0, relief="flat")
    username_entry.place(x=315, y=240, width=320, height=45) 
    
    # สร้างช่องกรอกข้อมูล 'รหัสผ่าน'
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 16),bg ="#fffbf2" , bd=0, relief="flat")
    password_entry.place(x=315, y=320, width=320, height=45) 

    # สร้างปุ่ม 'ย้อนกลับ'
    back_button = tk.Button(login_window, text="ย้อนกลับ", font=("UID SALMON 2019", 50, "bold"),
                            bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                            activebackground="#E3B2C3", command=lambda: back_to_main_page(login_window))
    back_button.place(x=280, y=42, width=150, height=50) 

    # สร้างปุ่ม 'ยืนยัน'
    confirm_button = tk.Button(login_window, text="ยืนยัน", font=("UID SALMON 2019", 50, "bold"),
                               bg="#ffe0f1", fg="#552c1f", bd=0, relief="flat",
                               activebackground="#E3B2C3", command=verify_login)
    confirm_button.place(x=540, y=420, width=150, height=50) 

def register_page():
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก'"""
    print("ไปยังหน้า 'สมัครสมาชิก'")

def back_to_main_page(current_window):
    """ฟังก์ชันสำหรับกลับไปหน้าหลัก"""
    current_window.destroy() # ปิดหน้าต่างปัจจุบัน
    root.deiconify() # แสดงหน้าต่างหลัก

def verify_login():
    """ฟังก์ชันสำหรับตรวจสอบข้อมูลการเข้าสู่ระบบ"""
    print("ตรวจสอบข้อมูล")
    # ส่วนนี้จะเพิ่มโค้ดการตรวจสอบในภายหลัง

def about_page():
    """ฟังก์ชันสำหรับหน้าผู้พัฒนาโปรแกรม"""
    print("ไปยังหน้า 'ผู้พัฒนาโปรแกรม'")

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

# เริ่มต้นการทำงานของโปรแกรม
root.mainloop()