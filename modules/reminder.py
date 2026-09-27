import sqlite3
import time
from datetime import datetime
from plyer import notification
from playsound import playsound

sent_reminders = set()

DB_PATH = "database/data/medtrack.db"


def start_reminders(dashboard):

    print("reminder thread started")

    while True:

        now = datetime.now().strftime("%I:%M %p")
        print("checking:", now)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, dosage, time, remaining_tablets
            FROM medicines
            WHERE time=?
        """, (now,))

        medicines = cursor.fetchall()

        print("medicine found:", medicines)

        conn.close()

        for medicine in medicines:

            medicine_id = medicine[0]
            medicine_name = medicine[1]
            dosage = medicine[2]
            medicine_time = medicine[3]
            remaining_tablets = medicine[4]

            key = (medicine_id, now)

            if key not in sent_reminders:

                notification.notify(
                    title="AMITHI MEDTRACK",
                    message=f"{medicine_name}\nDosage: {dosage}",
                    timeout=10
                )

                try:
                    playsound("assets/sounds/reminder.wav")
                except Exception as e:
                    print("Sound error:", e)

                dashboard.after(
                    0,
                    dashboard.show_reminder,
                    medicine_id,
                    medicine_name,
                    dosage,
                    medicine_time,
                    remaining_tablets
                )

                sent_reminders.add(key)

        time.sleep(60)
