import pygame

import assets.spritesheet as spritesheet
pygame.init()

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,name, cost = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.cost = cost
        self.sprite_sheet = None
        self.image = None
        self.scale = 3
        self.rect = pygame.surface.Surface((16,16))
        self.load_sprite_sheet()
        self.load_items()

    def load_sprite_sheet(self):
        self.sprite_sheet = pygame.image.load("../assets/map_entities/roguelikeitems.png").convert_alpha()

    def load_items(self):
        sprite_loader = spritesheet.HandleSpriteSheet(self.sprite_sheet)
        if self.name == "Lucky_die":
            self.image = sprite_loader.get_image(12, 11, 16, 16,scale=self.scale)
            self.rect = self.image.get_rect(topleft=(self.x*self.scale,self.y*self.scale))
            self.cost = 100

        if self.name == "Potion":
            self.image = sprite_loader.get_image(11, 4, 16, 16,scale=self.scale)
            self.rect = self.image.get_rect(topleft=(self.x*self.scale,self.y*self.scale))
            self.cost = 50

        if self.name == "Gold":
            self.image = sprite_loader.get_image(7, 3, 16, 16,scale=self.scale)
            self.rect = self.image.get_rect(topleft=(self.x*self.scale,self.y*self.scale))

    def use(self,player_state):
        if self.name == "Potion":
            player_state.current_health += 50
            if player_state.current_health > player_state.max_health:
                player_state.current_health = player_state.max_health