import pygame
import random
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
#A specific cube moves
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
#Draws specific cubes on the screen
        dis = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        pygame.draw.rect(surface, self.color, (rw * dis + 1, cm * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circle_middle = (rw * dis + center - radius - 2, cm * dis + 8)
            circle_middle2 = (rw * dis + dis - radius * 2, cm * dis + 8)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle, radius)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle2, radius)

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
#Responsible for moving the snake, remembering the position of the bends and transferring them to move subsequent body elements. It uses the operation of the Cube class.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    self.game_over()
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    self.game_over()
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    self.game_over()
                elif c.dirny == -1 and c.pos[1] <= 0:
                    self.game_over()
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.body.clear()
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
#He draws the whole thing with a snake consisting of smaller cubes. It uses the Cube class to operate
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def game_over(self):
        result = messagebox.askquestion("Game Over", "Do you want to play again?")
        if result == "yes":
            self.reset((10, 10))
        else:
            pygame.quit()
            quit()

def draw_grid(w, rows, surface):
#Draws a grid of lines on the screen
    size_between = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def draw_window(surface):
 #Responsible for main drawing the game window with each frame
    surface.fill((0, 255, 0))
    s.draw(surface)
    apple.draw(surface)
    draw_grid(size, rows, surface)
    pygame.display.update()

def draw_start_screen(surface):
 #START SCREEN
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    text_play = font.render("Play", True, (255, 255, 255))

    play_rect = text_play.get_rect(center=(size // 2, size // 2))
    pygame.draw.rect(surface, (50, 50, 50), play_rect)
    surface.blit(text_play, play_rect)

    pygame.display.update()

def random_apple(snake):
#resp random apples
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

def main():
#Main runs at the beginning of the game and is responsible for its operation
    global size, rows, s, apple
    size = 500 #game area
    rows = 20

    pygame.init()

    window = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    in_start_screen = True

    while in_start_screen:
        draw_start_screen(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    in_start_screen = False

    s = snake((0, 0, 0), (10, 10))
    apple = cube(random_apple(s), color=(255, 0, 0))
	# True game work
    flag = True

    while flag:
        pygame.time.delay(50)#the lower the value, the faster the game
        clock.tick(10)#the lower the value, the slower the game
        s.move()
        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = cube(random_apple(s), color=(255, 0, 0))

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):
                s.game_over()

        draw_window(window)

main()