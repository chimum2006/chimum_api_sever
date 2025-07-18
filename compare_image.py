from flask import request, jsonify, Blueprint
import base64
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

compare = Blueprint('compare', __name__)

def decode_base64_image(b64_string):
    """Chuyển base64 thành ảnh PIL"""
    if ',' in b64_string:
        b64_string = b64_string.split(',')[1]
    img_data = base64.b64decode(b64_string)
    return Image.open(BytesIO(img_data))

def compare_with_template(image_pil, template_path):
    """So sánh ảnh người dùng gửi với ảnh mẫu"""
    image_gray = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2GRAY)
    template_gray = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    return max_val

@compare.route('/api/compare_image', methods=['POST'])
def compare_imsa():
    data = request.json
    image_b64 = data.get('image_base64')
    check = data.get('check')
    if not data or not image_b64 or not check:
        return jsonify({"message": "Thiếu dữ liệu (image_base64 hoặc check) !"}), 400

    try:
        if check not in ['file', 'checknhafl', 'follow', 'comment', 'tim', 'trangchu', 'live', 'copy_link', 'favourite', 'personal_check', 'share']:
            return jsonify({
                "status": 100,
                "message": "Giá trị check không hợp lệ !"
            }), 400
        TEMPLATE_PATH = f'templates/{check}.png'  # ảnh mẫu
        img_user = decode_base64_image(data['image_base64'])
        confidence = compare_with_template(img_user, TEMPLATE_PATH)
        THRESHOLD = 0.8
        if confidence >= THRESHOLD:
            return jsonify({
                "status": 200,
                "matched": True,
                "message": "Image trùng khớp !"
            }), 200
        else:
            return jsonify({
                "status": 201,
                "matched": False,
                "message": "Image không khớp !"
            }), 201

    except Exception as e:
        return jsonify({"message": "Lỗi so sánh image !"}), 500
