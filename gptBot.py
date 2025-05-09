import tkinter as tk
from tkinter import messagebox, ttk
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
        self.root.title("AI Smart Assistant")
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
        self.gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')
        self.chat = self.gemini_model.start_chat(
            history=[
                {"role": "user", "parts": ["You are a Doctor, Physician, Medical, Healthcare Assistant"]},
                {"role": "model", "parts": ["I understand. I'll act as a healthcare assistant to help with medical questions. How can I assist you today?"]}
            ]
        )

        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#263238", font=("Helvetica", 12), foreground="white")
        style.configure("TEntry", fieldbackground="#f0f0f0", font=("Helvetica", 13))
        style.configure("TButton", font=("Helvetica", 13, "bold"), background="#1976D2", foreground="white")

        img = Image.open("Images/geminilogo.png").resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        image_label = tk.Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = tk.Label(self.root, text="AI Smart Assistant", font=("Helvetica", 30, "bold"),
                             bg="#1976D2", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)

        # Load user and bot icons
        self.bot_photo = self.load_icon("Images/bot1.png", size=(28, 28))
        self.user_photo = self.load_icon("Images/user1.png", size=(28, 28))

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=10, y=115, width=780, height=550)
        main_frame.rowconfigure(0, weight=2)
        main_frame.grid_columnconfigure(0, minsize=730)

        self.chat_history = tk.Text(
            main_frame,
            wrap="word",
            state="disabled",
            font=("Helvetica", 14),
            bg="#37474F",
            fg="white",
            padx=16,
            pady=10,
            spacing1=8,
            spacing3=8,
            relief="flat",
            borderwidth=0
        )
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.grid(row=0, column=3, sticky="ns", pady=10)

        self.h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.chat_history.xview)
        self.h_scrollbar.grid(row=2, column=0, columnspan=3, sticky="we", padx=10)

        self.chat_history.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.user_input = ttk.Entry(main_frame, style="TEntry", font=("Helvetica", 13))
        self.user_input.grid(row=1, column=0, padx=(10,5), pady=20, sticky="we", columnspan=2, ipady=8)

        img1 = Image.open("Images/send 3.png").resize((36, 36), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        self.send_button = ttk.Button(main_frame, image=self.photoimg1, command=self.send_message, style="TButton")
        self.send_button.grid(row=1, column=2, padx=(5,15), pady=20, sticky="nsew", ipadx=8, ipady=2)

        self.root.bind('<Return>', lambda event=None: self.send_message())

        # Display welcome message
        self.display_message("Hi! I'm your healthcare assistant. How can I help you today?", "bot")

    def send_message(self):
        msg = self.user_input.get().strip()
        if not msg:
            return

        self.display_message(msg, "user")
        try:
            response = self.chat.send_message(msg)
            bot_response = response.text
            self.display_message(bot_response, "bot")
        except Exception as e:
            error_message = f"Error communicating with Gemini API: {str(e)}"
            self.display_message(error_message, "bot")
        self.user_input.delete(0, "end")

    def display_message(self, message, sender):
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", "\n")
        if sender == "user":
            self.chat_history.image_create("end", image=self.user_photo, padx=4)
            self.chat_history.insert("end", f"  {message}\n", "user_bubble")
        else:
            self.chat_history.image_create("end", image=self.bot_photo, padx=4)
            self.chat_history.insert("end", f"  {message}\n", "bot_bubble")
        self.chat_history.tag_configure(
            "user_bubble",
            background="#1976D2",
            foreground="white",
            font=("Helvetica", 14, "bold"),
            justify="right",
            lmargin1=320,
            rmargin=10,
            spacing1=5,
            spacing3=5
        )
        self.chat_history.tag_configure(
            "bot_bubble",
            background="#37474F",
            foreground="white",
            font=("Helvetica", 14),
            justify="left",
            lmargin1=10,
            rmargin=320,
            spacing1=5,
            spacing3=5
        )
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def load_icon(self, filename, size=(28, 28)):
        icon = Image.open(filename)
        icon = icon.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(icon)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = GeminiBot(root)
    root.mainloop()
