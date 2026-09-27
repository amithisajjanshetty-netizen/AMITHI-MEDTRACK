from tkinter import messagebox
import customtkinter as ctk
from ui.dashboard import Dashboard

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AMITHI MEDTRACK - Login")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(fg_color="#F5F9FF")

        # App Title
        title = ctk.CTkLabel(
            self,
            text="AMITHI MEDTRACK",
            font=("Arial", 30, "bold"),
            text_color="#1565C0"
        )
        title.pack(pady=(50, 10))

        # Tagline
        tagline = ctk.CTkLabel(
            self,
            text="Never Miss a Dose.",
            font=("Arial", 18)
        )
        tagline.pack(pady=(0, 30))

        # Username
        self.username = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        # Password
        self.password = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        # Login Button
        login_btn = ctk.CTkButton(
            self,
            text="Login",
            width=300,
            command=self.login
        )
        login_btn.pack(pady=20)

    def login(self):

       username = self.username.get().strip()
       password = self.password.get()

       if username == "admin" and password == "1234":

        messagebox.showinfo(
            "Success",
            "Login Successful!"
        )

        self.destroy()

        dashboard = Dashboard()
        dashboard.mainloop()

       else:

        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()