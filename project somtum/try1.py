import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def login_page():
    """ฟังก์ชันสำหรับหน้า 'เข้าสู่ระบบ'"""
    print("ไปยังหน้า 'เข้าสู่ระบบ'")
    # โค้ดสำหรับหน้า 'เข้าสู่ระบบ' จะถูกเพิ่มที่นี่ในภายหลัง

def register_page():
    """ฟังก์ชันสำหรับหน้า 'สมัครสมาชิก'"""
    print("ไปยังหน้า 'สมัครสมาชิก'")
    # โค้ดสำหรับหน้า 'สมัครสมาชิก' จะถูกเพิ่มที่นี่ในภายหลัง

def about_page():
    """ฟังก์ชันสำหรับหน้าผู้พัฒนาโปรแกรม"""
    print("ไปยังหน้า 'ผู้พัฒนาโปรแกรม'")
    # โค้ดสำหรับหน้า 'ผู้พัฒนาโปรแกรม' จะถูกเพิ่มที่นี่ในภายหลัง

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("หนูดีส้มตำฟรุ้งฟริ้ง")
root.geometry("960x540")
root.resizable(False, False) # ป้องกันไม่ให้ผู้ใช้ปรับขนาดหน้าต่าง

# กำหนดรูปภาพพื้นหลัง
try:
    bg_image_pil = Image.open("D:\\ส้มตำฟรุ้งฟริ้ง\\picnudee\\1.png")
    bg_image_pil = bg_image_pil.resize((960, 540), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image_pil)

    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("ไม่พบไฟล์รูปภาพ '1.jpg' กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
    background_label = tk.Label(root, text="ไม่พบรูปภาพพื้นหลัง", font=("Arial", 24))
    background_label.pack(expand=True, fill="both")

# สร้างปุ่ม 'เข้าสู่ระบบ'
login_button = tk.Button(root, text="เข้าสู่ระบบ", font=(("UID SALMON 2019", 32, "bold")),
                         bg="#fe76b0", fg="white", bd=0, relief="flat",
                         activebackground="#ffabcf", command=login_page)
login_button.place(x=680, y=230, width=200, height=80)

# สร้างปุ่ม 'สมัครสมาชิก'
register_button = tk.Button(root, text="สมัครสมาชิก", font=("Arial", 28, "bold"),
                            bg="#fe76b0", fg="white", bd=0, relief="flat",
                            activebackground="#ffabcf", command=register_page)
register_button.place(x=680, y=330, width=200, height=80)



# เริ่มต้นการทำงานของโปรแกรม
root.mainloop()