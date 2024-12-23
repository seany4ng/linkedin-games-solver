from flask import Blueprint, jsonify, request
from core.tango.services import solve_tango_board
from core.app.schemas import TangoSolveRequest
from core.queens.services import solve_queens_board
from core.app.schemas import QueensSolveRequest

tango_solve = Blueprint('tango/solve', __name__)
queens_solve = Blueprint('queens/solve', __name__)


# BEGIN: Tango routes

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


@tango_solve.route('/generate', methods=["GET"])
def get():
    """
    Expect: TangoGenerateRequest
    Response: TangoGenerateResponse
    """
    return jsonify({"TODO": "finish this"}), 200


# BEGIN: Queens routes

@queens_solve.route('/queens/solve', methods=['POST'])
def post():
    """
    Expect: QueensSolveRequest
    Response: {
        "solved_board": list[list[int]],
    }
    """
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    try:
        payload = QueensSolveRequest(**data)

    except TypeError as e:
        return jsonify({"error": f"Invalid schema: {str(e)}"}), 400

    # Solve logic
    solved_board: list[list[int]] = solve_queens_board(
        board_size=payload.board_size,
        board=payload.board,
    )
    return jsonify({
        "solved_board": solved_board,
    }), 200
