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
    return board.generate_fields(properties.PLAYER)


def get_game_over_board(winner):
    """
    Tworzy planszę w której wygrywa podany gracz.
    :param winner: Gracz który wygra w wygenerowanej planszy.
    :return: Plansza w której podany gracz wygrywa.
    """
    result_board = board.generate_fields(properties.EMPTY)
    fields_in_row = 4
    for i in range(fields_in_row):
        result_board[properties.BOARD_HEIGHT - 1][i] = winner
    return result_board


def make_enemy_move(pygame, board):
    """
    Oddaje kontrolę nad ruchami przeciwnika. Można zamienić tą funkcję z funkcją enemy_turn()
    :param pygame:
    :return: Planszę z wykonanym ruchem oraz, True jeśli wykonany ruch wygrał.
    """
    # wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                move = gui.Gui.get_clicked_column(pygame.mouse.get_pos())

                if 0 <= move < properties.BOARD_WIDTH and board.is_column_valid(move):
                    row, col = board.make_move(move, properties.ENEMY)
                    enemy_victory = board.find_fours(row, col, properties.ENEMY)
                    return enemy_victory
