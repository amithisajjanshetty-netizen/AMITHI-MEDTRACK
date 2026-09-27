import customtkinter as ctk
import sqlite3


DB_PATH = "database/data/medtrack.db"


class EditMedicine(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        medicine_id,
        name,
        dosage,
        time,
        frequency,
        total_tablets,
        remaining_tablets
    ):
        super().__init__(parent)

        print("edit window created")

        self.medicine_id = medicine_id

        self.title("AMITHI MEDTRACK - Edit Medicine")
        self.geometry("450x600")
        self.resizable(False, False)

        # ---------- Title ----------
        ctk.CTkLabel(
            self,
            text="✏️ Edit Medicine",
            font=("Arial", 24, "bold"),
            text_color="#1565C0"
        ).pack(pady=(20, 15))

        # ---------- Medicine Name ----------
        self.name = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Medicine Name"
        )
        self.name.insert(0, name)
        self.name.pack(pady=8)

        # ---------- Dosage ----------
        self.dosage = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Dosage"
        )
        self.dosage.insert(0, dosage)
        self.dosage.pack(pady=8)

        # ---------- Time ----------
        self.time = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Time (example: 08:12 PM)"
        )
        self.time.insert(0, time)
        self.time.pack(pady=8)

        # ---------- Frequency ----------
        self.frequency = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Frequency"
        )
        self.frequency.insert(0, frequency)
        self.frequency.pack(pady=8)

        # ---------- Total Tablets ----------
        self.total_tablets = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Total Tablets"
        )
        self.total_tablets.insert(0, str(total_tablets))
        self.total_tablets.pack(pady=8)

        # ---------- Remaining Tablets ----------
        self.remaining_tablets = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Remaining Tablets"
        )
        self.remaining_tablets.insert(0, str(remaining_tablets))
        self.remaining_tablets.pack(pady=8)

        # ---------- Update Button ----------
        ctk.CTkButton(
            self,
            text="💾 Update Medicine",
            width=220,
            height=45,
            command=self.update_medicine
        ).pack(pady=20)

    def update_medicine(self):

        print("update button clicked")

        try:
            total = int(self.total_tablets.get())
            remaining = int(self.remaining_tablets.get())

            if total < 0 or remaining < 0:
                print("Tablet count cannot be negative")
                return

            if remaining > total:
                print("Remaining tablets cannot be greater than total tablets")
                return

        except ValueError:
            print("Please enter valid tablet numbers")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE medicines
            SET name=?,
                dosage=?,
                time=?,
                frequency=?,
                total_tablets=?,
                remaining_tablets=?
            WHERE id=?
        """, (
            self.name.get(),
            self.dosage.get(),
            self.time.get(),
            self.frequency.get(),
            total,
            remaining,
            self.medicine_id
        ))

        conn.commit()
        conn.close()

        print("Medicine updated successfully")

        self.master.load_medicines()

        self.destroy()

