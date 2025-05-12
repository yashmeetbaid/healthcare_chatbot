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
        self.root.title("HealthAssist AI - About")
        self.root.geometry("900x750")
        self.root.resizable(False, False)  # Fix window size for professional look
        
        # Set custom icon if available
        try:
            self.root.iconbitmap("Images/icon.ico")
        except:
            pass  # Use default icon if custom one not available
            
        # Set base background color
        self.root.configure(bg="#192024")
        
        # Create main container with scrollbar
        main_container = Frame(self.root, bg="#192024")
        main_container.pack(fill=BOTH, expand=1)
        
        # Create canvas with scrollbar
        self.canvas = Canvas(main_container, bg="#192024", highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        # Add scrollbar to canvas
        scrollbar = ttk.Scrollbar(main_container, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create another frame inside the canvas
        self.content_frame = Frame(self.canvas, bg="#192024")
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Bind mousewheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Add all content to the content frame
        self.create_content()
        
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_content(self):
        """Create all content for the About page"""
        # Create main frame with border effect
        main_frame = Frame(self.content_frame, bg="#263238", bd=0)
        main_frame.pack(padx=20, pady=20, fill=BOTH, expand=1)
        
        # Header section
        header_frame = Frame(main_frame, bg="#1E2A2F", pady=10)
        header_frame.pack(fill=X)
        
        # Logo and title in a horizontal layout
        logo_title_frame = Frame(header_frame, bg="#1E2A2F")
        logo_title_frame.pack(fill=X, padx=20)
        
        # Logo
        try:
            img = Image.open("Images/geminilogo.png")
            img = img.resize((70, 70), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            logo_label = Label(logo_title_frame, image=self.photoimg, bg="#1E2A2F")
            logo_label.pack(side=LEFT, padx=(0, 20))
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback if image not found
            logo_label = Label(logo_title_frame, text="HA", font=("Arial", 24, "bold"), bg="#1E2A2F", fg="#4169E1", width=3, height=2)
            logo_label.pack(side=LEFT, padx=(0, 20))
        
        # Title and subtitle in vertical layout
        title_frame = Frame(logo_title_frame, bg="#1E2A2F")
        title_frame.pack(side=LEFT, fill=BOTH, expand=1)
        
        # Title
        title_lbl = Label(title_frame, text="HealthAssist AI", font=("Montserrat", 28, "bold"), bg="#1E2A2F", fg="white", anchor="w")
        title_lbl.pack(fill=X)
        
        # Subtitle
        subtitle_lbl = Label(title_frame, text="Your Personal Health Assistant", font=("Montserrat", 14), bg="#1E2A2F", fg="#90CAF9", anchor="w")
        subtitle_lbl.pack(fill=X)
        
        # Main content area
        content_area = Frame(main_frame, bg="#263238", padx=20, pady=20)
        content_area.pack(fill=BOTH, expand=1)
        
        # About section
        about_frame = Frame(content_area, bg="#2C3940", bd=1, relief=RIDGE)
        about_frame.pack(fill=X, pady=(0, 15))
        
        about_title = Label(about_frame, text="About", font=("Montserrat", 18, "bold"), bg="#2C3940", fg="white", anchor="w", padx=15, pady=10)
        about_title.pack(fill=X)
        
        about_content = """HealthAssist AI is an advanced medical diagnostic and health advice application that uses 
artificial intelligence to help users identify potential health conditions based on their symptoms. 
The application is designed to provide preliminary insights and guidance, bridging the gap between 
self-diagnosis and professional medical consultation."""
        
        about_label = Label(about_frame, text=about_content, font=("Montserrat", 12), bg="#2C3940", fg="white", justify=LEFT, wraplength=820, padx=15, pady=10)
        about_label.pack(fill=X)
        
        # Features section
        features_frame = Frame(content_area, bg="#2C3940", bd=1, relief=RIDGE)
        features_frame.pack(fill=X, pady=(0, 15))
        
        features_title = Label(features_frame, text="Key Features", font=("Montserrat", 18, "bold"), bg="#2C3940", fg="white", anchor="w", padx=15, pady=10)
        features_title.pack(fill=X)
        
        # Feature list
        features = [
            ("🔍 Symptom Analysis", "Comprehensive assessment of user-reported symptoms using advanced pattern recognition"),
            ("💊 Medical Support", "Evidence-based information and guidance related to potential conditions"),
            ("🩺 AI Diagnosis", "Preliminary diagnosis suggestions using machine learning classification algorithms"),
            ("🥗 Health Recommendations", "Personalized lifestyle and dietary advice to improve overall wellness"),
            ("⚠️ Risk Assessment", "Identification of potential risk factors and preventive measures"),
            ("📊 Health Tracking", "Monitor your symptoms and health trends over time with visual analytics"),
            ("📱 24/7 Availability", "Access health insights anytime, anywhere without waiting for appointments")
        ]
        
        # Create feature entries with alternating background for better readability
        for i, (title, desc) in enumerate(features):
            bg_color = "#364049" if i % 2 == 0 else "#2C3940"
            feature_frame = Frame(features_frame, bg=bg_color, padx=15, pady=8)
            feature_frame.pack(fill=X)
            
            feature_title = Label(feature_frame, text=title, font=("Montserrat", 14, "bold"), bg=bg_color, fg="white", anchor="w")
            feature_title.pack(fill=X)
            
            feature_desc = Label(feature_frame, text=desc, font=("Montserrat", 12), bg=bg_color, fg="#D0D0D0", anchor="w")
            feature_desc.pack(fill=X)
        
        # Technology section
        tech_frame = Frame(content_area, bg="#2C3940", bd=1, relief=RIDGE)
        tech_frame.pack(fill=X, pady=(0, 15))
        
        tech_title = Label(tech_frame, text="Our Technology", font=("Montserrat", 18, "bold"), bg="#2C3940", fg="white", anchor="w", padx=15, pady=10)
        tech_title.pack(fill=X)
        
        tech_content = """HealthAssist AI utilizes cutting-edge machine learning algorithms and natural language 
processing to deliver accurate health insights:

• Decision Tree Classification: Analyzes symptom patterns to identify potential conditions
• Support Vector Machines (SVM): Provides high-precision classification for complex cases
• Natural Language Processing: Understands user descriptions of symptoms in everyday language
• Continuously Updated Medical Database: Incorporates the latest medical research and findings

Our system is trained on extensive medical datasets from reputable sources and undergoes 
regular validation by healthcare professionals to ensure accuracy and relevance."""
        
        tech_label = Label(tech_frame, text=tech_content, font=("Montserrat", 12), bg="#2C3940", fg="white", justify=LEFT, wraplength=820, padx=15, pady=10)
        tech_label.pack(fill=X)
        
        # Important notice
        notice_frame = Frame(content_area, bg="#1E2A2F", bd=1, relief=RIDGE)
        notice_frame.pack(fill=X, pady=(0, 15))
        
        notice_title = Label(notice_frame, text="⚠️ Important Notice", font=("Montserrat", 16, "bold"), bg="#1E2A2F", fg="#FF9800", anchor="w", padx=15, pady=10)
        notice_title.pack(fill=X)
        
        notice_content = """HealthAssist AI is designed to serve as a preliminary screening tool, not a replacement
for professional medical advice. The information provided by this application should 
never be used to disregard professional medical advice or delay seeking it. Always consult 
with qualified healthcare professionals for proper diagnosis, treatment plans, and 
medical guidance tailored to your specific health situation."""
        
        notice_label = Label(notice_frame, text=notice_content, font=("Montserrat", 12, "bold"), bg="#1E2A2F", fg="#E0E0E0", justify=LEFT, wraplength=820, padx=15, pady=10)
        notice_label.pack(fill=X)
        
        # Footer section with gradient effect
        footer_frame = Frame(main_frame, bg="#1E2A2F", padx=20, pady=15)
        footer_frame.pack(fill=X, side=BOTTOM)
        
        # Add a subtle line separator above footer
        separator = Frame(main_frame, bg="#4169E1", height=2)
        separator.pack(fill=X, side=BOTTOM)
        
        # Version and copyright info
        version_label = Label(footer_frame, text="Version 1.2.5", font=("Montserrat", 10), bg="#1E2A2F", fg="#90CAF9")
        version_label.pack(anchor="w")
        
        copyright_label = Label(footer_frame, text="© 2025 HealthAssist AI - All Rights Reserved", font=("Montserrat", 10), bg="#1E2A2F", fg="#90CAF9")
        copyright_label.pack(anchor="w")
        
        # Developer information
        dev_label = Label(footer_frame, text="Developed with ❤️ by Team Zenith", 
                     font=("Montserrat", 10, "italic"), bg="#1E2A2F", fg="#90CAF9")
        dev_label.pack(anchor="w")

def launch_about_page():
    """Function to launch the About page independently"""
    root = tk.Tk()
    app = About(root)
    # Center window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 750) // 2
    root.geometry(f"900x750+{x}+{y}")
    root.mainloop()
    return app

if __name__ == "__main__":
    launch_about_page()
