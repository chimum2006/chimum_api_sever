from flask import Flask, request, jsonify, Blueprint
import os
import json
import uuid
from datetime import datetime

get_key = Blueprint('get_key', __name__)
KEY_STORE_FILE = "key_store.json"

def load_keys():
    if os.path.exists(KEY_STORE_FILE):
        with open(KEY_STORE_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except:
                pass
    return []

def save_keys(data):
    with open(KEY_STORE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_key():
    return "CM_ASE_" + uuid.uuid4().hex[:10].upper()

def get_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)

@get_key.route('/api_sever_cm_tool/get_key', methods=['GET'])
def generate_key_route():
    ip = get_ip()
    today = datetime.now().strftime("%d/%m/%Y")
    keys = load_keys()
    for entry in keys:
        if entry["ip"] == ip:
            return jsonify({
                "status": False,
                "message": "This IP has already generated a key.",
                "ip": ip,
                "key": entry["key"],
                "created_at": entry["created_at"]
            }), 200

    new_key = generate_key()
    key_entry = {
        "ip": ip,
        "key": new_key,
        "created_at": today
    }
    keys.append(key_entry)
    save_keys(keys)

    return jsonify({
        "status": True,
        "message": "A new key has been generated successfully.",
        "ip": ip,
        "key": new_key,
        "created_at": today
    }), 200