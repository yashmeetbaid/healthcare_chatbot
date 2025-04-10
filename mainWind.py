from tkinter import *
import tkinter as tk
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from askBot import AskBot
from gptBot import GptBot
from about import About

class MainWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("800x700")
        self.root.configure(bg="#263238")
        img = Image.open("Images/logo4_GPT-removebg.png")
        img = img.resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        title_lbl=Label(self.root,text="HelathCare ChatBot",font=("times new roman",30,"bold"),bg="#6495ED",fg="black")
        title_lbl.place(x=100,y=20, width=677, height=80)
        
        image_label = tk.Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=2, y=15)

        b1=Button(self.root,text="About",cursor="hand2",command=self.about,font=("times new roman",20,"bold"),bg="#1E90FF",fg="black")
        b1.place(x=20,y=115,width=151,height=33)
        
        b2=Button(self.root,text="Get Diagnos",cursor="hand2",command=self.askBotFunc,font=("times new roman",20,"bold"),bg="#1E90FF",fg="black")
        b2.place(x=183,y=115,width=203,height=35)
        
        b3=Button(self.root,text="Ask Advisor",cursor="hand2",command=self.askGpt,font=("times new roman",20,"bold"),bg="#1E90FF",fg="black")
        b3.place(x=400,y=115,width=211,height=35)
        
        b4=Button(self.root,text="Exit",cursor="hand2",command=self.isExit,font=("times new roman",20,"bold"),bg="#1E90FF",fg="black")
        b4.place(x=626,y=115,width=151,height=35)


        img2 = Image.open("Images/frontpage.jpg")
        img2 = img2.resize((800, 600), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        label2 = tk.Label(self.root, image=self.photoimg2)
        label2.place(x=2, y=154, width=800, height=545)
    

    def askBotFunc(self):
        self.new_window=Toplevel(self.root)
        self.app=AskBot(self.new_window)

    def about(self):
        self.new_window=Toplevel(self.root)
        self.app=About(self.new_window)

    def askGpt(self):
        self.new_window=Toplevel(self.root)
        self.app=GptBot(self.new_window)
    
    def isExit(self):
        self.isExit=tkinter.messagebox.askyesno("Are You Sure To Exit This BOT",parent=self.root)
        if self.isExit>0:
            self.root.destroy()
        else:
            return
    

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = MainWin(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()