import customtkinter as ctk
import sqlite3

DB="database/data/medtrack.db"

class History(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        self.title("AMITHI MEDTRACK - History")
        self.geometry("1000x700")
        self.configure(fg_color=("white","#121212"))

        ctk.CTkLabel(self,text="📜 MEDICINE HISTORY",
                     font=("Arial",30,"bold"),
                     text_color="#1565C0").pack(pady=(20,5))
        ctk.CTkLabel(self,text="Every Dose. Every Record.",
                     text_color="gray").pack()

        
        ctk.CTkButton(
          self,
          text="← Home",
          width=180,
          height=40,
          fg_color="#1565C0",
          hover_color="#0D47A1",
          command=self.go_back
         ).pack(pady=10)


        self.stats=ctk.CTkLabel(self,text="📊 Total Logged : 0",
                                font=("Arial",18,"bold"))
        self.stats.pack(pady=10)

        self.search=ctk.CTkEntry(self,width=350,
                                 placeholder_text="🔍 Search Medicine...")
        self.search.pack(pady=5)
        self.search.bind("<KeyRelease>",self.filter_records)

        self.scroll=ctk.CTkScrollableFrame(self,width=900,height=540,
                                           fg_color="transparent")
        self.scroll.pack(pady=10,fill="both",expand=True)

        self.records=[]
        self.load_history()

    def load_history(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        con=sqlite3.connect(DB)
        cur=con.cursor()
        cur.execute("""SELECT medicine_name,dosage,date,time,status
                       FROM history ORDER BY id DESC""")
        self.records=cur.fetchall()
        con.close()

        self.stats.configure(text=f"📊 Total Logged : {len(self.records)}")
        self.show_cards(self.records,0)

    def show_cards(self,data,index):
        if index>=len(data):
            return
        self.create_card(data[index], index==0)
        self.after(150, lambda:self.show_cards(data,index+1))

    def filter_records(self,event=None):
        text=self.search.get().lower()
        for w in self.scroll.winfo_children():
            w.destroy()
        data=[r for r in self.records if text in r[0].lower()]
        self.show_cards(data,0)

    def create_card(self,rec,latest):
        row=ctk.CTkFrame(self.scroll,fg_color="transparent")
        row.pack(fill="x",padx=20,pady=8)

        left=ctk.CTkFrame(row,width=50,fg_color="transparent")
        left.pack(side="left",fill="y")

        ctk.CTkLabel(left,text="│",text_color="#1565C0",
                     font=("Arial",26)).pack()
        dot=ctk.CTkFrame(left,width=16,height=16,
                         corner_radius=8,fg_color="#1565C0")
        dot.pack()
        ctk.CTkLabel(left,text="│",text_color="#1565C0",
                     font=("Arial",26)).pack(expand=True)

        card=ctk.CTkFrame(row,corner_radius=20,fg_color=("white","#1E1E1E"))
        card.pack(side="left",fill="x",expand=True,padx=8)

        def enter(e): card.configure(fg_color=("#E3F2FD","#2A2A2A"))
        def leave(e): card.configure(fg_color=("white","#1E1E1E"))
        card.bind("<Enter>",enter)
        card.bind("<Leave>",leave)

        ctk.CTkLabel(card,text=f"💊 {rec[0]}",
                     font=("Arial",20,"bold"),
                     text_color=("#1565C0","#64B5F6")).pack(anchor="w",padx=20,pady=(12,2))
        if latest:
            ctk.CTkLabel(card,text="🆕 Latest Dose",
                         text_color=("#D32F2F","#FF6B6B")).pack(anchor="w",padx=20)
        ctk.CTkLabel(card,text=f"💉 Dosage : {rec[1]}",text_color=("black","white")).pack(anchor="w",padx=20)
        ctk.CTkLabel(card,text=f"📅 {rec[2]}",text_color=("black","white")).pack(anchor="w",padx=20)
        ctk.CTkLabel(card,text=f"🕒 {rec[3]}",text_color=("black","white")).pack(anchor="w",padx=20)

        badge=ctk.CTkFrame(card,corner_radius=12,fg_color=("#E3F2FD","#1E3A5F"))
        badge.pack(anchor="w",padx=20,pady=(8,12))
        ctk.CTkLabel(badge,text=rec[4],text_color=("#1565C0","#90CAF9")).pack(padx=10,pady=4)
    
    def go_back(self):
        self.destroy()


