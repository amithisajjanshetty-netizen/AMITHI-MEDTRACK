import customtkinter as ctk
import sqlite3
from datetime import datetime


DB_PATH = "database/data/medtrack.db"


class ReminderPopup(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        medicine_id,
        medicine_name,
        dosage,
        medicine_time,
        remaining_tablets
    ):
        super().__init__(parent)

        self.medicine_id = medicine_id
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.medicine_time = medicine_time
        self.remaining_tablets = remaining_tablets
        self.snooze_mintues=10

        self.title("💊 Medicine Reminder")
        self.geometry("400x380")
        self.resizable(False, False)

        # ---------- Title ----------
        ctk.CTkLabel(
            self,
            text="💊 MEDICINE REMINDER",
            font=("Arial", 24, "bold"),
            text_color="#1565C0"
        ).pack(pady=(25, 15))

        # ---------- Medicine Name ----------
        ctk.CTkLabel(
            self,
            text=self.medicine_name,
            font=("Arial", 22, "bold")
        ).pack(pady=5)

        # ---------- Dosage ----------
        ctk.CTkLabel(
            self,
            text=f"Dosage: {self.dosage}",
            font=("Arial", 16)
        ).pack(pady=5)

        # ---------- Time ----------
        ctk.CTkLabel(
            self,
            text=f"Time: {self.medicine_time}",
            font=("Arial", 15)
        ).pack(pady=3)

        # ---------- Remaining Tablets ----------
        ctk.CTkLabel(
            self,
            text=f"Remaining Tablets: {self.remaining_tablets}",
            font=("Arial", 15)
        ).pack(pady=3)

        # ---------- Take Now ----------
        ctk.CTkButton(
            self,
            text="💊 Take Now",
            width=220,
            height=45,
            command=self.take_now
        ).pack(pady=(20, 10))

        # ---------- Snooze ----------
        ctk.CTkButton(
            self,
            text="⏰ Snooze 10 Minutes",
            width=220,
            height=45,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=self.snooze
        ).pack()

    # ==========================================================
    # TAKE NOW
    # ==========================================================

    def take_now(self):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get current remaining tablet count
        cursor.execute(
            """
            SELECT remaining_tablets
            FROM medicines
            WHERE id=?
            """,
            (self.medicine_id,)
        )

        result = cursor.fetchone()

        if result is None:
            conn.close()
            print("Medicine not found")
            self.destroy()
            return

        remaining = result[0]

        # Prevent negative tablet count
        if remaining > 0:

            new_remaining = remaining - 1

            # Update medicine
            cursor.execute(
                """
                UPDATE medicines
                SET remaining_tablets=?,
                    status='🟢 Dose Logged'
                WHERE id=?
                """,
                (new_remaining, self.medicine_id)
            )

            # Add entry to History
            now = datetime.now()

            cursor.execute(
                """
                INSERT INTO history
                (medicine_name, dosage, date, time, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.medicine_name,
                    self.dosage,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%I:%M %p"),
                    "🟢 Dose Logged"
                )
            )

            conn.commit()

            print("Medicine taken successfully")
            print("Remaining tablets:", new_remaining)

        else:

            print("No tablets remaining")

        conn.close()

        self.destroy()

    # ==========================================================
    # SNOOZE
    # ==========================================================


    def snooze(self):

      print("Snooze clicked - reminder snoozed for 10 minutes")

    # Save the information before closing
      parent = self.master

      medicine_id = self.medicine_id
      medicine_name = self.medicine_name
      dosage = self.dosage
      medicine_time = self.medicine_time
      remaining_tablets = self.remaining_tablets

    # Close current popup
      self.destroy()

    # Show reminder again after 10 minutes
      parent.after(
          10  * 60* 1000,
        lambda: parent.show_reminder(
            medicine_id,
            medicine_name,
            dosage,
            medicine_time,
            remaining_tablets
        )
    )


    