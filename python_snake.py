"Python Snake Console Game | Author: Nazar Ponochevnyi | MIT License"

import os
import time
import random
import msvcrt


DIFFICULT = 1 # 1 - normal, 2 - easy, 0.5 - hard
AREA_HEIGHT = 20
AREA_WIDTH = 43


class Area:
    def __init__(self, height, width):
        self.AREA_HEIGHT = height
        self.AREA_WIDTH = width
        self.AREA = [[' ' for _ in range(AREA_WIDTH)] for _ in range(AREA_HEIGHT)]

    def print_area(self):
        print(' ' + '_' * self.AREA_WIDTH)
        for i in range(self.AREA_HEIGHT):
            print('|', end='')
            print(''.join(self.AREA[i]), end='')
            print('|', end='\n')
        print('|' + '_' * self.AREA_WIDTH + '|')


class Snake:
    def __init__(self):
        self.BODY = [[2, 1], [1, 1]]
        self.X, self.Y = 3, 1
        self.LENGHT = 2
        self.DIST = 'R'

    def move(self):
        pos = [self.X, self.Y]
        if pos in self.BODY:
            return True
        if self.DIST == 'R':
            self.X += 1
            if self.X >= AREA_WIDTH:
                self.X -= AREA_WIDTH
        if self.DIST == 'L':
            self.X -= 1
            if self.X < 0:
                self.X += AREA_WIDTH
        if self.DIST == 'U':
            self.Y += 1
            if self.Y >= AREA_HEIGHT:
                self.Y -= AREA_HEIGHT
        if self.DIST == 'D':
            self.Y -= 1
            if self.Y < 0:
                self.Y += AREA_HEIGHT
        for i in range(self.LENGHT):
            self.BODY[i], pos = pos, self.BODY[i]
        return False

    def mirror_move(self):
        pos = [self.X, self.Y]
        self.BODY = self.BODY[::-1]
        self.X, self.Y = self.BODY.pop(0)
        self.BODY.append(pos)

    def change_dist(self, key):
        last = self.DIST
        if key == 77 and last != 'L':
            self.DIST = 'R'
            # if last == 'L': self.mirror_move()
        if key == 75 and last != 'R':
            self.DIST = 'L'
            # if last == 'R': self.mirror_move()
        if key == 80 and last != 'D':
            self.DIST = 'U'
            # if last == 'D': self.mirror_move()
        if key == 72 and last != 'U':
            self.DIST = 'D'
            # if last == 'U': self.mirror_move()

    def eat(self, food):
        if self.X == food.X and self.Y == food.Y:
            self.BODY.append(self.BODY[-1])
            self.BODY[-1][0] -= 1
            self.LENGHT += 1
            food = Food(self)
        return food

    def print_snake(self, area):
        for x, y in self.BODY:
            area[y][x] = '♪' # *
        area[self.Y][self.X] = '☺' # 0


class Food:
    def __init__(self, snake):
        self.X = random.randint(0, AREA_WIDTH - 1)
        self.Y = random.randint(0, AREA_HEIGHT - 1)
        while [self.X, self.Y] in snake.BODY:
            self.X = random.randint(0, AREA_WIDTH - 1)
            self.Y = random.randint(0, AREA_HEIGHT - 1)

    def print_food(self, area):
        area[self.Y][self.X] = '○' # ~


class Game:
    def __init__(self, area_height, area_width, difficult):
        self.DIFFICULT = difficult
        self.AREA_HEIGHT = area_height
        self.AREA_WIDTH = area_width
        self.AREA = Area(self.AREA_HEIGHT, self.AREA_WIDTH)
        self.SNAKE = Snake()
        self.FOOD = Food(self.SNAKE)
        self.GAME_OVER = False

    def fill(self):
        os.system('cls')
        print('\n ' + ' ' * (self.AREA_WIDTH // 3) \
                    + 'YOUR LENGTH:', self.SNAKE.LENGHT)
        self.AREA = Area(self.AREA_HEIGHT, self.AREA_WIDTH)
        self.FOOD.print_food(self.AREA.AREA)
        self.SNAKE.print_snake(self.AREA.AREA)
        self.AREA.print_area()

    def time_delay(self):
        if self.SNAKE.DIST in ['R', 'L']:
            time.sleep(0.1 * self.DIFFICULT)
        else:
            time.sleep(0.2 * self.DIFFICULT)

    def start(self):
        # os.system('color c')
        while not self.GAME_OVER:
            self.fill()
            self.time_delay()
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                if key == 27:
                    break
                self.SNAKE.change_dist(key)
            self.GAME_OVER = self.SNAKE.move()
            self.FOOD = self.SNAKE.eat(self.FOOD)
        print('\n   ' + ' ' * (self.AREA_WIDTH // 3) + 'GAME OVER!')
        # os.system('color a')


if __name__ == '__main__':
    GAME = Game(AREA_HEIGHT, AREA_WIDTH, DIFFICULT)
    GAME.start()
