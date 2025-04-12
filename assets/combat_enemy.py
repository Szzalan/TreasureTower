import pygame
import random

from assets.spritesheet import HandleSpriteSheet

ENEMY_STATS = {
    "slime": {
        "max_health": 30,
        "damage_range": (3,7),
        "reward_range": (10,15)
    },
    "skeleton": {
        "max_health": 45,
        "damage_range": (10,14),
        "reward_range": (15,20)
    },
    "zombie": {
        "max_health": 60,
        "damage_range": (7,12),
        "reward_range": (20,25)
    },
    "boss":{
        "max_health": 80,
        "damage_range": (12,16),
        "reward_range": (20,25)
    }
}

class CombatEnemy(pygame.sprite.Sprite):
    """
    Represents an enemy object in the game's combat state.

    Attributes:
        x (int): The x coordinate of the enemy's position.
        y (int): The y coordinate of the enemy's position.
        enemy_type (str): The type of the enemy.
        max_health (int): The maximum health value of the enemy.
        current_health (int): The current health value of the enemy.
        damage (int): The amount of damage an enemy can deal to a target.
        reward (int): The reward value for defeating an enemy.
        image (pygame.Surface): The enemy's image.
        sprite_sheet (pygame.Surface): The sprite sheet containing animation
        frames for the enemy.
        frames (dict): A dictionary for different enemy states.
        frame_index (int): The index of the current frame being displayed in the
        enemy's animation.
        rect (pygame.Rect): The rectangle representing the enemy's position and size.
        frame_timer (int): The timestamp of the last frame update for timing animations.
        frame_delay (int): The delay between animation frame changes.
        state (str): The current state of the enemy.
        is_dead (bool): True if the enemy is dead, False otherwise.
        animation_finished (bool): True if the current animation is finished, False otherwise.
        next_state (str): The next state the enemy should transition after the current animation.
        attack_timer (int): A timer for handling delay after attack state.
        death_timer (int): A timer for handling delay after death state.
    """
    def __init__(self,x,y,enemy_type,frame_delay=250):
        """
        Initializes an enemy object.

        Args:
            x (int): The x coordinate of the enemy's position.
            y (int): The y coordinate of the enemy's position.
            enemy_type (str): The type of the enemy.
            frame_delay (int,optional): The delay between animation frame changes.
        """
        super().__init__()
        stats = ENEMY_STATS.get(enemy_type)
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.max_health = stats["max_health"]
        self.current_health = self.max_health
        self.damage = random.randint(*stats["damage_range"])
        self.reward = random.randint(*stats["reward_range"])
        self.image = None
        self.sprite_sheet = None
        self.frames = {}
        self.frame_index = 0
        self.rect = pygame.Rect(x,y,100,100)
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.state = "idle"
        self.is_dead = False
        self.animation_finished = False
        self.next_state = None
        self.attack_timer = 0
        self.death_timer = 0
        self.load_sprite_sheet()
        self.load_frames()

    def load_sprite_sheet(self):
        """
        Loads the sprite sheet for the enemy based on its type.
        """
        if self.enemy_type == "slime":
            self.sprite_sheet = pygame.image.load("../assets/map_entities/slime_sprite_sheet.png").convert_alpha()
        if self.enemy_type == "skeleton" or self.enemy_type == "boss":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/skeleton/Skeleton_enemy.png").convert_alpha()
        if self.enemy_type == "zombie":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Zombie.png").convert_alpha()

    def load_frames(self):
        """
        Loads the enemy's animation frames from the sprite sheet and associates them with their respective dictionary keys
        based on enemy type.
        """
        sprite_loader = HandleSpriteSheet(self.sprite_sheet)
        if self.enemy_type == "slime":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(1, 0, 24, 16, offset_h=4, scale=10)
            ]
            self.frames["attack"] = [
                sprite_loader.get_image(0, 1, 24, 16, offset_h=4,scale=10),
                sprite_loader.get_image(1, 1, 24, 16, offset_h=4,scale=10),
                sprite_loader.get_image(2, 1, 24, 16, offset_h=4,scale=10),
                sprite_loader.get_image(3, 1, 24, 16, offset_h=4,scale=10)
            ]
            self.frames["hurt"] = [
                sprite_loader.get_image(0, 2, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(0, 0, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(1, 0, 24, 16, offset_h=4, scale=10)
            ]
            self.frames["death"] = [
                sprite_loader.get_image(0, 2, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(1, 2, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(2, 2, 24, 16, offset_h=4, scale=10),
                sprite_loader.get_image(3, 2, 24, 16, offset_h=4, scale=10)
            ]
        if self.enemy_type == "zombie":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 32, 32, scale=8),
                sprite_loader.get_image(1, 0, 32, 32, scale=8),
                sprite_loader.get_image(2, 0, 32, 32, scale=8),
                sprite_loader.get_image(3, 0, 32, 32, scale=8),
                sprite_loader.get_image(4, 0, 32, 32, scale=8),
                sprite_loader.get_image(5, 0, 32, 32, scale=8),
                sprite_loader.get_image(6, 0, 32, 32, scale=8),
                sprite_loader.get_image(7, 0, 32, 32, scale=8)
            ]
            self.frames["attack"] = [
                sprite_loader.get_image(0, 1, 32, 32, scale=8),
                sprite_loader.get_image(1, 1, 32, 32, scale=8),
                sprite_loader.get_image(2, 1, 32, 32, scale=8),
                sprite_loader.get_image(3, 1, 32, 32, scale=8),
                sprite_loader.get_image(4, 1, 32, 32, scale=8),
                sprite_loader.get_image(5, 1, 32, 32, scale=8),
                sprite_loader.get_image(6, 1, 32, 32, scale=8)
            ]
            self.frames["hurt"] = [
                sprite_loader.get_image(0, 5, 32, 32, scale=8),
                sprite_loader.get_image(1, 5, 32, 32, scale=8),
                sprite_loader.get_image(2, 5, 32, 32, scale=8),
                sprite_loader.get_image(3, 5, 32, 32, scale=8)
            ]
            self.frames["death"] = [
                sprite_loader.get_image(0, 5, 32, 32, scale=8),
                sprite_loader.get_image(1, 5, 32, 32, scale=8),
                sprite_loader.get_image(2, 5, 32, 32, scale=8),
                sprite_loader.get_image(3, 5, 32, 32, scale=8),
                sprite_loader.get_image(4, 5, 32, 32, scale=8),
                sprite_loader.get_image(5, 5, 32, 32, scale=8),
                sprite_loader.get_image(6, 5, 32, 32, scale=8),
                sprite_loader.get_image(7, 5, 32, 32, scale=8)
            ]
        if self.enemy_type == "skeleton" or self.enemy_type == "boss":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 3, 64, 64, scale=6),
                sprite_loader.get_image(1, 3, 64, 64, scale=6),
                sprite_loader.get_image(2, 3, 64, 64, scale=6),
                sprite_loader.get_image(3, 3, 64, 64, scale=6)
            ]
            self.frames["attack"] = [
                sprite_loader.get_image(0, 0, 64, 64, scale=6),
                sprite_loader.get_image(1, 0, 64, 64, scale=6),
                sprite_loader.get_image(2, 0, 64, 64, scale=6),
                sprite_loader.get_image(3, 0, 64, 64, scale=6),
                sprite_loader.get_image(4, 0, 64, 64, scale=6),
                sprite_loader.get_image(5, 0, 64, 64, scale=6),
                sprite_loader.get_image(6, 0, 64, 64, scale=6),
                sprite_loader.get_image(7, 0, 64, 64, scale=6),
                sprite_loader.get_image(8, 0, 64, 64, scale=6),
                sprite_loader.get_image(9, 0, 64, 64, scale=6),
                sprite_loader.get_image(10, 0, 64, 64, scale=6),
                sprite_loader.get_image(11, 0, 64, 64, scale=6),
                sprite_loader.get_image(12, 0, 64, 64, scale=6)
            ]
            self.frames["hurt"] = [
                sprite_loader.get_image(0, 4, 64, 64, scale=6),
                sprite_loader.get_image(1, 4, 64, 64, scale=6),
                sprite_loader.get_image(2, 4, 64, 64, scale=6),

            ]
            self.frames["death"] = [
                sprite_loader.get_image(0, 1, 64, 64, scale=6),
                sprite_loader.get_image(1, 1, 64, 64, scale=6),
                sprite_loader.get_image(2, 1, 64, 64, scale=6),
                sprite_loader.get_image(3, 1, 64, 64, scale=6),
                sprite_loader.get_image(4, 1, 64, 64, scale=6),
                sprite_loader.get_image(5, 1, 64, 64, scale=6),
                sprite_loader.get_image(6, 1, 64, 64, scale=6),
                sprite_loader.get_image(7, 1, 64, 64, scale=6),
                sprite_loader.get_image(8, 1, 64, 64, scale=6),
                sprite_loader.get_image(9, 1, 64, 64, scale=6),
                sprite_loader.get_image(10, 1, 64, 64, scale=6),
                sprite_loader.get_image(11, 1, 64, 64, scale=6),
                sprite_loader.get_image(12, 1, 64, 64, scale=6)
            ]
        if self.frames[self.state]:
            self.image = self.frames[self.state][0]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def change_state(self,new_state):
        """
        Changes the state of the enemy to a new state based on if the current animation is finished
        or if the enemy's in idle state.
        """
        print(f"ENEMY:Changing state from {self.state} to {new_state}")
        if self.state == "death":
            return
        if self.animation_finished or self.state == "idle":
            print(f"ENEMY:State changed to {new_state}")
            self.state = new_state
            self.load_sprite_sheet()
            self.load_frames()
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()
            self.animation_finished = new_state != "idle"
            self.next_state = "idle" if new_state != "idle" else None
        else:
            print(f"ENEMY:Queued {new_state} to play after {self.state} finishes")
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
        Handles damage taken calculation and set's enemy's state into hurt if possible.
        Handles reward and set state into death if the enemy cannot take any more damage.

        Args:
            damage (int): The damage value taken by the enemy

        :returns: Reward for defeating an enemy,
        """
        if self.enemy_type == "boss":
            self.current_health -= damage // 2
            print(f"{self.enemy_type} takes {damage // 2} damage! Current health: {self.current_health}")
        else:
            self.current_health -= damage
            print(f"{self.enemy_type} takes {damage} damage! Current health: {self.current_health}")
        if self.current_health > 0:
            if self.state == "idle" or self.animation_finished:
                self.change_state("hurt")
                self.attack_timer = pygame.time.get_ticks()
        else:
            self.change_state("death")
            self.death_timer = pygame.time.get_ticks()
            print(f"{self.enemy_type} is defeated! Reward: {self.reward}")
            self.is_dead = True
            return self.reward

    def attack(self,player,dice_roll_value):
        """
        Sets enemy's state to attack if possible. Handles enemy damage calculation.

        Args:
            player (CombatPlayer): The player object that will take the damage value from the enemy's attack
            dice_roll_value (int): The value rolled by a die which will be added to the enemy's attack
            damage.

        """
        attack_damage = self.damage + dice_roll_value
        if self.state == "idle" or self.animation_finished:
            self.change_state("attack")
            self.next_state = "idle"
            print(f"Enemy attacks for Dice roll value {dice_roll_value}, damage {self.damage}")
            player.take_damage(attack_damage)