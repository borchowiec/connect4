from board import *
from random import shuffle


def minimax(board, depth):
    possible_moves = get_possible_moves(board)
    shuffle(possible_moves)
    best_move = possible_moves[0]
    best_score = float("-inf")

    alpha = float("-inf")
    beta = float("inf")

    for move in possible_moves:
        temp_board = make_move(board, move, ENEMY)[0]
        board_score = minimize(temp_board, depth - 1, alpha, beta)
        if board_score > best_score:
            best_score = board_score
            best_move = move
    return best_move


def minimize(board, depth, alpha, beta):
    possible_moves = get_possible_moves(board)

    if depth == 0 or len(possible_moves) == 0 or is_game_over(board):
        return evaluate(board, ENEMY)

    for move in possible_moves:
        score = float("inf")
        if alpha < beta:
            temp_board = make_move(board, move, PLAYER)[0]
            score = maximize(temp_board, depth - 1, alpha, beta)
        if score < beta:
            beta = score
    return beta


def maximize(board, depth, alpha, beta):
    possible_moves = get_possible_moves(board)

    if depth == 0 or len(possible_moves) == 0 or is_game_over(board):
        return evaluate(board, ENEMY)

    for move in possible_moves:
        score = float("-inf")
        if alpha < beta:
            temp_board = make_move(board, move, ENEMY)[0]
            score = minimize(temp_board, depth - 1, alpha, beta)
        if score > alpha:
            alpha = score
    return alpha
