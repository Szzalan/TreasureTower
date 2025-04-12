import pygame

import assets.spritesheet as spritesheet
pygame.init()

class Item(pygame.sprite.Sprite):
    """
    Represents an in-game item with a specific position, name, cost, and
    associated sprite.

    Attributes:
        x (int): The x-coordinate of the item.
        y (int): The y-coordinate of the item.
        name (str): The name of the item.
        cost (int): The cost of the item.
        sprite_sheet (pygame.Surface): The sprite sheet containing the item's sprite.
        image (pygame.Surface): The image representing the item.
        scale (int): The scale factor for the item's image.
        rect (pygame.Rect): The rectangle representing the item's position and size.
    """
    def __init__(self,x,y,name, cost = 0):
        """
        Initializes an Item object.

        Args:
            x (int): The x-coordinate of the item.
            y (int): The y-coordinate of the item.
            name (str): The name of the item.
            cost (int): The cost of the item.
        """
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
        """
        Loads the sprite sheet for the item.
        """
        self.sprite_sheet = pygame.image.load("../assets/map_entities/roguelikeitems.png").convert_alpha()

    def load_items(self):
        """
        Loads the item's image and set it's cost.
        """
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
        """
        Adds functionality to the item.

        Args:
             player_state (PlayerState): The player's current state.
        """
        if self.name == "Potion":
            player_state.current_health += 50
            if player_state.current_health > player_state.max_health:
                player_state.current_health = player_state.max_health