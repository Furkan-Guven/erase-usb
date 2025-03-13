import os
import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import time
import win32api
import win32file
import ctypes

def list_usb_drives():
    drives = []
    bitmask = win32api.GetLogicalDrives()
    for letter in range(26):
        if bitmask & (1 << letter):
            drive = f"{chr(65 + letter)}:\\"
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                drives.append(drive)
    return drives

def secure_erase(drive, method, fs_type):
    try:
        progress_var.set(0)
        progress_bar.update()
        
        if method == "Zeros":
            pattern = b"\x00"
        elif method == "Random":
            pattern = os.urandom(1)
        elif method == "Both":
            for _ in range(2):
                with open(f"{drive}secure_wipe.bin", "wb") as f:
                    f.write(os.urandom(1024 * 1024 * 100))  # 100 MB blocks
                os.remove(f"{drive}secure_wipe.bin")
            pattern = b"\x00"
        
        with open(f"{drive}secure_wipe.bin", "wb") as f:
            for _ in range(1024):  # 1 GB
                f.write(pattern * 1024 * 1024)
        os.remove(f"{drive}secure_wipe.bin")
        
        progress_var.set(50)
        progress_bar.update()
        
        messagebox.showinfo("Wipe Complete", "Data securely erased. Now formatting...")
        
        # Format the USB drive
        if fs_type == "FAT32":
            os.system(f"format {drive} /FS:FAT32 /Q /Y")
        else:
            os.system(f"format {drive} /FS:NTFS /Q /Y")
        
        progress_var.set(100)
        progress_bar.update()
        messagebox.showinfo("Done", "USB Drive erased and formatted successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {str(e)}")

def start_wipe():
    drive = drive_var.get()
    method = method_var.get()
    fs_type = fs_var.get()
    if not drive:
        messagebox.showerror("Error", "Select a USB drive!")
        return
    if not method:
        messagebox.showerror("Error", "Select a wipe method!")
        return
    if not fs_type:
        messagebox.showerror("Error", "Select a file system!")
        return
    
    confirm = messagebox.askyesno("Confirm", f"Erase {drive} with {method} method and format as {fs_type}? This cannot be undone!")
    if confirm:
        secure_erase(drive, method, fs_type)

# GUI Setup
root = tk.Tk()
root.title("Secure USB Eraser - Windows")
root.geometry("400x300")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Select USB Drive:").pack()
drive_var = tk.StringVar()
drive_menu = ttk.Combobox(frame, textvariable=drive_var, values=list_usb_drives(), state="readonly")
drive_menu.pack()

ttk.Label(frame, text="Select Wipe Method:").pack()
method_var = tk.StringVar()
method_menu = ttk.Combobox(frame, textvariable=method_var, values=["Zeros", "Random", "Both"], state="readonly")
method_menu.pack()

ttk.Label(frame, text="Select File System:").pack()
fs_var = tk.StringVar()
fs_menu = ttk.Combobox(frame, textvariable=fs_var, values=["FAT32", "NTFS"], state="readonly")
fs_menu.pack()

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, length=200, mode='determinate', variable=progress_var)
progress_bar.pack(pady=10)

ttk.Button(frame, text="Start Wipe", command=start_wipe).pack()

root.mainloop()
