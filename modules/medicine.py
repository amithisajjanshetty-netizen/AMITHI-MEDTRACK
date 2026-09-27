import customtkinter as ctk
from database import add_medicine
class MedicineWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Add Medicine")
        self.geometry("400X400")
        ctk.CTkLabel(
            self,
            text="Add Medicine",
            font=("Arial",20)
        ).pack(pady=20)
        ctk.CTkLabel(self,text="Medicine Name").pack()
        self.name_entry=ctk.CTkEntry(self)
        self.name_entry.pack(pady=5)
        ctk.CTkLabel(self,text="dosage").pack()
        self.dosage_entry=ctk.CTkEntry(
            self,
            width=250
        )
        self.dosage_entry.pack(pady=5)
        ctk.CTkLabel(self,text="time").pack()
        self.time_entry=ctk.CTkEntry(self)
        self.time_entry.pack(pady=5)
        ctk.CTkButton(
            self,
            text="Save",
            command=self.save_medicine
        ).pack(pady=20) 
        def save_medicine(self):
            name=self.name_entry.get()
            time=self.time_entry.get()
            add_medicine(name,time)
            print("Medicine saved!")