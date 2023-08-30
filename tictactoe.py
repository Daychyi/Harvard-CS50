"""
Tic Tac Toe Player
"""

import math
import copy

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
    board_1D = [y for x in board for y in x]
    if board_1D.count(EMPTY) == 9 or board_1D.count(X)<=board_1D.count(O) :
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return sorted({(i,j) for i in range(3) for j in range(3) if board[i][j] == EMPTY})
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] == EMPTY:
        board_copy[action[0]][action[1]] = player(board_copy)
        return board_copy
    raise Exception("Error, invalid action!")
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
     #winner by rows
    for row in board:
        if row.count(row[0])==3 and (row[0] is not EMPTY):
            return row[0] #winner
    
    #winner by columns
    for col in range(3):
        if len(set(row[col] for row in board)) == 1 and (board[0][col] is not EMPTY):
            return board[0][col] #winner
        
    #winner by diagonal
    if len(set(board[i][i] for i in range(3))) == 1 and (board[0][0] is not EMPTY):
        return board[0][0] #left to right diagonal
    if len(set(board[-i-1][i] for i in range(3))) == 1 and (board[-1][0] is not EMPTY):
        return board[-1][0] #right to left diagonal
    
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or [y for x in board for y in x].count(EMPTY) == 0:
        return True
    return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    match win:
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0
    raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X: #max_value
        # value, move = max_value(board)
        value, move = max_alpha_beta(board,-2,2) #alpha-beta 
    else: 
        # value, move = min_value(board)
        value, move = min_alpha_beta(board,-2,2) #alpha-beta 
    return move
    raise NotImplementedError


def max_value(board):
    """
    Returns the maximum value for the current player on the board.
    """
    if terminal(board):
        return utility(board), None
    
    value = -2
    best_action = None
    for act in actions(board):
        score, a = min_value(result(board, act))
        if score > value:
            value = score
            best_action = act
    return value, best_action

def min_value(board):
    """
    Returns the minimum value for the current player on the board.
    """
    if terminal(board):
        return utility(board), None
    
    value = 2
    best_action = None
    for act in actions(board):
        score,b = max_value(result(board, act))
        if score < value:
            value = score
            best_action = act
    return value, best_action


def max_alpha_beta(board,alpha, beta):
    """
    Returns the maximum value for the current player on the board.
    """
    if terminal(board):
        return utility(board), None
    
    value = -2
    best_action = None
    for act in actions(board):
        score, a = min_alpha_beta(result(board, act),alpha,beta)
        if score > value:
            value = score
            best_action = act

        if value >= beta:
            return value, best_action
        if value > alpha:
            alpha = value        
    return value, best_action

def min_alpha_beta(board,alpha, beta):
    """
    Returns the minimum value for the current player on the board.
    """
    if terminal(board):
        return utility(board), None
    
    value = 2
    best_action = None
    for act in actions(board):
        score,b = max_alpha_beta(result(board, act),alpha,beta)
        if score < value:
            value = score
            best_action = act
        
        if value <= alpha:
            return value, best_action
        if value < beta:
            beta = value
    return value, best_action
