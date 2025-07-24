from flask import Flask, jsonify, request
import os
from get_info_golike import get_info
from follow_ins import follow_instagram
from click_coordinates import click_xy
from compare_image import compare

app = Flask(__name__)
app.register_blueprint(get_info)
app.register_blueprint(follow_instagram)
app.register_blueprint(click_xy)
app.register_blueprint(compare)


@app.route('/', methods=['GET'])
def hello():
    established_date = "13/07/2025"
    zalo_admin = "0834617174"
    return jsonify({
        "Author": "Chí Mum",
        "admin_zalo": zalo_admin,
        "established_date": established_date,
        "message": "Welcome to API"
    }), 200
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
