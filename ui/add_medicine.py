import customtkinter as ctk
from modules.database import add_medicine
from tkinter import filedialog
import shutil
import os

class AddMedicine(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.image_path = ""

        self.title("Add Medicine")
        self.geometry("900x600")
        self.configure(fg_color=("white","#121212"))

        ctk.CTkLabel(
            self,
            text="Add Medicine",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        self.name = ctk.CTkEntry(self, width=300, placeholder_text="Medicine Name")
        self.name.pack(pady=10)

        self.dosage = ctk.CTkEntry(self, width=300, placeholder_text="Dosage (e.g. 500 mg)")
        self.dosage.pack(pady=10)

       # self.time = ctk.CTkEntry(self, width=300, placeholder_text="Time (e.g. 08:00 AM)")
        #self.time.pack(pady=10)
        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.pack(pady=10)

        self.hour = ctk.CTkComboBox(
             time_frame,
             values=[f"{i:02}" for i in range(1, 13)],
             width=80
)
        self.hour.set("08")
        self.hour.pack(side="left", padx=5)

        self.minute = ctk.CTkComboBox(
             time_frame,
             values=[f"{i:02}" for i in range(60)],
             width=80
)
        self.minute.set("00")
        self.minute.pack(side="left", padx=5)

        self.ampm = ctk.CTkComboBox(
           time_frame,
           values=["AM", "PM"],
           width=80
)
        self.ampm.set("AM")
        self.ampm.pack(side="left", padx=5)

        self.frequency = ctk.CTkEntry(self, width=300, placeholder_text="Frequency (Daily/Weekly)")
        self.frequency.pack(pady=10)

        self.total_tablets = ctk.CTkEntry(
        self,
        width=300,
        placeholder_text="Total Tablets (e.g. 10)"
    )
        self.total_tablets.pack(pady=10)

        ctk.CTkButton(
         self,
         text="📷 Upload Medicine Image",
         width=220,
         command=self.upload_image
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save_medicine
            ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="⬅ Home",
            width=200,
            fg_color="#5C7CB8",
            hover_color="#24333A",
            command=self.back_to_dashboard
        ).pack(pady=10)

    def save_medicine(self):
         add_medicine(
            self.name.get(),
            self.dosage.get(),
            f"{self.hour.get()}:{self.minute.get()} {self.ampm.get()}",
            self.frequency.get(),
            int(self.total_tablets.get()),
            self.image_path
         )
         print("Medicine saved successfully!")
         self.destroy()
        

    def upload_image(self):

        file_path = filedialog.askopenfilename(
         title="Select Medicine Image",
         filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

        if file_path:
           filename = os.path.basename(file_path)

           destination = os.path.join(
              "assets",
              "medicines",
            filename
        )

           shutil.copy(file_path, destination)

           self.image_path = destination

           print("Image Selected:", self.image_path)      

    def back_to_dashboard(self):
        self.destroy()
       

if __name__ == "__main__":
    app = AddMedicine()
    app.mainloop()