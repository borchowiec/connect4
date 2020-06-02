"""
Zawiera algorytm minimax.
"""

import copy
import math
import random

import properties


def alphabeta(current_board, depth):
    """
    Zwraca ruch wykonany przez przeciwnika.
    :param current_board: Aktualna plansza.
    :param depth: Głębokość algorytmu.
    :return: Ruch wykonany przez przeciwnika.
    """
    possible_moves = current_board.get_possible_moves()
    random.shuffle(possible_moves)
    best_move = possible_moves[0]
    best_score = -math.inf

    alpha = -math.inf
    beta = math.inf

    for move in possible_moves:
        temp_board = copy.deepcopy(current_board)
        temp_board.make_move(move, properties.ENEMY)
        board_score = minimize(temp_board, depth - 1, alpha, beta)
        if board_score > best_score:
            best_score = board_score
            best_move = move
    return best_move


def minimize(current_board, depth, alpha, beta):
    possible_moves = current_board.get_possible_moves()

    if depth == 0 or len(possible_moves) == 0 or current_board.is_game_over():
        return current_board.evaluate(properties.ENEMY)

    for move in possible_moves:
        score = math.inf
        if alpha < beta:
            temp_board = copy.deepcopy(current_board)
            temp_board.make_move(move, properties.PLAYER)
            score = maximize(temp_board, depth - 1, alpha, beta)
        if score < beta:
            beta = score
    return beta


def maximize(current_board, depth, alpha, beta):
    possible_moves = current_board.get_possible_moves()

    if depth == 0 or len(possible_moves) == 0 or current_board.is_game_over():
        return current_board.evaluate(properties.ENEMY)

    for move in possible_moves:
        score = -math.inf
        if alpha < beta:
            temp_board = copy.deepcopy(current_board)
            temp_board.make_move(move, properties.ENEMY)
            score = minimize(temp_board, depth - 1, alpha, beta)
        if score > alpha:
            alpha = score
    return alpha
