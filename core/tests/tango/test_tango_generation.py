from core.tango.tango_generation import generate_random_tango_board


def test_try_generate_board():
    """
    Try generating a Tango board 100 times.
    """
    for i in range(100):
        generated_board = generate_random_tango_board()
