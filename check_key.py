from flask import request, jsonify, Blueprint
import json, os
from datetime import datetime

check_key = Blueprint('check_key', __name__)

KEY_FILE = "key_store.json"
ACTIVATION_FILE = "activation_api.json"

def load_json_file(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@check_key.route('/api_sever_cm_tool/check_key', methods=['POST'])
def check_key_CM():
    data = request.get_json()
    user_key = data.get("key")

    if not user_key:
        return jsonify({"status": "error", "message": "Key không được để trống"}), 400

    keys = load_json_file(KEY_FILE)
    activations = load_json_file(ACTIVATION_FILE)
    today = datetime.now().strftime("%d/%m/%Y")

    matched_key = next((k for k in keys if k["key"] == user_key), None)

    if not matched_key:
        return jsonify({"status": "error", "message": "Key không tồn tại trên sever !"}), 401

    if matched_key["created_at"] != today:
        keys = [k for k in keys if k["key"] != user_key]
        save_json_file(KEY_FILE, keys)
        return jsonify({"status": "error", "message": "Key không đúng hoặc đã hết hạn !"}), 403

    if any(k["key"] == user_key for k in activations):
        return jsonify({
            "status": "success",
            "message": "Key đã được kích hoạt trước đó",
            "data": matched_key
        }), 200
    
    activations.append(matched_key)
    save_json_file(ACTIVATION_FILE, activations)

    return jsonify({
        "status": "success",
        "message": "Key hợp lệ và đã được kích hoạt",
        "data": matched_key
    }), 200