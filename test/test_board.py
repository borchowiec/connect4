import unittest

import board
import properties


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_is_column_valid(self):
        # wszystkie kolumny są pełne
        self.board.fields = board.generate_fields(properties.PLAYER)
        for col in range(properties.BOARD_WIDTH):
            self.assertFalse(self.board.is_column_valid(col))

        # wszystkie kolumny są puste
        self.board.fields = board.generate_fields(properties.EMPTY)
        for col in range(properties.BOARD_WIDTH):
            self.assertTrue(self.board.is_column_valid(col))

    def test_get_possible_moves(self):
        self.board.fields = board.generate_fields(properties.PLAYER)
        self.board.fields[0][0] = properties.EMPTY
        self.board.fields[0][1] = properties.EMPTY
        self.board.fields[0][2] = properties.EMPTY
        self.assertEqual(self.board.get_possible_moves(), [0, 1, 2])

    def test_make_move(self):
        self.board.fields = board.generate_fields(properties.EMPTY)
        col = 3
        player = properties.PLAYER

        self.board.make_move(col, player)

        expected = board.generate_fields(properties.EMPTY)
        expected[properties.BOARD_HEIGHT - 1][col] = player
        self.assertEqual(expected, self.board.fields)

    def test_is_board_full(self):
        self.board.fields = board.generate_fields(properties.PLAYER)
        self.assertTrue(self.board.is_board_full())

        self.board.fields = board.generate_fields(properties.EMPTY)
        self.assertFalse(self.board.is_board_full())

    def test_capitalize(self):
        squares = [(0, 0), (2, 2)]
        self.board.fields = board.generate_fields(properties.PLAYER)

        self.board.capitalize(squares)

        expected = board.generate_fields(properties.PLAYER)
        expected[0][0] = expected[0][0].upper()
        expected[2][2] = expected[2][2].upper()
        self.assertEqual(expected, self.board.fields)

    def test_find_fours(self):
        self.board.fields = board.generate_fields(properties.EMPTY)
        for row in range(properties.BOARD_HEIGHT):
            self.board.fields[row][0] = properties.ENEMY
        self.assertTrue(self.board.find_fours(0, 0, properties.ENEMY))

    def test_count_sequences(self):
        self.board.fields = board.generate_fields(properties.EMPTY)
        self.board.fields[properties.BOARD_HEIGHT - 1][0] = properties.ENEMY
        self.board.fields[properties.BOARD_HEIGHT - 1][1] = properties.ENEMY
        self.board.fields[properties.BOARD_HEIGHT - 1][2] = properties.ENEMY
        self.assertEqual(2, self.board.count_sequences(properties.ENEMY, 2))

    def test_evaluate(self):
        self.board.fields = board.generate_fields(properties.EMPTY)
        self.board.fields[properties.BOARD_HEIGHT - 1][0] = properties.ENEMY
        self.board.fields[properties.BOARD_HEIGHT - 1][1] = properties.ENEMY
        self.board.fields[properties.BOARD_HEIGHT - 1][2] = properties.ENEMY
        self.board.fields[properties.BOARD_HEIGHT - 1][3] = properties.ENEMY
        self.assertEqual((102294, 1), self.board.evaluate_player(properties.ENEMY))

    def test_is_game_over(self):
        self.board.fields = board.generate_fields(properties.ENEMY)
        self.assertTrue(self.board.is_game_over())

        self.board.fields = board.generate_fields(properties.EMPTY)
        self.assertFalse(self.board.is_game_over())
