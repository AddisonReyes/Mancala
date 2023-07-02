from pygame.sprite import Group as Layer
from pygame.locals import *
from objects import *
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
FPS = 30

class Game:
    def __init__(self, gameManager):
        self.clock = pygame.time.Clock()
        self.gameManager = gameManager

        self.table = Table()
        p1 = Player(self.table, 0, [i for i in range(1, 7)])
        p2 = Player(self.table, 7, [i for i in range(8, 14)])
        self.players = [p1, p2]
        self.turn = 0

    def get_current_player(self) -> Player:
        return self.players[self.turn]
    
    def start_game(self):
        self.draw_clusters()
        self.draw_stones()

    def draw_clusters(self):
        global clusters
        clusters = self.table.give_clusters()
        
        x_padding = 108
        y_padding = 252
        x, y = 208, 144
        aux = 0
        
        for cluster in clusters:
            if cluster not in OBJECTS:
                OBJECTS.append(cluster)

            if cluster.is_store():
                pass

            else:
                cluster.add_position(x, y)
                if aux == 5:
                    x, y = 208 + 4, 144 + y_padding
                    
                else:
                    x += x_padding

                aux += 1

    def draw_stones(self):
        for cluster in clusters:
            if cluster.is_store():
                continue
            
            else:
                x, y = cluster.give_position()
                x, y = x - 21, y - 21
                X, Y = x, y
                y_padding = 24
                aux = 0

                for stone in cluster.stones:
                    if stone not in OBJECTS:
                        OBJECTS.append(stone)

                    if aux == 3:
                        x, y = X, Y
                        y += y_padding
                        
                        y_padding += y_padding
                        aux = 0

                    stone.add_position(x, y)
                    x += 24
                    
                    aux +=1
                    
    
    def main(self):
        self.gameManager.new_game()
        self.start_game()
        update_layers()

        aux = 1
        while self.gameManager.In_Game:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        #    print(f"\nTURNO {self.turn}")

            #curr_player = self.get_current_player()

            #while True:
                #cluster_id = int(input("Cluster to stream: "))
                #last_cluster = curr_player.stream(cluster_id)
                #if last_cluster is not None: break
                #print("Cluster invalido !!!!!!")
            
            #if last_cluster.pos == curr_player.store_id:
                #print("Felicidades, otro turno!!!")
                #continue
            
            #self.turn += 1
            #if self.turn >= len(self.players): 
                #self.turn = 0

            update_layers()


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


def run():
    global GameManager
    gameManager = GameManager()

    game = Game(gameManager)
    game.main()


if __name__ == '__main__':
    run()