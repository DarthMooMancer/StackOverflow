import pygame
from pygame import mixer
import math
from os import path
from settings import *
import sys

def init():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    pygame.init()
    win = pygame.display.set_mode((ScreenWidth, ScreenHeight), vsync=1)
    pygame.display.set_caption("Gloombound")
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', font_size[0])
    pixel_font = pygame.font.Font('Minecraft.ttf', font_size[1])
    
    return win, clock, font, pixel_font

def load_data(map_file):
    global map_data
    map_data = []
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'img')
    map_folder = path.join(game_folder, "maps")
    sound_folder = path.join(game_folder, "sounds")
    with open(path.join(map_folder, map_file), 'rt') as f:
        for line in f:
            map_data.append(line.strip())     
            
    return img_folder, sound_folder

def draw_text(text, font, color, surface, pos):
    textobj = font.render(text, 1, color)
    surface.blit(textobj, pos)

win, clock, font, pixel_font = init()
            
current_map = 'map.txt'
previous_map = ""
default_slider_pos = 500
img_folder, sound_folder = load_data(current_map)

# Load Images
play_img = pygame.transform.scale(pygame.image.load(path.join(img_folder,'play_button.png')), button_size).convert_alpha()
play_img_alt = pygame.transform.scale(pygame.image.load(path.join(img_folder,'play_button_alt.png')), button_size).convert_alpha()
quit_img = pygame.transform.scale(pygame.image.load(path.join(img_folder,'quit_button.png')), button_size).convert_alpha()
quit_img_alt = pygame.transform.scale(pygame.image.load(path.join(img_folder,'quit_button_alt.png')), button_size).convert_alpha()
continue_img = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'continue_button.png')), pause_button_size).convert_alpha()
continue_img_alt = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'continue_button_alt.png')), pause_button_size).convert_alpha()
main_menu = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'main_menu_button.png')), pause_button_size).convert_alpha()
main_menu_alt = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'main_menu_button_alt.png')), pause_button_size).convert_alpha()
settings_img = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'settings_button.png')), pause_button_size).convert_alpha()
settings_img_alt = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'settings_button_alt.png')), pause_button_size).convert_alpha()

# Load Sounds
player_hit = pygame.mixer.Sound(path.join(sound_folder, "player_hit.wav"))
player_mainclock = 0
global_volume = 99
new_volume = 10
mainclock = 0
max_time = 80
distance = 0
increment = 13
speed_of_game_movement = 3
increment_for_every = 5
run = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.groups = sprite_group
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
        self.test_point_topleft = (self.rect.x, self.rect.y)
        self.test_point_topright = (self.rect.x + TILESIZE, self.rect.y)
        self.test_point_bottomleft = (self.rect.x, self.rect.y + TILESIZE)
        self.test_point_bottomright = (self.rect.x + TILESIZE, self.rect.y + TILESIZE)
        
        # Update player initial position
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'e':
                    self.rect.topleft = (col * TILESIZE, row * TILESIZE)
   
    def reset_movement(self):
        self.vel_x = 0
        self.vel_y = 0
        self.movement = {"up": False, "down": False, "left": False, "right": False, "dodge": False}

    def check_map_change(self, current_map, map_data, prev_map):
        tile_x = self.rect.centerx // TILESIZE
        tile_y = self.rect.centery // TILESIZE

        # Check if player has collided with 'P' to switch to map2
        if current_map == "map.txt" and map_data[tile_y][tile_x] == "P":
            prev_map = current_map
            current_map = g.switch_map("map2.txt", "E")
            
        if current_map == 'map2.txt' and self.rect.x < 10 and map_data[tile_y][tile_x] == "P":
            prev_map = current_map
            current_map = g.switch_map("map.txt", "E")
            
        if current_map == 'map2.txt' and map_data[tile_y][tile_x] == "Q":
            prev_map = current_map
            current_map = g.switch_map("map3.txt", "E")
            
        if current_map == 'map3.txt' and map_data[tile_y][tile_x] == "P":
            prev_map = current_map
            current_map = g.switch_map('map2.txt', "R")

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
        return pygame.draw.circle(win, WHITE, (self.rect.x + TILESIZE // 2, self.rect.y + TILESIZE // 2), TILESIZE, 2)
    
    def radius_check_point(self, test_point):
        if enemy.point_in_circle(*test_point):
            pygame.draw.circle(win, (255, 255, 255), (test_point), 5)
        else:
            pygame.draw.circle(win, (255, 255, 255), (test_point), 5)
    
    def dodge_multiple_dir(self, x_increment, y_increment):
        global mainclock, running, run, move
        
        print("Hello World")
        while run:
            mainclock += speed_of_game_movement
            new_clock = round(mainclock / increment_for_every)
            if mainclock <= max_time:
                if new_clock * increment_for_every == mainclock:
                    print("Debug")
                    self.movement["left"] = False
                    self.movement["right"] = False
                    self.movement["up"] = False
                    self.movement["down"] = False
                    self.vel_x += x_increment
                    self.vel_y += y_increment

            else:
                break
            
            print("Loop")
            return run, self.movement["left"], self.movement["right"], self.movement["up"], self.movement["down"]
        return run, self.movement["left"], self.movement["right"], self.movement["up"], self.movement["down"]
    
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
        
        self.draw_player_stats(win, 150, 740, (self.mainclock / 100) / 10, BLACK, 1, .5)
        self.draw_player_stats(win, 40, 740, self.health / PLAYER_HEALTH, BLACK, .6, .3)
        self.draw_cirle()

        self.radius_check_point(self.test_point_bottomleft)
        self.radius_check_point(self.test_point_bottomright)
        self.radius_check_point(self.test_point_topleft)
        self.radius_check_point(self.test_point_topright)
        
        self.rect.clamp_ip(0, 0, ScreenWidth, ScreenHeight) 

        self.rect.x += self.vel_x
        self.collision_sprites = pygame.sprite.spritecollide(self, walls, False)
        for sprite in self.collision_sprites:
            if self.vel_x > 0:  # Moving right
                self.rect.right = sprite.rect.left

            elif self.vel_x < 0:  # Moving left
                self.rect.left = sprite.rect.right

        self.rect.y += self.vel_y
        self.collision_sprites = pygame.sprite.spritecollide(self, walls, False)
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

        if self.movement["dodge"]:
        # Dodge Functionality 
            if self.current_time < .1:
                self.movement["dodge"] = False

            elif self.current_time >= .1:
                self.mainclock = 0

                if self.movement["up"]:
                    self.dodge_multiple_dir(0, -increment)
                if self.movement["down"]:
                    self.vel_y = DODGE_DISTANCE
                if self.movement["left"]:
                    self.vel_x = -DODGE_DISTANCE
                if self.movement["right"]:
                    self.vel_x = DODGE_DISTANCE        
                    
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, map_data):
        pygame.sprite.Sprite.__init__(self, walls, sprite_group)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = pygame.Rect((x * TILESIZE, y * TILESIZE), (TILESIZE, TILESIZE))
        self.x =  x
        self.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.groups = sprite_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((200, 132, 12))
        self.rect = self.image.get_rect(center=(ScreenWidth // 2 + 40, ScreenHeight // 2 + 80))
        self.health = MOB_HEALTH
        self.speed = MOB_SPEED
        self.vel_x = 0
        self.vel_y = 0
        self.center = (self.rect.centerx, self.rect.centery)  # Center of the enemy
        self.radius = 200
        self.circle_color = (255, 0, 0)  # Red color for the circle

    def point_in_circle(self, x, y):
        return math.sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2) <= self.radius

    def calculate_distance(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        return distance, dx, dy

    def update(self):
        distance, dx, dy = self.calculate_distance(player)

        self.vel_x = 0
        self.vel_y = 0

        player_center_x, player_center_y = player.rect.centerx, player.rect.centery
        enemy_center_x, enemy_center_y = self.rect.centerx, self.rect.centery

        distance_to_player = math.hypot(player_center_x - enemy_center_x, player_center_y - enemy_center_y)

        # Handle collision with walls
        self.rect.clamp_ip(0, 0, ScreenWidth, ScreenHeight)

        # Draw the circle only when the player is within a certain distance
        if distance < 1000:  # Adjust the distance threshold as needed
            pygame.draw.circle(win, self.circle_color, (self.rect.centerx, self.rect.centery), self.radius, 2)

        # Check if the player is inside the enemy's circle
        if distance_to_player <= self.radius:
            # Move towards the player if the player is inside the circle
            self.vel_x += self.speed * dx / distance
            self.vel_y += self.speed * dy / distance
        
        else:
            # Implement idle movement behavior (move up and down slowly)
            if pygame.time.get_ticks() % 2000 < 1000:  # Change direction every 2 seconds
                self.vel_y = 1  # Move down slowly
                
            else:
                self.vel_y = -1  # Move up slowly

        # Handle collision with the player
        collision = pygame.sprite.spritecollideany(self, sprite_group)
        if collision and isinstance(collision, Player):
            collision.health -= 10
            dx = self.rect.centerx - collision.rect.centerx
            dy = self.rect.centery - collision.rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                # Knock back player in the opposite direction
                pygame.mixer.Sound.play(player_hit)
                collision.rect.x -= 30 * dx / distance
                collision.rect.y -= 30 * dy / distance

        # Horizontal movement
        self.rect.x += self.vel_x
        collision_sprites = pygame.sprite.spritecollide(self, walls, False)
        for sprite in collision_sprites:
            if self.vel_x > 0:  # Moving right
                self.rect.right = sprite.rect.left
            elif self.vel_x < 0:  # Moving left
                self.rect.left = sprite.rect.right

        # Vertical movement
        self.rect.y += self.vel_y
        collision_sprites = pygame.sprite.spritecollide(self, walls, False)
        for sprite in collision_sprites:
            if self.vel_y > 0:  # Moving down
                self.rect.bottom = sprite.rect.top
            elif self.vel_y < 0:  # Moving up
                self.rect.top = sprite.rect.bottom
                        
class Button(pygame.sprite.Sprite):
    def __init__(self, screen, img, img_alt, x, y, group, command=None, command_args=None, debug=None, collision_offset=(0, 0)):
        super().__init__()
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = img
        self.image_get = img
        self.image_alt = img_alt
        self.command = command
        self.command_args = command_args
        self.x = x
        self.y = y
        self.screen = screen
        self.debug = debug
        self.rect = self.image.get_rect()
        self.mx, self.my = pygame.mouse.get_pos()

        # Create collision rect with offset from image rect
        self.collision_offset = collision_offset
        self.collision_rect = pygame.Rect(x + collision_offset[0], y + collision_offset[1], self.rect.width - 2*collision_offset[0], self.rect.height - 2*collision_offset[1])

    def collision(self):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.collision_rect.collidepoint((self.mx, self.my)):
            self.image = self.image_alt
            if pygame.mouse.get_pressed()[0]:
                if callable(self.command):
                    self.command(*self.command_args)
        else:
            self.image = self.image_get

    def Debug(self, screen):
        if self.debug:
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, pygame.Color("white"), self.collision_rect, 2)
            
    def update(self):
        self.mx, self.my = pygame.mouse.get_pos()
        self.rect.topleft = (self.x, self.y)
        
        # Move collision rect with same offset from image rect
        self.collision_rect.topleft = (self.x + self.collision_offset[0], self.y + self.collision_offset[1])
        self.collision_rect.width = self.rect.width - 2*self.collision_offset[0]
        self.collision_rect.height = self.rect.height - 2*self.collision_offset[1]
        
        self.collision()
        self.Debug(self.screen)

class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, color, min_volume, max_volume):
        super().__init__()
        self.size = [50, 50]
        self.image = pygame.Surface((self.size[0], self.size[1]))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.new_volume = 0
        self.step_size = 40  # Increment by 10
        self.snap_positions = [i for i in range(0, ScreenWidth, self.step_size)]
        self.percentage = 0.0
        self.current_snap_index = len(self.snap_positions) // 2  # Start at the middle position
        self.dragging = False

    def update(self):
        global new_volume, default_slider_pos, slider_volume
        mx, my = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint((mx, my)):  # Check if mouse is over the slider
                self.dragging = True
                
            else:
                self.dragging = False

        if self.dragging:
            # Determine the nearest snap position to the current mouse position
            nearest_position_index = min(range(len(self.snap_positions)), key=lambda i: abs(self.snap_positions[i] - mx))
            self.current_snap_index = nearest_position_index

            # Update the slider position based on the nearest snap position
            self.rect.x = self.snap_positions[self.current_snap_index]

            # Calculate volume based on slider position
            self.percentage = self.current_snap_index / (len(self.snap_positions) - 1)
            new_volume = int(self.percentage * (self.max_volume - self.min_volume)) + self.min_volume
            mixer.music.set_volume(new_volume / 100)
            default_slider_pos = new_volume * 10

            if self.rect.x <= 100:
                self.rect.x = 100

            if self.rect.x >= ScreenWidth - 150:
                self.rect.x = ScreenWidth - 150
                
            return new_volume

        if pygame.mouse.get_pressed()[0] == 0:
            self.dragging = False

        if float(self.percentage) >= 1.0:
            decimal_part = 0.99
        else:
            decimal_part = (float(self.percentage) * 100) % 100

        # Print the volume as it changesdefault_slider_pos
        print(f"Current volume: {int(float(self.percentage) * 100)}.{int(decimal_part)}%")
        print(default_slider_pos)
        
        # Set global volume variable
        slider_volume = new_volume

        return new_volume, slider_volume, default_slider_pos

class Line(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.groups = sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    def draw(self, screen, x, y, width, height, col):
        rect = (x, y, width, height)
        pygame.draw.rect = (screen, col, rect)

class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    def draw(self, screen, color, x, y, width, height):
        box_rect = (x, y, width, height)
        pygame.draw.rect(screen, pygame.Color(color), box_rect)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_folder, image_file)), (ScreenWidth, ScreenHeight)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

sprite_group = pygame.sprite.Group()
walls = pygame.sprite.Group()
button_sprite = pygame.sprite.Group()
pause_button_sprite = pygame.sprite.Group()
settings_sprite = pygame.sprite.Group()

BackGround = Background('background.png', [0,0])
slider_image = pygame.Surface((200, 20))
slider_image.fill((50, 50, 50))
slider = Slider(default_slider_pos, 50, WHITE, 0, 100)
slider_volume = slider.new_volume

def draw_objects():
    for row, tiles in enumerate(map_data):
        for col, tile in enumerate(tiles):
            if tile == '1':
                Wall(col, row, map_data)
                  
player = Player()
enemy = Enemy()
wall = Wall(0, 0, None)
box = Box()
    
class Game:
    def __init__(self):
        super().__init__()
        
    def switch_map(self, new_map, symbol):
        global current_map, player, walls, enemy, player_mainclock
        player_mainclock = player.mainclock
        current_map = new_map
        load_data(current_map)
        sprite_group.empty()
        player = Player()
        walls.empty()
        enemy = Enemy()

        # Restore player's mainclock time
        player.mainclock = player_mainclock

        # Update player initial position
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == symbol:
                    player.rect.topleft = (col * TILESIZE, row * TILESIZE)

        return current_map, draw_objects()

    def reset_game_state(self):
        global playing, current_map, player, walls, enemy, sprite_group
        playing = False
        current_map = 'map.txt'
        sprite_group.empty()
        player = Player()
        walls.empty()
        enemy = Enemy()
        self.main()
    
    def back_to_pause(self):
        global settings
        settings = False
        
        return settings
        
    def main(self):
        Button(win, play_img, play_img_alt, 25, 675, button_sprite, self.play, (), collision_offset=(10, 30))
        Button(win, quit_img, quit_img_alt, 900, 675, button_sprite, exit, (), collision_offset=(10, 30))
        pygame.mixer.music.load(path.join(sound_folder, "main_menu_background.wav"))
        pygame.mixer.music.play(-1)
        while True:
            clock.tick(FPS // 2)
            win.blit(BackGround.image, BackGround.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                        
            draw_text("GloomBound", pixel_font, WHITE, win, (275, 50))
            
            button_sprite.draw(win)         
            button_sprite.update()
            
            pygame.display.update()
    
    def play(self):
        global playing, slider_volume
        playing = True # Set playing to True before starting game loop
        draw_objects()
        pygame.mixer.music.load(path.join(sound_folder, "play_menu_background.wav"))
        pygame.mixer.music.play(-1)
        while playing:
            clock.tick(FPS)
            win.fill((BGCOLOR))
                
            for event in pygame.event.get():
                player.event_handler(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                    playing = False
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    g.switch_map(current_map, "e")
            
            player.check_map_change(current_map, map_data, previous_map)
            sprite_group.draw(win)
            sprite_group.update()
            pygame.mixer.music.set_volume(slider_volume / 100)
            pygame.display.update()
    
    def pause(self):
        global pause
        pause = True
        player.reset_movement()
        
        Button(win, continue_img, continue_img_alt, (ScreenWidth / 2) - (button_size[0]), 200, pause_button_sprite, self.play, (), collision_offset=(0, 70))
        Button(win, settings_img, settings_img_alt, (ScreenWidth / 2) - (button_size[0]), 300, pause_button_sprite, self.settings, (), collision_offset=(0, 70))
        Button(win, main_menu, main_menu_alt, (ScreenWidth / 2) - (button_size[0]), 400, pause_button_sprite, self.reset_game_state, (), collision_offset=(0, 70))
        
        while pause:
            win.fill(BGCOLOR)
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
            pause_button_sprite.draw(win)
            pause_button_sprite.update()
            
            pygame.display.update()
        
    def settings(self):
        global settings, new_volume
        settings = True
        Button(win, continue_img, continue_img_alt, (ScreenWidth / 2) - (button_size[0]), 200, settings_sprite, self.back_to_pause, (), collision_offset=(0, 70))
        
        while settings:
            win.fill(BGCOLOR)
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            slider.new_volume = slider.update()

            # Move the Slider
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if slider.rect.collidepoint((mx, my)):
                    slider.rect.centerx = mx
            
            # Draw the Slider
            up_pix_font = pygame.font.Font("Minecraft.ttf", font_size[0])
            draw_text("Master volume", up_pix_font, GREEN, win, (ScreenWidth // 2 - 100, 15))
            box.draw(win, WHITE, 100, 75, 824, 3)

            win.blit(slider.image, slider.rect)
            settings_sprite.draw(win)
            settings_sprite.update()
            pygame.display.update()
    
    def run(self):
        self.main()

g = Game()
g.run()
