from flask import Flask, request, jsonify
from embeddings import create_embeddings
import requests
import threading
import time

app = Flask(__name__)

# Load vector store when the application starts
url = "https://brainlox.com/courses/category/technical"
vector_store = create_embeddings(url)



def generate_response(user_input, saved_information):
    # Add an LLM layer here this would make it so that the responses given out are more cohorent although so training
    # data would be necessary
    return saved_information


@app.route('/chat', methods=['POST'])
def chat():
    print(f"Received request method: {request.method}")
    user_input = request.json.get('input')

    response = vector_store.similarity_search(user_input, k=1)  # Get the closest match
    if response:
        # Done like this to work even for k>1
        response_list = [x.page_content for x in response]
        final_response = "   ".join(response_list)
        return jsonify({'response': final_response})
    else:
        return jsonify({'response': ""}), 404


@app.route('/', methods=['GET'])
def index():
    return "Flask server is running."


def talk_to_chatbot():
    url = "http://127.0.0.1:5000/chat"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Keep trying to send the request until the server is up
        while True:
            try:
                api_response = requests.post(url, json={"input": user_input})

                if api_response.status_code == 200:
                    chat_bot_response = api_response.json().get("response")
                    bot_response = generate_response(user_input, chat_bot_response)
                    print("Bot:", bot_response)
                    break
                else:
                    print("Error:", response.json().get("error"))
                    break
            except requests.exceptions.ConnectionError:
                print("Waiting for the server to start...")
                time.sleep(1)  # Wait before retrying


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    flask_thread.start()

    while True:
        try:
            response = requests.get("http://127.0.0.1:5000/")
            if response.status_code == 200:  # 200 means the server is accessible
                print("Flask server is running, starting chatbot interaction.")
                break
        except requests.exceptions.ConnectionError:
            print("Waiting for the server to start...")
            time.sleep(1)  # Wait before retrying

    # Run the chatbot interaction
    talk_to_chatbot()
