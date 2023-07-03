from pygame.sprite import Group as Layer
from pygame.locals import *
from objects import *
import numpy as np
import pygame
import time
import sys

pygame.init()
WIDTH, HEIGHT = 960, 540
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
        p1 = Player(self.table, 7, [i for i in range(8, 14)], 1)
        p2 = Player(self.table, 0, [i for i in range(1, 7)], 2)       
        #p2.change_auto()

        self.players = [p1, p2]
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

    def check_game_status(self):
        clear_table = False
        for player in self.players:
            no_stones = 0
            for idx in player.cluster_ids:
                if len(self.table.clusters[idx].stones) == 0:
                    no_stones += 1

                else:
                    break

            if no_stones >= len(player.cluster_ids):
                self.gameManager.check_for_winner()
                clear_table = True

        if clear_table:
            for player in self.players:
                for idx in player.cluster_ids:
                    while len(self.table.clusters[idx].stones) >= 1:
                        try:
                            self.table.clusters[player.store_id].stones.append(self.table.clusters[idx].stones[0])
                            self.table.clusters[idx].stones.remove(self.table.clusters[idx].stones[0])
                            update_layers()
                        
                        except:
                            break

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
            print(f"\nTurno del jugador #{curr_player.num}")
            if played == -1:
                break

            while played != True:
                self.check_game_status()
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

            self.check_game_status()
            update_layers()

        return self.gameManager


class GameManager():
    def __init__(self):
        self.You_Win = False
        self.In_Game = False
        self.real = False

        self.winner = None

    def new_game(self):
        self.search_winner = False
        self.In_Game = True
        self.You_Win = False
        self.winner = None

    def check_for_winner(self):
        self.In_Game = False
        self.search_winner = True

    def win(self, winner):
        self.winner = winner
        print(f"\nEl jugador #{self.winner.num} ganó el juego")

    def tie(self):
        print("Empate!")

    def repeat(self):
        self.In_Game = False
        self.You_Win = False
        self.winner = None
        return -1


class MinimaxSolver():
    def __init__(self, max_depth=6, ts=None, max_time=None, timeit=False):
        self.max_depth = max_depth
        self.max_time = max_time
        self.timeit = timeit
        self.ts = ts

    def solve(self, state):
        max_child, _ = self.__maximize(state, -np.inf, np.inf, 0)
        return max_child

    def __maximize(self, state, alpha, beta, depth):
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = game.check_game_status()
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic())
        
        max_child, max_utility = (None, -np.inf)
        for child in state.childrens():
            _, utility = self.__minimize(child, alpha, beta, depth + 1)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if utility >= beta:
                break

            alpha = max(alpha, max_utility)
        return max_child, max_utility
    
    def __minimize(self, state, alpha, beta, depth):
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = game.check_game_status()
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic())
        
        min_child, min_utility = (None, np.inf)
        for child in state.childrens():
            _, utility = self.__maximize(child, alpha, beta, depth + 1)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if utility < alpha:
                break

            beta = min(beta, min_utility)
        return min_child, min_utility


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
    global gameManager
    global game

    gameManager = GameManager()
    game = Game(gameManager)
    
    while True:
        gameManager = game.main()

        if game.gameManager.search_winner:
            p1 = game.players[0].count_stones()
            p2 = game.players[1].count_stones()

            print(f"Conteo:\nJugador #1(Tu): {p1}\nJugador #2: {p2}")
            if p1 > p2:
                gameManager.win(game.players[0])
            elif p2 > p1:
                gameManager.win(game.players[1])
            else:
                gameManager.tie()


if __name__ == '__main__':
    run()