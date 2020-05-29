"""
Zawiera funkcje które rysują elementy gry.
"""

import sys
import pygame
import properties

pygame.init()
screen = pygame.display.set_mode((properties.SCREEN_WIDTH, properties.SCREEN_HEIGHT))
font = pygame.font.SysFont("comicsansms", properties.FONT_SIZE)


def get_clicked_column(pos):
    """
    Na podstawie pozycji kliknięcia które zostało przesłane, wylicza która kolumna została kliknięta.
    :param pos: Pozycja kliknięcia myszki.
    :return: Number klikniętej kolumny.
    """
    x, y = pos
    return int(x // (properties.FIELD_SIZE + properties.GAP + properties.GAP / properties.BOARD_WIDTH))


def paint_board(board):
    """
    Rysuje przesłaną planszę.
    :param board: Plansza która będzie narysowana.
    """

    # background
    screen.fill((0, 150, 255))

    # paint all squares
    for j in range(properties.BOARD_WIDTH):
        for i in range(properties.BOARD_HEIGHT):
            x = properties.GAP * (j + 1) + j * properties.FIELD_SIZE
            y = properties.GAP * (i + 1) + i * properties.FIELD_SIZE

            # uppercase character means winning move
            if board[i][j].isupper():
                size = properties.FIELD_SIZE + properties.GAP*2
                pygame.draw.rect(screen, (34, 10, 209), pygame.Rect(x - properties.GAP, y - properties.GAP, size, size))
                board[i][j] = board[i][j].lower()

            if board[i][j] == properties.PLAYER:
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))
            elif board[i][j] == properties.ENEMY:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))

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
    x = (properties.SCREEN_WIDTH - text.get_width()) // 2
    y = (properties.SCREEN_HEIGHT - text.get_height()) // 2
    screen.blit(text, (x, y))
    pygame.display.flip()

    # quit game or play again
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                wait = False
