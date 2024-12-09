from flask import Flask, request, jsonify
from chatbot.bot import CollegeAdmissionChatbot

# Initialize Flask app
app = Flask(__name__)

# Load chatbot
chatbot = CollegeAdmissionChatbot(
    model_path='models/nlp/intent_model.pkl',
    dataset_path='data/training_data/college_admissions.json',
    log_path='logs/chatbot_logs.jsonl'
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Parse user query from the request
        user_query = request.json.get('query', '')
        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        # Process query and get chatbot response
        bot_response = chatbot.process_query(user_query)
        return jsonify({"query": user_query, "response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        # Fetch interaction logs
        with open('logs/chatbot_logs.jsonl', 'r') as f:
            logs = [json.loads(line) for line in f.readlines()]
        return jsonify(logs)
    except FileNotFoundError:
        return jsonify({"error": "No logs found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
