import customtkinter as ctk
import sqlite3


class TodaySchedule(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("AMITHI MEDTRACK - Today's Schedule")
        self.geometry("850x600")
        self.resizable(False, False)
        self.configure(fg_color=("white","#121212"))

        # ---------- Title ----------
        ctk.CTkLabel(
            self,
            text="📅 TODAY'S MEDICINE SCHEDULE",
            font=("Arial", 28, "bold"),
            text_color="#1565C0"
        ).pack(pady=(20, 10))

        # ---------- Back Button ----------
        ctk.CTkButton(
            self,
            text="← Back to Dashboard",
            width=180,
            height=40,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.go_back
        ).pack(pady=(0, 10))

        # ---------- Scroll Frame ----------
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=750,
            height=430
        )

        self.scroll_frame.pack(pady=10)

        self.load_schedule()

    def load_schedule(self):

        conn = sqlite3.connect("database/data/medtrack.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, dosage, time, frequency, status
            FROM medicines
            ORDER BY time
        """)

        medicines = cursor.fetchall()

        conn.close()

        if len(medicines) == 0:

            ctk.CTkLabel(
                self.scroll_frame,
                text="No medicines scheduled today.",
                font=("Arial", 18)
            ).pack(pady=50)

            return

        for medicine in medicines:

            card = ctk.CTkFrame(
                self.scroll_frame,
                corner_radius=20
            )

            card.pack(
                fill="x",
                padx=15,
                pady=10
            )

            ctk.CTkLabel(
                card,
                text=f"💊 {medicine[0]}",
                font=("Arial", 22, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(10, 5)
            )

            ctk.CTkLabel(
                card,
                text=f"💉 Dosage : {medicine[1]}"
            ).pack(
                anchor="w",
                padx=20
            )

            ctk.CTkLabel(
                card,
                text=f"🕒 Time : {medicine[2]}"
            ).pack(
                anchor="w",
                padx=20
            )

            ctk.CTkLabel(
                card,
                text=f"🔁 Frequency : {medicine[3]}"
            ).pack(
                anchor="w",
                padx=20
            )

            ctk.CTkLabel(
                card,
                text=medicine[4],
                text_color=(
                    "green"
                    if medicine[4] == "🟢 Dose Logged"
                    else "orange"
                )
            ).pack(
                anchor="w",
                padx=20,
                pady=(5, 15)
            )

    def go_back(self):
        self.destroy()


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    schedule = TodaySchedule(app)
    app.mainloop()

