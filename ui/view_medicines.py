import customtkinter as ctk
import sqlite3
from ui.edit_medicine import EditMedicine
from datetime import datetime
from PIL import Image

class ViewMedicines(ctk.CTkToplevel):

    def __init__(self,parent):
        super().__init__(parent)

        self.title("AMITHI MEDTRACK - View Medicines")
        self.geometry("950x650")
        self.configure(fg_color=("white","#121212"))

        # ---------- Title ----------
        ctk.CTkLabel(
            self,
            text="💊 MY MEDICINES",
            font=("Arial", 30, "bold"),
            text_color="#1565C0"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Never Miss a Dose • Stay Healthy",
            font=("Arial", 14),
            text_color="gray"
        ).pack()

        ctk.CTkButton(
                 self,
                 text="⬅ Home",
                 width=120,
                 command=self.destroy
        ).pack(pady=(0, 10))

        # ---------- Search ----------
        self.search = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="🔍 Search Medicine..."
        )
        self.search.pack(pady=15)
        self.search.bind(
             "<KeyRelease>",
              self.search_medicines
)



        # ---------- Summary ----------
        self.total_label = ctk.CTkLabel(
            self,
            text="📊 Total Medicines : 0",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack()

        # ---------- Scroll Area ----------
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=850,
            height=450,
            fg_color="transparent"
        )
        self.scroll_frame.pack(pady=20)

        self.load_medicines()

       

    def create_card(self, medicine_id, name, dosage, time, frequency, status,total_tablets,remaining_tablets,image_path):

        card = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=18,
            fg_color=("white","#1E1E1E"),
            border_width=2,
            border_color="#D6EAF8"
        )
        card.pack(fill="x", padx=15, pady=10)

        if image_path:
           try:
              img = ctk.CTkImage(
              light_image=Image.open(image_path),
              size=(90, 90)
        )

              image_label = ctk.CTkLabel(
                   card,
                   image=img,
                   text=""
        )
              image_label.pack(pady=(10, 5))

           except Exception as e:
              print("Image Error:", e)
        

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=f"💊 {name}",
            font=("Arial", 22, "bold"),
            text_color="#1565C0"
        ).pack(side="left")
        status_color = "#4CAF50" if "Logged" in status else "#FF9800"

        ctk.CTkLabel(
          header,
          text=status,
          fg_color=status_color,
          corner_radius=12,
          text_color="white",
          padx=12,
          pady=4,
          font=("Arial", 12, "bold")
        ).pack(side="right")

        ctk.CTkLabel(
            card,
            text=f"💉 Dosage        : {dosage}",
            text_color=("black","white")
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            card,
            text=f"🕒 Time          : {time}",
            text_color=("black","white")
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            card,
            text=f"🔁 Frequency     : {frequency}",
            text_color=("black","white")
        ).pack(anchor="w", padx=20)

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=10)

        # ---------- Tablet Stock Status ----------

        if remaining_tablets == 0:
          tablet_text = "❌ OUT OF STOCK"
          tablet_color = "#D32F2F"

        elif remaining_tablets <= 2:
          tablet_text = "🔴 VERY LOW"
          tablet_color = "#D32F2F"

        elif remaining_tablets <= 5:
          tablet_text = "🟡 LOW STOCK"
          tablet_color = "#F57C00"

        else:
          tablet_text = "🟢 GOOD"
          tablet_color =( "#2E7D32","#81C784")


        ctk.CTkLabel(
          card,
          text=f"💊 Remaining Tablets : {remaining_tablets} / {total_tablets}",
          font=("Arial", 14, "bold")
        ).pack(
          anchor="w",
          padx=20,
          pady=(5, 2)
)

        ctk.CTkLabel(
          card,
          text=tablet_text,
          font=("Arial", 13, "bold"),
          text_color=tablet_color
        ).pack(
          anchor="w",
          padx=20,
          pady=(0, 10)
          )

        ctk.CTkFrame(
           card,
           height=2,
           fg_color="#E0E0E0"
        ).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
          button_frame,
          text="✏️ Edit",
          width=120,
          height=40,
          corner_radius=10,
          command=lambda: self.edit_medicine(
          medicine_id,
          name,
          dosage,
          time,
          frequency,
          total_tablets,
          remaining_tablets
    )
).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🗑 Delete",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="red",
            hover_color="#B71C1C",
            command=lambda: self.delete_medicine(medicine_id)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="✅ dose logged",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=lambda:self.mark_dose_logged(medicine_id)
        ).pack(side="left", padx=5)

       

    def load_medicines(self):

        # Remove old cards
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("database/data/medtrack.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, dosage, time, frequency,status,total_tablets,remaining_tablets,image_path
            FROM medicines
        """)

        medicines = cursor.fetchall()

        conn.close()

        self.total_label.configure(
            text=f"📊 Total Medicines : {len(medicines)}"
        )

        for medicine in medicines:
            self.create_card(
                medicine[0],   # id
                medicine[1],   # name
                medicine[2],   # dosage
                medicine[3],   # time
                medicine[4],   # frequency
                medicine[5],
                medicine[6],
                medicine[7],
                medicine[8],
            )


    def search_medicines(self, event=None):

         search_text = self.search.get().lower().strip()

    # Clear existing cards
         for widget in self.scroll_frame.winfo_children():
          widget.destroy()

         conn = sqlite3.connect("database/data/medtrack.db")
         cursor = conn.cursor()

         cursor.execute("""
        SELECT id, name, dosage, time, frequency,
               status, total_tablets, remaining_tablets, image_path
        FROM medicines
        WHERE LOWER(name) LIKE ?
        ORDER BY name
    """, (f"%{search_text}%",))

         medicines = cursor.fetchall()

         conn.close()

    # Update count
         self.total_label.configure(
            text=f"📊 Medicines Found : {len(medicines)}"
    )

    # Display filtered medicines
         for medicine in medicines:

          self.create_card(
            medicine[0],
            medicine[1],
            medicine[2],
            medicine[3],
            medicine[4],
            medicine[5],
            medicine[6],
            medicine[7],
            medicine[8]
        )

    # No results
         if len(medicines) == 0:

          ctk.CTkLabel(
            self.scroll_frame,
            text="🔍 No medicine found",
            font=("Arial", 18, "bold"),
            text_color="gray"
        ).pack(pady=50)
        

    
    def delete_medicine(self, medicine_id):

    # Get medicine name
        conn = sqlite3.connect("database/data/medtrack.db")
        cursor = conn.cursor()

        cursor.execute(
          "SELECT name FROM medicines WHERE id=?",
        (medicine_id,)
    )

        result = cursor.fetchone()

        conn.close()

        if result is None:
         print("medicine not found")
         return

        medicine_name = result[0]

    # Confirmation window
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirm Delete")
        confirm.geometry("400x220")
        confirm.resizable(False, False)
        confirm.grab_set()

        ctk.CTkLabel(
          confirm,
          text="⚠️ Delete Medicine?",
          font=("Arial", 22, "bold"),
          text_color="#D32F2F"
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
         confirm,
         text=f"Are you sure you want to delete\n{medicine_name}?",
         font=("Arial", 15)
        ).pack(pady=5)

        button_frame = ctk.CTkFrame(
         confirm,
         fg_color="transparent"
    )
        button_frame.pack(pady=20)

        ctk.CTkButton(
         button_frame,
         text="Cancel",
         width=120,
         height=40,
         fg_color="gray",
         hover_color="#555555",
         command=confirm.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="delete",
            width=120,
            height=40,
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=lambda: self.perform_delete(
               medicine_id,
               confirm
            )
         ).pack(side="left",padx=10)

    def perform_delete(self, medicine_id, confirm):

         print("DELETE BUTTON CLICKED")
         print("Medicine ID:", medicine_id)

         conn = sqlite3.connect("database/data/medtrack.db")
         cursor = conn.cursor()

         cursor.execute(
         "DELETE FROM medicines WHERE id=?",
         (medicine_id,)
    )

         print("Rows deleted:", cursor.rowcount)

         conn.commit()
         conn.close()

    # Close confirmation popup
         confirm.destroy()

    # Reload medicine cards
         self.load_medicines()

       
    def mark_dose_logged(self, medicine_id):

       conn = sqlite3.connect("database/data/medtrack.db")
       cursor = conn.cursor()

    # Get medicine details
       cursor.execute("""
        SELECT name, dosage, time,remaining_tablets
        FROM medicines
        WHERE id=?
    """, (medicine_id,))

       medicine = cursor.fetchone()

       if medicine:

         today = datetime.now().strftime("%Y-%m-%d")

         cursor.execute("""
            INSERT INTO history
            (medicine_name, dosage, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            medicine[0],
            medicine[1],
            today,
            medicine[2],
            "🟢 Dose Logged"
        ))

       remaining = medicine[3]
       if remaining > 0:
               remaining -= 1

       cursor.execute("""
            UPDATE medicines
            SET status=?, remaining_tablets=?
            WHERE id=?
        """, (
           "🟢 Dose Logged",
            remaining,
            medicine_id
        )) 

       conn.commit()
       conn.close()
       self.load_medicines()

    def edit_medicine(self, medicine_id, name, dosage, time, frequency,total_tablets,remaining_tablets):
     print("before edit window")
     edit_window = EditMedicine(
       self,
       medicine_id,
       name,
      dosage,
      time,
      frequency,
      total_tablets,
      remaining_tablets
    )
     print("after edit medicine")
     self.wait_window(edit_window)
     
       

if __name__ == "__main__":
   
   app = ViewMedicines()
   app.mainloop()