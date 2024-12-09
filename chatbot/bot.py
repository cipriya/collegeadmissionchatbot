import joblib
import random
import json
import os
from datetime import datetime

class CollegeAdmissionChatbot:
    def __init__(self, model_path, dataset_path, log_path):
        # Load NLP model and dataset
        self.intent_model = joblib.load(model_path)
        with open(dataset_path, 'r') as f:
            self.dataset = json.load(f)["dataset"]
        
        # Load logging settings
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Prepare responses
        self.responses = {item["Category"]: item["Bot Response"] for item in self.dataset}
        self.default_response = "I'm sorry, I didn't understand that. Could you please clarify?"

    def get_response(self, user_query):
        # Predict the intent
        intent = self.intent_model.predict([user_query.lower()])[0]
        return self.responses.get(intent, self.default_response)
    
    def log_interaction(self, user_query, bot_response):
        # Save interaction logs
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_query": user_query,
            "bot_response": bot_response
        }
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def process_query(self, user_query):
        bot_response = self.get_response(user_query)
        self.log_interaction(user_query, bot_response)
        return bot_response

if __name__ == "__main__":
    chatbot = CollegeAdmissionChatbot(
        model_path='models/nlp/intent_model.pkl',
        dataset_path='data/training_data/college_admissions.json',
        log_path='logs/chatbot_logs.jsonl'
    )
    
    print("Chatbot is ready. Type 'exit' to quit.")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        response = chatbot.process_query(user_message)
        print(f"Chatbot: {response}")
