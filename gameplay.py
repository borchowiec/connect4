"""
Plik startowy. Zawiera funkcje związane z gameplayem np wykonywanie ruchów.
"""
import sys
import pygame
import properties
import gui
import minimax
import board

# głębokość algorytmu minimax
depth = 4


def player_turn(current_board):
    """
    Wykonanie ruchu przez użytkownika. Po wywołaniu funkcji program czeka na wykonanie ruchu, po czym
    zwraca planszę z wykonanym ruchem, oraz wartość True, jeśli wykonany ruch wygrał.
    :param current_board: Aktualna plansza.
    :return: Plansza z wykonanym ruchem, oraz wartość True, jeśli wykonany ruch wygrał.
    """
    # wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                move = gui.Gui.get_clicked_column(pygame.mouse.get_pos())

                if 0 <= move < properties.BOARD_WIDTH and board.is_column_valid(current_board, move):
                    current_board, row, col = board.make_move(current_board, move, properties.PLAYER)
                    player_victory = board.find_fours(current_board, row, col, properties.PLAYER)
                    return current_board, player_victory


def enemy_turn(current_board):
    """
    Wykonanie ruchu przez przeciwnika.
    :param current_board: Aktualna plansza.
    :return: Plansza z wykonanym ruchem, oraz wartość True, jeśli wykonany ruch wygrał.
    """
    move = minimax.minimax(current_board, depth)
    current_board, row, col = board.make_move(current_board, move, properties.ENEMY)
    enemy_victory = board.find_fours(current_board, row, col, properties.ENEMY)
    return current_board, enemy_victory


def main():
    """
    Funkcja startująca grę. Zawiera główną pętlę.
    """

    pygame.init()
    screen = pygame.display.set_mode((properties.SCREEN_WIDTH, properties.SCREEN_HEIGHT))
    font = pygame.font.SysFont("comicsansms", properties.FONT_SIZE)
    current_board = board.create_empty_board()
    gui_tools = gui.Gui(screen, font, pygame)

    # Main loop
    while True:
        gui_tools.paint_board(current_board)

        # Draw
        if board.is_board_full(current_board):
            gui_tools.game_over(current_board, "Remis!")
            current_board = board.create_empty_board()
            continue

        # Player
        current_board, player_victory = player_turn(current_board)
        if player_victory:
            gui_tools.game_over(current_board, "Wygrywa gracz!")
            current_board = board.create_empty_board()
            continue
        gui_tools.paint_board(current_board)

        # Enemy
        current_board, enemy_victory = enemy_turn(current_board)
        if enemy_victory:
            gui_tools.game_over(current_board, "Wygrywa przeciwnik!")
            current_board = board.create_empty_board()
            continue


if __name__ == '__main__':
    main()
