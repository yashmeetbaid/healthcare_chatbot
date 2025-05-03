import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import csv
import os
import warnings
import google.generativeai as genai
warnings.filterwarnings("ignore", category=DeprecationWarning)

class GeminiBot:
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

        # Initialize Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Set up the Gemini model
        self.gemini_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

        # Start the chat conversation
        self.chat = self.gemini_model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["You are a Doctor, Physician, Medical, Healthcare Assistant"]
                },
                {
                    "role": "model",
                    "parts": ["I understand. I'll act as a healthcare assistant to help with medical questions. How can I assist you today?"]
                }
            ]
        )

        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#263238", font=("Helvetica", 11), foreground="white")
        style.configure("TEntry", fieldbackground="#f0f0f0", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11), background="#4CAF50", foreground="white")

        img = Image.open("Images/geminilogo.png")
        img = img.resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        image_label = Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = Label(self.root, text="AI Smart Assistant", font=("times new roman", 30, "bold"), bg="#1E90FF", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)

        # Load user and bot icons
        self.bot_icon = self.load_icon("Images/bot_icon.png")
        self.user_icon = self.load_icon("Images/user_icon.png")

        img1 = Image.open("Images/send 3.png")
        img1= img1.resize((40, 20), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        
        # Reduce the size of the TFrame
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=10, y=115, width=780, height=550)
        main_frame.rowconfigure(0, weight=2)
        main_frame.grid_columnconfigure(0, minsize=730)
        
        self.user_input = ttk.Entry(main_frame, style="TEntry", font=("times new roman", 11))
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="we", columnspan=2)

        self.send_button = ttk.Button(main_frame, image=self.photoimg1, command=self.send_message, style="TButton")
        self.send_button.grid(row=1, column=2, padx=0, pady=10, sticky="nsew")
        
        self.chat_history = tk.Text(main_frame, wrap="word", state="disabled", font=("times new roman", 11),
                             bg="#37474F", fg="white")
        self.scrollbar = ttk.Scrollbar(main_frame, command=self.chat_history.yview)
        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        # Grid the chat history and scrollbar
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")
        self.root.bind('<Return>', lambda event=None: self.send_message())

        # Display welcome message
        self.display_message("Hi! I'm your healthcare assistant. How can I help you today?", "bot")

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message(user_message, "user")

            try:
                # Get response from Gemini
                response = self.chat.send_message(user_message)
                bot_response = response.text
                
                self.display_message(bot_response, "bot")
            except Exception as e:
                error_message = f"Error communicating with Gemini API: {str(e)}"
                self.display_message(error_message, "bot")
                
            self.user_input.delete(0, "end")

    def display_message(self, message, sender):
        self.chat_history.config(state="normal")
        
        self.chat_history.tag_configure("user", foreground="#ffffff", background="#263238", justify="right", font=("times new roman", 15))
        self.chat_history.tag_configure("bot", foreground="#ffffff", background="#263238", justify="left", font=("times new roman", 15))
        
        self.chat_history.insert("end", message + "\n\n", sender)
        self.chat_history.see("end")
        self.chat_history.config(state="disabled")
    
    def load_icon(self, filename):
        try:
            icon = Image.open(filename)
            icon = icon.resize((20, 20), Image.LANCZOS)
            icon = ImageTk.PhotoImage(icon)
            return icon
        except Exception as e:
            print(f"Error loading icon {filename}: {e}")
            return None
    
if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = GeminiBot(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
