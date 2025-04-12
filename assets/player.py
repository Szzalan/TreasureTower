import pygame

import assets.spritesheet as spritesheet

class Player(pygame.sprite.Sprite):
    """
    Represents the player in the game's exploration state.

    Attributes:
        x (int): The x-coordinate of the player.
        y (int): The y-coordinate of the player.
        width (int): The width of the player.
        height (int): The height of the player.
        image (pygame.Surface): The player's image.
        current_frame (pygame.Surface): The current animation frame of the player.
        frame_index (int): The index of the current animation frame.
        facing (str): The direction the player is facing.
        running (bool): Whether the player is currently moving.
        pre_x (int): The previous x-coordinate of the player.
        pre_y (int): The previous y-coordinate of the player.
        frames (dict): A dictionary containing the player's animation frames.
    """
    def __init__(self, x, y, width, height):
        """
        Initializes the Player object with the provided parameters.

        Args:
            x (int): The x-coordinate of the player.
            y (int): The y-coordinate of the player.
            width (int): The width of the player.
            height (int): The height of the player.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("../assets/map_entities/player_sheet.png")
        self.current_frame = None
        self.frame_index = 0
        self.facing = "front"
        self.running = False
        self.pre_x = self.x
        self.pre_y = self.y

        self.frames = {
            "right_idle": [],
            "left_idle": [],
            "back_idle": [],
            "front_idle": [],
            "right_run": [],
            "left_run": [],
            "back_run": [],
            "front_run": []
        }
        self.load_frames()

    def load_frames(self):
        """
        Loads the player's animation frames from the sprite sheet and associates them with their respective dictionary keys.
        """
        sprite_sheet = spritesheet.HandleSpriteSheet(self.image)
        self.frames["right_idle"] = [sprite_sheet.get_image(0, 0, 16, 16, offset_v=8)]
        self.frames["left_idle"] = [sprite_sheet.get_image(1, 0, 16, 16, offset_v=8)]
        self.frames["back_idle"] = [sprite_sheet.get_image(2, 0, 16, 16, offset_v=8)]
        self.frames["front_idle"] = [sprite_sheet.get_image(3, 0, 16, 16, offset_v=8)]
        self.frames["right_run"] = [sprite_sheet.get_image(0, 1, 16, 16, offset_v=8),
                                    sprite_sheet.get_image(0, 2, 16, 16, offset_v=8)]
        self.frames["left_run"] = [sprite_sheet.get_image(1, 1, 16, 16, offset_v=8),
                                   sprite_sheet.get_image(1, 2, 16, 16, offset_v=8)]
        self.frames["back_run"] = [sprite_sheet.get_image(2, 1, 16, 16, offset_v=8),
                                   sprite_sheet.get_image(2, 2, 16, 16, offset_v=8)]
        self.frames["front_run"] = [sprite_sheet.get_image(3, 1, 16, 16, offset_v=8),
                                    sprite_sheet.get_image(3, 2, 16, 16, offset_v=8)]
        self.current_frame = self.frames["front_idle"][0]

    def animation_loop(self):
        """
        Handles the player's frames when the player isn't moving.
        """
        if not self.running:
            self.current_frame = self.frames[self.facing + "_idle"][0]

    def move(self, dx, dy,dungeon_map, event):
        """
        Moves the player based on the provided input. Validates the move and updates the player's position if it's valid.
        Checks if the player has moved.

        Args:
            dx (int): The x-coordinate change.
            dy (int): The y-coordinate change.
            dungeon_map (list): The list representing the dungeon.
            event (pygame.event): The event object representing the user input.
        """
        new_x = self.x
        new_y = self.y
        self.running = False

        if event.key == pygame.K_w:
            new_y -= dy
            self.facing = "back"
            self.running = True
        elif event.key == pygame.K_a:
            new_x -= dx
            self.facing = "left"
            self.running = True
        elif event.key == pygame.K_s:
            new_y += dy
            self.facing = "front"
            self.running = True
        elif event.key == pygame.K_d:
            new_x += dx
            self.facing = "right"
            self.running = True

        if self.running:
            animation_frames = self.frames.get(self.facing + "_run",[self.current_frame])
            self.frame_index = (self.frame_index + 1) % len(animation_frames)
            self.current_frame = animation_frames[self.frame_index]

        if dungeon_map[new_y // 16][new_x // 16] in ["FLOOR","TRAPDOOR","CORRIDOR"]:
            self.x = new_x
            self.y = new_y
        else:
            self.running = False

        if self.x == self.pre_x and self.y == self.pre_y:
            self.running = False

        self.pre_x = self.x
        self.pre_y = self.y


