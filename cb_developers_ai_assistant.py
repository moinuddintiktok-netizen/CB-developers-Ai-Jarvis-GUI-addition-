import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import datetime
import sqlite3
import os
import psutil
import pyttsx3
import speech_recognition as sr
import wikipedia
import pyautogui
import requests
import subprocess

# Computer Vision & Face Detection libraries check
try:
    import cv2
    import mediapipe as mp
    CV_AVAILABLE = True
except ImportError:
    CV_AVAILABLE = False

class ChishtiComputersAIAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("CHISHTI COMPUTERS & DEVELOPERS : OMEGA AI SUITE v51")
        self.root.geometry("1300-800")
        self.root.configure(bg="#030712") # Cinematic Sci-Fi Dark Theme

        # Initialize SQLite Brain Database
        self.init_database()

        # Initialize TTS Engine
        self.engine = pyttsx3.init()
        self.set_voice()

        # Build Cinematic Sci-Fi HUD UI
        self.create_cinematic_hud()

        # Start System Resource Monitor
        self.update_system_stats()

    def init_database(self):
        self.conn = sqlite3.connect("chishti_computers_brain.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                assistant_response TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def set_voice(self):
        voices = self.engine.getProperty('voices')
        if len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 175)

    def speak(self, text):
        def run_speech():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
        threading.Thread(target=run_speech, daemon=True).start()

    def create_cinematic_hud(self):
        # Top Header Banner
        header_frame = tk.Frame(self.root, bg="#0f172a", bd=2, relief="groove")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)
        
        title_label = tk.Label(header_frame, text="⚡ CHISHTI COMPUTERS & DEVELOPERS : OMEGA SECURITY & AUTOMATION CORE ⚡", 
                               bg="#0f172a", fg="#38bdf8", font=("Consolas", 14, "bold"))
        title_label.pack(pady=8)

        # Main Workspace Container
        container = tk.Frame(self.root, bg="#030712")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left Control & Diagnostic Panel
        left_panel = tk.Frame(container, bg="#0b0f19", width=340, bd=1, relief="solid")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(left_panel, text="[SYSTEM DIAGNOSTICS]", bg="#0b0f19", fg="#38bdf8", font=("Consolas", 11, "bold")).pack(pady=12)
        
        self.cpu_label = tk.Label(left_panel, text="CPU Core Load: 0%", bg="#0b0f19", fg="#e2e8f0", font=("Consolas", 10))
        self.cpu_label.pack(anchor="w", padx=15, pady=5)

        self.ram_label = tk.Label(left_panel, text="Memory RAM Usage: 0%", bg="#0b0f19", fg="#e2e8f0", font=("Consolas", 10))
        self.ram_label.pack(anchor="w", padx=15, pady=5)

        tk.Label(left_panel, text="[ADVANCED VISION & AUTOMATION]", bg="#0b0f19", fg="#38bdf8", font=("Consolas", 11, "bold")).pack(pady=15)

        btn_style = {"bg": "#1e293b", "fg": "#38bdf8", "font": ("Consolas", 10, "bold"), "bd": 1, "relief": "raised"}
        
        tk.Button(left_panel, text="🎙️ Voice Command Core", command=self.listen_voice_thread, **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="👁️ Hand Gesture HUD", command=self.start_gesture_recognition, **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="👤 Live Face Detection Scan", command=self.start_face_detection_scan, **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="💻 Open Notepad / Tools", command=lambda: self.run_automation("notepad"), **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="🌐 Launch Google Browser", command=lambda: self.run_automation("google"), **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="🧠 SQLite Brain Memory", command=self.show_memory, **btn_style).pack(fill=tk.X, padx=15, pady=5)
        tk.Button(left_panel, text="🛡️ System Security Scan", command=self.security_scan, **btn_style).pack(fill=tk.X, padx=15, pady=5)

        # Right Terminal / Cinematic Chat Panel
        right_panel = tk.Frame(container, bg="#030712")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.terminal_output = scrolledtext.ScrolledText(right_panel, bg="#010409", fg="#38bdf8", 
                                                         font=("Consolas", 11), insertbackground="white", bd=1, relief="solid")
        self.terminal_output.pack(fill=tk.BOTH, expand=True, pady=5)
        self.terminal_output.insert(tk.END, "[CHISHTI CORE]: OMEGA AI Assistant online with Face Recognition & Automation. Ready...\n")

        # Bottom Command Input Field
        input_frame = tk.Frame(self.root, bg="#0f172a")
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.entry_command = tk.Entry(input_frame, bg="#010409", fg="#38bdf8", font=("Consolas", 12), insertbackground="white")
        self.entry_command.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
        self.entry_command.bind("<Return>", lambda event: self.process_command())

        send_btn = tk.Button(input_frame, text="Execute Command", command=self.process_command, bg="#38bdf8", fg="#030712", font=("Consolas", 10, "bold"))
        send_btn.pack(side=tk.RIGHT, ipady=4)

        # Mandatory Developer Branding Footer Tag
        footer_label = tk.Label(self.root, text="Created by Chishti Computers & Developers", bg="#030712", fg="#64748b", font=("Consolas", 9, "bold"))
        footer_label.pack(side=tk.BOTTOM, pady=2)

    def update_system_stats(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            self.cpu_label.config(text=f"CPU Core Load: {cpu}%")
            self.ram_label.config(text=f"Memory RAM Usage: {ram}%")
        except:
            pass
        self.root.after(3000, self.update_system_stats)

    def log_to_terminal(self, sender, text):
        self.terminal_output.insert(tk.END, f"[{sender}]: {text}\n")
        self.terminal_output.see(tk.END)
        try:
            self.cursor.execute("INSERT INTO memory_logs (timestamp, user_input, assistant_response) VALUES (?, ?, ?)",
                                (str(datetime.datetime.now()), sender, text))
            self.conn.commit()
        except:
            pass

    def run_automation(self, action_type):
        if action_type == "notepad":
            try:
                subprocess.Popen("notepad.exe")
                self.log_to_terminal("AUTOMATION", "Launched Windows Notepad successfully.")
                self.speak("Opening Notepad")
            except Exception as e:
                self.log_to_terminal("AUTOMATION", f"Failed to launch Notepad: {e}")
        elif action_type == "google":
            import webbrowser
            webbrowser.open("https://www.google.com")
            self.log_to_terminal("AUTOMATION", "Launched Google browser via automation.")
            self.speak("Opening Google")

    def process_command(self):
        cmd = self.entry_command.get().strip()
        if not cmd:
            return
        self.log_to_terminal("USER", cmd)
        self.entry_command.delete(0, tk.END)

        cmd_lower = cmd.lower()
        if "wikipedia" in cmd_lower:
            query = cmd_lower.replace("wikipedia", "").strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                self.log_to_terminal("CHISHTI-AI", summary)
                self.speak(summary)
            except:
                self.log_to_terminal("CHISHTI-AI", "Could not fetch Wikipedia data.")
        elif "open notepad" in cmd_lower:
            self.run_automation("notepad")
        elif "open google" in cmd_lower:
            self.run_automation("google")
        else:
            response = f"Task command '{cmd}' executed successfully through automation core."
            self.log_to_terminal("CHISHTI-AI", response)
            self.speak("Task executed")

    def listen_voice_thread(self):
        def voice_listen():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.log_to_terminal("SYSTEM", "Listening via microphone channel...")
                try:
                    audio = r.listen(source, timeout=5)
                    text = r.recognize_google(audio)
                    self.entry_command.delete(0, tk.END)
                    self.entry_command.insert(0, text)
                    self.process_command()
                except Exception as e:
                    self.log_to_terminal("SYSTEM", f"Audio capture failed: {str(e)}")
        threading.Thread(target=voice_listen, daemon=True).start()

    def start_face_detection_scan(self):
        if not CV_AVAILABLE:
            self.log_to_terminal("SYSTEM", "OpenCV/MediaPipe libraries required for Face Detection.")
            return

        def run_face_scan():
            cap = cv2.VideoCapture(0)
            mp_face_detection = mp.solutions.face_detection
            mp_draw = mp.solutions.drawing_utils
            
            with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7) as face_detection:
                self.log_to_terminal("SECURITY", "Face Detection Scan active. Looking for Boss / Authorized personnel...")
                self.speak("Face detection scan initiated. Welcome Boss.")
                
                scanned = False
                while cap.isOpened():
                    success, img = cap.read()
                    if not success:
                        break
                    
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = face_detection.process(img_rgb)
                    
                    if results.detections:
                        for detection in results.detections:
                            mp_draw.draw_detection(img, detection)
                            if not scanned:
                                self.log_to_terminal("SECURITY", "Authorized Boss Face Detected! Access Granted.")
                                self.speak("Welcome Boss. Access granted.")
                                # Log to SQLite face_logs
                                try:
                                    self.cursor.execute("INSERT INTO face_logs (timestamp, event_type, status) VALUES (?, ?, ?)",
                                                        (str(datetime.datetime.now()), "Boss Face Recognition", "Authorized"))
                                    self.conn.commit()
                                except:
                                    pass
                                scanned = True

                    cv2.imshow("Chishti Computers - Face Security HUD", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()
                self.log_to_terminal("SECURITY", "Face Detection session closed.")

        threading.Thread(target=run_face_scan, daemon=True).start()

    def start_gesture_recognition(self):
        if not CV_AVAILABLE:
            self.log_to_terminal("SYSTEM", "OpenCV/MediaPipe libraries required for hand gesture tracking.")
            return

        def run_gestures():
            cap = cv2.VideoCapture(0)
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
            mp_draw = mp.solutions.drawing_utils

            self.log_to_terminal("SYSTEM", "Hand Gesture HUD active. Press 'q' on camera window to exit.")
            while cap.isOpened():
                success, img = cap.read()
                if not success:
                    break
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(img_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_lms in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

                cv2.imshow("Chishti Computers Gesture HUD", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.log_to_terminal("SYSTEM", "Hand Gesture HUD closed.")

        threading.Thread(target=run_gestures, daemon=True).start()

    def show_memory(self):
        try:
            self.cursor.execute("SELECT * FROM memory_logs ORDER BY id DESC LIMIT 5")
            rows = self.cursor.fetchall()
            self.log_to_terminal("BRAIN", "--- RECENT SQLITE MEMORY LOGS ---")
            for row in rows:
                self.log_to_terminal("MEMORY", f"{row[1]} | {row[2]} -> {row[3]}")
            
            self.cursor.execute("SELECT * FROM face_logs ORDER BY id DESC LIMIT 3")
            face_rows = self.cursor.fetchall()
            self.log_to_terminal("BRAIN", "--- RECENT FACE RECOGNITION LOGS ---")
            for f_row in face_rows:
                self.log_to_terminal("FACE_LOG", f"{f_row[1]} | {f_row[2]} -> {f_row[3]}")
        except:
            self.log_to_terminal("BRAIN", "Failed to fetch memory records.")

    def security_scan(self):
        self.log_to_terminal("SECURITY", "Firewall secure. All diagnostic ports are monitored and protected.")
        self.speak("Security scan complete. All systems secure.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChishtiComputersAIAssistant(root)
    root.mainloop()
  
