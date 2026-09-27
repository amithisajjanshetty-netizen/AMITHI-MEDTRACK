import customtkinter as ctk
import sqlite3
from ui.add_medicine import AddMedicine
from ui.view_medicines import ViewMedicines
from datetime import datetime
from ui.today_schedule import TodaySchedule
from ui.history import History
from ui.reminder_popup import ReminderPopup
import threading
from modules.reminder import start_reminders
from ui.settings import SettingsPage


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AMITHI MEDTRACK - Dashboard")
        self.geometry("900x650")
        self.resizable(False, False)
        self.configure(fg_color=("white", "#121212"))

        # =====================================================
        # DASHBOARD FRAME
        # =====================================================

        self.dashboard_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.dashboard_frame.pack(
            fill="both",
            expand=True
        )

        # ---------- Title ----------

        title = ctk.CTkLabel(
            self.dashboard_frame,
            text="Welcome to AMITHI MEDTRACK",
            font=("Arial", 28, "bold"),
            text_color="#1565C0"
        )
        title.pack(pady=20)

        today = datetime.now().strftime("%A, %d %B %Y")

        ctk.CTkLabel(
            self.dashboard_frame,
            text=today,
            font=("Arial", 15),
            text_color="gray"
        ).pack(pady=(0, 15))

        # =====================================================
        # STATISTICS
        # =====================================================

        stats_frame = ctk.CTkFrame(
            self.dashboard_frame,
            fg_color="transparent"
        )
        stats_frame.pack(pady=15)

        # ---------- Total Medicines ----------

        self.total_card = ctk.CTkFrame(
            stats_frame,
            width=180,
            height=100,
            corner_radius=15,
            fg_color=("#F5F9FF","#1E1E1E")
        )
        self.total_card.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            self.total_card,
            text="💊",
            font=("Arial", 28)
        ).pack(pady=(10, 0))

        self.total_label = ctk.CTkLabel(
            self.total_card,
            text="0",
            font=("Arial", 24, "bold")
        )
        self.total_label.pack()

        ctk.CTkLabel(
            self.total_card,
            text="Total Medicines"
        ).pack(pady=(0, 10))

        # ---------- Dose Logged ----------

        self.logged_card = ctk.CTkFrame(
            stats_frame,
            width=180,
            height=100,
            corner_radius=15,
            fg_color=("#F5F9FF","#1E1E1E")
        )
        self.logged_card.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            self.logged_card,
            text="🟢",
            font=("Arial", 28)
        ).pack(pady=(10, 0))

        self.logged_label = ctk.CTkLabel(
            self.logged_card,
            text="0",
            font=("Arial", 24, "bold")
        )
        self.logged_label.pack()

        ctk.CTkLabel(
            self.logged_card,
            text="Dose Logged"
        ).pack(pady=(0, 10))

        # ---------- Pending ----------

        self.pending_card = ctk.CTkFrame(
            stats_frame,
            width=180,
            height=100,
            corner_radius=15,
            fg_color=("#F5F9FF","#1E1E1E")
        )
        self.pending_card.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            self.pending_card,
            text="🟡",
            font=("Arial", 28)
        ).pack(pady=(10, 0))

        self.pending_label = ctk.CTkLabel(
            self.pending_card,
            text="0",
            font=("Arial", 24, "bold")
        )
        self.pending_label.pack()

        ctk.CTkLabel(
            self.pending_card,
            text="Pending"
        ).pack(pady=(0, 10))

        # =====================================================
        # BUTTONS
        # =====================================================

        ctk.CTkButton(
            self.dashboard_frame,
            text="💊 Add Medicine",
            width=250,
            command=self.open_add_medicine
        ).pack(pady=10)

        ctk.CTkButton(
            self.dashboard_frame,
            text="📋 View Medicines",
            width=250,
            command=self.open_view_medicines
        ).pack(pady=10)

        ctk.CTkButton(
            self.dashboard_frame,
            text="⏰ Today's Schedule",
            width=250,
            fg_color="#0051FF",
            hover_color="#0039F5",
            command=self.open_today_schedule
        ).pack(pady=10)

        ctk.CTkButton(
            self.dashboard_frame,
            text="📜 History",
            width=250,
            fg_color="#1430D3",
            hover_color="#7259E0",
            command=self.open_history
        ).pack(pady=10)

        ctk.CTkButton(
            self.dashboard_frame,
            text="⚙️ Settings",
            width=250,
            command=self.open_settings
        ).pack(pady=10)

        # =====================================================
        # LOAD STATS
        # =====================================================

        self.load_dashboard_stats()

        # =====================================================
        # REMINDER THREAD
        # =====================================================

        threading.Thread(
            target=start_reminders,
            args=(self,),
            daemon=True
        ).start()

    # =========================================================
    # ADD MEDICINE
    # =========================================================

    def open_add_medicine(self):

        self.withdraw()

        add_window = AddMedicine(self)

        self.wait_window(add_window)

        self.deiconify()

        self.load_dashboard_stats()

    # =========================================================
    # VIEW MEDICINES
    # =========================================================

    def open_view_medicines(self):

        self.withdraw()

        view = ViewMedicines(self)

        self.wait_window(view)

        self.deiconify()

        self.load_dashboard_stats()

    # =========================================================
    # TODAY'S SCHEDULE
    # =========================================================

    def open_today_schedule(self):

        self.withdraw()

        schedule_window = TodaySchedule(self)

        self.wait_window(schedule_window)

        self.deiconify()

        self.load_dashboard_stats()

    # =========================================================
    # HISTORY
    # =========================================================

    def open_history(self):

        self.withdraw()

        history_window = History(self)

        self.wait_window(history_window)

        self.deiconify()

        self.load_dashboard_stats()

    # =========================================================
    # REMINDER
    # =========================================================

    def show_reminder(
        self,
        medicine_id,
        medicine_name,
        dosage,
        medicine_time,
        remaining_tablets
    ):

        ReminderPopup(
            self,
            medicine_id,
            medicine_name,
            dosage,
            medicine_time,
            remaining_tablets
        )

    # =========================================================
    # DASHBOARD STATISTICS
    # =========================================================

    def load_dashboard_stats(self):

        conn = sqlite3.connect(
            "database/data/medtrack.db"
        )

        cursor = conn.cursor()

        # ---------- Total Medicines ----------

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
        """)

        total = cursor.fetchone()[0]

        # ---------- Today's Dose Logged ----------

        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT COUNT(*)
            FROM history
            WHERE date=?
            AND status='🟢 Dose Logged'
        """, (today,))

        logged = cursor.fetchone()[0]

        # ---------- Today's Pending ----------

        pending = total - logged

        if pending < 0:
            pending = 0

        conn.close()

        # ---------- Update Dashboard ----------

        self.total_label.configure(
            text=str(total)
        )

        self.logged_label.configure(
            text=str(logged)
        )

        self.pending_label.configure(
            text=str(pending)
        )

    # =========================================================
    # OPEN SETTINGS
    # =========================================================

    def open_settings(self):

        # Hide Dashboard frame
        self.dashboard_frame.pack_forget()

        # Create Settings page
        self.settings_page = SettingsPage(
            self,
            self.show_dashboard
        )

        self.settings_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # BACK TO DASHBOARD
    # =========================================================

    def show_dashboard(self):

        # Remove Settings page
        if hasattr(self, "settings_page"):

            self.settings_page.destroy()

            del self.settings_page

        # Show Dashboard frame again
        self.dashboard_frame.pack(
            fill="both",
            expand=True
        )

        # Refresh statistics
        self.load_dashboard_stats()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    app = Dashboard()

    app.mainloop()