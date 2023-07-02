from objects import Player
from pygame.sprite import Group as Layer
from pygame.locals import *
import numpy as np
import pygame
import time
import sys

pygame.init()
WIDTH, HEIGHT = 960, 540 # 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Mancala')

ICON = pygame.image.load("assets/icon.png").convert_alpha()
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load(f"assets/Table.png").convert_alpha()
WINDOW.blit(BACKGROUND, (0, 0))

OBJECTS = []
LAYERS = {0: Layer()}

PLAYERS = [Player(num) for num in range(2)]
FPS = 60


class Table():
    def __init__(self):
        self.turn = 0
        self.spacing = 95
        self.first_game = True


class GameManager():
    def __init__(self):
        self.You_Win = False
        self.In_Game = False
        self.real = False

        self.winner = None

    def new_game(self):
        self.In_Game = True
        self.You_Win = False
        self.winner = None


def update_layers():
    #WINDOW.blit(BACKGROUND, (0, 0))

    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)

    for _, layer in LAYERS.items():
        layer.update()
        layer.draw(WINDOW)

    pygame.display.flip()
    pygame.display.update() 


def main():
    clock = pygame.time.Clock()
    gameManager = GameManager()
    gameManager.new_game()

    while gameManager.In_Game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        update_layers()


if __name__ == '__main__':
    main()