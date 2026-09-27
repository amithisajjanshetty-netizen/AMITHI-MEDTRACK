import customtkinter as ctk
from ui.login import LoginPage 
class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Amithi MedTrack") #title of window
        self.geometry("900x600") # size of window
        self.resizable(False,False) # cannot change
        self.configure(fg_color="#F5F9FF")
        self.title_label=ctk.CTkLabel(
            self,
            text="AMITHI MEDTRACK",
            font=("Arial",32,"bold"),
            text_color="#1565C0" 
        )
        self.title_label.pack(pady=(150,10))
        #tagline
        self.tagline=ctk.CTkLabel(
            self,
            text="Never Miss a Dose.",
            font=("Arial",18)
        )
        self.tagline.pack()
        self.progress=ctk.CTkProgressBar(self,width=400)
        self.progress.pack(pady=50)
        self.progress.set(0)
        self.loading=0
        self.animate()
    def animate(self):
            if self.loading<100:
                self.loading+=1
                self.progress.set(self.loading/100)
                self.after(30,self.animate)
            else:
                self.destroy()
                login=LoginPage()
                login.mainloop()
if __name__=="__main__":
    app=SplashScreen()
    app.mainloop()                