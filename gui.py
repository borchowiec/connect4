"""
Zawiera funkcje które rysują elementy gry.
"""

import sys
import properties


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
        self.screen.fill((0, 150, 255))

        # paint all squares
        for j in range(properties.BOARD_WIDTH):
            for i in range(properties.BOARD_HEIGHT):
                x = properties.GAP * (j + 1) + j * properties.FIELD_SIZE
                y = properties.GAP * (i + 1) + i * properties.FIELD_SIZE

                # uppercase character means winning move
                if board.fields[i][j].isupper():
                    size = properties.FIELD_SIZE + properties.GAP * 2
                    self.pygame.draw.rect(self.screen, (34, 10, 209),
                                          self.pygame.Rect(x - properties.GAP, y - properties.GAP, size, size))
                    board.fields[i][j] = board.fields[i][j].lower()

                if board.fields[i][j] == properties.PLAYER:
                    self.pygame.draw.rect(self.screen, (255, 255, 0),
                                          self.pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))
                elif board.fields[i][j] == properties.ENEMY:
                    self.pygame.draw.rect(self.screen, (255, 0, 0),
                                          self.pygame.Rect(x, y, properties.FIELD_SIZE, properties.FIELD_SIZE))
                else:
                    self.pygame.draw.rect(self.screen, (255, 255, 255),
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
        text = self.font.render(message, True, (0, 0, 0))
        x = (properties.SCREEN_WIDTH - text.get_width()) // 2
        y = (properties.SCREEN_HEIGHT - text.get_height()) // 2
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
