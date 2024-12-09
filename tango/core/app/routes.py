from flask import Blueprint, jsonify


tango_solve = Blueprint('tango/solve', __name__)

@tango_solve.route('/tango/solve', methods=['POST'])
def post():
    data = request.get_json()
    if not data:
        return jsonify("error": "Invalid payload"), 400

    try:
        payload = TangoSolveRequest(**data)

    except TypeError as e:
        return jsonify({"error": f"Invalid schema: {str(e)}"}), 400

    # Solve logic
    return jsonify({"placeholder": "hi"}), 200
