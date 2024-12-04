from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/api/board', methods=['GET'])
def hello_world():
    return jsonify({'board': 'Board placeholder'}), 200
