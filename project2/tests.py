import unittest
from tictactoe import X, O, EMPTY, winner, utility


# A test class represents a group of related test cases
# Must subclass unittest.TestCase
class TestWinner(unittest.TestCase):

    # Each test name must start with "test"
    # Each test case should use an Assert statement to verify the result
    def test_detect_win_vert(self):
        board = [
            [X, X, O],
            [X, O, EMPTY],
            [X, O, O]
        ]
        self.assertEqual(winner(board), X)

    def test_detect_win_horiz(self):
        board = [
            [X, X, X],
            [O, O, EMPTY],
            [X, O, O]
        ]

        self.assertEqual(winner(board), X)

    def test_detect_win_diag(self):
        board = [
            [O, X, EMPTY],
            [X, O, EMPTY],
            [EMPTY, X, O]
        ]

        self.assertEqual(winner(board), O)


class TestUtility(unittest.TestCase):

    def test_utility_1(self):
        board = [
            [X, O, EMPTY],
            [O, X, EMPTY],
            [EMPTY, O, X]
        ]

        self.assertEqual(utility(board), 1)

    def test_utility_neg1(self):
        board = [
            [EMPTY, X, O],
            [X, EMPTY, O],
            [EMPTY, X, O]
        ]

        self.assertEqual(utility(board), -1)

    def test_utility_zero(self):
        board = [
            [X, X, O],
            [O, O, X],
            [X, X, O]
        ]

        self.assertEqual(utility(board), 0)


# Calling unittest.main() will run all the tests in your module
if __name__ == "__main__":
    unittest.main()
