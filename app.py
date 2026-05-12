import os
import requests
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
# පින්තූරය 16MB වෙනකම් අවසර දෙනවා
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Hugging Face API Settings
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    if 'photo' not in request.files:
        return jsonify({"error": "Photo එකක් තෝරන්න!"}), 400
    
    file = request.files['photo']
    try:
        img_data = base64.b64encode(file.read()).decode("utf-8")
        
        payload = {
            "inputs": f"data:image/jpeg;base64,{img_data}",
            "parameters": {
                "do_sample": True,
                "max_new_tokens": 80,
                "prompt": "USER: <image>\nGive a very short, funny, and savage sarcastic roast about this person in English. Focus on their style. ASSISTANT:"
            }
        }
        
        # API එකට request එක යැවීම
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            raw_text = output[0].get('generated_text', '')
            roast_msg = raw_text.split("ASSISTANT:")[-1].strip()
            return jsonify({"roast": roast_msg})
        else:
            return jsonify({"error": "AI is busy. Try again!"}), 500

    except Exception as e:
        return jsonify({"error": "Connection slow, try a smaller photo"}), 500

# Vercel needs this
app = app
        
