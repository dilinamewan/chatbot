import customtkinter as ctk
import threading
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set appearance mode and theme
ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alex Chatbot")
        self.geometry("600x700")
        self.minsize(400, 500)

        self.configure(padx=15, pady=15)

        self.setup_ui()
        self.initialize_chatbot()

        self.add_message("Alex: Hi there! I'm Alex, your friendly assistant. How can I help you today?", "bot")

    def setup_ui(self):
        # Chat display area (read-only)
        self.chat_display = ctk.CTkTextbox(self, width=500, height=500, font=("Segoe UI", 13), wrap="word")
        self.chat_display.configure(state="disabled")
        self.chat_display.pack(fill="both", expand=True, pady=(0, 15))

        # Input + Button Frame
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x")

        self.user_input = ctk.CTkEntry(input_frame, placeholder_text="Type your message...", font=("Segoe UI", 13))
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)
        self.user_input.bind("<Return>", self.send_message)

        send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right")

    def initialize_chatbot(self):
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
        self.chat_display.configure(state="normal")
        prefix = "You: " if sender == "user" else ""
        self.chat_display.insert("end", f"{prefix}{message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self.add_message(user_message, "user")
        self.user_input.delete(0, "end")
        threading.Thread(target=self.get_bot_response, args=(user_message,), daemon=True).start()

    def get_bot_response(self, user_message):
        try:
            response = self.client.generate_content(user_message)
            self.add_message(f"Alex: {response.text}", "bot")
        except Exception as e:
            self.add_message(f"Alex: Oops, something went wrong! Error: {str(e)}", "bot")

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
