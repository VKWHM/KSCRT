
def is_place_okey(board: dict[int, int], place: tuple[int, int]) -> bool:
    """
    Check if specified place is not under attack
    Args:
        board(dict): Board.
        place(tuple): Place (row, column)
    """
    pass

def print_board(board) -> None:
    """
    Print board
    Args:
        board(dict): Board.
    """
    pass


def main(board, row=1) -> dict[int, int]:
    """
    Solve the puzzle and return solution.
    Args:
        board(dict): Board.
    """
    pass


if __name__ == "__main__":
    place_board: dict[int, int] = {}  # row : column
    solution = main(place_board)
    print_board(solution)
