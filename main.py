import os
import sys
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import librosa
import numpy as np

# ตั้งค่าเริ่มต้น
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    return "ffmpeg"

class BPMConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Studio BPM Master Pro v3")
        self.geometry("950x700")

        self.file_paths = []
        self.output_folder = "ยังไม่ได้เลือก..."

        # --- Header & Theme Selector ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=15, padx=20, fill="x")

        self.label = ctk.CTkLabel(self.header_frame, text="Studio BPM Converter", font=("Helvetica", 24, "bold"))
        self.label.pack(side="left")

        self.theme_switch = ctk.CTkSegmentedButton(self.header_frame, values=["Dark", "Light"], 
                                                   command=self.change_theme)
        self.theme_switch.set("Dark")
        self.theme_switch.pack(side="right")

        # --- Control Frame ---
        self.ctrl_frame = ctk.CTkFrame(self)
        self.ctrl_frame.pack(pady=10, padx=20, fill="x")

        self.btn_select = ctk.CTkButton(self.ctrl_frame, text="1. เพิ่มไฟล์ MP3", command=self.select_files)
        self.btn_select.grid(row=0, column=0, padx=10, pady=15)

        self.btn_clear = ctk.CTkButton(self.ctrl_frame, text="ล้างรายการ", command=self.clear_files, fg_color="#8B0000", hover_color="#660000")
        self.btn_clear.grid(row=0, column=1, padx=10)

        self.target_bpm_entry = ctk.CTkEntry(self.ctrl_frame, placeholder_text="Target BPM (เช่น 128)", width=150)
        self.target_bpm_entry.grid(row=0, column=2, padx=10)

        self.btn_folder = ctk.CTkButton(self.ctrl_frame, text="2. เลือกปลายทาง", command=self.select_folder, fg_color="#5D3FD3")
        self.btn_folder.grid(row=0, column=3, padx=10)

        # --- Destination Path Label ---
        self.path_display_frame = ctk.CTkFrame(self, height=35)
        self.path_display_frame.pack(pady=5, padx=20, fill="x")
        self.path_label = ctk.CTkLabel(self.path_display_frame, text=f"ปลายทาง: {self.output_folder}", font=("Helvetica", 11))
        self.path_label.pack(side="left", padx=10)

        # --- Table ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("filename", "orig_bpm", "status"), show="headings")
        self.tree.heading("filename", text="ชื่อไฟล์")
        self.tree.heading("orig_bpm", text="BPM เดิม")
        self.tree.heading("status", text="สถานะ")
        self.tree.column("filename", width=450)
        self.tree.column("orig_bpm", width=100, anchor="center")
        self.tree.column("status", width=200, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # --- Progress Section ---
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(pady=10, padx=20, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=10)

        self.percent_label = ctk.CTkLabel(self.progress_frame, text="0%", width=50)
        self.percent_label.pack(side="right")

        self.btn_convert = ctk.CTkButton(self, text="เริ่มแปลงไฟล์ทั้งหมด (Multi-Task)", 
                                         height=50, font=("Helvetica", 16, "bold"),
                                         fg_color="green", command=self.start_conversion)
        self.btn_convert.pack(pady=20)

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio files", "*.mp3")])
        if files:
            for f in files:
                if f not in self.file_paths:
                    self.file_paths.append(f)
                    self.tree.insert("", tk.END, iid=f, values=(os.path.basename(f), "รอวิเคราะห์...", "พร้อม"))

    def clear_files(self):
        self.file_paths = []
        for i in self.tree.get_children(): self.tree.delete(i)
        self.progress_bar.set(0)
        self.percent_label.configure(text="0%")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.path_label.configure(text=f"ปลายทาง: {self.output_folder}")

    def process_audio(self, input_path, target_bpm):
        try:
            # ใช้ Logic การดึง BPM แบบที่เคยผ่าน (ตรวจสอบประเภทตัวแปรให้ชัวร์)
            y, sr = librosa.load(input_path, sr=None, duration=60)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # แปลงเป็น float ไม่ว่าจะเป็น array หรือ scalar
            current_bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
            
            self.after(0, lambda: self.tree.item(input_path, values=(os.path.basename(input_path), f"{current_bpm:.1f}", "กำลังแปลง...")))
            
            ratio = float(target_bpm) / current_bpm
            out_name = f"Studio_{target_bpm}BPM_{os.path.basename(input_path)}"
            out_path = os.path.join(self.output_folder, out_name)
            
            cmd = [get_ffmpeg_path(), "-y", "-i", input_path, "-filter:a", f"atempo={ratio}", "-b:a", "320k", out_path]
            subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.after(0, lambda: self.tree.item(input_path, values=(os.path.basename(input_path), f"{current_bpm:.1f}", "✅ สำเร็จ")))
        except Exception as e:
            print(f"Error: {e}")
            self.after(0, lambda: self.tree.item(input_path, values=(os.path.basename(input_path), "Error", "❌ ล้มเหลว")))

    def start_conversion(self):
        target = self.target_bpm_entry.get()
        if not self.file_paths or self.output_folder == "ยังไม่ได้เลือก..." or not target:
            messagebox.showwarning("เตือน", "กรุณาตั้งค่าให้ครบถ้วน")
            return

        self.btn_convert.configure(state="disabled")
        
        def run():
            total = len(self.file_paths)
            with ThreadPoolExecutor(max_workers=4) as exe:
                futures = [exe.submit(self.process_audio, f, target) for f in self.file_paths]
                for i, future in enumerate(futures):
                    future.result() # รอให้แต่ละ task เสร็จ
                    p = (i + 1) / total
                    # แก้ไข Error .after() โดยใช้ lambda
                    self.after(0, lambda val=p: self.progress_bar.set(val))
                    self.after(0, lambda val=p: self.percent_label.configure(text=f"{int(val*100)}%"))
            
            self.after(0, lambda: [self.btn_convert.configure(state="normal"), messagebox.showinfo("เสร็จสิ้น", "แปลงไฟล์ทั้งหมดเรียบร้อยแล้ว!")])

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    app = BPMConverterApp()
    app.mainloop()
