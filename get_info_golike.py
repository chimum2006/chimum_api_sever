from flask import jsonify, request, Blueprint
import cloudscraper
scraper = cloudscraper.create_scraper()
get_info = Blueprint('get_info', __name__)
@get_info.route('/api/information_golike', methods=['POST'])
def get_information_golike():
    auth_header = request.headers.get('Authorization')
    Bearer_token = auth_header.split(' ')[0]
    if Bearer_token != "Bearer":
        return jsonify({"message": "Sai Định Dạng Của Authorization Golike !"}), 400
    
    response = scraper.get('https://gateway.golike.net/api/users/me', headers={'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=utf-8', 'Authorization': auth_header, 't': 'VFZSak1FOVVZelZPYWxrelRrRTlQUT09', 'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'}).json()
    if 'status' in response and response['status'] == 200:
        username = response['data']['username']
        coin = response['data']['coin']
        data_extra = {
            "username": username,
            "coin": coin
        }
        return jsonify({"status": 200, "data": data_extra, "message": "Login Golike Success"}), 200
    else:
        return jsonify({"message": "Authorization Golike Của Bạn Không Chính Xác"}), 400
