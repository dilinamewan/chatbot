def load_data(file_path):
    # Function to load data from a given file path
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def format_response(response):
    # Function to format the chatbot's response
    return response.strip().capitalize()