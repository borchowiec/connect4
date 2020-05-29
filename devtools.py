"""
Zawiera funkcje umożliwiające symulowanie pewnych sytuacji.
"""

import sys

import board
import gui
import properties


def get_full_board():
    """
    :return: Pełna plansza.
    """
    return [[properties.PLAYER for _ in range(properties.BOARD_WIDTH)] for _ in range(properties.BOARD_HEIGHT)]


def get_game_over_board(winner):
    """
    Tworzy planszę w której wygrywa podany gracz.
    :param winner: Gracz który wygra w wygenerowanej planszy.
    :return: Plansza w której podany gracz wygrywa.
    """
    board = [[' ' for _ in range(properties.BOARD_WIDTH)] for _ in range(properties.BOARD_HEIGHT)]
    for i in range(4):
        board[properties.BOARD_HEIGHT - 1][i] = winner
    return board


def make_enemy_move(pygame, current_board):
    """
    Oddaje kontrolę nad ruchami przeciwnika. Można zamienić tą funkcję z funkcją enemy_turn()
    :param pygame:
    :param current_board:
    :return: Planszę z wykonanym ruchem oraz, True jeśli wykonany ruch wygrał.
    """
    # wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                move = gui.get_clicked_column(pygame.mouse.get_pos())

                if 0 <= move < properties.BOARD_WIDTH and board.is_column_valid(current_board, move):
                    current_board, row, col = board.make_move(current_board, move, properties.ENEMY)
                    enemy_victory = board.find_fours(current_board, row, col, properties.ENEMY)
                    return current_board, enemy_victory
