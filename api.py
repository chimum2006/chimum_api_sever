from flask import Flask, jsonify, request
import cloudscraper, os
from DATA import get_info
scraper = cloudscraper.create_scraper()
app = Flask(__name__)
app.register_blueprint(get_info)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Xin Chào Bạn Đến Với Api !"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)