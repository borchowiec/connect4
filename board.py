"""
Zawiera funkcje które operują na planszy.
"""

import properties


class Board:
    def __init__(self):
        """
        Tworzy pustą tablicę o wymiarach określonych w properties.py
        :return: Pusta plansza
        """
        self.fields = [[' ' for _ in range(properties.BOARD_WIDTH)] for _ in range(properties.BOARD_HEIGHT)]

    def is_column_valid(self, col):
        """
        Sprawdza czy do danej kolumny można dodać pionek
        :param col: kolumna która będzie sprawdzana
        :return: True, jeśli kolumna ma wolne miejsce
        """
        if self.fields[0][col] == ' ':  # wystarczy sprawdzić czy kolumna jest pusta na samej górze
            return True
        return False

    def get_possible_moves(self):
        """
        Zwraca listę kolumn do których można wrzucić pionek.
        :return: Listę możliwych ruchów
        """
        return [col for col in range(properties.BOARD_WIDTH) if self.is_column_valid(col)]

    def make_move(self, col, player):
        """
        Dodaje wrzuca pionek określonego gracza do danej kolumny
        :param col: Kolumna do której zostanie wrzucony pionek
        :param player: Gracz który wykona ruch.
        :return: Planszę z wykonanym ruchem. Plansza jest kopią.
        """
        for row in range(5, -1, -1):
            if self.fields[row][col] == ' ':  # szuka od dołu pustego pola
                self.fields[row][col] = player
                return row, col

    def is_board_full(self):
        """
        Sprawdza czy plansza jest pełna.
        :return: True, jeśli plansza jest pełna
        """
        for col in range(properties.BOARD_WIDTH):
            # jeśli wszystkie pola na samej górze planszy są pełne, to plansza jest pełna
            if self.fields[0][col] == ' ':
                return False
        return True

    def capitalize(self, squares):
        for square in squares:
            y = square[0]
            x = square[1]
            self.fields[y][x] = self.fields[y][x].upper()

    def find_fours(self, prev_row, prev_col, player):
        """
        Szuka sekwencji złożonych z przynajmniej czterech pionków jednego gracza. Jeśli jakaś sekwencja zostaje znaleziona,
        literki odwzorowujące graczy zostają zamienione na duże. Duża literka oznacza pole które wygrało. Jeśli sekwencja
        została znaleziona, zostaje zwrócona wartość True. Sekwencje są szukane wokół ostatniego ruchu.
        :param self: Plansza na której będziemy szukać sekwencji.
        :param prev_row: Poprzedni wykonany ruch
        :param prev_col: Poprzedni wykonany ruch
        :param player: Będą szukane sekwencje tylko podanego gracza.
        :return: True, jeśli znaleziono sekwencje.
        """

        squares = []
        # vertical
        for y in range(prev_row, properties.BOARD_HEIGHT):
            # w tym przypadku wystarczy policzyć od ostatniego ruchu, w dół
            if self.fields[y][prev_col] == player:
                squares.append((y, prev_col))
            else:
                break
        # capitalize
        if len(squares) >= 4:
            self.capitalize(squares)
            return True

        # sprawdzanie polega na policzeniu pionków gracza w jednym kierunku od wykonanego ruchu i w drugim.
        # Np. jeśli szukamy horyzontalnie to najpierw liczymy w prawo, a potem w lewo.
        # Następnie jeśli znajdziemy sekwencję, oznaczamy kwadraty i zwracamy True

        # horizontal
        # right
        squares = []
        for x in range(prev_col, properties.BOARD_WIDTH):
            if self.fields[prev_row][x] == player:
                squares.append((prev_row, x))
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            if self.fields[prev_row][x] == player:
                squares.append((prev_row, x))
            else:
                break
        # capitalize
        if len(squares) >= 4:
            self.capitalize(squares)
            return True

        # /
        # right
        squares = []
        for x in range(prev_col, properties.BOARD_WIDTH):
            y = prev_row - (x - prev_col)
            if y >= 0 and self.fields[y][x] == player:
                squares.append((y, x))
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            y = prev_row + (prev_col - x)
            if y < properties.BOARD_HEIGHT and self.fields[y][x] == player:
                squares.append((y, x))
            else:
                break
        # capitalize
        if len(squares) >= 4:
            self.capitalize(squares)
            return True

        # \
        # right
        squares = []
        for x in range(prev_col, properties.BOARD_WIDTH):
            y = prev_row + (x - prev_col)
            if y < properties.BOARD_HEIGHT and self.fields[y][x] == player:
                squares.append((y, x))
            else:
                break
        # left
        for x in range(prev_col - 1, -1, -1):
            y = prev_row - (prev_col - x)
            if y >= 0 and self.fields[y][x] == player:
                squares.append((y, x))
            else:
                break
        # capitalize
        if len(squares) >= 4:
            self.capitalize(squares)
            return True
        return False

    def count_sequences(self, player, length):
        """
        Liczy ilość sekwencji o podanej długości w podanej planszy.
        :param player: Sprawdzane będą sekwencje podanego gracza.
        :param length: Długość sekwencji któych szukamy.
        :return:
        """

        def vertical(row, col):
            count = 0
            for row_index in range(row, properties.BOARD_HEIGHT):
                if self.fields[row_index][col] == self.fields[row][col]:
                    count += 1
                else:
                    break
            if count >= length:
                return 1
            return 0

        def horizontal(row, col):
            count = 0
            for col_index in range(col, properties.BOARD_WIDTH):
                if self.fields[row][col_index] == self.fields[row][col]:
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
                if self.fields[row_index][col_index] == self.fields[row][col]:
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
                if self.fields[row_index][col_index] == self.fields[row][col]:
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
                if self.fields[row][col] == player:
                    total_count += vertical(row, col)
                    total_count += horizontal(row, col)
                    total_count += (positive_diagonal(row, col) + negative_diagonal(row, col))
        return total_count

    def evaluate_player(self, player):
        """
        Liczy wartość aktualnego stanu planszy.
        :param player: Gracz na podstawie którego będzie liczona wartość.
        :return: Wartość aktualnego stanu planszy.
        """
        fours = self.count_sequences(player, 4)
        threes = self.count_sequences(player, 3)
        twos = self.count_sequences(player, 2)
        return fours * 99999 + threes * 999 + twos * 99, fours

    def evaluate(self, player):
        """
        Liczy wartość aktualnego stanu planszy.
        :param player: Gracz na podstawie którego będzie liczona wartość.
        :return: Wartość aktualnego stanu planszy.
        """
        if player == properties.PLAYER:
            opponent = properties.ENEMY
        else:
            opponent = properties.PLAYER

        player_score, _ = self.evaluate_player(player)
        opponent_score, opponent_fours = self.evaluate_player(opponent)

        if opponent_fours > 0:
            return -1e500
        return player_score - opponent_score

    def is_game_over(self):
        """
        Sprawdza czy gra jest skończona na podanej planszy.
        :param board: Plansza którą będziemy sprawdzać
        :return: True, jesli gra jest skończona.
        """
        return self.count_sequences(properties.PLAYER, 4) >= 1 or self.count_sequences(properties.ENEMY, 4) >= 1
