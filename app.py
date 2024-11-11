import json
from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz


app = Flask(__name__)

""" faq_data = [
    {"question": "入學規定", "answer": "入學規定的詳細資訊..."},
    # 其他問答
] """
with open('question.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    user_input = data.get('text')
    if not user_input:
        return jsonify({"response": "No text provided"}), 400

    best_match, best_score = None, 0
    for item in faq_data:
        question = item["question"]
        score = fuzz.ratio(user_input, question)
        if score > best_score:
            best_score, best_match = score, item["response"]

    if best_score >= 70:
        response = best_match
    elif best_score >= 50:
        response = f"您是指「{question}」嗎？"
    else:
        response = "抱歉，我不太理解您的意思。"

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
