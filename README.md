 # 💊 AMITHI MEDTRACK

### Smart Medicine Reminder System

AMITHI MEDTRACK is a Python-based desktop application designed to help users manage their medicines and never miss a scheduled dose.

> **Never Miss a Dose.**

---

## 🌟 Features

- 💊 Add and manage medicines
- ⏰ Schedule medicine reminders
- 🔔 Reminder notifications
- 📅 View today's medicine schedule
- 📋 View medicine history
- ✏️ Edit medicine details
- 🗑️ Delete medicines
- 📊 Track medicine status
- 🌓 Dark mode support
- 🔊 Reminder sound notifications
- 🖼️ Medicine image support

---

## 🛠️ Technologies Used

- **Python**
- **CustomTkinter** – Modern graphical user interface
- **SQLite** – Local database
- **Pillow (PIL)** – Image handling
- **Plyer** – Desktop notifications
- **Playsound** – Reminder sounds

---

## 📂 Project Structure

```text
AMITHI MEDTRACK/
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── sounds/
│       └── reminder.wav
│
├── database/
│   └── data/
│
├── modules/
│   ├── database.py
│   ├── medicine.py
│   └── reminder.py
│
├── ui/
│   ├── add_medicine.py
│   ├── dashboard.py
│   ├── edit_medicine.py
│   ├── history.py
│   ├── login.py
│   ├── reminder_popup.py
│   ├── settings.py
│   ├── splash_screen.py
│   ├── today_schedule.py
│   └── view_medicines.py
│
├── main.py
├── README.md
└── .gitignore