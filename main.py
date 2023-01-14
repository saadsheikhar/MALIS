import pygame
from copy import deepcopy
from random import choice, randrange

from SDG import get_move

from utils import *


class Game:
    def __init__(self):
        self.W, self.H = 10, 20
        self.TILE = 45  # Dimension of Tile
        self.GAME_RES = self.W * self.TILE, self.H * self.TILE  # Dimension of the Game-part window
        self.RES = 900, 940
        self.FPS = 60

    def check_borders(self, figure, field, i):
        if figure[i].x < 0 or figure[i].x > self.W - 1:
            return False
        elif figure[i].y > self.H - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

    def get_record(self):
        try:
            with open('record') as file:
                return file.readline()
        except FileNotFoundError:
            with open('record', 'w') as file:
                file.write('0')

    def set_record(self, record, score):
        best_score = max(int(record), score)
        with open('record', 'w') as file:
            file.write(str(best_score))

    def get_score(self):
        return self.score

    def run(self):
        pygame.init()
        pygame.mixer.music.load('./music/Tetris.mp3')
        pygame.mixer.music.play()

        screen = pygame.display.set_mode(self.RES)
        game_screen = pygame.Surface(self.GAME_RES)
        clock = pygame.time.Clock()

        # To prepare the grid
        grid = [pygame.Rect(x * self.TILE, y * self.TILE, self.TILE, self.TILE) for x in range(self.W) for y in
                range(self.H)]

        # To generate colors

        get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

        # To draw the 7 types of figures

        figures_positions = [[(-2, 0), (-1, 0), (0, 0), (1, 0)],
                             [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                             [(0, -1), (1, -1), (0, 0), (-1, 0)],
                             [(0, 0), (0, -1), (1, 0), (-1, -1)],
                             [(0, 0), (-1, 0), (1, 0), (-1, -1)],
                             [(0, 0), (-1, 0), (1, 0), (1, -1)],
                             [(-1, 0), (0, 0), (1, 0), (0, -1)]]

        PIECES = {
            '0': 'I',
            '1': 'O',
            '2': 'S',
            '3': 'Z',
            '4': 'J',
            '5': 'L',
            '6': 'T'
        }

        figures = [[pygame.Rect(x + self.W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_positions]
        figure_rect = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)

        anim_count, anim_speed, anim_limit = 0, 2000, 2000
        figure, next_figure = deepcopy(choice(
            figures)), deepcopy(choice(
            figures))  # We want to keep a save of the figure before any modification of his attributes and make the choice random

        color, next_color = get_color(), get_color()
        piece = {"shape": PIECES[str(figures.index(figure))], "rotation": 0, "x": W // 2 - 2, "y": -2}

        score, lines = 0, 0
        scores = {0: 0, 1: 100, 2: 300, 3: 700,
                  4: 1500}  # Score and Bonus points depending on the number of lines destroyed

        field = [[0 for i in range(self.W)] for j in range(self.H)]



        background = pygame.image.load('./images/Background.jpg').convert()
        game_background = pygame.image.load('./images/background2.jpg').convert()

        main_font = pygame.font.Font('./Fonts/font.ttf', 50)
        main_font = pygame.font.Font('./Fonts/font.ttf', 30)

        title = main_font.render('Machine Learning Tetris', True, pygame.Color('darkorange'))
        title_score = main_font.render('Score : ', True, pygame.Color('green'))
        title_record = main_font.render('Record :', True, pygame.Color('purple'))
        u = 0
        p = 0
        while True:
            record = self.get_record()
            dx = 0  # To be able to move the figure horizontally
            rotate = False
            screen.blit(background, (0, 0))
            screen.blit(game_screen, (20, 20))
            game_screen.blit(game_background, (0, 0))

            board = [['0' for i in range(self.H)] for i in range(self.W)]
            for x in range(len(field[0])):
                for y in range (len(field[1])):
                    if type(field[y][x]) is int:
                        board[x][y] = str(field[y][x])
            # Delay for full lines
            for i in range(lines):
                pygame.time.wait(200)

            move = get_move(board, piece)
            print(move)

            # To manage events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:  # If we press a button
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    if event.key == pygame.K_RIGHT:
                        dx = 1
                    if event.key == pygame.K_DOWN:  # Acceleration when key down is pressed
                        anim_limit = 100
                    if event.key == pygame.K_UP:
                        rotate = True

            figure_old = deepcopy(figure)

            # To Rotate
            center = figure[0]
            if move is not None :
                while u < move[1]:
                    u += 1
                    for i in range(4):  # We move every point of the figure
                        x = figure[i].y - center.y
                        y = figure[i].x - center.x
                        figure[i].x = center.x - x
                        figure[i].y = center.y + y

                        if not self.check_borders(figure, field, i):
                            figure = deepcopy(figure_old)  # we restore the old figure because we are out of borders
                            break

            # Remove lines where they are completed
            line, lines = self.H - 1, 0  # To count number of lines destroyed / remaining
            for row in range(self.H - 1, -1, -1):
                count = 0
                for i in range(self.W):
                    if field[row][i]:
                        count += 1
                    field[line][i] = field[row][i]
                if count < self.W:
                    line -= 1
                else:
                    anim_speed += 1  # Increasing speed / Difficulty
                    lines += 1

            # Compute score
            score += scores[lines]
            # To move x
            if move is not None:
                while p < abs(move[0]):
                    p += 1
                    for i in range(4):  # We move every point of the figure
                        if move[0] > 0:
                            figure[i].x += 1
                        else:
                            figure[i].x -= 1
                        if not self.check_borders(figure, field, i):
                            figure = deepcopy(figure_old)  # we restore the old figure because we are out of borders
                            break

            # To move y
            anim_count += anim_speed
            if anim_count > anim_limit:
                anim_count = 0
                figure_old = deepcopy(figure)
                for i in range(4):
                    figure[i].y += 1
                    if not self.check_borders(figure, field, i):
                        for i in range(4):
                            field[figure_old[i].y][figure_old[i].x] = color  # To see the following figures

                        figure, color = next_figure, next_color
                        piece = {"shape": PIECES[str(figures.index(figure))], "rotation": 0, "x": W // 2 - 2, "y": -2}
                        u =0
                        p =0
                        next_figure, next_color = deepcopy(choice(figures)), get_color()  # Generation of next figure
                        anim_limit = 2000
                        break
            # To draw grid
            [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

            # To draw figure
            for i in range(4):  # 4 blocks per figure
                figure_rect.x = figure[i].x * self.TILE
                figure_rect.y = figure[i].y * self.TILE
                pygame.draw.rect(game_screen, color, figure_rect)

            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x, figure_rect.y = x * self.TILE, y * self.TILE
                        pygame.draw.rect(game_screen, col, figure_rect)

            # Draw Next figure

            for i in range(4):  # 4 blocks per figure
                figure_rect.x = next_figure[i].x * self.TILE + 450  # Overflow x to render on right
                figure_rect.y = next_figure[i].y * self.TILE + 250  # Overflow y
                pygame.draw.rect(screen, next_color, figure_rect)

            # draw Title & score
            screen.blit(title, (485, -10))
            screen.blit(title_score, (600, 800))
            screen.blit(main_font.render(str(score), True, pygame.Color('white')), (600, 850))

            screen.blit(title_record, (600, 600))
            screen.blit(main_font.render(record, True, pygame.Color('gold')), (625, 660))
            # If we loose
            for i in range(self.W):
                if field[0][i]:
                    self.set_record(record, score)
                    field = [[0 for i in range(self.W)] for i in range(self.H)]  # Clean game map
                    anim_count, anim_speed, anim_limit = 0, 2000, 2000  # Reset the speed to initial parameter
                    score = 0
                    for i_rect in grid:  # Animated Ending
                        pygame.draw.rect(game_screen, get_color(), i_rect)
                        screen.blit(game_screen, (20, 20))
                        pygame.display.flip()
                        clock.tick(200)
            pygame.display.flip()
            clock.tick()


A = Game()
A.run()
