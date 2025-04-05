import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def initialize_chatbot():
    """Initialize the Gemini client with system instructions"""
    # Get API key from environment variable
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env file or environment. Please set it to your Gemini API key.")
    
    genai.configure(api_key=API_KEY)
    
    client = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Using a supported model
        generation_config={
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 500,
        },
        system_instruction="You are a friendly, helpful human named Alex. Respond in a warm, conversational tone as a knowledgeable assistant."
    )
    return client

def chat_with_alex():
    """Main chat function to interact with Alex"""
    client = initialize_chatbot()
    
    print("Hi there! I'm Alex, your friendly assistant. How can I help you today? (Type 'quit' to stop)")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Alex: Goodbye! It was nice chatting with you. Take care!")
            break
        
        try:
            response = client.generate_content(user_input)
            print("Alex:", response.text)
        except Exception as e:
            print(f"Alex: Oops, something went wrong! Error: {str(e)}")
            print("Alex: Let’s try that again—how can I assist you?")

def main():
    """Main function to run the chatbot"""
    try:
        print("Starting Alex Chatbot...")
        chat_with_alex()
    except KeyboardInterrupt:
        print("\nAlex: Caught me mid-sentence! Bye for now!")
    except Exception as e:
        print(f"Alex: Uh-oh, something broke! Error: {str(e)}")

if __name__ == "__main__":
    main()