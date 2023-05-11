import customtkinter
import pyperclip
import time
import threading
import core

Core = core
customtkinter.set_appearance_mode("dark")

class G(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("unSNI-tool")
        self.resizable(0,0)
        self.geometry("460x200")
        self.FONT = ("Comic Sans MS",15,"bold")
        self.BFONT = ("Comic Sans MS",13,"bold")

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.labelFrame = customtkinter.CTkFrame(self,border_width=3,border_color="red")
        self.labelFrame.grid(row=0,column=0,padx=10,pady=(10,0),sticky="nsew")
        self.buttonFrame = customtkinter.CTkFrame(self,border_width=3,border_color="red")
        self.buttonFrame.grid(row=0,column=1,padx=(0,10),pady=(10,0),sticky="nsew")
        self.ulTraffic = customtkinter.CTkLabel(self.labelFrame,text="Upload    :    "+str(0)+" KB",font=self.FONT,state="disabled")
        self.ulTraffic.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.dlTraffic = customtkinter.CTkLabel(self.labelFrame,text="Download :    "+str(0)+" KB",font=self.FONT,state="disabled")
        self.dlTraffic.grid(row=1,column=0,padx=10,pady=10,sticky="w")
        self.statusLabel = customtkinter.CTkLabel(self.labelFrame,text="Deactive",font=self.FONT,state="disabled")
        self.statusLabel.grid(row=2,column=0,padx=10,pady=10,sticky="w")
        self.copyConfigButton = customtkinter.CTkButton(self.buttonFrame,text="copy config",command=self.copyConfig,border_width=2,border_color="red",font=self.FONT)
        self.copyConfigButton.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.startButton = customtkinter.CTkButton(self,text="- Active -",border_color="red",border_width=3,command=self.handleStartButton,font=self.BFONT)
        self.startButton.grid(row=3,column=0,padx=10,pady=10,sticky="ew",columnspan=2)
    
    def updateTraffic(self):
        dlt,ult = 0,0
        while True:
            time.sleep(1)
            for i in Core.IP_DL_traffic.values():
                dlt += i
            for i in Core.IP_UL_traffic.values():
                ult += i
            self.ulTraffic.configure(text = "Upload    :    "+str(int(ult/1024))+" KB")
            self.dlTraffic.configure(text = "Download :    "+str(int(dlt/1024))+" KB")

    def handleStartButton(self):
        self.Active = True
        self.statusLabel.configure(text="listen to 127.0.0.1:"+str(Core.listen_PORT),state="normal")
        self.ulTraffic.configure(state="normal")
        self.dlTraffic.configure(state="normal")
        self.startButton.configure(border_color="#39FF14",state="disabled")
        self.labelFrame.configure(border_color="#39FF14")
        self.buttonFrame.configure(border_color="#39FF14")
        self.copyConfigButton.configure(border_color="#39FF14")
        threading.Thread(target=self.updateTraffic).start()
        threading.Thread(target=Core.ThreadedServer('', Core.listen_PORT).listen).start()

    def copyConfig(self):
        pyperclip.copy(str(open("v2ray_HTTPS_config.json").read()))
        self.copyConfigButton.configure(text="copied !")




app = G()
app.mainloop()