"""
Zawiera algorytm minimax.
"""

import board
import properties
import random


def minimax(current_board, depth):
    """
    Zwraca ruch wykonany przez przeciwnika.
    :param current_board: Aktualna plansza.
    :param depth: Głębokość algorytmu.
    :return: Ruch wykonany przez przeciwnika.
    """
    possible_moves = board.get_possible_moves(current_board)
    random.shuffle(possible_moves)
    best_move = possible_moves[0]
    best_score = -1e500

    alpha = -1e500
    beta = 1e500

    for move in possible_moves:
        temp_board = board.make_move(current_board, move, properties.ENEMY)[0]
        board_score = minimize(temp_board, depth - 1, alpha, beta)
        if board_score > best_score:
            best_score = board_score
            best_move = move
    return best_move


def minimize(current_board, depth, alpha, beta):
    possible_moves = board.get_possible_moves(current_board)

    if depth == 0 or len(possible_moves) == 0 or board.is_game_over(current_board):
        return board.evaluate(current_board, properties.ENEMY)

    for move in possible_moves:
        score = 1e500
        if alpha < beta:
            temp_board = board.make_move(current_board, move, properties.PLAYER)[0]
            score = maximize(temp_board, depth - 1, alpha, beta)
        if score < beta:
            beta = score
    return beta


def maximize(current_board, depth, alpha, beta):
    possible_moves = board.get_possible_moves(current_board)

    if depth == 0 or len(possible_moves) == 0 or board.is_game_over(current_board):
        return board.evaluate(current_board, properties.ENEMY)

    for move in possible_moves:
        score = -1e500
        if alpha < beta:
            temp_board = board.make_move(current_board, move, properties.ENEMY)[0]
            score = minimize(temp_board, depth - 1, alpha, beta)
        if score > alpha:
            alpha = score
    return alpha
