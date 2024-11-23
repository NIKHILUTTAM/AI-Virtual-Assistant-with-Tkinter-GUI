import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import threading
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class VirtualAssistant:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("AI Virtual Assistant")
        self.window.geometry("600x700")
        
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Load intents with simpler pattern matching
        self.intents = {
            "greeting": ["hello", "hi", "hey", "greetings"],
            "goodbye": ["bye", "goodbye", "see you", "exit"],
            "time": ["time", "what time", "current time"],
            "weather": ["weather", "temperature", "forecast"],
            "search": ["search", "look up", "find"],
            "joke": ["joke", "tell me a joke", "make me laugh"]
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)
        
        # Input field
        self.input_field = tk.Entry(self.window, width=50)
        self.input_field.pack(padx=10, pady=5)
        self.input_field.bind('<Return>', lambda e: self.process_text_input())
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)
        
        # Send button
        send_button = tk.Button(button_frame, text="Send", command=self.process_text_input)
        send_button.pack(side=tk.LEFT, padx=5)
        
        # Voice input button
        voice_button = tk.Button(button_frame, text="🎤 Speak", command=self.start_voice_input)
        voice_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.window, text="Ready", fg="green")
        self.status_label.pack(pady=5)
        
    def update_chat(self, message, sender="You"):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self.chat_area.see(tk.END)
        
    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass
        
    def process_text_input(self):
        user_input = self.input_field.get().strip()
        if user_input:
            self.input_field.delete(0, tk.END)
            self.update_chat(user_input)
            
            # Get and display assistant's response immediately
            response = self.get_response(user_input)
            self.update_chat(response, "Assistant")
            
            # Speak the response in a separate thread
            threading.Thread(target=lambda: self.speak(response), daemon=True).start()
            
    def start_voice_input(self):
        self.status_label.config(text="Listening...", fg="blue")
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
        
    def listen_for_speech(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                self.window.after(0, lambda: self.process_voice_input(text))
        except Exception as e:
            self.window.after(0, self.status_label.config, {"text": f"Error: {str(e)}", "fg": "red"})
        finally:
            self.window.after(0, self.status_label.config, {"text": "Ready", "fg": "green"})
            
    def process_voice_input(self, text):
        self.update_chat(text)
        response = self.get_response(text)
        self.update_chat(response, "Assistant")
        threading.Thread(target=lambda: self.speak(response), daemon=True).start()
        
    def get_response(self, text):
        # Convert input to lowercase for matching
        text_lower = text.lower().strip()
        
        # Check each intent for matches
        for intent, patterns in self.intents.items():
            if any(pattern in text_lower for pattern in patterns):
                return self.handle_intent(intent, text)
        
        # Default response if no intent matches
        return "I'm not sure how to help with that. Could you please rephrase?"
        
    def handle_intent(self, intent, text):
        if intent == "greeting":
            responses = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! How may I assist you?",
                "Greetings! How can I be of service?"
            ]
            return random.choice(responses)
            
        elif intent == "joke":
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What did the grape say when it got stepped on? Nothing, it just let out a little wine!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a bear with no teeth? A gummy bear!"
            ]
            return random.choice(jokes)
            
        elif intent == "time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
            
        elif intent == "weather":
            return "I'm sorry, but I need to be configured with a weather API key to provide weather information."
            
        elif intent == "search":
            search_query = text.lower().replace("search", "").replace("look up", "").replace("find", "").strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return f"I've opened a search for '{search_query}'"
            return "What would you like me to search for?"
            
        elif intent == "goodbye":
            responses = [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! Let me know if you need anything else!"
            ]
            return random.choice(responses)

    def run(self):
        self.input_field.focus_set()
        self.window.mainloop()

if __name__ == "__main__":
    assistant = VirtualAssistant()
    assistant.run()