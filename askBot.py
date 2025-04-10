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
        style.configure("TButton", font=("Helvetica", 11), background="#4CAF50", foreground="white")

        img = Image.open("Images/logo4_GPT-removebg.png")
        img = img.resize((90, 90), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        image_label = Label(self.root, image=self.photoimg, bg="#263238")
        image_label.place(x=20, y=20)

        title_lbl = Label(self.root, text="WelCome to Ask BOT", font=("times new roman", 30, "bold"), bg="#1E90FF", fg="white")
        title_lbl.place(x=120, y=20, width=670, height=80)
        
        self.bot_photo = self.load_icon("Images/bot1.png")
        self.user_photo = self.load_icon("Images/user1.png")

        
        # Reduce the size of the TFrame
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=10, y=115, width=780, height=550)
        main_frame.rowconfigure(0, weight=2)
        main_frame.grid_columnconfigure(0, minsize=679)

        img1 = Image.open("Images/send 3.png")
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
        # self.scrollbar.grid(row=0, column=1,padx=0, pady=5,sticky="ns")




        # Bind the send button to the return key
        self.root.bind('<Return>', lambda event=None: self.send_message())
       
        self.user_icon = self.load_icon("Images/user_icon.png")
        self.bot_icon = self.load_icon("Images/bot_icon.png")
        self.nameask = 0  # Initialize as instance attribute
        self.disease_input = ""
        self.num_days = 0
        self.symptomsExp=""
        self.symptoms_exp = []
        self.symptoms_given = []
        self.consultation=""
        self.getDescription()
        self.getSeverityDict()
        self.getprecautionDict()

        self.display_message("Hi, What is your Name?", "bot")
        self.syms=""
       

    def send_message(self):
        msg = self.user_input.get()

        if self.nameask == 0:
            welcome_message = f"Hello, {msg}! from which disease do you think you suffering from  ?"
            self.nameask += 1
            if msg.strip():
                self.display_message(msg, "user")
                self.display_message(welcome_message, "bot")
                self.user_input.delete(0, "end")
                return "hello"
            else:
                return ""
        else:
            if msg.strip():
                self.display_message(msg, "user")
                if not self.disease_input:
                    self.disease_input = msg
                    self.user_input.delete(0, "end")
                    self.display_message("Okay. From how many days?", "bot")
                elif self.num_days == 0:
                    try:
                        self.num_days = int(msg)
                        self.user_input.delete(0, "end")
                        self.display_message("Can you experess any symptoms? (yes/no)", "bot")
                    except ValueError:
                        self.display_message("Please enter a valid number of days.", "bot")

                else:
                    if msg.lower() == "yes":
                        # self.ask_symptom("yes")
                        self.tree_to_code(self.clf, self.cols, self.disease_input, self.num_days)
                        self.user_input.delete(0, "end")
                    elif msg.lower() == "no":
                        self.handle_symptom_input("no")
                        self.user_input.delete(0, "end")
                        self.display_message("Please wait a moment...", "bot")
                        self.tree_to_code(self.clf, self.cols, self.disease_input, self.num_days)
                        self.disease_input = ""
                        self.num_days = 0
                    else:
                        self.display_message("Please enter 'yes' or 'no'.", "bot")
                # else: 
                #     if msg.lower() == "yes":
                #         self.symptoms_exp.append(self.syms)
                #     elif msg.lower() == "no":
                #         pass
                #     else :
                #         display_message("provide proper answers i.e. (yes/no) : ")


            else:
                return ""

    # def ask_symptom(self,):
    #     if self.symptoms_given:
    #         symptom = self.symptoms_given.pop(0)
    #         self.display_message(f"Are you experiencing {symptom}? (yes/no)", "bot")
    #         self.user_input.focus()
    #     else:
    #         # No more symptoms to ask, proceed to the next step
    #         self.display_message("Please wait a moment...", "bot")
    #         self.tree_to_code(self.clf, self.cols, self.disease_input, self.num_days)
    #         self.disease_input = ""
    #         self.num_days = 0

    # def handle_symptom_input(self, response):
    #     self.tree_to_code(self.clf, self.cols, self.disease_input, self.num_days)
    #     if response.strip().lower() == "yes":
    #         self.self.symptoms_exp.append(self.symptoms_given.pop(0))
    #     elif response.strip().lower() == "no":
    #         self.symptoms_given.pop(0)  # Remove the symptom from the list
    #     else:
    #         self.display_message("Please enter 'yes' or 'no'.", "bot")
    #         return

    #     # Proceed to ask the next symptom or proceed if there are no more symptoms
    #     self.ask_symptom()

    # def display_message(self, message, sender):
    #     self.chat_history.config(state="normal")
    #     if sender == "user":
    #         self.chat_history.insert("end", "\n ")
    #         self.chat_history.image_create("end", image=self.user_icon)
    #         self.chat_history.insert("end", " : ")
    #         justify = "right"  # Justify user's message to the right
    #     else:
    #         self.chat_history.insert("end", "\n ")
    #         self.chat_history.image_create("end", image=self.bot_icon)
    #         self.chat_history.insert("end", " : ")
    #         justify = "left"  # Justify system's message to the left

    #     self.chat_history.insert("end", f" {message}\n\n")
    #     self.chat_history.tag_configure(sender, foreground="#37474F", justify=justify)
    #     self.chat_history.config(state="disabled")


    def display_message(self, message, sender):
        self.chat_history.config(state="normal")
        
        self.chat_history.tag_configure("user", foreground="#ffffff", background="#263238", justify="right",font=("times new roman", 15))
        self.chat_history.insert("end", message + "\n\n", sender)
        self.chat_history.tag_configure("bot", foreground="#ffffff", background="#263238",justify="left",font=("times new roman", 15))
        self.chat_history.config(state="disabled")
        
    
    
    def load_icon(self, filename):
        icon = Image.open(filename)
        icon = icon.resize((20, 20), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        return icon


    def getDescription(self):
        with open('MasterData/symptom_Description.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                _description = {row[0]: row[1]}
                self.description_list.update(_description)  # Access description_list via the instance attribute

    def getSeverityDict(self):  # Add self parameter here
        with open('MasterData/symptom_severity.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            try:
                for row in csv_reader:
                    _diction = {row[0]: int(row[1])}
                    self.severityDictionary.update(_diction)
            except:
                pass

    def getprecautionDict(self):
        with open('MasterData/symptom_precaution.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
                self.precautionDictionary.update(_prec)

    def tree_to_code(self, tree, feature_names, disease_input, num_days):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        chk_dis = ",".join(feature_names).split(",")
        symptoms_present = []

        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                if name == disease_input:
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = self.print_disease(tree_.value[node])
                # print( "You may have " +  present_disease )
                red_cols = self.reduced_data.columns 
                symptoms_given = red_cols[self.reduced_data.loc[present_disease].values[0].nonzero()]
                # dis_list=list(symptoms_present)
                # if len(dis_list)!=0:
                #     print("symptoms present  " + str(list(symptoms_present)))
                # print("symptoms given "  +  str(list(symptoms_given)) )

                #print(Are you experiencing any) ##
                
                for self.syms in list(symptoms_given):
                    inp=""
                    # self.display_message(f"Are you experiencing any {self.syms} ? yes/no","bot")
                    # while True:
                    # inp=input("")
                    #     if(inp=="yes" or inp=="no"):
                    #         break
                    #     else:
                    #         print("provide proper answers i.e. (yes/no) : ",end="")
                    # if(inp=="yes"):
                    #     self.symptoms_exp.append(self.syms)

                    while True:
                        inp = messagebox.askyesno("Symptoms",f"Are you experiencing any {self.syms} ? yes/no ?")
                        break
                        
                    if(inp=="yes"):
                        self.symptoms_exp.append(self.syms)


                second_prediction=self.sec_predict(self.symptoms_exp)
                # print(second_prediction)
                self.calc_condition(self.symptoms_exp,num_days)
                if(present_disease[0]==second_prediction[0]):
                    self.display_message("You may have ", present_disease[0],"bot")
                    self.display_message(self.description_list[present_disease[0]],"bot")

                    # readn(f"You may have {present_disease[0]}")
                    # readn(f"{description_list[present_disease[0]]}")

                else:
                    self.display_message(f"You may have  {present_disease[0]} OR  {second_prediction[0]}" ,"bot")
                    self.display_message(self.description_list[present_disease[0]],"bot")
                    self.display_message(self.description_list[second_prediction[0]],"bot")

                # print(description_list[present_disease[0]])
                precution_list=self.precautionDictionary[present_disease[0]]
                # self.display_message("Take following measures : ","bot")

                for  i,j in enumerate(precution_list):
                    self.consultation+= f"{i+1}) {j} \n "
                self.display_message(f"Take following measures : \n {self.consultation}","bot")
                # confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
                # print("confidence level is " + str(confidence_level))

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
            input_vector[[symptoms_dict[item]]] = 1

        return rf_clf.predict([input_vector])

    def print_disease(self, node):
        node = node[0]
        val  = node.nonzero() 
        disease = self.le.inverse_transform(val[0])
        return list(map(lambda x: x.strip(), list(disease)))

    def calc_condition(self, exp, days):
        sum = 0
        for item in exp:
            try:
                sum += self.severityDictionary[item]
            except KeyError:
                self.display_message(f"KeyError: '{item}' not found in severity dictionary.","bot")

        if ((sum * days) / (len(exp) + 1) > 13):
            self.display_message("You should take the consultation from a doctor.","bot")
        else:
            self.display_message("It might not be that bad but you should take precautions.","bot")


if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = AskBot(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
