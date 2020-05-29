"""
Zawiera funkcje które operują na planszy.
"""

import copy
import properties


def create_empty_board():
    """
    Tworzy pustą tablicę o wymiarach określonych w properties.py
    :return: Pusta plansza
    """
    return [[' ' for _ in range(properties.BOARD_WIDTH)] for _ in range(properties.BOARD_HEIGHT)]


def is_column_valid(board, col):
    """
    Sprawdza czy do danej kolumny można dodać pionek
    :param board: plansza w której kolumna będzie sprawdzana
    :param col: kolumna która będzie sprawdzana
    :return: True, jeśli kolumna ma wolne miejsce
    """
    if board[0][col] == ' ':  # wystarczy sprawdzić czy kolumna jest pusta na samej górze
        return True
    return False


def get_possible_moves(board):
    """
    Zwraca listę kolumn do których można wrzucić pionek.
    :param board: Plansza która będzie sprawdzana
    :return: Listę możliwych ruchów
    """
    return [col for col in range(properties.BOARD_WIDTH) if is_column_valid(board, col)]


def make_move(board, col, player):
    """
    Dodaje wrzuca pionek określonego gracza do danej kolumny
    :param board: Aktualna plansza.
    :param col: Kolumna do której zostanie wrzucony pionek
    :param player: Gracz który wykona ruch.
    :return: Planszę z wykonanym ruchem. Plansza jest kopią.
    """
    board_copy = copy.deepcopy(board)
    for row in range(5, -1, -1):
        if board_copy[row][col] == ' ':  # szuka od dołu pustego pola
            board_copy[row][col] = player
            return board_copy, row, col


def is_board_full(board):
    """
    Sprawdza czy plansza jest pełna.
    :param board: Plansza która będzie sprawdzana
    :return: True, jeśli plansza jest pełna
    """
    for col in range(properties.BOARD_WIDTH):
        if board[0][col] == ' ':  # jeśli wszystkie pola na samej górze planszy nie są pełne, to plansza jest pełna
            return False
    return True


def find_fours(board, prev_row, prev_col, player):
    """
    Szuka sekwencji złożonych z przynajmniej czterech pionków jednego gracza. Jeśli jakaś sekwencja zostaje znaleziona,
    literki odwzorowujące graczy zostają zamienione na duże. Duża literka oznacza pole które wygrało. Jeśli sekwencja
    została znaleziona, zostaje zwrócona wartość True. Sekwencje są szukane wokół ostatniego ruchu.
    :param board: Plansza na której będziemy szukać sekwencji.
    :param prev_row: Poprzedni wykonany ruch
    :param prev_col: Poprzedni wykonany ruch
    :param player: Będą szukane sekwencje tylko podanego gracza.
    :return: True, jeśli znaleziono sekwencje.
    """
    count = 0

    # vertical
    for y in range(prev_row, properties.BOARD_HEIGHT):  # w tym przypadku wystarczy policzyć od ostatniego ruchu, w dół
        if board[y][prev_col] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        for y in range(prev_row, prev_row + count):
            board[y][prev_col] = board[y][prev_col].upper()
        return True

    # sprawdzanie polega na policzeniu pionków gracza w jednym kierunku od wykonanego ruchu i w drugim.
    # Np. jeśli szukamy horyzontalnie to najpierw liczymy w prawo, a potem w lewo.
    # Następnie jeśli znajdziemy sekwencję, oznaczamy pionki i zwracamy True

    # horizontal
    # right
    count = 0
    for x in range(prev_col, properties.BOARD_WIDTH):
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
        for x in range(prev_col, properties.BOARD_WIDTH):
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
    for x in range(prev_col, properties.BOARD_WIDTH):
        y = prev_row - (x - prev_col)
        if y >= 0 and board[y][x] == player:
            count += 1
        else:
            break
    # left
    for x in range(prev_col - 1, -1, -1):
        y = prev_row + (prev_col - x)
        if y < properties.BOARD_HEIGHT and board[y][x] == player:
            count += 1
        else:
            break
    # capitalize
    if count >= 4:
        for x in range(prev_col, properties.BOARD_WIDTH):
            y = prev_row - (x - prev_col)
            if y >= 0 and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            y = prev_row + (prev_col - x)
            if y < properties.BOARD_HEIGHT and board[y][x] == player:
                board[y][x] = board[y][x].upper()
            else:
                break
        return True

    # \
    # right
    count = 0
    for x in range(prev_col, properties.BOARD_WIDTH):
        y = prev_row + (x - prev_col)
        if y < properties.BOARD_HEIGHT and board[y][x] == player:
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
        for x in range(prev_col, properties.BOARD_WIDTH):
            y = prev_row + (x - prev_col)
            if y < properties.BOARD_HEIGHT and board[y][x] == player:
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
    """
    Liczy ilość sekwencji o podanej długości w podanej planszy.
    :param board: Plansza na której będziemy szukać sekwencji
    :param player: Sprawdzane będą sekwencje podanego gracza.
    :param length: Długość sekwencji któych szukamy.
    :return:
    """
    def vertical(row, col):
        count = 0
        for row_index in range(row, properties.BOARD_HEIGHT):
            if board[row_index][col] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        return 0

    def horizontal(row, col):
        count = 0
        for col_index in range(col, properties.BOARD_WIDTH):
            if board[row][col_index] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        return 0

    def negative_diagonal(row, col):
        count = 0
        col_index = col
        for row_index in range(row, -1, -1):
            if col_index > properties.BOARD_HEIGHT:
                break
            if board[row_index][col_index] == board[row][col]:
                count += 1
            else:
                break
            col_index += 1
        if count >= length:
            return 1
        return 0

    def positive_diagonal(row, col):
        count = 0
        col_index = col
        for row_index in range(row, properties.BOARD_HEIGHT):
            if col_index > properties.BOARD_HEIGHT:
                break
            if board[row_index][col_index] == board[row][col]:
                count += 1
            else:
                break
            col_index += 1
        if count >= length:
            return 1
        return 0

    total_count = 0
    for row in range(properties.BOARD_HEIGHT):
        for col in range(properties.BOARD_WIDTH):
            if board[row][col] == player:
                total_count += vertical(row, col)
                total_count += horizontal(row, col)
                total_count += (positive_diagonal(row, col) + negative_diagonal(row, col))
    return total_count


def evaluate_player(board, player):
    """
    Liczy wartość aktualnego stanu planszy.
    :param board: Plansza na podstawie której liczymy wartość.
    :param player: Gracz na podstawie którego będzie liczona wartość.
    :return: Wartość aktualnego stanu planszy.
    """
    fours = count_sequences(board, player, 4)
    threes = count_sequences(board, player, 3)
    twos = count_sequences(board, player, 2)
    return fours * 99999 + threes * 999 + twos * 99, fours


def evaluate(board, player):
    """
    Liczy wartość aktualnego stanu planszy.
    :param board: Plansza na podstawie której liczymy wartość.
    :param player: Gracz na podstawie którego będzie liczona wartość.
    :return: Wartość aktualnego stanu planszy.
    """
    if player == properties.PLAYER:
        opponent = properties.ENEMY
    else:
        opponent = properties.PLAYER

    player_score, _ = evaluate_player(board, player)
    opponent_score, opponent_fours = evaluate_player(board, opponent)

    if opponent_fours > 0:
        return float('-inf')
    return player_score - opponent_score


def is_game_over(board):
    """
    Sprawdza czy gra jest skończona na podanej planszy.
    :param board: Plansza którą będziemy sprawdzać
    :return: True, jesli gra jest skończona.
    """
    return count_sequences(board, properties.PLAYER, 4) >= 1 or count_sequences(board, properties.ENEMY, 4) >= 1
