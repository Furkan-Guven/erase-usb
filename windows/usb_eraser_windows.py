import os
import tkinter as tk
from tkinter import ttk, messagebox
import win32api
import win32file
import random
import time

def list_usb_drives():
    """USB sürücülerini listeler."""
    drives = []
    bitmask = win32api.GetLogicalDrives()
    for letter in range(26):
        if bitmask & (1 << letter):
            drive = f"{chr(65 + letter)}:\\"
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                drives.append(drive)
    return drives

def write_pattern(drive, pattern, passes=1):
    """Belirtilen deseni sürücüye belirli sayıda yazar."""
    try:
        for _ in range(passes):
            with open(f"{drive}secure_wipe.bin", "wb") as f:
                for _ in range(1024):  # 1GB bloklar halinde yazma
                    f.write(pattern * 1024 * 1024)
            os.remove(f"{drive}secure_wipe.bin")
    except Exception as e:
        messagebox.showerror("Hata", f"Yazma hatası: {str(e)}")

def secure_erase(drive, method, extra_security, fs_type):
    try:
        progress_var.set(0)
        progress_bar.update()
        
        # Kullanıcının seçtiği silme yöntemi
        if method == "Zeros":
            write_pattern(drive, b"\x00", 1)
        elif method == "Random":
            write_pattern(drive, os.urandom(1), 1)
        elif method == "Both":
            write_pattern(drive, os.urandom(1), 1)
            write_pattern(drive, b"\x00", 1)
        
        progress_var.set(50)
        progress_bar.update()
        
        # Ekstra güvenlik önlemleri
        if extra_security:
            write_pattern(drive, os.urandom(1), 3)  # 3 geçişli ekstra silme
            
            # Yazma doğrulama testi
            try:
                with open(f"{drive}verify_check.bin", "rb") as f:
                    data = f.read(1024 * 1024)  # İlk 1MB kontrolü
                    if all(b == 0 for b in data):
                        messagebox.showinfo("Doğrulama", "Silme işlemi başarıyla doğrulandı!")
                    else:
                        messagebox.showwarning("Doğrulama", "Silme doğrulama başarısız!")
                os.remove(f"{drive}verify_check.bin")
            except Exception as e:
                messagebox.showerror("Doğrulama Hatası", f"{str(e)}")
        
        messagebox.showinfo("Format", "Veri güvenli şekilde silindi, şimdi format atılıyor...")
        os.system(f"format {drive} /FS:{fs_type} /Q /Y")
        
        progress_var.set(100)
        progress_bar.update()
        messagebox.showinfo("Tamamlandı", "USB başarıyla silindi ve formatlandı!")
        
    except Exception as e:
        messagebox.showerror("Hata", f"İşlem başarısız: {str(e)}")

def start_wipe():
    drive = drive_var.get()
    method = method_var.get()
    fs_type = fs_var.get()
    extra_security = extra_security_var.get()
    
    if not drive:
        messagebox.showerror("Hata", "Lütfen bir USB seçin!")
        return
    if not method:
        messagebox.showerror("Hata", "Silme yöntemini seçin!")
        return
    if not fs_type:
        messagebox.showerror("Hata", "Dosya sistemini seçin!")
        return
    
    confirm = messagebox.askyesno("Onay", f"{drive} sürücüsünü {method} yöntemiyle silmek ve {fs_type} olarak biçimlendirmek istediğinize emin misiniz?\nEkstra güvenlik: {bool(extra_security)}")
    if confirm:
        secure_erase(drive, method, extra_security, fs_type)

# GUI Tanımlama
root = tk.Tk()
root.title("Güvenli USB Silici - Windows")
root.geometry("400x350")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="USB Sürücüsünü Seçin:").pack()
drive_var = tk.StringVar()
drive_menu = ttk.Combobox(frame, textvariable=drive_var, values=list_usb_drives(), state="readonly")
drive_menu.pack()

ttk.Label(frame, text="Silme Yöntemini Seçin:").pack()
method_var = tk.StringVar()
method_menu = ttk.Combobox(frame, textvariable=method_var, values=["Zeros", "Random", "Both"], state="readonly")
method_menu.pack()

ttk.Label(frame, text="Dosya Sistemi Seçin:").pack()
fs_var = tk.StringVar()
fs_menu = ttk.Combobox(frame, textvariable=fs_var, values=["FAT32", "NTFS"], state="readonly")
fs_menu.pack()

ttk.Label(frame, text="Ekstra Güvenlik:").pack()
extra_security_var = tk.IntVar()
extra_security_check = ttk.Checkbutton(frame, text="Ekstra Güvenliği Etkinleştir", variable=extra_security_var)
extra_security_check.pack()

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, length=200, mode='determinate', variable=progress_var)
progress_bar.pack(pady=10)

ttk.Button(frame, text="Silme İşlemini Başlat", command=start_wipe).pack()

root.mainloop()
