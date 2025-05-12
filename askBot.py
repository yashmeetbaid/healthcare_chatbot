import tkinter as tk
from tkinter import messagebox, ttk
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

class AskBot:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("800x700")
        self.root.configure(bg="#263238")
        style = ttk.Style()
        self.description_list = {}
        self.severityDictionary = {}
        self.precautionDictionary = {}

        # Data/model setup
        self.training = pd.read_csv('Data/Training.csv')
        self.testing = pd.read_csv('Data/Testing.csv')
        self.cols = self.training.columns[:-1]
        self.x = self.training[self.cols]
        self.y = self.training['prognosis']
        self.reduced_data = self.training.groupby(self.training['prognosis']).max()
        self.le = preprocessing.LabelEncoder()
        self.le.fit(self.y)
        self.y = self.le.transform(self.y)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=0.33, random_state=42
        )
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
        style.configure("TLabel", background="#263238", font=("Helvetica", 12), foreground="white")
        style.configure("TEntry", fieldbackground="#f0f0f0", font=("Helvetica", 13))
        style.configure("TButton", font=("Helvetica", 13, "bold"), background="#1976D2", foreground="white")

        img = Image.open("Images/geminilogo.png").resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        image_label = tk.Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = tk.Label(self.root, text="Welcome to Ask BOT", font=("Helvetica", 30, "bold"),
                             bg="#1976D2", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)

        self.bot_photo = self.load_icon("Images/bot1.png", size=(28, 28))
        self.user_photo = self.load_icon("Images/user1.png", size=(28, 28))

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=10, y=115, width=780, height=550)
        main_frame.rowconfigure(0, weight=2)
        main_frame.grid_columnconfigure(0, minsize=730)

        self.chat_history = tk.Text(
            main_frame,
            wrap="none",
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

        # State variables
        self.state = 0
        self.user_name = ""
        self.user_age = ""
        self.user_gender = ""
        self.symptom_list = []
        self.days = 0
        self.severity = ""
        self.disease_input = ""
        self.symptoms_exp = []
        self.consultation = ""
        self.getDescription()
        self.getSeverityDict()
        self.getprecautionDict()

        self.display_message("Hello! I'm Ask BOT, your health assistant.\nLet's start with your name. What should I call you?", "bot")

    def send_message(self):
        msg = self.user_input.get().strip()
        if not msg:
            return

        if self.state == 0:
            self.user_name = msg
            self.display_message(msg, "user")
            self.display_message(f"Hi {self.user_name}! How old are you?", "bot")
            self.state = 1
        elif self.state == 1:
            self.user_age = msg
            self.display_message(msg, "user")
            self.display_message("What is your gender? (Male/Female/Other)", "bot")
            self.state = 2
        elif self.state == 2:
            self.user_gender = msg
            self.display_message(msg, "user")
            self.display_message("Please list your symptoms separated by commas (e.g., cough, fever)", "bot")
            self.state = 3
        elif self.state == 3:
            self.symptom_list = [s.strip().lower() for s in msg.split(',') if s.strip()]
            self.display_message(msg, "user")
            self.display_message("How many days have you been experiencing these symptoms?", "bot")
            self.state = 4
        elif self.state == 4:
            try:
                self.days = int(msg)
                self.display_message(msg, "user")
                self.display_message("On a scale of 1 (mild) to 10 (severe), how would you rate your symptoms?", "bot")
                self.state = 5
            except ValueError:
                self.display_message("Please enter a valid number for days.", "bot")
        elif self.state == 5:
            self.severity = msg
            self.display_message(msg, "user")
            self.display_message("Do you have any relevant medical history or chronic conditions? (If none, type 'None')", "bot")
            self.state = 6
        elif self.state == 6:
            self.display_message(msg, "user")
            self.display_message("Thank you! Please wait a moment while I analyze your symptoms...", "bot")
            self.disease_input = self.symptom_list[0] if self.symptom_list else ""
            self.tree_to_code(self.clf, self.cols, self.disease_input, self.days)
            self.state = 7
        else:
            self.display_message("If you have more questions, please restart the chat.", "bot")

        self.user_input.delete(0, "end")

    def display_message(self, message, sender):
        self.chat_history.config(state="normal")
        if sender == "user":
            self.chat_history.insert("end", "\n")
            self.chat_history.image_create("end", image=self.user_photo, padx=4)
            self.chat_history.insert("end", f"  {message}\n", "user_bubble")
        else:
            self.chat_history.insert("end", "\n")
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

    def display_precautions(self, precautions):
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", "\nPrecautions:\n", "precaution_title")
        self.chat_history.tag_configure("precaution_title", font=("Helvetica", 14, "bold"), foreground="#FFD600")
        for idx, item in enumerate(precautions, 1):
            self.chat_history.insert("end", f"  {idx}. {item}\n", "precaution_item")
        self.chat_history.tag_configure("precaution_item", font=("Helvetica", 13), lmargin1=30)
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def load_icon(self, filename, size=(28, 28)):
        icon = Image.open(filename)
        icon = icon.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(icon)

    def getDescription(self):
        with open('MasterData/symptom_Description.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.description_list[row[0]] = row[1]

    def getSeverityDict(self):
        with open('MasterData/symptom_severity.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    self.severityDictionary[row[0]] = int(row[1])
                except:
                    continue

    def getprecautionDict(self):
        with open('MasterData/symptom_precaution.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]

    def tree_to_code(self, tree, feature_names, disease_input, num_days):
        tree_ = tree.tree_
        feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]
        symptoms_present = []

        def recurse(node, depth):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                val = 1 if name == disease_input else 0
                if val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = self.print_disease(tree_.value[node])
                red_cols = self.reduced_data.columns
                symptoms_given = red_cols[self.reduced_data.loc[present_disease].values[0].nonzero()]

                self.symptoms_exp = self.symptom_list.copy()  # Start with user-given symptoms

                for symptom in list(symptoms_given):
                    if symptom not in self.symptom_list:
                        inp = messagebox.askyesno("Symptoms", f"Are you experiencing {symptom}?")
                        if inp:
                            self.symptoms_exp.append(symptom)

                second_prediction = self.sec_predict(self.symptoms_exp)
                self.calc_condition(self.symptoms_exp, num_days)

                if present_disease[0] == second_prediction[0]:
                    self.display_message(f"You may have {present_disease[0]}", "bot")
                    self.display_message(self.description_list[present_disease[0]], "bot")
                else:
                    self.display_message(f"You may have {present_disease[0]} OR {second_prediction[0]}", "bot")
                    self.display_message(self.description_list[present_disease[0]], "bot")
                    self.display_message(self.description_list[second_prediction[0]], "bot")

                precautions = self.precautionDictionary.get(present_disease[0], [])
                self.display_precautions(precautions)

        recurse(0, 1)

    def sec_predict(self, symptoms_exp1):
        df = pd.read_csv('Data/Training.csv')
        X = df.iloc[:, :-1]
        y = df['prognosis']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
        rf_clf = DecisionTreeClassifier()
        rf_clf.fit(X_train, y_train)
        symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
        input_vector = np.zeros(len(symptoms_dict))
        for item in symptoms_exp1:
            if item in symptoms_dict:
                input_vector[[symptoms_dict[item]]] = 1
        return rf_clf.predict([input_vector])

    def print_disease(self, node):
        node = node[0]
        val = node.nonzero()
        disease = self.le.inverse_transform(val[0])
        return list(map(lambda x: x.strip(), list(disease)))

    def calc_condition(self, exp, days):
        total = 0
        for item in exp:
            total += self.severityDictionary.get(item, 0)
        if ((total * days) / (len(exp) + 1)) > 13:
            self.display_message("You should consult a doctor as soon as possible.", "bot")
        else:
            self.display_message("It might not be serious, but you should take precautions.", "bot")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = AskBot(root)
    root.mainloop()
