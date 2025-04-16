import requests
import json
import time
import os
import pygame
from flask import Flask, render_template, request, jsonify

pygame.mixer.init()  

app = Flask(__name__)

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file) 
    pygame.mixer.music.play()  
@app.route('/')
def index():
    return render_template('index.html') 
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    tu_khoa = data.get('tu_khoa')
    phong_cach = data.get('phong_cach')

    phong_cach_dict = {
        "1": "phong cách hài hước, dễ thương, khiến người đọc cười 😄",
        "2": "phong cách nhẹ nhàng, tình cảm và ngọt ngào 💕",
        "3": "phong cách trầm lắng, sâu sắc và mang hơi hướng cảm xúc 🌌",
        "4": "phong cách mang tính học thuật, logic, thông minh 📘",
        "5": "phong cách ngẫu hứng, sáng tạo không giới hạn 🌈"
    }
    phong_cach_text = phong_cach_dict.get(phong_cach, phong_cach_dict["5"])  

    prompt = f"Hãy viết một câu tiếng Việt rõ nghĩa, hợp ngữ cảnh từ: '{tu_khoa}'. " \
             f"Phong cách thể hiện: {phong_cach_text}. Thêm icon dễ thương vào cuối câu."

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'gemma3:4b',
            'prompt': prompt,
            'stream': True,
            'temperature': 0.7,
        },
        stream=True,
    )

    # Lấy kết quả từ response
    generated_text = ""
    for line in response.iter_lines():
        if line:
            try:
                data = line.decode('utf-8')
                json_data = json.loads(data)
                text_chunk = json_data.get("response", "")
                generated_text += text_chunk
                words = generated_text.split()
                max_words = 50 
                if len(words) > max_words:
                    generated_text = ' '.join(words[:max_words]) + '...'
            except Exception as e:
                print(f"Lỗi khi xử lý dòng: {e}")
    
    play_sound("./am_thanh/snd_fragment_retrievewav-14728.mp3")  

    return jsonify({"sentence": generated_text}) 

if __name__ == '__main__':
    app.run(debug=True)
