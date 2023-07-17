from pygame.sprite import Group as Layer
from pygame.locals import *
from objects import *
import numpy as np
import pygame
import time
import sys


pygame.init()
#mixer.init()

WIDTH, HEIGHT = 960, 540
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Mancala')
ICON = pygame.image.load("assets/icon.png").convert_alpha()
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load(f"assets/{SKINS[skin]} Table.png").convert_alpha()
WINDOW.blit(BACKGROUND, (0, 0))

turn_pos = (400, 36)
new_turn_pos = (700, 37)

OBJECTS = []
LAYERS = {0: Layer()}

SKINS = SKINS
skin = skin

TAKEIT_SOUND =  pygame.mixer.Sound('assets/Audio/take_it.mp3')
ROCKS_SOUND =  pygame.mixer.Sound('assets/Audio/rocks.mp3')
WIN_SOUND =  pygame.mixer.Sound('assets/Audio/win.mp3')

sleep_time = 0.6
FPS = 30


class Game():
    def __init__(self, gameManager):
        self.arrows = np.array([Arrow("arrow.png") for _ in range(6)], dtype=object)

        self.clock = pygame.time.Clock()
        self.gameManager = gameManager
        self.first_game = True
        self.NUM_STONES = 3

        self.TWO_PLAYERS = False
        self.another_turn = False

    def get_current_player(self) -> Player:
        return self.players[self.turn]
    
    def start_game(self):
        self.table = Table(self.NUM_STONES)
        p1 = Player(self.table, 7, [i for i in range(8, 14)], 1)
        p2 = Player(self.table, 0, [i for i in range(1, 7)], 2)

        #p1.change_auto()
        if not self.TWO_PLAYERS:
            p2.change_auto()

        self.players = np.array([p1, p2], dtype=object)
        self.turn = 0

        self.draw_clusters()

        if self.first_game:
            self.create_buttons()
            self.first_game = False
        
        else:
            self.refresh_sprites()

    def draw_arrows(self):
        player = self.get_current_player()
        idx = 0

        if not player.manual:
            self.hide_arrows()
            return

        for cluste_idx in player.cluster_ids:
            if player.num == 1:
                if self.arrows[idx] not in OBJECTS:
                    OBJECTS.append(self.arrows[idx])

                cluster = clusters[cluste_idx]
                x, y = cluster.give_position()
                x, y = x, y - 66

                if len(cluster.stones) == 0:
                    self.arrows[idx].add_position(x, y)
                    self.arrows[idx].reset_orientation()
                    self.arrows[idx].hide()

                    self.arrows[idx].update()

                else:
                    self.arrows[idx].add_position(x, y)
                    self.arrows[idx].reset_orientation()
                    self.arrows[idx].show()

                    self.arrows[idx].update()

                idx += 1
            
            else:
                if self.arrows[idx] not in OBJECTS:
                    OBJECTS.append(self.arrows[idx])

                cluster = clusters[cluste_idx]
                x, y = cluster.give_position()
                x, y = x, y + 66

                if len(cluster.stones) == 0:
                    self.arrows[idx].add_position(x, y)
                    self.arrows[idx].change_orientation()
                    self.arrows[idx].hide()

                    self.arrows[idx].update()

                else:
                    self.arrows[idx].add_position(x, y)
                    self.arrows[idx].change_orientation()
                    self.arrows[idx].show()

                    self.arrows[idx].update()

                idx += 1

    def hide_arrows(self):
        for i in range(6):
            self.arrows[i].hide()
            self.arrows[i].update()

    def draw_clusters(self):
        global clusters
        clusters = self.table.give_clusters()
        
        x_padding = 108
        y_padding = 252
        x, y = 208, 144
        second_row = False
        aux = 0

        store_x, store_y = 99, 270
        for cluster in clusters:
            if cluster not in OBJECTS:
                OBJECTS.append(cluster)

            if cluster.is_store():
                cluster.add_position(store_x, store_y)
                store_x += 762

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
                x, y = x - 35, y - 120
                X, Y = x, y

                x_padding = 24
                y_padding = 24
                stone_added = 0
                aux = 0

                for stone in cluster.stones:
                    if stone not in OBJECTS:
                        OBJECTS.append(stone)

                    if stone_added < 44:
                        if aux == 4:
                            x = X
                            y += y_padding
                            aux = 0

                    elif stone_added == 44:
                        x, y = X + x_padding/2, Y - y_padding/2

                    elif stone_added == 47:
                        x, y = X + x_padding/2, Y + y_padding/2
                        aux = 0

                    else:
                        if aux == 3:
                            x, y = X + x_padding/2, y + y_padding/2
                            aux = 0

                    if stone_added == 84:
                        break

                    stone.add_position(x, y)

                    aux +=1
                    x += x_padding
                    stone_added += 1
            
            else:
                x, y = cluster.give_position()
                x, y = x - 24, y - 26
                X, Y = x, y

                x_padding = 24
                y_padding = 24
                stone_added = 0
                aux = 0

                for stone in cluster.stones:
                    if stone not in OBJECTS:
                        OBJECTS.append(stone)

                    if stone_added < 9:
                        if aux == 3:
                            x = X
                            y += y_padding
                            aux = 0
                    
                    elif stone_added == 9:
                        x, y = X + x_padding/2, Y - y_padding/2

                    elif stone_added == 11:
                        x, y = X - x_padding/2, Y + y_padding/2

                    elif stone_added == 15:
                        x, y = X - x_padding/2, Y + y_padding/2 + y_padding

                    elif stone_added == 19:
                        x, y = X + x_padding/2, Y + y_padding*2 + y_padding/2

                    elif stone_added >= 21:
                        break

                    stone.add_position(x, y)

                    x += x_padding
                    aux +=1

                    stone_added += 1

    def create_buttons(self):
        global CHANGE_TABLE
        global ONE_PLAYER
        global TWO_PLAYER
        global STONES_3
        global STONES_5
        global STONES_7
        global NEW_GAME
        global HELP
        global EXIT

        NEW_GAME = Button("NEW1.png")
        EXIT = Button("EXIT1.png")

        x, y = 93, 48
        buttons = np.array([EXIT, NEW_GAME], dtype=object)
        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

            button.add_position(x, y)
            x += 48

        STONES_3 = Button("3p1.png")
        STONES_5 = Button("5p1.png")
        STONES_7 = Button("7p1.png")

        x, y = 771, 492
        buttons = np.array([STONES_3, STONES_5, STONES_7], dtype=object)
        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

            button.add_position(x, y)
            x += 48

        ONE_PLAYER = Button("onep1.png")
        TWO_PLAYER = Button("twop1.png")

        x, y = 588, 492
        buttons = np.array([ONE_PLAYER, TWO_PLAYER], dtype=object)
        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

            button.add_position(x, y)
            x += 48

        CHANGE_TABLE = Button("Change_Table1.png")
        HELP = Button("Help1.png")

        x, y = 93, 492
        buttons = np.array([HELP, CHANGE_TABLE], dtype=object)
        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

            button.add_position(x, y)
            x += 48

    def mouse_event(self):
        played = False
        if NEW_GAME.click_me():
            self.gameManager.repeat()
            played = -1

        if EXIT.click_me():
            pygame.quit()
            sys.exit()

        if STONES_3.click_me():
            self.NUM_STONES = 3
            played = -1

        if STONES_5.click_me():
            self.NUM_STONES = 5
            played = -1

        if STONES_7.click_me():
            self.NUM_STONES = 7
            played = -1

        if ONE_PLAYER.click_me():
            if self.TWO_PLAYERS:
                self.TWO_PLAYERS = False
                played = -1
                        
        if TWO_PLAYER.click_me():
            if not self.TWO_PLAYERS:
                self.TWO_PLAYERS = True
                played = -1

        if CHANGE_TABLE.click_me():
            global SKINS
            global skin 

            SKINS, skin = next_skin()
            self.refresh_sprites()

        if HELP.click_me():
            tutorial()

        return played
    
    def refresh_sprites(self):
        global BACKGROUND
        global new_turn
        global OBJECTS
        global turn
        global SKIN
        global skin

        BACKGROUND = pygame.image.load(f"assets/{SKINS[skin]} Table.png").convert_alpha()
        self.win_png = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} ganador.png").convert_alpha()
        self.tie_png = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} empate.png").convert_alpha()

        if not self.TWO_PLAYERS:
            turn = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} Tu turno.png").convert_alpha()

        if self.another_turn:
            new_turn = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} Otro_turno.png").convert_alpha()
        else:
            new_turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()

        for obj in OBJECTS:
            try:
                obj.change_skin()
            
            except:
                continue

        update_layers()

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
                clear_table = True
                break

        if clear_table:
            for player in self.players:
                for idx in player.cluster_ids:
                    while len(self.table.clusters[idx].stones) >= 1:
                        try:
                            self.table.clusters[player.store_id].stones = np.append(self.table.clusters[player.store_id].stones, self.table.clusters[idx].stones[0])
                            self.table.clusters[idx].stones = np.delete(self.table.clusters[idx].stones, np.where(self.table.clusters[idx].stones == self.table.clusters[idx].stones[0]))
                            update_layers()
                        
                        except:
                            break
            
            self.gameManager.check_for_winner()
            self.break_game = True

    def clean(self):
        self.table.clear_clusters()

    def main(self):
        self.gameManager.new_game()
        self.start_game()

        self.break_game = False
        last_cluster = None
        max_time = .6

        if not self.TWO_PLAYERS:
            global turn
            turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()

        global new_turn
        new_turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()

        while self.gameManager.In_Game:
            self.clock.tick(FPS)
            update_layers()

            self.real = False
            played = False

            self.check_game_status()
            if self.break_game or self.gameManager.In_Game != True:
                break

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    played = self.mouse_event()

            curr_player = self.get_current_player()
            if played == -1:
                break

            if curr_player.manual and self.gameManager.In_Game:
                if not self.TWO_PLAYERS:
                    turn = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} Tu turno.png").convert_alpha()

                self.check_game_status()
                cluster_selected = False

                while played != True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == MOUSEBUTTONDOWN:
                            played = self.mouse_event()

                        if event.type == MOUSEBUTTONDOWN and cluster_selected != True:
                            for cluster in self.table.clusters:
                                if cluster.click_me() and cluster.player_store != True:
                                    last_cluster = curr_player.stream(cluster.cluster_id)

                                    if last_cluster is not None:
                                        cluster_selected = True
                                        played = True

                    if played == -1:
                        break
                    
                    update_layers()
                ROCKS_SOUND.play()

            else:
                state = Fake_Table(self.table.clusters, player=curr_player)
                best_state = None

                ts = time.time()
                minimax_solver = MinimaxSolver(max_time=max_time, ts=ts)
                
                for depth in range(1, 20):
                    minimax_solver.max_depth = depth
                    new_state = minimax_solver.solve(state)

                    if new_state is not None:
                        best_state = new_state

                    if time.time() - ts >= max_time:
                        break

                
                last_cluster = curr_player.stream(best_state.played)
                
                update_layers()
                ROCKS_SOUND.play()
            
            if played == -1:
                break

            time.sleep(sleep_time) 
            if len(last_cluster.stones) == 1 and last_cluster.cluster_id != 0 and last_cluster.cluster_id != 7:
                sound = self.table.take_it_all(last_cluster, curr_player)
                
                if sound:
                    TAKEIT_SOUND.play()

            if last_cluster.cluster_id == curr_player.store_id:
                new_turn = pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} Otro_turno.png").convert_alpha()
                self.another_turn = True
                continue
            
            self.turn += 1
            if not self.TWO_PLAYERS:
                turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()

            new_turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()
            if self.turn >= len(self.players): 
                self.turn = 0

            self.check_game_status()
            update_layers()

        if not self.TWO_PLAYERS:
            turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()
        new_turn = pygame.image.load(f"assets/Mancala (Interface)/_.png").convert_alpha()
        self.another_turn = False
        
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
        WIN_SOUND.play()

        if self.winner.store_id == 0:
            WINDOW.blit(pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} ganador.png").convert_alpha(), (8, 166))
        else:
            WINDOW.blit(pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} ganador.png").convert_alpha(), (772, 166))

        pygame.display.flip()
        pygame.display.update()

    def tie(self):
        WINDOW.blit(pygame.image.load(f"assets/Mancala (Interface)/{SKINS[skin]} empate.png").convert_alpha(), (400, 240))

        pygame.display.flip()
        pygame.display.update()

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
        if state is None:
            return (None, -np.inf)
        
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = state.check_game_status(game.players)
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic())
        
        max_child, max_utility = (None, -np.inf)
        for child in state.childrens():
            if child is not None and max_child is None:
                max_child = child

            _, utility = self.__minimize(child, alpha, beta, depth + 1)

            if utility > max_utility and child is not None:
                max_child, max_utility = child, utility

            if utility >= beta:
                break

            alpha = max(alpha, max_utility)
        return max_child, max_utility
    
    def __minimize(self, state, alpha, beta, depth):
        if state is None:
            return (None, -np.inf)
        
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = state.check_game_status(game.players)
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic())
        
        min_child, min_utility = (None, np.inf)
        for child in state.childrens():
            if child is not None and min_child is None:
                min_child = child

            _, utility = self.__maximize(child, alpha, beta, depth + 1)

            if utility < min_utility and child is not None:
                min_child, min_utility = child, utility

            if utility < alpha:
                break

            beta = min(beta, min_utility)
        return min_child, min_utility


def update_layers():
    WINDOW.blit(BACKGROUND, (0, 0))
    game.draw_clusters()

    if game.TWO_PLAYERS:
        WINDOW.blit(new_turn, turn_pos)
        game.draw_arrows()

    else:
        game.draw_arrows()
        WINDOW.blit(new_turn, new_turn_pos)
        WINDOW.blit(turn, turn_pos)

    if gameManager.search_winner:
        game.hide_arrows()

    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)

    for _, layer in LAYERS.items():
        layer.update()
        layer.draw(WINDOW)

    pygame.display.flip()
    pygame.display.update()


def draw_total_stones(p1_stones, p2_stones):
    if len(p1_stones) == 2:
        p1_num0 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p1_stones[0]}.png").convert_alpha()
        p1_num1 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p1_stones[1]}.png").convert_alpha()

    else:
        p1_num0 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p1_stones}.png").convert_alpha()

    if len(p2_stones) == 2:
        p2_num0 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p2_stones[0]}.png").convert_alpha()
        p2_num1 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p2_stones[1]}.png").convert_alpha()

    else:
        p2_num0 = pygame.image.load(f"assets/Mancala (Game)/{SKINS[skin]} {p2_stones}.png").convert_alpha()

    stores = np.array([0, 7], dtype=int)
    x_padding = 36
    y_padding = 56

    for idx in stores:
        x, y = clusters[idx].give_position()
        x, y = x - x_padding, y - y_padding

        if idx == 7:
            if len(p1_stones) == 2:
                WINDOW.blit(p1_num0, (x, y))
                WINDOW.blit(p1_num1, (x+x_padding, y))
            
            else:
                WINDOW.blit(p1_num0, (x+x_padding/2, y))

        if idx == 0:
            if len(p2_stones) == 2:
                WINDOW.blit(p2_num0, (x, y))
                WINDOW.blit(p2_num1, (x+x_padding, y))
            
            else:
                WINDOW.blit(p2_num0, (x+x_padding/2, y))

    pygame.display.flip()
    pygame.display.update()


def tutorial():
    pass


def run():
    global gameManager
    global game

    gameManager = GameManager()
    game = Game(gameManager)
    
    while True:
        gameManager = game.main()
        update_layers()

        if game.gameManager.search_winner:
            p1 = game.players[0].count_stones()
            p2 = game.players[1].count_stones()
            draw_total_stones(str(p1), str(p2))

            if p1 > p2:
                gameManager.win(game.players[0])
            elif p2 > p1:
                gameManager.win(game.players[1])
            else:
                gameManager.tie()

            time.sleep(sleep_time*4)

        game.clean()
        for obj in OBJECTS:
            try:
                obj.destroy()
                del obj

            except:
                continue


if __name__ == '__main__':
    run()