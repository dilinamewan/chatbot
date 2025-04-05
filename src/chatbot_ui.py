import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alex Chatbot")
        self.root.geometry("600x700")
        self.root.minsize(400, 500)
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        self.initialize_chatbot()
        
        # Add initial greeting from Alex
        self.add_message("Alex: Hi there! I'm Alex, your friendly assistant. How can I help you today?", "bot")
    
    def setup_ui(self):
        """Set up the UI components"""
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = tk.Entry(input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", self.send_message)
        
        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
    
    def initialize_chatbot(self):
        """Initialize the Gemini client"""
        API_KEY = os.getenv("GOOGLE_API_KEY")
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in .env file or environment. Please set it to your Gemini API key.")
        
        genai.configure(api_key=API_KEY)
        self.client = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 500,
            },
            system_instruction="You are a friendly, helpful human named Alex. Respond in a warm, conversational tone as a knowledgeable assistant."
        )
    
    def add_message(self, message, sender):
        """Add a message to the chat display"""
        self.chat_display.configure(state='normal')
        if sender == "user":
            self.chat_display.insert(tk.END, f"You: {message}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"{message}\n", "bot")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Handle sending a message"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        self.add_message(user_message, "user")
        self.user_input.delete(0, tk.END)
        
        # Run chatbot response in a separate thread to avoid freezing the UI
        threading.Thread(target=self.get_bot_response, args=(user_message,), daemon=True).start()
    
    def get_bot_response(self, user_message):
        """Get the chatbot's response"""
        try:
            response = self.client.generate_content(user_message)
            self.add_message(f"Alex: {response.text}", "bot")
        except Exception as e:
            self.add_message(f"Alex: Oops, something went wrong! Error: {str(e)}", "bot")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()