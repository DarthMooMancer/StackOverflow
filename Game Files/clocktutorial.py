import pygame
import time
from settings import *

mainclock = 0
max_time = 80
distance = 0
increment = 13
speed_of_game_movement = 3
increment_for_every = 5
run = True
move = True

def init():
    pygame.init()
    win = pygame.display.set_mode((ScreenWidth, ScreenHeight), vsync=1)
    pygame.display.set_caption("Gloombound")
    clock = pygame.time.Clock()
    
    return win, clock

win, clock = init()

class Player(pygame.sprite.Sprite):
    def __init__(self, win, sprite_group):
        super().__init__()
        self.groups = sprite_group
        self.win = win
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((40, 132, 200))
        self.rect = self.image.get_rect(topleft=(500, 100))
        self.default_start = self.rect.x
        self.new_start = self.rect.x
    
    def dodge_multiple_dir(self, x_increment, y_increment):
        global mainclock, running, run, move
            
        while run:
            mainclock += speed_of_game_movement
            self.new_start = self.rect.x
            new_clock = round(mainclock / increment_for_every)  # Calculate the multiple of increment_for_every for mainclock
            if mainclock <= max_time:
                if new_clock * increment_for_every == mainclock:
                    move = False
                    self.rect.x += x_increment  # Increment distance by increment for every multiple of increment_for_every in mainclock
                    self.rect.y += y_increment

            else:
                run = False
                move = True
                
            return run, move
        return run, move  
        
    def update(self):
        self.dodge_multiple_dir(increment, 0)
    
       
sprite_group = pygame.sprite.Group()     
player = Player(win, sprite_group)

running = True
def main():
    while running:
        win.fill((0, 0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        
        sprite_group.draw(win)
        sprite_group.update()
        
        pygame.display.update()
        
        print(move)
        if not run:
            break

main()