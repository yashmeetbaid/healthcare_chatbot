
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
import os
import warnings
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
warnings.filterwarnings("ignore", category=DeprecationWarning)

class GptBot:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("800x700")
        self.root.configure(bg="#263238")
        style = ttk.Style()
        self.description_list = {}
        self.severityDictionary = {}
        self.precautionDictionary = {}
        self.training = pd.read_csv('Data/Training.csv')
        self.testing = pd.read_csv('Data/Testing.csv')
        self.cols = self.training.columns[:-1]
        self.x = self.training[self.cols]
        self.y = self.training['prognosis']
        self.reduced_data = self.training.groupby(self.training['prognosis']).max()
        self.le = preprocessing.LabelEncoder()
        self.le.fit(self.y)
        self.y = self.le.transform(self.y)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.33, random_state=42)
        self.testx = self.testing[self.cols]
        self.testy = self.testing['prognosis']
        self.testy = self.le.transform(self.testy)
        self.clf1 = DecisionTreeClassifier()
        self.clf = self.clf1.fit(self.x_train, self.y_train)
        self.model = SVC()
        self.model.fit(self.x_train, self.y_train)
        self.importances = self.clf.feature_importances_
        self.indices = np.argsort(self.importances)[::-1]
        self.features = self.cols

        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#263238", font=("Helvetica", 11), foreground="white")
        style.configure("TEntry", fieldbackground="#f0f0f0", font=("Helvetica", 11))
        style.configure("TButton", font=("Bahnschrift Condensed", 11), background="blue", foreground="black")

        img = Image.open("/Users/yashmeetbaid/Downloads/Healthcare_Chatbot-main/Images/logo4_GPT-removebg.png")
        img = img.resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        image_label = Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = Label(self.root, text="AI Smart Asssitant", font=("times new roman", 30, "bold"), bg="#1E90FF", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)

        img1 = Image.open("/Users/yashmeetbaid/Downloads/Healthcare_Chatbot-main/Images/send 3.png")
        img1= img1.resize((40, 20), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        # Reduce the size of the TFrame
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=10, y=115, width=780, height=550)
        main_frame.rowconfigure(0, weight=2)
        main_frame.grid_columnconfigure(0, minsize=730)
        
        self.user_input = ttk.Entry(main_frame, style="TEntry", font=("times new roman", 11))
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="we",columnspan = 2)

        self.send_button = ttk.Button(main_frame, image=self.photoimg1 ,command=self.send_message, style="TButton")
        self.send_button.grid(row=1, column=2, padx=0, pady=10, sticky="nsew")
        
        self.chat_history = tk.Text(main_frame, wrap="word", state="disabled", font=("times new roman", 11),
                             bg="#37474F", fg="white")
        self.scrollbar = ttk.Scrollbar(main_frame, command=self.chat_history.yview)
        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        # Grid the chat history and scrollbar
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan = 3,sticky="nsew")
        self.root.bind('<Return>', lambda event=None: self.send_message())

        self.messages = [{"role": "system", "content": "You are a Doctor, Pysician, Medical, HealthCare Assistent"}]

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message(user_message, "user")

            # OpenAI GPT-3.5 Turbo
            self.messages.append({"role": "user", "content": user_message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
            bot_response = chat.choices[0].message.content

            self.display_message(bot_response, "bot")
            self.user_input.delete(0, "end")

    def display_message(self, message, sender):
        self.chat_history.config(state="normal")
        self.chat_history.tag_configure("user", foreground="#ffffff", background="#263238", justify="right",font=("times new roman", 15))
        self.chat_history.insert("end", message + "\n\n", sender)
        self.chat_history.tag_configure("bot", foreground="#ffffff", background="#263238",justify="left",font=("times new roman", 15))
        self.chat_history.config(state="disabled")
    
if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = GptBot(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
