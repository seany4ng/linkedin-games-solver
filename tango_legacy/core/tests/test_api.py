import json
from core.tango.tango_board import BOARD_SIZE


def test_tango_api(client):
    """
    Tango no. 57.
    Source: https://www.linkedin.com/posts/tango-game_tango-no-57-activity-7269621400477327361-NWjE
    This test is intended to ensure the API works as desired by setting up a test client
    """
    # Arrange
    board = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    board[0][0] = "O"
    board[0][1] = "O"
    board[1][0] = "O"
    board[1][1] = "O"
    vertical_lines = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    horizontal_lines = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    vertical_lines[2][2] = "="
    vertical_lines[3][2] = "="
    vertical_lines[4][4] = "x"
    vertical_lines[5][4] = "x"

    horizontal_lines[2][2] = "="
    horizontal_lines[2][3] = "="
    horizontal_lines[4][4] = "x"
    horizontal_lines[4][5] = "x"

    body = {
        "board": board,
        "vertical_lines": vertical_lines,
        "horizontal_lines": horizontal_lines,
    }

    # Act
    response = client.post(
        "/tango/solve",
        data=json.dumps(body),
        content_type="application/json",
    )

    # Assert
    assert response.status_code == 200
    solved_board = response.get_json().get("solved_board")
    assert solved_board

    expected_board = (
        [
            ["O", "O", "X", "X", "O", "X"],
            ["O", "O", "X", "X", "O", "X"],
            ["X", "X", "O", "O", "X", "O"],
            ["X", "X", "O", "O", "X", "O"],
            ["O", "O", "X", "X", "O", "X"],
            ["X", "X", "O", "O", "X", "O"],
        ]
    )
    assert solved_board == expected_board
    