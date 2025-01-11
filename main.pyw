import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil

# ドライブを検出する関数
def detect_drives():
    drives = []
    for drive in range(ord('D'), ord('Z') + 1):
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

# コピー先フォルダを選択する関数
def select_destination_folder():
    dest_folder = filedialog.askdirectory()
    if dest_folder:
        destination_label.config(text=f"コピー先フォルダ: {dest_folder}")
        destination_label.dest_folder = dest_folder

# コピー元ドライブとコピー先フォルダを選択してコピーする関数
def copy_dcim():
    src_drive = drive_combobox.get()
    dest_folder = getattr(destination_label, 'dest_folder', '')
    if not src_drive or not dest_folder:
        messagebox.showerror("エラー", "コピー元ドライブとコピー先フォルダを選択してください。")
        return
    
    src_dcim = os.path.join(src_drive, "DCIM")
    if not os.path.exists(src_dcim):
        messagebox.showerror("エラー", f"{src_drive}にDCIMフォルダが見つかりません。")
        return

    try:
        for item in os.listdir(src_dcim):
            src_item = os.path.join(src_dcim, item)
            dest_item = os.path.join(dest_folder, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item)
            else:
                shutil.copy2(src_item, dest_item)
        messagebox.showinfo("成功", "DCIMフォルダの中身のコピーが完了しました。")
    except Exception as e:
        messagebox.showerror("エラー", f"コピー中にエラーが発生しました: {e}")

# メインウィンドウの設定
root = tk.Tk()
root.title("DCIMフォルダコピーアプリ")
root.geometry("400x250")

# ドライブ選択用のラベルとコンボボックス
drive_label = tk.Label(root, text="コピー元ドライブ:")
drive_label.pack(pady=10)

drive_combobox = ttk.Combobox(root, values=detect_drives())
drive_combobox.pack(pady=10)

# コピー先フォルダ選択ボタンとラベル
destination_button = tk.Button(root, text="コピー先フォルダを選択", command=select_destination_folder)
destination_button.pack(pady=10)

destination_label = tk.Label(root, text="コピー先フォルダ: 未選択")
destination_label.pack(pady=10)

# コピー実行ボタン
copy_button = tk.Button(root, text="コピー", command=copy_dcim)
copy_button.pack(pady=20)

# メインループの開始
root.mainloop()
