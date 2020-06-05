import unittest

import alphabeta
import board
import properties


class AlphabetaTest(unittest.TestCase):
    def test_alphabeta(self):
        current_board = board.Board()
        current_board.fields[properties.BOARD_HEIGHT - 1][0] = properties.ENEMY
        current_board.fields[properties.BOARD_HEIGHT - 1][1] = properties.ENEMY
        current_board.fields[properties.BOARD_HEIGHT - 1][2] = properties.ENEMY
        current_board.fields[properties.BOARD_HEIGHT - 2][0] = properties.PLAYER
        current_board.fields[properties.BOARD_HEIGHT - 2][1] = properties.PLAYER
        current_board.fields[properties.BOARD_HEIGHT - 2][2] = properties.PLAYER
        current_board.fields[properties.BOARD_HEIGHT - 3][2] = properties.PLAYER

        expected = 3
        self.assertEqual(expected, alphabeta.alphabeta(current_board, 4))


if __name__ == '__main__':
    unittest.main()
