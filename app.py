import os
import requests
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Security: Hugging Face Token එක කෙලින්ම කෝඩ් එකේ නොදා Variable එකක් විදිහට ගන්නවා
# Render එකේ Settings වල 'HF_TOKEN' කියලා මේක දාන්න පුළුවන්
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400
    
    file = request.files['photo']
    img_data = base64.b64encode(file.read()).decode("utf-8")
    
    payload = {
        "inputs": f"data:image/jpeg;base64,{img_data}",
        "parameters": {
            "do_sample": True,
            "max_new_tokens": 100,
            "prompt": "USER: <image>\nGive a very funny, short sarcastic roast about this person in the photo. Focus on their expression or vibe. Be witty. ASSISTANT:"
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        output = response.json()
        raw_text = output[0]['generated_text']
        # AI එකේ උත්තරේ විතරක් වෙන් කරලා ගැනීම
        roast_msg = raw_text.split("ASSISTANT:")[-1].strip()
        return jsonify({"roast": roast_msg})
    except Exception as e:
        return jsonify({"error": "AI is busy or error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
