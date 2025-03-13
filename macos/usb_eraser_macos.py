import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

def list_usb_drives():
    result = subprocess.run(["diskutil", "list", "external"], capture_output=True, text=True)
    return result.stdout

def secure_erase(disk, method, fs_type, apply_extra_security):
    if not disk:
        messagebox.showerror("Hata", "Lütfen bir USB seçin.")
        return
    
    confirm = messagebox.askyesno("Onay", f"{disk} sürücüsünü {method} yöntemiyle silmek istediğinize emin misiniz?")
    if not confirm:
        return
    
    progress_label.config(text="İşlem devam ediyor, lütfen bekleyin...")
    root.update()
    
    erase_command = ["diskutil", "secureErase"]
    if method == "Sıfırlarla Doldur":
        erase_command.append("0")
    elif method == "Rastgele Veri Yaz":
        erase_command.append("1")
    elif method == "Tam Güvenli Silme":
        erase_command.append("3")
    
    erase_command.append(disk)
    
    try:
        subprocess.run(erase_command, check=True)
        
        if apply_extra_security:
            messagebox.showinfo("Ekstra Güvenlik", "Ekstra güvenlik önlemleri uygulanıyor...")
            
            for i in range(3):
                subprocess.run(erase_command, check=True)
                progress_label.config(text=f"Ekstra güvenlik: {i+1}. geçiş tamamlandı...")
                root.update()
                
            subprocess.run(["diskutil", "zeroDisk", disk], check=True)
            messagebox.showinfo("Doğrulama", "Silme işlemi tamamlandı ve doğrulandı!")
        
        format_command = ["diskutil", "eraseDisk", fs_type, "USB", disk]
        subprocess.run(format_command, check=True)
        messagebox.showinfo("Tamamlandı", f"{disk} başarıyla güvenli şekilde silindi ve {fs_type} olarak biçimlendirildi.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Hata", "Disk silinirken hata oluştu.")
    
    progress_label.config(text="")

def update_drive_list():
    drive_list.delete(0, tk.END)
    drives = list_usb_drives()
    for line in drives.split("\n"):
        if "disk" in line:
            drive_list.insert(tk.END, line.strip())

def get_selected_drive():
    try:
        selected_text = drive_list.get(drive_list.curselection())
        return selected_text.split()[0]
    except:
        return None

root = tk.Tk()
root.title("Güvenli USB Silme - Mac/Linux")
root.geometry("500x500")

tk.Label(root, text="USB Sürücüleri:").pack()
drive_list = tk.Listbox(root)
drive_list.pack(fill=tk.BOTH, expand=True)
tk.Button(root, text="Listeyi Güncelle", command=update_drive_list).pack()

tk.Label(root, text="Silme Yöntemi:").pack()
method_var = tk.StringVar(value="Sıfırlarla Doldur")
methods = ["Sıfırlarla Doldur", "Rastgele Veri Yaz", "Tam Güvenli Silme"]
tk.OptionMenu(root, method_var, *methods).pack()

tk.Label(root, text="Dosya Sistemi:").pack()
fs_var = tk.StringVar(value="FAT32")
fs_options = ["FAT32", "exFAT", "APFS", "ext4"]
tk.OptionMenu(root, fs_var, *fs_options).pack()

tk.Label(root, text="Ekstra Güvenlik Önlemleri:").pack()
apply_extra_security_var = tk.BooleanVar()
tk.Checkbutton(root, text="Ekstra Güvenlik", variable=apply_extra_security_var).pack()

tk.Button(root, text="Silmeyi Başlat", command=lambda: secure_erase(get_selected_drive(), method_var.get(), fs_var.get(), apply_extra_security_var.get())).pack()

progress_label = tk.Label(root, text="")
progress_label.pack()

root.mainloop()
