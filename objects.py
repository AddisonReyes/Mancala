import numpy as np
import pygame
import os

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, layer=0, x_scale=1, y_scale=1, orientation=0, img_path=os.path.join("assets", "empty.png")):
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

    def add_position(self, x, y):
        self.position = np.array([x, y])
        self.x = x
        self.y = y

    def give_rect(self):
        return self.rect
    
    def give_position(self):
        return self.x, self.y

    def destroy(self):
        pass


class Stone(GameObject):
    def __init__(self):
        self.path = "stone.png"
        
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


class Cluster(GameObject):
    def __init__(self, pos, stones=None, path="cluster.png", x=0, y=0):
        super().__init__(img_path = os.path.join("assets", "Mancala (Game)", path), x=x, y=y)

        if stones is None: stones = np.array([])
        self.player_store = False
        self.stones = stones
        self.pos = pos

    def add_position(self, x, y):
        super().add_position(x, y)
        self.pos = np.array([x, y])
        self.x = x
        self.y = y

    def give_position(self):
        return super().give_position()

    def change_store(self):
        self.player_store = True

    def is_store(self):
        return self.player_store
    
    def click_me(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False

    def __str__(self):
        return f"POS({self.pos}) - {self.stones}"

    def __repr__(self):
        return str(self)


class Store(Cluster):
    def __init__(self, *args, **kwargs):
        self.path = "_.png"
        super().__init__(path = self.path, *args, **kwargs)
        super().change_store()

    def is_store(self):
        return super().is_store()
    

class Table():
    def __init__(self):
        self.clusters = self.__construct_clusters(n_stones=3)

    def give_clusters(self):
        return self.clusters

    def __construct_clusters(self, n_clusters_pp=6, n_players=2, n_stones=3):
        clusters = []
        for j in range(n_players):
            clusters += [Store((n_clusters_pp + 1)*j)]
            clusters += [Cluster(1 + i + (n_clusters_pp + 1)*j, [Stone() for _ in range(n_stones)]) for i in range(n_clusters_pp)]

        return clusters
    
    def stream_cluster(self, cluster_id, valid_store_id):
        cluster = self.clusters[cluster_id]
        n_clusters = len(self.clusters)

        if len(cluster.stones) == 0: return
        print("CLUSTER:", cluster)

        idx = -1
        offset = 0
        limit = len(cluster.stones)
        while idx > -limit - 1 + offset:
            next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            if next_cluster.is_store() and next_cluster.pos != valid_store_id:
                offset -= 1
            else:
                next_cluster.stones.append(cluster.stones.pop())
                print(f"Appending stones to: {next_cluster}, idx: {idx}")
            idx -= 1

        #for idx in range(-1, -len(cluster.stones) - 1, -1):
            #next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            #next_cluster.stones.append(cluster.stones.pop())
            #print(f"Appending stones to: {next_cluster}, idx: {idx}")

        return next_cluster


class Player():
    def __init__(self, table: Table, store_id: int, cluster_ids: int):
        self.store_id = store_id
        self.cluster_ids = cluster_ids
        self.table = table

    def stream(self, cluster_id: int):
        if cluster_id not in self.cluster_ids: return
        return self.table.stream_cluster(cluster_id, self.store_id)