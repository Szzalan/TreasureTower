import pygame
import random
pygame.init()
import assets.spritesheet as spritesheet

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy entity in the game's exploration state.

    Attributes:
        x (int): The x coordinate of the enemy on the map.
        y (int): The y coordinate of the enemy on the map.
        enemy_type (str): The type of the enemy.
        image (pygame.Surface): The image representing the enemy
        sprite_sheet (pygame.Surface): The sprite sheet containing the enemy's image.
        frames (dict): A dictionary containing the enemy's animation frames.
        frame_index (int): The index of the current animation frame.
        frame_timer (int): The timestamp of the last frame update for timing animations.
        frame_delay (int): The delay between animation frames, in milliseconds.
        rect (pygame.Rect): The rectangle object defining the position and boundaries of the enemy.
    """
    def __init__(self, x, y,enemy_type, frame_delay=250):
        """
        Initializes an enemy object.

        Args:
            x (int): The x coordinate of the enemy on the map.
            y (int): The y coordinate of the enemy on the map.
            enemy_type (str): The type of the enemy
            frame_delay (int): The delay between animation frames, in milliseconds.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.image = None
        self.sprite_sheet = None
        self.frames = []
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.load_sprite_sheet()
        self.load_frames()
        self.rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)

    def load_sprite_sheet(self):
        """
        Loads the enemy's respective sprite sheet depending on its type.
        """
        if self.enemy_type == "slime":
            self.sprite_sheet = pygame.image.load("../assets/map_entities/slime_sprite_sheet.png").convert_alpha()
        elif self.enemy_type == "skeleton":
            self.sprite_sheet = pygame.image.load("../assets/map_entities/undead_sprites.png").convert_alpha()
        elif self.enemy_type == "zombie":
            self.sprite_sheet = pygame.image.load("../assets/map_entities/undead_sprites.png").convert_alpha()
        elif self.enemy_type == "boss":
            self.sprite_sheet = pygame.image.load("../assets/map_entities/boss_summon_circle.png").convert_alpha()


    def load_frames(self):
        """
        Loads and initializes sprite frames for an enemy object based on its type.
        """
        sprite_loader = spritesheet.HandleSpriteSheet(self.sprite_sheet)
        if self.enemy_type == "slime":
            self.frames = [
                sprite_loader.get_image(0, 0, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 0, 16, 16,offset_h=16)
            ]
        elif self.enemy_type == "zombie":
            self.frames = [
                sprite_loader.get_image(0, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(1, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(2, 1, 16, 16,offset_h=11),
                sprite_loader.get_image(3, 1, 16, 16,offset_h=11)
            ]
        elif self.enemy_type == "skeleton":
            self.frames = [
                sprite_loader.get_image(0, 2, 16, 16,offset_h=10),
                sprite_loader.get_image(1, 2, 16, 16, offset_h=10),
                sprite_loader.get_image(2, 2, 16, 16, offset_h=10),
                sprite_loader.get_image(3, 2, 16, 16, offset_h=10)

            ]
        elif self.enemy_type == "boss":
            self.frames = [
                sprite_loader.get_image(0, 0, 16, 16)
            ]
        self.image = self.frames[0]

    def animation_loop(self,current_time=0):
        """
        Updates the current animation frame in the loop based on the elapsed time.

        Arg:
            current_time (int): The current time in milliseconds. Defaults to 0.
        """
        if current_time - self.frame_timer > self.frame_delay:
            self.frame_timer = current_time
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def update(self,current_time):
        """
        Calls animation_loop() to update each individual enemy.
        """
        self.animation_loop(current_time=current_time)

    def check_interact(self, player):
        """
        Checks player interactions with the enemy based on their position.

        Args:
            player (Player): The player object interacting with the enemy.

        :returns bool: True if player interacts with the enemy, False otherwise.
        """
        enemy_x,enemy_y = self.x, self.y
        player_x, player_y = player.x // 16, player.y // 16
        if enemy_x == player_x and enemy_y == player_y - 1:  # Above
            return True
        if enemy_x == player_x and enemy_y == player_y + 1:  # Below
            return True
        if enemy_x == player_x - 1 and enemy_y == player_y:  # Left
            return True
        if enemy_x == player_x + 1 and enemy_y == player_y:  # Right
            return True
        return False

    def interact(self,event,player):
        """
        Handles player interactions with the enemy.

        Args:
            event (pygame.event.Event): The event object representing the user input.
            player (Player): The player object interacting with the enemy.

        :returns boolean: True if the player interacts with the enemy False otherwise.
        """
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.check_interact(player):
                return True
        if self.rect.colliderect(player_rect):
            return True
        else:
            return False


