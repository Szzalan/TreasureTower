import pygame
import random
pygame.init()
import assets.spritesheet as spritesheet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y,enemy_type, frame_delay=250):
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.image = None
        self.sprite_sheet = None
        self.frames = {}
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.load_sprite_sheet()
        self.load_frames()

    def load_sprite_sheet(self):
        if self.enemy_type == "slime":
            self.sprite_sheet = pygame.image.load("../assets/slime_sprite_sheet.png").convert_alpha()
        elif self.enemy_type == "skeleton":
            self.sprite_sheet = pygame.image.load("../assets/undead_sprites.png").convert_alpha()
        elif self.enemy_type == "zombie":
            self.sprite_sheet = pygame.image.load("../assets/undead_sprites.png").convert_alpha()


    def load_frames(self):
        sprite_loader = spritesheet.HandleSpriteSheet(self.sprite_sheet)
        if self.enemy_type == "slime":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 0, 16, 16,offset_h=16)
            ]
        elif self.enemy_type == "zombie":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(1, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(2, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(3, 1, 16, 16,offset_h=11)
            ]
        elif self.enemy_type == "skeleton":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 2, 16, 16,offset_h=10),
                sprite_loader.get_image(1, 2, 16, 16, offset_h=10),
                sprite_loader.get_image(2, 2, 16, 16, offset_h=10),
                sprite_loader.get_image(3, 2, 16, 16, offset_h=10)

            ]
        self.image = self.frames["idle"][0]

    def animation_loop(self, action="idle",current_time=0):
        if action in self.frames:
            if current_time - self.frame_timer > self.frame_delay:
                self.frame_timer = current_time
                self.frame_index = (self.frame_index + 1) % len(self.frames[action])
                self.image = self.frames[action][self.frame_index]

    def update(self,current_time):
        self.animation_loop(action="idle",current_time=current_time)

    def check_interact(self,player):
        #check for diagonal places
        if ((self.x == player.x+1 or self.x == player.x-1) and self.y == player.y) or ((self.y == player.y+1 or self.y == player.y-1) and self.x == player.x):
            return True
        else:
            return False

    def interact(self,event,player):
        if event.key == pygame.K_e and self.check_interact(player):
            return True
        else:
            return False


