import json
from flask import Flask, request, jsonify, send_from_directory
from fuzzywuzzy import fuzz
import os

# 初始化 Flask 應用
app = Flask(__name__, static_url_path='', static_folder='public')

# 讀取 FAQ 資料
with open('question.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

# 定義處理靜態文件的路由
@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)

# 定義處理 /submit POST 請求的路由
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json  # 解析 JSON 請求
    if not data:
        return jsonify({"response": "No data received"}), 400
    print("Received data:", data)  # 輸出接收到的數據
    return jsonify({"response": "數據已接收"}), 200

# 定義處理 /process POST 請求的路由
@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    user_input = data.get('text')
    if not user_input:
        return jsonify({"response": "No text provided"}), 400

    best_match, best_score = None, 0
    best_question = None
    for item in faq_data:
        question = item["question"]
        score = fuzz.ratio(user_input, question)
        if score > best_score:
            best_score, best_match = score, item["response"]
            best_question = item["question"]

    if best_score >= 70:
        response = best_match
    elif best_score >= 50:
        response = f"您是指「{best_question}」嗎？"
    else:
        response = "抱歉，我不太理解您的意思。"

    return jsonify({"response": response}), 200  # 返回 JSON 格式的字典

# 啟動伺服器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
