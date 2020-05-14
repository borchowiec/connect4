import sys

from board import is_column_valid, make_move, find_fours
from gui import get_clicked_column
from properties import BOARD_WIDTH, BOARD_HEIGHT, PLAYER, ENEMY


def get_full_board():
    return [[PLAYER for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def get_game_over_board(winner):
    board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    for i in range(4):
        board[BOARD_HEIGHT - 1][i] = winner
    return board


def make_enemy_move(pygame, board):
    # wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                move = get_clicked_column(pygame.mouse.get_pos())

                if 0 <= move < BOARD_WIDTH and is_column_valid(board, move):
                    board, row, col = make_move(board, move, ENEMY)
                    enemy_victory = find_fours(board, row, col, ENEMY)
                    return board, enemy_victory
