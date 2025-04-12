import pygame
import random
from assets.spritesheet import HandleSpriteSheet

class CombatPlayer(pygame.sprite.Sprite):
    """
       Represents a player object in the game's combat state.

       Attributes:
           x (int): The x coordinate of the enemy's position.
           y (int): The y coordinate of the enemy's position.
           max_health (int): The maximum health value of the player.
           current_health (int): The current health value of the player.
           damage (int): The amount of damage the player can deal to an enemy.
           image (pygame.Surface): The player's image.
           sprite_sheet (pygame.Surface): The sprite sheet containing animation
           frames for the player.
           frames (dict): A dictionary for different player states.
           frame_index (int): The index of the current frame being displayed in the
           enemy's animation.
           rect (pygame.Rect): The rectangle representing the enemy's position and size.
           frame_timer (int): The timestamp of the last frame update for timing animations.
           frame_delay (int): The delay between animation frame changes.
           state (str): The current state of the player.
           animation_finished (bool): True if the current animation is finished, False otherwise.
           next_state (str): The next state the player should transition after the current animation.
           death_timer (int): A timer for handling delay after death state.
       """
    def __init__(self, x, y,health,damage,frame_delay=250):
        """
            Initializes a player object.

            Args:
                x (int): The x coordinate of the enemy's position.
                y (int): The y coordinate of the enemy's position.
                health (int): The initial health value of the player.
                damage (int): The base damage value of the player.
                frame_delay (int,optional): The delay between animation frame changes.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.max_health = health
        self.current_health = health
        self.damage = damage
        self.image = None
        self.sprite_sheet = None
        self.frames = {}
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.state = "idle"
        self.rect = pygame.Rect(x,y,100,100)
        self.animation_finished = False
        self.next_state = None
        self.death_timer = 0
        self.load_sprite_sheet()
        self.load_frames()

    def load_sprite_sheet(self):
        """
        Loads the sprite sheet for the player based on its state.
        """
        if self.state == "idle":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Idle.png").convert_alpha()
        if self.state == "attack":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Attack_1.png").convert_alpha()
        if self.state == "hurt":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Hurt.png").convert_alpha()
        if self.state == "death":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Dead.png").convert_alpha()

    def load_frames(self):
        """
        Loads the player's animation frames from the sprite sheet and associates them with their respective dictionary keys
        based on player state.
        """
        sprite_loader = HandleSpriteSheet(self.sprite_sheet)
        self.frames["idle"] = [
            sprite_loader.get_image(0, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(1, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(2, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(3, 0, 128, 128, offset_h=8, scale=4),
        ]
        self.frames["attack"] = [
            sprite_loader.get_image(0, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(1, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(2, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(3, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(4, 0, 128, 128, offset_h=8, scale=4),
        ]
        self.frames["hurt"] = [
            sprite_loader.get_image(0, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(1, 0, 128, 128, offset_h=8, scale=4)
        ]
        self.frames["death"] = [
            sprite_loader.get_image(0, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(1, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(2, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(3, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(4, 0, 128, 128, offset_h=8, scale=4),
            sprite_loader.get_image(5, 0, 128, 128, offset_h=8, scale=4)
        ]
        if self.frames[self.state]:
            self.image = self.frames[self.state][0]
            self.rect = self.image.get_rect(topleft=(self.x,self.y))


    def change_state(self,new_state):
        """
        Changes the state of the player to a new state based on if the current animation is finished
        or if the player is in attack state.
        """
        print(f"PLAYER:Changing state from {self.state} to {new_state}")
        if self.state == "death":
            return
        if self.animation_finished or new_state == "attack":
            print(f"PLAYER:State changed to {new_state}")
            self.state = new_state
            self.load_sprite_sheet()
            self.load_frames()
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()
            self.animation_finished = new_state != "idle"
            self.next_state = "idle" if new_state != "idle" else None
        else:
            print(f"PLAYER:Queued {new_state} to play after {self.state} finishes")
            self.next_state = new_state

    def animate(self):
        """
        Updates the animation frames based on the current state and elapsed time.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.frame_timer > self.frame_delay:
            self.frame_index += 1
            self.frame_timer = current_time
            if self.frame_index >= len(self.frames[self.state]):
                if self.state == "idle":
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.frames[self.state]) - 1
                    self.animation_finished = True

                if self.next_state:
                    self.change_state(self.next_state)
                    self.next_state = None

            self.image = self.frames[self.state][self.frame_index]

    def update(self):
        """
        Handles death state and calls animate() to update the animation frames.
        """
        if self.state in self.frames:
            self.animate()
        if self.current_health <= 0 and self.state != "death":
            self.change_state("death")

    def take_damage(self,damage):
        """
        Handles damage taken calculation and set's player's state into hurt if possible.
        Set state into death if the player cannot take any more damage.

        Args:
            damage (int): The damage value taken by the player
         """

        self.current_health -= damage
        print(f"Player takes {damage} damage! Current health: {self.current_health}")
        if self.current_health > 0:
            if self.state == "idle" or self.animation_finished:
                self.change_state("hurt")
        else:
            self.change_state("death")
            self.death_timer = pygame.time.get_ticks()
            print("Player has died!")

    def attack(self,enemy,dice_roll_value,lucky_die_amount):
        """
        Sets player's state to attack if possible. Handles player damage calculation.

        Args:
            enemy (CombatEnemy): The enemy object that will take the damage value from the player's attack
            dice_roll_value (int): The value rolled by a die which will be added to the enemy's attack
            damage.
            lucky_die_amount (int): The amount of lucky dice the player currently holds. This will be added to the
            damage value.
        """
        attack_damage = self.damage + dice_roll_value + (lucky_die_amount * random.randint(1,6))
        print(f"Dice roll value {dice_roll_value}, damage {self.damage}")
        if self.state == "idle" or self.animation_finished:
            self.change_state("attack")
            print(f"Player attacks for {attack_damage} damage!")
            enemy.take_damage(attack_damage)