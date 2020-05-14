from copy import deepcopy
from properties import *


def init():
    return [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def is_column_valid(board, col):
    if board[0][col] == ' ':
        return True
    return False


def get_possible_moves(board):
    return [col for col in range(BOARD_WIDTH) if is_column_valid(board, col)]


def make_move(board, col, player):
    temp = deepcopy(board)
    for row in range(5, -1, -1):
        if temp[row][col] == ' ':
            temp[row][col] = player
            return temp, row, col


def is_board_full(board):
    for col in range(BOARD_WIDTH):
        if board[0][col] == ' ':
            return False
    return True


def find_fours(board, prev_row, prev_col, player):
    count = 0

    # vertical
    for y in range(prev_row, BOARD_HEIGHT):
        if board[y][prev_col] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        for y in range(prev_row, prev_row + count):
            board[y][prev_col] = board[y][prev_col].upper()
        return True

    # horizontal
    # right
    count = 0
    for x in range(prev_col, BOARD_WIDTH):
        if board[prev_row][x] == player:
            count += 1
        else:
            break
    # left
    for x in range(prev_col - 1, -1, -1):
        if board[prev_row][x] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        # right
        for x in range(prev_col, BOARD_WIDTH):
            if board[prev_row][x] == player:
                board[prev_row][x] = board[prev_row][x].upper()
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            if board[prev_row][x] == player:
                board[prev_row][x] = board[prev_row][x].upper()
            else:
                break
        return True

    # /
    # right
    count = 0
    for x in range(prev_col, BOARD_WIDTH):
        y = prev_row - (x - prev_col)
        if y >= 0 and board[y][x] == player:
            count += 1
        else:
            break
    # left
    for x in range(prev_col - 1, -1, -1):
        y = prev_row + (prev_col - x)
        if y < BOARD_HEIGHT and board[y][x] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        for x in range(prev_col, BOARD_WIDTH):
            y = prev_row - (x - prev_col)
            if y >= 0 and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            y = prev_row + (prev_col - x)
            if y < BOARD_HEIGHT and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        return True

    # \
    # right
    count = 0
    for x in range(prev_col, BOARD_WIDTH):
        y = prev_row + (x - prev_col)
        if y < BOARD_HEIGHT and board[y][x] == player:
            count += 1
        else:
            break
    # left
    for x in range(prev_col - 1, -1, -1):
        y = prev_row - (prev_col - x)
        if y >= 0 and board[y][x] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        for x in range(prev_col, BOARD_WIDTH):
            y = prev_row + (x - prev_col)
            if y < BOARD_HEIGHT and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            y = prev_row - (prev_col - x)
            if y >= 0 and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        return True
    return False


def count_sequences(board, player, length):
    def vertical(row, col):
        count = 0
        for row_index in range(row, BOARD_HEIGHT):
            if board[row_index][col] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def horizontal(row, col):
        count = 0
        for col_index in range(col, BOARD_WIDTH):
            if board[row][col_index] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def negative_diagonal(row, col):
        count = 0
        col_index = col
        for row_index in range(row, -1, -1):
            if col_index > BOARD_HEIGHT:
                break
            elif board[row_index][col_index] == board[row][col]:
                count += 1
            else:
                break
            col_index += 1
        if count >= length:
            return 1
        else:
            return 0

    def positive_diagonal(row, col):
        count = 0
        col_index = col
        for row_index in range(row, BOARD_HEIGHT):
            if col_index > BOARD_HEIGHT:
                break
            elif board[row_index][col_index] == board[row][col]:
                count += 1
            else:
                break
            col_index += 1
        if count >= length:
            return 1
        else:
            return 0

    total_count = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == player:
                total_count += vertical(row, col)
                total_count += horizontal(row, col)
                total_count += (positive_diagonal(row, col) + negative_diagonal(row, col))
    return total_count


def evaluate_player(board, player):
    fours = count_sequences(board, player, 4)
    threes = count_sequences(board, player, 3)
    twos = count_sequences(board, player, 2)
    return fours * 99999 + threes * 999 + twos * 99, fours


def evaluate(board, player):
    if player == PLAYER:
        opponent = ENEMY
    else:
        opponent = PLAYER

    player_score, player_fours = evaluate_player(board, player)
    opponent_score, opponent_fours = evaluate_player(board, opponent)

    if opponent_fours > 0:
        return float('-inf')
    return player_score - opponent_score


def is_game_over(board):
    return count_sequences(board, PLAYER, 4) >= 1 or count_sequences(board, ENEMY, 4) >= 1
