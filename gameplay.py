from gui import *
from minimax import *

depth = 4


def player_turn(board):
    # wait for interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                move = get_clicked_column(pygame.mouse.get_pos())

                if 0 <= move < BOARD_WIDTH and is_column_valid(board, move):
                    board, row, col = make_move(board, move, PLAYER)
                    player_victory = find_fours(board, row, col, PLAYER)
                    return board, player_victory


def enemy_turn(board):
    move = minimax(board, depth)
    board, row, col = make_move(board, move, ENEMY)
    enemy_victory = find_fours(board, row, col, ENEMY)
    return board, enemy_victory


def gameplay():
    board = init()

    # Main loop
    while True:
        paint_board(board)

        # Draw
        if is_board_full(board):
            game_over(board, "Remis!")
            board = init()
            continue

        # Player
        board, player_victory = player_turn(board)
        if player_victory:
            game_over(board, "Wygrywa gracz!")
            board = init()
            continue
        paint_board(board)

        # Enemy
        board, enemy_victory = enemy_turn(board)
        if enemy_victory:
            game_over(board, "Wygrywa przeciwnik!")
            board = init()
            continue


gameplay()
