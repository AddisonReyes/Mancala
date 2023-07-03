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

turn_pos = (187, 35)

OBJECTS = []
LAYERS = {0: Layer()}
FPS = 30

class Game():
    def __init__(self, gameManager):
        self.clock = pygame.time.Clock()
        self.gameManager = gameManager
        self.NEW_GAME = Button("NEW1.png")
        self.EXIT = Button("EXIT1.png")

    def get_current_player(self) -> Player:
        return self.players[self.turn]
    
    def start_game(self):
        self.table = Table()
        p1 = Player(self.table, 0, [i for i in range(1, 7)])
        p2 = Player(self.table, 7, [i for i in range(8, 14)])
        #p2.change_auto()

        self.players = [p2, p1]
        self.turn = 0

        self.draw_clusters()
        self.create_buttons()

    def draw_clusters(self):
        global clusters
        clusters = self.table.give_clusters()
        
        x_padding = 108
        y_padding = 252
        x, y = 208, 144
        second_row = False
        aux = 0

        store_x, store_y = 100, 270
        for cluster in clusters:
            if cluster not in OBJECTS:
                OBJECTS.append(cluster)

            if cluster.is_store():
                cluster.add_position(store_x, store_y)
                store_x += 761

            else:
                cluster.add_position(x, y)
                if aux == 5:
                    x, y = 752, 144 + y_padding
                    second_row = True
                    
                else:
                    if second_row:
                        x -= x_padding
                    else:
                        x += x_padding

                aux += 1

        self.draw_stones()

    def draw_stones(self):
        for cluster in clusters:
            if cluster.is_store():
                x, y = cluster.give_position()
                x, y = x - 35, y - 80
                X, Y = x, y
                y_padding = 24
                aux = 0

                for stone in cluster.stones:
                    if stone not in OBJECTS:
                        OBJECTS.append(stone)

                    if aux == 4:
                        x, y = X, Y
                        y += y_padding
                        
                        y_padding += y_padding
                        aux = 0

                    stone.add_position(x, y)
                    x += 24
                    
                    aux +=1
            
            else:
                x, y = cluster.give_position()
                x, y = x - 24, y - 22
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

    def create_buttons(self):
        global NEW_GAME
        global EXIT

        NEW_GAME = self.NEW_GAME
        EXIT = self.EXIT

        x, y = 93, 48
        buttons = [NEW_GAME, EXIT]
        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

            button.add_position(x, y)
            x += 48

    def main(self):
        global turn

        self.gameManager.new_game()
        self.start_game()
        update_layers()

        last_cluster = None
        turn = None

        while self.gameManager.In_Game:
            self.clock.tick(FPS)
            update_layers()
            played = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if NEW_GAME.click_me():
                        self.gameManager.repeat()
                        played = -1
                        break

                    if EXIT.click_me():
                        pygame.quit()
                        sys.exit()

            curr_player = self.get_current_player()
            if played == -1:
                break

            while played != True:
                if curr_player.manual:
                    turn = pygame.image.load(f"assets/Mancala (Interface)/Tu turno.png").convert_alpha()
                    cluster_selected = False

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == MOUSEBUTTONDOWN and cluster_selected != True:
                            for cluster in self.table.clusters:
                                if cluster.click_me() and cluster.player_store != True:
                                    cluster_selected = True

                                    last_cluster = curr_player.stream(cluster.cluster_id)
                                    if last_cluster is not None: 
                                        played = True

                        if event.type == MOUSEBUTTONDOWN:
                            if NEW_GAME.click_me():
                                self.gameManager.repeat()
                                played = -1
                                break

                            if EXIT.click_me():
                                pygame.quit()
                                sys.exit()

                    update_layers()

                else:
                    pass

                if played == -1:
                    break
            
            if played == -1:
                break

            if last_cluster.cluster_id == curr_player.store_id:
                print("Felicidades, otro turno!!!")
                continue

            if len(last_cluster.stones) == 1:
                self.table.take_it_all(last_cluster, curr_player)
            
            self.turn += 1
            turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()
            if self.turn >= len(self.players): 
                self.turn = 0

            update_layers()

        return None


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

    def win(self, winner):
        self.In_Game = False
        self.You_Win = True
        self.winner = winner

    def repeat(self):
        self.In_Game = False
        self.You_Win = False
        self.winner = None
        return -1


def update_layers():
    WINDOW.blit(BACKGROUND, (0, 0))
    game.draw_clusters()

    try:
        WINDOW.blit(turn, turn_pos)
    except:
        pass

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
    global game

    gameManager = GameManager()
    game = Game(gameManager)
    
    while True:
        game.main()


if __name__ == '__main__':
    run()