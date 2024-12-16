from flask import Blueprint, jsonify, request
from core.tango.services import solve_tango_board
from core.app.schemas import TangoSolveRequest


tango_solve = Blueprint('tango/solve', __name__)

@tango_solve.route('/tango/solve', methods=['POST'])
def post():
    """
    Expect: TangoSolveRequest
    Response: {
        "solved_board": list[list[str]],
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    try:
        payload = TangoSolveRequest(**data)

    except TypeError as e:
        return jsonify({"error": f"Invalid schema: {str(e)}"}), 400

    # Solve logic
    solved_board_str: list[list[str]] = solve_tango_board(
        board=payload.board,
        vertical_lines=payload.vertical_lines[:6],
        horizontal_lines=payload.horizontal_lines[:6],
    )
    return jsonify({
        "solved_board": solved_board_str,
    }), 200
