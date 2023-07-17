import numpy as np
import random
import pygame
import os


SKINS = {
    0: "Classic_table",
    1: "Black_and_White",
    2: "Wood_table"
}

skin = 0
last_skin = SKINS[skin]

def next_skin():
    global SKINS
    global skin

    if skin == len(SKINS) - 1:
        skin = 0
    
    else:
        skin += 1

    return SKINS, skin

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, layer=0, x_scale=1, y_scale=1, orientation=0, img_path=os.path.join("assets", "Mancala (Interface)", "_.png")):
        super().__init__()
        self.x = x
        self.y = y
        self.layer = layer
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.position = np.array([x, y])
        self.orientation = orientation
        self.load_image(img_path)
        self.image_path = img_path
        self.blank_path = os.path.join("assets", "Mancala (Interface)", "_.png")
        self.change_vals = False

    def load_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()

    def update_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    def refresh_sprite(self):
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.rect = self.image.get_rect()

    def update(self):
        self.refresh_sprite()
        self.rect.center = (self.x, self.y) 

    def is_colliding(self, position):
        return self.rect.collidepoint(position)
    
    def change_sprite(self, path):
        self.load_image(path)
    
    def hide(self):
        self.load_image(self.blank_path)

    def show(self):
        self.load_image(self.image_path)

    def change_orientation(self, new_orientation):
        self.orientation = new_orientation
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()

    def add_position(self, x, y):
        self.position = np.array([x, y])
        self.x = x
        self.y = y

    def give_rect(self):
        return self.rect
    
    def give_position(self):
        return self.x, self.y

    def destroy(self):
        self.kill()
        del self


class Stone(GameObject):
    def __init__(self):
        if SKINS[skin] == "Classic_table":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 8)}.png"

        if SKINS[skin] == "Black_and_White":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 2)}.png"

        if SKINS[skin] == "Wood_table":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 5)}.png"
        
        super().__init__(img_path = os.path.join("assets", "Mancala (Game)", self.path), x_scale=1, y_scale=1, orientation=0)
        self.rect = super().give_rect()

    def add_position(self, x, y):
        super().add_position(x, y)
        self.pos = np.array([x, y])
        self.x = x
        self.y = y

    def show(self):
        super().show()

    def hide(self):
        super().hide()

    def update(self):
        super().update()

    def change_skin(self):
        if SKINS[skin] == "Classic_table":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 8)}.png"

        if SKINS[skin] == "Black_and_White":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 2)}.png"

        if SKINS[skin] == "Wood_table":
            self.path = f"{SKINS[skin]} stone{random.randint(1, 5)}.png"

        super().change_sprite(os.path.join("assets", "Mancala (Game)", self.path))  

    def destroy(self):
        return super().destroy()

    def __repr__(self):
        return "o"


class Cluster(GameObject):
    def __init__(self, pos, stones=None, path=f"{SKINS[skin]} cluster.png", cluster_id=None, x=0, y=0):
        super().__init__(img_path = os.path.join("assets", "Mancala (Game)", path), x=x, y=y)
        self.rect = super().give_rect()
        self.path = path

        if stones is None: 
            stones = np.array([], dtype=object)

        self.cluster_id = cluster_id
        self.player_store = False
        self.stones = np.array(stones, dtype=object)
        self.pos = pos

    def recive_id(self, id):
        self.cluster_id = id

    def add_position(self, x, y):
        super().add_position(x, y)
        self.pos = np.array([x, y])
        self.x = x
        self.y = y

    def give_position(self):
        return super().give_position()

    def change_store(self):
        self.player_store = True

    def update(self):
        super().update()

    def change_skin(self):
        if self.player_store:
            self.path = f"{SKINS[skin]} store.png"

        else:
            self.path = f"{SKINS[skin]} cluster.png"

        super().change_sprite(os.path.join("assets", "Mancala (Game)", self.path))  

    def is_store(self):
        return self.player_store
    
    def click_me(self):
        if self.player_store != True:
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position):
                return True
            else:
                return False

    def __str__(self):
        return f"\nCluster #({self.cluster_id}): {self.stones}"

    def __repr__(self):
        return str(self)


class Store(Cluster):
    def __init__(self, *args, **kwargs):
        self.path = f"{SKINS[skin]} store.png"
        super().__init__(path = self.path, *args, **kwargs)
        self.rect = super().give_rect()
        super().change_store()

    def update(self):
        super().update()

    def change_skin(self):
        super().change_skin()

    def recive_stones(self):
        self.stones = super().stones

    def sum_stones(self):
        return len(self.stones)

    def is_store(self):
        return super().is_store()
    
    def give_position(self):
        return super().give_position()
    
    def recive_id(self, id):
        super().recive_id(id)

    def __repr__(self):
        return super().__repr__()
    

class Table():
    def __init__(self, num_stones):
        self.clusters = self.__construct_clusters(n_stones=num_stones) #3, 5, 7

    def __copy__(self):
        new_instance = self.__reconstruct_clusters()
        return new_instance

    def give_clusters(self):
        return self.clusters

    def __construct_clusters(self, n_clusters_pp=6, n_players=2, n_stones=3):
        clusters = []
        for j in range(n_players):
            clusters += [Store((n_clusters_pp + 1)*j)]
            clusters += [Cluster(1 + i + (n_clusters_pp + 1)*j, [Stone() for _ in range(n_stones)]) for i in range(n_clusters_pp)]

        for i in range(len(clusters)):
            clusters[i].recive_id(i)

        return np.array(clusters, dtype=object)

    def stream_cluster(self, cluster_id, valid_store_id):
        cluster = self.clusters[cluster_id]
        n_clusters = len(self.clusters)

        if len(cluster.stones) == 0: 
            return None

        idx = -1
        offset = 0
        limit = len(cluster.stones)
        while idx > -limit - 1 + offset:
            next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            if next_cluster.is_store() and next_cluster.cluster_id != valid_store_id:
                offset -= 1
            else:
                next_cluster.stones = np.append(next_cluster.stones, cluster.stones[-1])
                cluster.stones = np.delete(cluster.stones, -1)
                
            idx -= 1

        for idx in range(-1, -len(cluster.stones) - 1, -1):
            next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            next_cluster.stones = np.append(next_cluster.stones, cluster.stones[-1])
            cluster.stones = np.delete(cluster.stones, -1)

        return next_cluster
    
    def take_it_all(self, last_cluster, player):
        opposite_index = 14 - last_cluster.cluster_id

        if len(self.clusters[opposite_index].stones) == 0 or last_cluster.cluster_id not in player.cluster_ids:
            return False

        while len(self.clusters[opposite_index].stones) != 0:
            for stone in self.clusters[opposite_index].stones:
                self.clusters[player.store_id].stones = np.append(self.clusters[player.store_id].stones, stone)
                self.clusters[opposite_index].stones = np.delete(self.clusters[opposite_index].stones, np.where(self.clusters[opposite_index].stones == stone))

        self.clusters[player.store_id].stones = np.append(self.clusters[player.store_id].stones, last_cluster.stones[0])
        last_cluster.stones = np.delete(last_cluster.stones, np.where(last_cluster.stones == last_cluster.stones[0]))
        return True

    def clear_clusters(self):
        self.clear_clusters = np.array([], dtype=object)


class Fake_Table():
    def __init__(self, clusters, next_cluster=None, played=None, player=None, take_all=False):
        self.clusters = self.recreate_clusters(clusters)
        self.next_cluster = next_cluster
        self.take_all = take_all
        self.player = player
        self.played = played

    def recreate_clusters(self, clusters):
        fake_clusters = np.array([], dtype=object)

        for cluster in clusters:
            fake_clusters = np.append(fake_clusters, Fake_Cluster(pos=cluster.pos, cluster_id=cluster.cluster_id))
                
        for i in range(len(clusters)):
            stone_qty = len(clusters[i].stones)
                
            for _ in range(stone_qty):
                fake_clusters[i].add_stone(Fake_Stone())

        return list(fake_clusters)

    def give_clusters(self):
        return self.clusters

    def childrens(self):
        playable_clusters = self.check_player_clusters()
        childrens = np.array([], dtype=object)

        for clusters, cluster, cluster_id, take_all in playable_clusters:
            childrens = np.append(childrens, Fake_Table(clusters, cluster, cluster_id, self.player, take_all))

        return childrens
    
    def check_player_clusters(self):
        playable_clusters = []

        for cluster_id in self.player.cluster_ids:
            if len(self.clusters[cluster_id].stones) == 0:
                continue

            new_clusters, next_cluster, take_all = self.stream_cluster(self.recreate_clusters(self.clusters), cluster_id, self.player.store_id)

            if new_clusters is not None and next_cluster is not None:
                playable_clusters.append([new_clusters, next_cluster, cluster_id, take_all])

        return playable_clusters

    def stream_cluster(self, clusters, cluster_id, valid_store_id):
        if cluster_id not in self.player.cluster_ids: 
            return None, None

        cluster = clusters[cluster_id]
        n_clusters = len(clusters)
        take_all = False

        if len(cluster.stones) == 0: 
            return None

        idx = -1
        offset = 0
        limit = len(cluster.stones)
        while idx > -limit - 1 + offset:
            next_cluster = clusters[(cluster_id + idx)%n_clusters]
            if next_cluster.is_store() and next_cluster.cluster_id != valid_store_id:
                offset -= 1
            else:
                next_cluster.stones = np.append(next_cluster.stones, cluster.stones[-1])
                cluster.stones = np.delete(cluster.stones, -1)
                
            idx -= 1

        for idx in range(-1, -len(cluster.stones) - 1, -1):
            next_cluster = clusters[(cluster_id + idx)%n_clusters]
            next_cluster.stones = np.append(next_cluster.stones, cluster.stones[-1])
            cluster.stones = np.delete(cluster.stones, -1)

        if len(next_cluster.stones) == 1 and next_cluster.cluster_id != 0 and next_cluster.cluster_id != 7:
            clusters, next_cluster = self.take_it_all(clusters, next_cluster, self.player)
            take_all = True
            
        return clusters, next_cluster, take_all
    
    def take_it_all(self, clusters, last_cluster, player):
        opposite_index = 14 - last_cluster.cluster_id

        if len(clusters[opposite_index].stones) == 0 or last_cluster.cluster_id not in player.cluster_ids:
            return clusters, last_cluster

        while len(clusters[opposite_index].stones) != 0:
            for stone in clusters[opposite_index].stones:
                clusters[player.store_id].stones = np.append(clusters[player.store_id].stones, stone)
                clusters[opposite_index].stones = np.delete(clusters[opposite_index].stones, np.where(clusters[opposite_index].stones == stone))

        clusters[player.store_id].stones = np.append(clusters[player.store_id].stones, last_cluster.stones[0])
        last_cluster.stones = np.delete(last_cluster.stones, np.where(last_cluster.stones == last_cluster.stones[0]))
        
        return clusters, last_cluster

    def check_game_status(self, players):
        terminal_val = None
        clear_table = False

        for player in players:
            if player.manual != True:
                computer = player.num

            no_stones = 0
            for idx in player.cluster_ids:
                try:
                    if len(self.clusters[idx].stones) == 0:
                        no_stones += 1

                    else:
                        break
                except:
                    pass

            if no_stones >= len(player.cluster_ids):
                clear_table = True
                break

        if clear_table:
            p1 = 0
            p2 = 0

            for player in players:
                store = 0
                for idx in player.cluster_ids:
                    stones = len(self.clusters[idx].stones)
                    store += stones

                if player.num == 1:
                    p1 = store

                if player.num == 1:
                    p2 = store

            if p1 > p2:
                if computer == 1:
                    return 1 * np.inf
                else:
                    return -1 * np.inf
                
            elif p2 > p1:
                if computer == 2:
                    return 1 * np.inf
                else:
                    return -1 * np.inf
                
            else:
                return -1 * np.inf
            
        return terminal_val

    def heuristic(self):
        computer_store = self.player.store_id
        if computer_store == 7:
            player_store = 0
        else:
            player_store = 7

        heuristic = 0
        heuristic += (len(self.clusters[computer_store].stones) - len(self.clusters[player_store].stones)) * 16

        if self.take_all:
            heuristic += 600

        if self.next_cluster.cluster_id == self.player.store_id:
            heuristic += 66

        elif self.next_cluster.cluster_id not in self.player.cluster_ids:
            heuristic -= 66

        else:
            heuristic += 1

        for cluster_id in self.player.cluster_ids:
            opposite_index = 14 - self.clusters[cluster_id].cluster_id
            if len(self.clusters[cluster_id].stones) == 0:
                continue
            
            if len(self.clusters[opposite_index].stones) == 0 and len(self.clusters[cluster_id].stones) >= 3:
                heuristic -= len(self.clusters[cluster_id].stones)/2
            
            else:
                heuristic += len(self.clusters[cluster_id].stones)/2

            if len(self.clusters[cluster_id].stones) <= 9:
                heuristic += len(self.clusters[cluster_id].stones)/3

            else:
                heuristic -= len(self.clusters[cluster_id].stones)/3


        return heuristic


class Fake_Stone():
    def __repr__(self):
        return "o"
        

class Fake_Cluster():
    def __init__(self, pos, stones=None, cluster_id=None):
        if stones is None: 
            stones = np.array([], dtype=object)

        self.cluster_id = cluster_id
        self.player_store = False
        self.stones = np.array(stones, dtype=object)
        self.pos = pos

    def add_stone(self, stone):
        self.stones = np.append(self.stones, stone)

    def is_store(self):
        return self.player_store

    def __str__(self):
        return f"\nCluster #({self.cluster_id}): {self.stones}"

    def __repr__(self):
        return str(self)
  

class Button(GameObject):
    def __init__(self, path):
        self.path1 = path
        self.path2 = path.replace("1", "2")
        self.position = None

        super().__init__(img_path=os.path.join("assets", "Mancala (Interface)", self.path1), x_scale=1, y_scale=1, orientation=0)
        self.rect = super().give_rect()
        self.on_screen = True

    def add_position(self, x, y):
        super().add_position(x, y)

    def change_orientation(self):
        super().change_orientation(180)

    def change_orientation_manual(self, new_orientation):
        super().change_orientation(new_orientation)

    def hide(self):
        self.on_screen = False
        super().change_sprite(os.path.join("assets", "Mancala (Interface)", "_.png"))
        super().update()

    def show(self):
        self.on_screen = True
        super().change_sprite(os.path.join("assets", "Mancala (Interface)", self.path1))
        super().update()

    def update(self):
        if self.on_screen:
            if super().is_colliding(pygame.mouse.get_pos()):
                super().change_sprite(os.path.join("assets", "Mancala (Interface)", self.path2))

            else:
                super().change_sprite(os.path.join("assets", "Mancala (Interface)", self.path1))  
            
        super().update()

    def click_me(self):
        if self.on_screen:
            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if self.rect.collidepoint(mouse_position) and mouse_pressed[0]:
                return True
                    
            else:
                return False


class Arrow(GameObject):
    def __init__(self, path):
        self.path1 = path
        self.path2 = "_.png"

        super().__init__(img_path=os.path.join("assets", "Mancala (Interface)", self.path1), x_scale=1, y_scale=1, orientation=0)

    def add_position(self, x, y):
        super().add_position(x, y)

    def change_orientation(self):
        super().change_orientation(180)

    def reset_orientation(self):
        super().change_orientation(0)

    def update(self):
        super().update()

    def hide(self):
        super().change_sprite(os.path.join("assets", "Mancala (Interface)", self.path2))
        super().update()

    def show(self):
        super().change_sprite(os.path.join("assets", "Mancala (Interface)", self.path1))
        super().update()


class Player():
    def __init__(self, table: Table, store_id: int, cluster_ids: int, num):
        self.cluster_ids = np.array(cluster_ids, dtype=int)
        self.store_id = store_id
        self.manual = True
        self.table = table
        self.num = num

        self.store = self.table.clusters[store_id]

    def count_stones(self):
        return self.store.sum_stones()

    def change_manual(self):
        self.manual = True

    def change_auto(self):
        self.manual = False

    def stream(self, cluster_id: int):
        if cluster_id not in self.cluster_ids: return
        return self.table.stream_cluster(cluster_id, self.store_id)