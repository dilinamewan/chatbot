class Chatbot:
    def __init__(self):
        self.greetings = ["hello", "hi", "hey"]
        self.farewells = ["bye", "goodbye", "see you later"]

    def respond_to_message(self, message):
        message = message.lower()
        if any(greet in message for greet in self.greetings):
            return "Hello! How can I assist you today?"
        elif any(farewell in message for farewell in self.farewells):
            return "Goodbye! Have a great day!"
        else:
            return "I'm sorry, I didn't understand that."