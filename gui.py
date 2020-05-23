"""
Zawiera funkcje które rysują elementy gry.
"""

import sys

import pygame
from properties import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("comicsansms", FONT_SIZE)


def get_clicked_column(pos):
    """
    Na podstawie pozycji kliknięcia które zostało przesłane, wylicza która kolumna została kliknięta.
    :param pos: Pozycja kliknięcia myszki.
    :return: Number klikniętej kolumny.
    """
    x, y = pos
    return int(x // (FIELD_SIZE + GAP + GAP / BOARD_WIDTH))


def paint_board(board):
    """
    Rysuje przesłaną planszę.
    :param board: Plansza która będzie narysowana.
    """

    # background
    screen.fill((0, 150, 255))

    # paint all squares
    for j in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT):
            x = GAP * (j + 1) + j * FIELD_SIZE
            y = GAP * (i + 1) + i * FIELD_SIZE

            # uppercase character means winning move
            if board[i][j].isupper():
                size = FIELD_SIZE + GAP*2
                pygame.draw.rect(screen, (34, 10, 209), pygame.Rect(x - GAP, y - GAP, size, size))
                board[i][j] = board[i][j].lower()

            if board[i][j] == PLAYER:
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, FIELD_SIZE, FIELD_SIZE))
            elif board[i][j] == ENEMY:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, FIELD_SIZE, FIELD_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, FIELD_SIZE, FIELD_SIZE))

    pygame.display.flip()


def game_over(board, message):
    """
    Rysuje planszę wraz z komunikatem.
    :param board: Plansza która będzie narysowana.
    :param message: Wiadomość która zostanie wypisana na ekranie.
    :return:
    """
    # print message and wait
    paint_board(board)
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    pygame.display.flip()

    # quit game or play again
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                wait = False
