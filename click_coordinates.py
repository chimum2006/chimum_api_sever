from flask import request, jsonify, Blueprint
from PIL import Image
import cv2
import numpy as np
import base64
from io import BytesIO
import json
import os
from datetime import datetime

click_xy = Blueprint('click_xy', __name__)
ACTIVATION_FILE = "activation_api.json"

def decode_base64_image(b64_string):
    if ',' in b64_string:
        b64_string = b64_string.split(',')[1]
    img_data = base64.b64decode(b64_string)
    return Image.open(BytesIO(img_data))

def find_template_coords(big_img_pil, template_path):
    big = cv2.cvtColor(np.array(big_img_pil), cv2.COLOR_RGB2GRAY)
    small = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(big, small, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc, max_val

def load_activations():
    if not os.path.exists(ACTIVATION_FILE):
        return []
    try:
        with open(ACTIVATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_activations(data):
    with open(ACTIVATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@click_xy.route('/api/find_position', methods=['POST'])
def find_position():
    data = request.json
    image_b64 = data.get('image_base64')
    check = data.get('check')
    user_key = data.get('key')

    if not data or not image_b64 or not check or not user_key:
        return jsonify({
            "status": 401,
            "message": "Thiếu dữ liệu (image_base64, check hoặc key)!"
        }), 400

    activations = load_activations()
    today = datetime.now().strftime("%d/%m/%Y")
    matched = next((k for k in activations if k["key"] == user_key), None)

    if not matched:
        return jsonify({
            "status": 401,
            "message": "Vui lòng lấy key kích hoạt API !"
        }), 401

    if matched["created_at"] != today:

        activations = [k for k in activations if k["key"] != user_key]
        save_activations(activations)
        return jsonify({
            "status": 401,
            "message": "Key hết hạn. Vui lòng lấy key kích hoạt API hôm nay !"
        }), 403

    try:
        if check not in [
            'file', 'checknhafl', 'follow', 'comment', 'tim', 'trangchu',
            'live', 'copy_link', 'favourite', 'personal_check', 'share'
        ]:
            return jsonify({
                "status": 401,
                "message": "Giá trị check không hợp lệ !"
            }), 400

        TEMPLATE_PATH = f'templates/{check}.png'
        img_pil = decode_base64_image(image_b64)
        position, confidence = find_template_coords(img_pil, TEMPLATE_PATH)
        THRESHOLD = 0.5
        if confidence >= THRESHOLD:
            return jsonify({
                "status": 200,
                "matched": True,
                "position": {"x": position[0], "y": position[1]},
                "confidence": round(confidence, 4)
            }), 200
        else:
            return jsonify({
                "status": 201,
                "matched": False,
                "message": "Không tìm thấy ảnh trùng khớp.",
                "confidence": round(confidence, 4)
            }), 201

    except Exception as e:
        return jsonify({
            "status": 401,
            "message": "Lỗi tìm tọa độ (x, y)!",
            "error": str(e)
        }), 500
