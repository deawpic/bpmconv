# 🎵 Studio BPM Master Pro (Multi-Core)

เครื่องมือจัดการความเร็วเพลง (BPM) คุณภาพระดับสตูดิโอ พัฒนาด้วย Python รองรับการทำงานแบบขนาน (Parallel Processing) โดยไม่เสียคุณภาพเสียง

---

## ✨ คุณสมบัติหลัก (Key Features)

- 🎧 **Studio Quality:** ใช้เทคโนโลยี `atempo` จาก FFmpeg รักษาค่า Pitch และคุณภาพเสียงดั้งเดิม
- 🤖 **Auto Detection:** วิเคราะห์ค่า BPM เดิมของเพลงโดยอัตโนมัติด้วย `Librosa`
- ⚡ **Multi-Tasking:** ระบบประมวลผลแบบขนาน (Parallel Processing) สูงสุด 4 ไฟล์พร้อมกัน
- 🎨 **Modern UI:** หน้าตาโปรแกรมทันสมัย รองรับโหมด **Dark / Light**
- 📂 **Destination Display:** แสดงโฟลเดอร์ปลายทางชัดเจนตลอดเวลา

---

## 🛠 การติดตั้ง (Installation)

### 1. ติดตั้งไลบรารี
```bash
pip install customtkinter librosa numpy soundfile
```

### 2. เตรียมโปรแกรมเสริม
ดาวน์โหลด ffmpeg.exe จาก FFmpeg.org
นำไฟล์ ffmpeg.exe มาวางไว้ที่ Root Directory (โฟลเดอร์เดียวกับไฟล์โค้ด)

---

### 🚀 วิธีใช้งาน (Usage)
1. เปิดโปรแกรม:   python main.py
2. เลือกเพลง: กดปุ่ม "1. เพิ่มไฟล์ MP3" (เลือกหลายไฟล์ได้พร้อมกัน)
3. ตั้งค่า: ระบุ Target BPM ที่ต้องการในช่องกรอกข้อมูล
4. เลือกที่เก็บ: กดปุ่ม "2. เลือกปลายทาง" เพื่อกำหนดโฟลเดอร์สำหรับไฟล์ใหม่
5. เริ่มทำงาน: กดปุ่ม "เริ่มแปลงไฟล์ทั้งหมด" และรอรับไฟล์ที่เสร็จสมบูรณ์

---

### 📦 การสร้างไฟล์ EXE (Standalone Build)
คุณสามารถรวมโปรแกรมเป็นไฟล์ EXE เพียงไฟล์เดียว (มี FFmpeg ในตัว) ด้วยคำสั่ง:
```bash
pyinstaller --noconsole --onefile \
--add-data "ffmpeg.exe;." \
--collect-all customtkinter \
--collect-all librosa \
main.py
```
---
![Main App](Screenshot1png)
