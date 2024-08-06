import sys


def is_place_okey(board: dict[int, int], place: tuple[int, int]) -> bool:
    """
    Check if specified place is not under attack
    Args:
        board(dict): Board.
        place(tuple): Place (row, column)
    """
    match place:
        case (row, _) if row in board.keys():  # horizontal check
            return False

        case (_, column) if column in board.values():  # vertical check
            return False

        case (row, column):
            diagonal_right_position = row + column
            diagonal_left_position = row - column
            for queen_row, queen_column in board.items():
                if (
                    diagonal_right_position == queen_row + queen_column
                ):  # diagonal right check
                    return False

                elif (
                    diagonal_left_position == queen_row - queen_column
                ):  # diagonal left check
                    return False
    return True


def print_board(board: dict[int, int]) -> None:
    """
    Check if specified place is not under attack
    Args:
        board(dict): Board.
        place(tuple): Place (row, column)
    """
    print("#" * 50)
    for i in range(1, 9):
        for j in range(1, 9):
            print(" Q " if board.get(i) == j else " - ", end="")
        print()
    print("#" * 50)


def main(board: dict[int, int], row=1) -> dict[int, int]:
    """
    Solve the puzzle and return solution.
    Args:
        board(dict): Board.
    """
    if len(board) == 8:
        return board
    elif row in board.keys():
        return main(board, row + 1)

    for column in range(1, 9):
        if is_place_okey(board, (row, column)):
            board_copy = board.copy()
            board_copy[row] = column
            next_board = main(board_copy, row + 1)
            if len(next_board) != 0:
                return next_board
    else:
        return {}


if __name__ == "__main__":
    place_board: dict[int, int] = {}  # row : column
    solution = main(place_board)
    print_board(solution)
