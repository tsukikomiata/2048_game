import pygame as pg
import random
import sys
import copy

from pygame.locals import *


black_color = (0, 0, 0)
white_color = (255, 255, 255)


class Board:
    def __init__(self, game, copied=False):
        self.board = [['.', '.', '.', '.'],
                      ['.', '.', '.', '.'],
                      ['.', '.', '.', '.'],
                      ['.', '.', '.', '.']]
        self.board[random.randint(0, 3)][random.randint(0, 3)] = 4
        self.board[random.randint(0, 3)][random.randint(0, 3)] = 2
        self.game = game
        self.copied = copied

    def get_empty(self):
        empty = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == '.':
                    empty.append((i, j))
        return empty

    def random(self):
        empty = self.get_empty()
        if empty:
            i, j = random.choice(empty)
            value = random.choice([2] * 9 + [4])
            self.board[i][j] = value

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == '.':
                    return False
        return True

    def no_moves(self):
        for move in range(4):
            new_board = Board(game, True)
            new_board.board = copy.deepcopy(self.board)
            move_list = [new_board.up, new_board.down, new_board.left, new_board.right]
            move_list[move]()
            if new_board.board != self.board:
                return False
        return True

    def up(self):
        score = 0
        can_combine = [True, True, True, True]
        move_count = -1

        for j in range(4):
            if '.' not in [self.board[i][j] for i in range(4)] and \
                    self.board[0][j] == self.board[1][j] and \
                    self.board[2][j] == self.board[3][j]:
                self.board[0][j] *= 2
                self.board[1][j] = self.board[2][j] * 2
                self.board[2][j] = '.'
                self.board[3][j] = '.'
                can_combine[j] = False
                score += self.board[0][j] + self.board[1][j]
                if not self.copied:
                    self.game.draw()

        while move_count != 0:
            move_count = 0
            for i in range(1, 4):
                for j in range(4):
                    if self.board[i][j] != '.':
                        if self.board[i - 1][j] == '.':
                            self.board[i][j], self.board[i - 1][j] = self.board[i - 1][j], self.board[i][j]
                            move_count += 1
                        elif self.board[i - 1][j] == self.board[i][j] and can_combine[j]:
                            self.board[i - 1][j] *= 2
                            self.board[i][j] = '.'
                            can_combine[j] = False
                            score += self.board[i - 1][j]
                            move_count += 1
                if not self.copied:
                    self.game.draw()
        return score

    def left(self):
        score = 0
        can_combine = [True, True, True, True]
        move_count = -1

        for i in range(4):
            if '.' not in [self.board[i][j] for j in range(4)] and \
                    self.board[i][0] == self.board[i][1] and \
                    self.board[i][2] == self.board[i][3]:
                self.board[i][0] *= 2
                self.board[i][1] = self.board[i][2] * 2
                self.board[i][2] = '.'
                self.board[i][3] = '.'
                can_combine[i] = False
                score += self.board[i][0] + self.board[i][1]
                if not self.copied:
                    self.game.draw()

        while move_count != 0:
            move_count = 0
            for j in range(1, 4):
                for i in range(4):
                    if self.board[i][j] != '.':
                        if self.board[i][j - 1] == '.':
                            self.board[i][j], self.board[i][j - 1] = self.board[i][j - 1], self.board[i][j]
                            move_count += 1
                        elif self.board[i][j - 1] == self.board[i][j] and can_combine[i]:
                            self.board[i][j - 1] *= 2
                            self.board[i][j] = '.'
                            can_combine[i] = False
                            score += self.board[i][j - 1]
                            move_count += 1
                if not self.copied:
                    self.game.draw()
        return score

    def down(self):
        can_combine = [True, True, True, True]
        score = 0
        move_count = -1
        for j in range(4):
            if '.' not in [self.board[i][j] for i in range(4)] and \
                    self.board[0][j] == self.board[1][j] and \
                    self.board[2][j] == self.board[3][j]:
                self.board[3][j] *= 2
                self.board[2][j] = self.board[1][j] * 2
                self.board[1][j] = '.'
                self.board[0][j] = '.'
                can_combine[j] = False
                score += self.board[3][j] + self.board[2][j]
                if not self.copied:
                    self.game.draw()

        while move_count != 0:
            move_count = 0
            for i in [2, 1, 0]:
                for j in range(4):
                    if self.board[i][j] != '.':
                        if self.board[i + 1][j] == '.':
                            self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
                            move_count += 1
                        elif self.board[i + 1][j] == self.board[i][j] and can_combine[j]:
                            self.board[i + 1][j] *= 2
                            self.board[i][j] = '.'
                            can_combine[j] = False
                            score += self.board[i + 1][j]
                            move_count += 1
                if not self.copied:
                    self.game.draw()
        return score

    def right(self):
        can_combine = [True, True, True, True]
        score = 0
        move_count = -1
        for i in range(4):
            if '.' not in [self.board[i][j] for j in range(4)] and \
                    self.board[i][0] == self.board[i][1] and \
                    self.board[i][2] == self.board[i][3]:
                self.board[i][3] *= 2
                self.board[i][2] = self.board[i][1] * 2
                self.board[i][1] = '.'
                self.board[i][0] = '.'
                can_combine[i] = False
                score += self.board[i][3] + self.board[i][2]
                if not self.copied:
                    self.game.draw()

        while move_count != 0:
            move_count = 0
            for j in [2, 1, 0]:
                for i in range(4):
                    if self.board[i][j] != '.':
                        if self.board[i][j + 1] == '.':
                            self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
                            move_count += 1
                        elif self.board[i][j + 1] == self.board[i][j] and can_combine[i]:
                            self.board[i][j + 1] *= 2
                            self.board[i][j] = '.'
                            can_combine[i] = False
                            score += self.board[i][j + 1]
                            move_count += 1
                if not self.copied:
                    self.game.draw()
        return score


class Cell(pg.sprite.Sprite):
    colors = {'.': Color(254, 232, 138), 2: Color(254, 209, 93), 4: Color(254, 186, 47), 8: Color(255, 168, 20),
              16: Color(255, 158, 15), 32: Color(250, 69, 10), 64: Color(255, 77, 0),
              128: Color(255, 36, 0), 256: Color(255, 43, 43), 512: Color(255, 0, 0), 1024: Color(204, 0, 0),
              2048: Color(169, 29, 17), 4096: Color(120, 21, 12)}

    def __init__(self, pos, width=100, height=100, value=2):
        font = pg.font.Font('8-BIT WONDERmini.TTF', 48)
        pg.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.value = value
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = pos
        self.image = pg.Surface(self.rect.size)
        self.image.fill(Color(self.colors[self.value]))
        self.label = font.render(str(self.value), 1, black_color)
        self.labelrect = self.label.get_rect()
        self.imagerect = self.image.get_rect()
        self.labelrect.center = self.imagerect.center
        if self.value != '.':
            self.image.blit(self.label, self.labelrect)


class GameMain():
    done = False
    color_bg = Color(Color(242, 232, 201))

    def __init__(self, width=550, height=550, high_score=0):
        pg.init()
        self.game_over = False
        self.font = pg.font.Font('8-BIT WONDERmini.TTF', 24)
        self.width, self.height = width, height
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.board = Board(self)
        self.score = 0
        try:
            if high_score == 0:
                with open("high_score.txt", "rb") as f:
                    self.high_score = int(f.read().strip())
        except:
            self.high_score = high_score

    def draw_board(self):
        self.cells = pg.sprite.Group()

        cur_x, cur_y = 100, 100
        for row in self.board.board:
            for square in row:
                new_cell = Cell((cur_x, cur_y), value=square)
                self.cells.add(new_cell)
                cur_x += 110
            cur_y += 110
            cur_x = 100
        self.cells.draw(self.screen)

    def main_loop(self):
        while not self.done:
            self.handle_events()

            if self.score > self.high_score:
                self.high_score = self.score

            self.draw()
            self.clock.tick(30)
            if self.board.no_moves():
                self.game_over = True
                self.end_screen = pg.Surface((500, 500))
                self.end_screen_rect = self.end_screen.get_rect()
                # self.done = True
        with open("high_score.txt", 'wb') as f:
            f.write(bytes(self.high_score))
        pg.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(self.color_bg)
        if self.game_over:
            self.game_over_label1 = self.font.render("Game Over", 1, white_color)
            self.game_over_label2 = self.font.render("Final Score: %d" % (self.score), 1, white_color)
            self.game_over_label3 = self.font.render("Press Space Bar to Play Again", 1, white_color)
            self.end_screen.blit(self.game_over_label1, (175, 30))
            self.end_screen.blit(self.game_over_label2, (150, 70))
            self.end_screen.blit(self.game_over_label3, (20, 440))
            self.screen.blit(self.end_screen, (25, 25))
        else:
            self.draw_board()
            self.score_label = self.font.render("Score: %d" % (self.score), 1, black_color)
            self.screen.blit(self.score_label, (50, 10))
            self.hiscore_label = self.font.render("High Score: %d" % (self.high_score), 1, black_color)
            self.screen.blit(self.hiscore_label, (300, 10))
        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == KEYDOWN and not self.game_over:
                if event.key == K_ESCAPE:
                    self.done = True
                elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                    self.current_board = copy.deepcopy(self.board.board)
                    if event.key == K_UP:
                        self.score += self.board.up()
                    elif event.key == K_DOWN:
                        self.score += self.board.down()
                    elif event.key == K_LEFT:
                        self.score += self.board.left()
                    elif event.key == K_RIGHT:
                        self.score += self.board.right()

                    if self.current_board != self.board.board:
                        self.board.random()
            elif event.type == KEYDOWN and self.game_over:
                if event.key == K_SPACE:
                    self.__init__(high_score=self.high_score)


if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
