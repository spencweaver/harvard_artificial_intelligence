"""
Tic Tac Toe Player
"""

import copy
import math

import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the X's and O's then compare
    num_X = sum(i.count(X) for i in board)
    num_O = sum(i.count(O) for i in board)
    if num_X == num_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check the board for all the empty spaces
    actions_list = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.append((i, j))
    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # unpack tuple and return copied board
    i, j = action
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check if the rows equal
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O

        # check if columns equal
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O

    # Check the diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O

    # Check the other diagonal
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
    # If no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for a winner
    for i in range(3):
        # check the rows
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return True

        # check the columns
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True

    # check both diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True

    # check to see if no empty spaces
    if sum(i.count(EMPTY) for i in board) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # check if X wins
    if terminal(board) and winner(board) == X:
        return 1

    # check if O wins
    elif terminal(board) and winner(board) == O:
        return -1

    # else it is a tie
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if game is over
    if terminal(board):
        return utility(board)

    # If the first player is X simply go in the top corner
    elif player(board) == X and sum(i.count(EMPTY) for i in board) == 9:
        return random.choice([(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)])

    # check every available action for its utility
    utility_list = []
    for action in actions(board):
        result_board = result(board, action)

        # continue calculating until terminal board
        while terminal(result_board) is not True:
            result_board = result(result_board, minimax(result_board))
        # Append utility to the end of the list
        utility_list.append((utility(result_board), action))

    # return highest move for O
    if player(board) == O:
        highest_utility = math.inf
        best_action = utility_list[0][1]
        for utility_action in utility_list:
            if utility_action[0] < highest_utility:
                highest_utility = utility_action[0]
                best_action = utility_action[1]

    # return highest move for X
    elif player(board) == X:
        highest_utility = -math.inf
        best_action = utility_list[0][1]
        for utility_action in utility_list:
            if utility_action[0] > highest_utility:
                highest_utility = utility_action[0]
                best_action = utility_action[1]

    return best_action
