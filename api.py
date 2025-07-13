from flask import Flask, jsonify, request
import cloudscraper
from DATA import get_info
scraper = cloudscraper.create_scraper()
app = Flask(__name__)
app.register_blueprint(get_info)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Xin Chào Bạn Đến Với Api !"}), 200

if __name__ == '__main__':
    app.run(debug=True)

