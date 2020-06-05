"""
Zawiera funkcje które rysują elementy gry.
"""

import sys

import properties


class Colors:
    BACKGROUND = (0, 43, 54)
    HIGHLIGHT = (238, 232, 213)
    EMPTY_FIELD = (253, 246, 227)
    FONT = (253, 246, 227)
    PLAYER = (181, 137, 0)
    ENEMY = (220, 50, 47)


FIELD_COLORS = {
    properties.EMPTY: Colors.EMPTY_FIELD,
    properties.PLAYER: Colors.PLAYER,
    properties.ENEMY: Colors.ENEMY
}


class Gui:
    def __init__(self, screen, font, pygame):
        self.screen = screen
        self.font = font
        self.pygame = pygame

    @staticmethod
    def get_clicked_column(pos):
        """
        Na podstawie pozycji kliknięcia które zostało przesłane, wylicza która kolumna została kliknięta.
        :param pos: Pozycja kliknięcia myszki.
        :return: Number klikniętej kolumny.
        """
        x, y = pos
        return int(x // (properties.FIELD_SIZE + properties.GAP + properties.GAP / properties.BOARD_WIDTH))

    def paint_board(self, board):
        """
        Rysuje przesłaną planszę.
        :param board: Plansza która będzie narysowana.
        """

        # background
        self.screen.fill(Colors.BACKGROUND)

        # paint all squares
        for j in range(properties.BOARD_WIDTH):
            for i in range(properties.BOARD_HEIGHT):
                x = properties.GAP * (j + 1) + j * properties.FIELD_SIZE
                y = properties.GAP * (i + 1) + i * properties.FIELD_SIZE

                # uppercase character means winning move
                if board.fields[i][j].isupper():
                    size = properties.FIELD_SIZE + properties.GAP * 2
                    self.pygame.draw.rect(self.screen, Colors.FONT,
                                          self.pygame.Rect(x - properties.GAP, y - properties.GAP, size, size))
                    board.fields[i][j] = board.fields[i][j].lower()

                self.pygame.draw.rect(self.screen, FIELD_COLORS[board.fields[i][j]],
                                      self.pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))
        self.pygame.display.flip()

    def game_over(self, board, message):
        """
        Rysuje planszę wraz z komunikatem.
        :param board: Plansza która będzie narysowana.
        :param message: Wiadomość która zostanie wypisana na ekranie.
        :return:
        """
        # print message and wait
        self.paint_board(board)
        text = self.font.render(message, True, Colors.EMPTY_FIELD)
        x = (properties.SCREEN_WIDTH - text.get_width()) // 2
        y = (properties.SCREEN_HEIGHT - text.get_height()) // 2

        # box
        s = self.pygame.Surface((text.get_width(), text.get_height()))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (x, y))

        # text
        self.screen.blit(text, (x, y))
        self.pygame.display.flip()

        # quit game or play again
        wait = True
        while wait:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    sys.exit(0)
                elif event.type == self.pygame.MOUSEBUTTONUP:
                    wait = False
