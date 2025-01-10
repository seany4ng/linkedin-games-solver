from dataclasses import asdict
from flask import Blueprint, jsonify, request
from core.queens.queens_generation import generate_random_queens_board
from core.tango.services import solve_tango_board
from core.app.schemas import QueensGenerationResponse, TangoGenerationResponse, TangoSolveRequest
from core.queens.services import solve_queens_board
from core.app.schemas import QueensSolveRequest
from core.tango.tango_board import VALUE_TO_STR_TYPE
from core.tango.tango_generation import convert_eqs_diffs_to_str, generate_random_tango_board

tango_solve = Blueprint('tango', __name__)
queens_solve = Blueprint('queens', __name__)


# BEGIN: Tango routes

@tango_solve.route('/solve', methods=['POST'])
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
    Expect: numEqDiff
    Response: TangoGenerateResponse
    """
    num_eq_diff = request.args.get("numEqDiff", default=8, type=int)
    (
        generated_board,
        eqs,
        diffs,
        solution,
    ) = generate_random_tango_board(num_eqs_or_diff=num_eq_diff)
    solution_str = [[VALUE_TO_STR_TYPE[x] for x in row] for row in solution]
    row_lines, col_lines = convert_eqs_diffs_to_str(
        eqs=eqs,
        diffs=diffs,
    )
    response = TangoGenerationResponse(
        board=generated_board,
        row_lines=row_lines,
        col_lines=col_lines,
        solution=solution_str,
    )
    return jsonify(asdict(response)), 200


# BEGIN: Queens routes

@queens_solve.route('/solve', methods=['POST'])
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


@queens_solve.route('/generate', methods=["GET"])
def get():
    """
    Expect: numRows
    Response: QueensGenerateResponse
    """
    num_rows = request.args.get("numRows", default=8, type=int)
    (
        _,
        generated_board,
        generated_solution,
    ) = generate_random_queens_board(
        n=num_rows,
    )
    response = QueensGenerationResponse(
        board_size=num_rows,
        board=generated_board,
        solution=generated_solution
    )
    return jsonify(asdict(response)), 200
