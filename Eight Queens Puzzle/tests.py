from unittest import TestCase
import unittest
from random import randint
from solution import is_place_okey, main, print_board


class TestIsPlaceOkeyFunction(TestCase):
    def setUp(self) -> None:
        self.board = {
            # row : column
            1: 1,
            7: 2,
            5: 3,
            8: 4,
            2: 5,
        }
        return super().setUp()

    def test_function_horizontal_check(self):
        place = (2, 8)

        place_status = is_place_okey(self.board, place)

        self.assertEqual(place_status, False)

    def test_function_vertical_check(self):
        place = (6, 4)

        place_status = is_place_okey(self.board, place)

        self.assertEqual(place_status, False)

    def test_function_diagonal_right_check(self):
        place = (3, 6)

        place_status = is_place_okey(self.board, place)

        self.assertEqual(place_status, False)

    def test_function_diagonal_left_check(self):
        place = (4, 7)

        place_status = is_place_okey(self.board, place)

        self.assertEqual(place_status, False)

    def test_function_place_okey(self):
        place = (3, 8)

        place_status = is_place_okey(self.board, place)

        self.assertEqual(place_status, True)


class TestMainFunction(TestCase):
    def A(self, board, place):
        D = board.copy()
        C = False
        D.pop(place[0])
        match place:
            case A, _ if A in D.keys():
                return C
            case _, B if B in D.values():
                return C
            case A, B:
                G = A + B
                H = A - B
                for E, F in D.items():
                    if G == E + F:
                        return C
                    elif H == E - F:
                        return C
        return True

    def test_main_function_behavior(self):
        solution = main({})

        for queen in solution.items():
            self.assertTrue(self.A(solution, queen), solution)

    def test_challange_solution(self):
        for i in range(1, 9):
            for j in range(1, 9):
                out_board = main({i: j})
                self.assertEqual(
                    len(out_board),
                    8,
                    f"Input board: {{i:j}}, Output board: {out_board}",
                )
                for queen in out_board.items():
                    self.assertTrue(self.A(out_board, queen), out_board)


if __name__ == "__main__":
    unittest.main()
