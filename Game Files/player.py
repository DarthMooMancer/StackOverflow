import pygame
from settings import *
import math
from os import path

def init():
    pygame.init()

def load_data(map_file):
    global map_data
    map_data = []
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, "maps")
    with open(path.join(map_folder, map_file), 'rt') as f:
        for line in f:
            map_data.append(line.strip())       

init()
            
current_map = 'map.txt'
load_data(current_map)

class Player(pygame.sprite.Sprite):
    def __init__(self, win, sprite_group, walls, switch_map):
        super().__init__()
        self.groups = sprite_group
        self.win = win
        self.win = walls
        self.switch_map = switch_map
        self.previous_map = ""
        self.player_mainclock = 0
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((40, 132, 200))
        self.rect = self.image.get_rect(topleft=(300, 400))
        self.vel_x = 0
        self.vel_y = 0
        self.mainclock = 0
        self.current_time = (self.mainclock / 100) / 10
        self.health = PLAYER_HEALTH
        self.movement = {"up": False, "down": False, "left": False, "right": False, "dodge": False}
        self.center = (self.vel_x + (TILESIZE // 2), self.vel_y + (TILESIZE // 2))  # Center of the circle
        self.radius = 50
        self.test_point_topleft = (self.rect.x, self.rect.y)
        self.test_point_topright = (self.rect.x + TILESIZE, self.rect.y)
        self.test_point_bottomleft = (self.rect.x, self.rect.y + TILESIZE)
        self.test_point_bottomright = (self.rect.x + TILESIZE, self.rect.y + TILESIZE)
        
        # Update player initial position
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'e':
                    self.rect.topleft = (col * TILESIZE, row * TILESIZE)

    def point_in_circle(self, x, y):
        return math.sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2) <= self.radius
        
    def reset_movement(self):
        self.vel_x = 0
        self.vel_y = 0
        self.movement = {"up": False, "down": False, "left": False, "right": False, "dodge": False}

    def check_map_change(self, current_map, map_data):
        tile_x = self.rect.centerx // TILESIZE
        tile_y = self.rect.centery // TILESIZE

        # Check if player has collided with 'P' to switch to map2
        if current_map == "map.txt" and map_data[tile_y][tile_x] == "P":
            self.previous_map = current_map
            current_map = self.switch_map("map2.txt", "E")
            
        if current_map == 'map2.txt' and self.rect.x < 10 and map_data[tile_y][tile_x] == "P":
            self.previous_map = current_map
            current_map = self.switch_map("map.txt", "E")
            
        if current_map == 'map2.txt' and map_data[tile_y][tile_x] == "Q":
            self.previous_map = current_map
            current_map = self.switch_map("map3.txt", "E")
            
        if current_map == 'map3.txt' and map_data[tile_y][tile_x] == "P":
            self.previous_map = current_map
            current_map = self.switch_map('map2.txt', "R")

        return current_map
    
    def event_handler(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.movement["up"] = True
            if event.key == pygame.K_DOWN:
                self.movement["down"] = True
            if event.key == pygame.K_LEFT:
                self.movement["left"] = True
            if event.key == pygame.K_RIGHT:
                self.movement["right"] = True
            if event.key == pygame.K_z:
                self.movement["dodge"] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.movement["up"] = False
                self.vel_y = 0
            if event.key == pygame.K_DOWN:
                self.movement["down"] = False
                self.vel_y = 0
            if event.key == pygame.K_LEFT:
                self.movement["left"] = False
                self.vel_x = 0
            if event.key == pygame.K_RIGHT:
                self.movement["right"] = False
                self.vel_x = 0
            if event.key == pygame.K_z:
                self.movement["dodge"] = False 
            
    def draw_player_stats(self, surf, x, y, pct, color, max_stat, half_stat):
        pct = max(pct, 0)
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct > max_stat:
            col = GREEN
        elif pct > half_stat:
            col = YELLOW
        else:
            col = RED
        pygame.draw.rect(surf, col, fill_rect)
        pygame.draw.rect(surf, color, outline_rect, 2)
    
    def draw_cirle(self):
        return pygame.draw.circle(self.win, WHITE, (self.rect.x + TILESIZE // 2, self.rect.y + TILESIZE // 2), TILESIZE, 2)
    
    def radius_check_point(self, test_point):
        if self.point_in_circle(*test_point):
            print(f"The point {test_point} is inside the circle.")
            pygame.draw.circle(self.win, (255, 255, 255), (test_point), 5)
        else:
            print(f"The point {test_point} is outside the circle.")
            pygame.draw.circle(self.win, (255, 255, 255), (test_point), 5)
        
    def update(self):
        self.test_point_topleft = (self.rect.x, self.rect.y)
        self.test_point_topright = (self.rect.x + TILESIZE, self.rect.y)
        self.test_point_bottomleft = (self.rect.x, self.rect.y + TILESIZE)
        self.test_point_bottomright = (self.rect.x + TILESIZE, self.rect.y + TILESIZE)
        if ((self.mainclock / 100) / 10) >= 1:
            self.mainclock += 0
            
        else:
            self.mainclock += 1.6
        self.current_time = (self.mainclock / 100) / 100
        
        self.draw_player_stats(self.win, 150, 740, (self.mainclock / 100) / 10, BLACK, 1, .5)
        self.draw_player_stats(self.win, 40, 740, self.health / PLAYER_HEALTH, BLACK, .6, .3)
        self.draw_cirle()
        
                # Iterate through all points in the circle's bounding box
        for x in range(self.center[0] - self.radius, self.center[0] + self.radius):
            for y in range(self.center[1] - self.radius, self.center[1] + self.radius):
                if self.point_in_circle(x, y):
                    pygame.draw.circle(self.win, (255, 0, 0), (x, y), 1)
        
                # Check if the test point is inside the circle
        
        self.radius_check_point(self.test_point_bottomleft)
        self.radius_check_point(self.test_point_bottomright)
        self.radius_check_point(self.test_point_topleft)
        self.radius_check_point(self.test_point_topright)
        
        self.rect.clamp_ip(0, 0, ScreenWidth, ScreenHeight) 
        
        # Horizontal movement
        self.rect.x += self.vel_x
        self.collision_sprites = pygame.sprite.spritecollide(self, self.walls, False)
        for sprite in self.collision_sprites:
            if self.vel_x > 0:  # Moving right
                self.rect.right = sprite.rect.left

            elif self.vel_x < 0:  # Moving left
                self.rect.left = sprite.rect.right

        # Vertical movement
        self.rect.y += self.vel_y
        self.collision_sprites = pygame.sprite.spritecollide(self, self.walls, False)
        for sprite in self.collision_sprites:
            if self.vel_y > 0:  # Moving down
                self.rect.bottom = sprite.rect.top
            elif self.vel_y < 0:  # Moving up
                self.rect.top = sprite.rect.bottom
        
        # Movement
        if self.movement["up"]:
            self.vel_y = -PLAYER_SPEED
        if self.movement["down"]: 
            self.vel_y = PLAYER_SPEED
        if self.movement["left"]: 
            self.vel_x = -PLAYER_SPEED
        if self.movement["right"]: 
            self.vel_x = PLAYER_SPEED

        # Dodge Functionality 
        if self.movement["dodge"] and self.current_time < .1:
            self.movement["dodge"] = False

        else:
            if self.movement["dodge"] and self.current_time >= .1:
                self.mainclock = 0
                if self.movement["up"]:
                    self.vel_y = -DODGE_DISTANCE
                if self.movement["down"]:
                    self.vel_y = DODGE_DISTANCE
                if self.movement["left"]:
                    self.vel_x = -DODGE_DISTANCE
                if self.movement["right"]:
                    self.vel_x = DODGE_DISTANCE        
