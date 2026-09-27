import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, back_command):
        super().__init__(
            parent,
            fg_color=("white", "#121212")
        )

        self.back_command = back_command

        # ---------- Title ----------
        ctk.CTkLabel(
            self,
            text="⚙️ SETTINGS",
            font=("Arial", 30, "bold"),
            text_color=("#1565C0", "#64B5F6")
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self,
            text="Customize AMITHI MEDTRACK",
            font=("Arial", 14),
            text_color=("gray20", "gray70")
        ).pack(pady=(0, 30))

        # ---------- Appearance ----------
        appearance_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )
        appearance_frame.pack(
            fill="x",
            padx=80,
            pady=10
        )

        ctk.CTkLabel(
            appearance_frame,
            text="🌙 Appearance",
            font=("Arial", 17, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=20
        )

        self.appearance = ctk.CTkOptionMenu(
            appearance_frame,
            values=["Light", "Dark"],
            command=self.change_appearance
        )

        self.appearance.set("Light")

        self.appearance.pack(
            side="right",
            padx=20
        )

        # ---------- Reminder Sound ----------
        sound_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )
        sound_frame.pack(
            fill="x",
            padx=80,
            pady=10
        )

        ctk.CTkLabel(
            sound_frame,
            text="🔔 Reminder Sound",
            font=("Arial", 17, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=20
        )

        self.sound_switch = ctk.CTkSwitch(
            sound_frame,
            text="ON"
        )

        self.sound_switch.select()

        self.sound_switch.pack(
            side="right",
            padx=20
        )

        # ---------- About ----------
        about_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )
        about_frame.pack(
            fill="x",
            padx=80,
            pady=10
        )

        ctk.CTkLabel(
            about_frame,
            text="ℹ️ About",
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            about_frame,
            text="AMITHI MEDTRACK\n"
                 "Smart Medicine Reminder System\n\n"
                 "Never Miss a Dose. 💊",
            font=("Arial", 13),
            text_color=("gray20", "gray70")
        ).pack(
            padx=20,
            pady=(0, 15)
        )

        # ---------- Back ----------
        ctk.CTkButton(
            self,
            text="⬅ Back to Dashboard",
            width=220,
            height=40,
            command=self.back_command
        ).pack(pady=25)

    def change_appearance(self, choice):

        if choice == "Dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")