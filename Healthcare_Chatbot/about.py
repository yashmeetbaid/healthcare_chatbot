import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class About:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("800x700")
        self.root.configure(bg="#263238")

        img = Image.open("/Users/yashmeetbaid/Downloads/Healthcare_Chatbot-main/Images/logo4_GPT-removebg.png")
        img = img.resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        image_label = Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = Label(self.root, text="About ChatBot",  font=("times new roman", 30, "bold"), bg="#4169E1", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)
        
        about_text = Label(self.root,text="1) Symptom Assessment. \n2) Healthy Living Advice. \n3) Medical Support. \n4) Potential Dignosis as per Symptoms. \n5) Advance Precautions",font=("times new roman", 16, "bold"),fg="white",bg="#263238" ,justify="left")   
        about_text.place(x=10, y=130)
        img1 = Image.open("/Users/yashmeetbaid/Downloads/Healthcare_Chatbot-main/Images/about1.png")
        img1 = img1.resize((800, 420), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        image_label1 = Label(self.root, image=self.photoimg1, bg="#263238")
        image_label1.place(x=0, y=260)

          
            

       
    
if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = About(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
