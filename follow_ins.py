from flask import jsonify, request, Blueprint
import requests

follow_instagram = Blueprint('follow_instagram', __name__)
@follow_instagram.route('/api/follow_instagram', methods=['POST'])
def job_follow_instagram():
    data = request.json
    idig = data.get('idig')
    cookie = data.get('cookie')
    if not idig or not cookie:
        return jsonify({"message": "Thiếu idig hoặc cookie !"}), 400
    try:
        csrftoken = cookie.split('csrftoken=')[1].split(';')[0]
    except:
        return jsonify({"message": "Cookie Không Đúng !"}), 400
    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
    }
    try:
        button_follow = requests.post(f'https://i.instagram.com/api/v1/web/friendships/{idig}/follow/', headers=headers).text
        if button_follow == '':
            return jsonify({"status": 200, "message": "Follow Instagram Success"}), 200
        else:
            return jsonify({"message": "Follow Instagram Fail !"}), 400
    except:
        return jsonify({"message": "Lỗi không xác định !"}), 400