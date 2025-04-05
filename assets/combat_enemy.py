import pygame
import random

from assets.spritesheet import HandleSpriteSheet
ENEMY_STATS = {
    "slime": {
        "max_health": 50,
        "damage_range": (3,7),
        "reward_range": (5,10)
    },
    "skeleton": {
        "max_health": 100,
        "damage_range": (10,15),
        "reward_range": (15,20)
    },
    "zombie": {
        "max_health": 150,
        "damage_range": (7,12),
        "reward_range": (20,25)
    }
}

class CombatEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type,damage,max_health,frame_delay=250):
        super().__init__()
        stats = ENEMY_STATS.get(enemy_type,{
            "max_health": 100,
            "damage_range": (5,10),
            "reward_range": (5,10)
        })
        self.enemy_type = enemy_type
        self.max_health = stats["max_health"]
        self.current_health = self.max_health
        self.damage = random.randint(*stats["damage_range"])
        self.reward = random.randint(*stats["reward_range"])
        self.image = None
        self.sprite_sheet = None
        self.frames = {}
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.state = "idle"
        self.is_dead = False
        self.load_sprite_sheet()
        self.load_frames()

    def load_sprite_sheet(self):
        if self.enemy_type == "slime":
            self.sprite_sheet = pygame.image.load("../assets/slime_sprite_sheet.png").convert_alpha()
        if self.enemy_type == "skeleton":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/skeleton/Skeleton_enemy.png").convert_alpha()
        if self.enemy_type == "zombie":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Zombie.png").convert_alpha()

    def load_frames(self):
        sprite_loader = HandleSpriteSheet(self.sprite_sheet)
        if self.enemy_type == "slime":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 0, 16, 16, offset_h=16)
            ]
            self.frames["attack"] = [
                sprite_loader.get_image(0, 1, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 1, 16, 16, offset_h=8),
                sprite_loader.get_image(2, 1, 16, 16, offset_h=8),
                sprite_loader.get_image(3, 1, 16, 16, offset_h=8)
            ]
            self.frames["hurt"] = [
                sprite_loader.get_image(0, 2, 16, 16, offset_h=8),
                sprite_loader.get_image(0, 0, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 0, 16, 16, offset_h=16)
            ]
            self.frames["death"] = [
                sprite_loader.get_image(0, 2, 16, 16, offset_h=8),
                sprite_loader.get_image(1, 2, 16, 16, offset_h=8),
                sprite_loader.get_image(2, 2, 16, 16, offset_h=8),
                sprite_loader.get_image(3, 2, 16, 16, offset_h=8),
            ]
        if self.enemy_type == "zombie":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 1, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 2, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 3, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 4, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 5, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 6, 32, 32, offset_h=8),
                sprite_loader.get_image(0, 7, 32, 32, offset_h=8)
            ]
            self.frames["attack"] = [
                sprite_loader.get_image(1, 0, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 1, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 2, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 3, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 4, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 5, 32, 32, offset_h=8),
                sprite_loader.get_image(1, 6, 32, 32, offset_h=8)
            ]
            self.frames["hurt"] = [
                sprite_loader.get_image(5, 0, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 1, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 2, 32, 32, offset_h=8)
            ]
            self.frames["death"] = [
                sprite_loader.get_image(5, 0, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 1, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 2, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 3, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 4, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 5, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 6, 32, 32, offset_h=8),
                sprite_loader.get_image(5, 7, 32, 32, offset_h=8)
            ]
        if self.enemy_type == "skeleton":
            self.frames["idle"] = [
                sprite_loader.get_image(0, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(1, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(2, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(3, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(4, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(5, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(6, 0, 64, 96, offset_h=8),
                sprite_loader.get_image(7, 0, 64, 96, offset_h=8)
            ]
            self.frames["attack"] = [
            ]
            self.frames["hurt"] = [

            ]
            self.frames["death"] = [
            ]
        self.image = self.frames["idle"][0]

    def change_state(self,new_state):
        if self.state == new_state:
            return
        self.state = new_state
        self.frame_index = 0
        self.frame_timer = 0

    def update(self,delta_time):
        if self.is_dead and self.state != "death":
            self.change_state("death")
        self.frame_timer += delta_time
        if self.frame_timer > self.frame_delay:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames[self.state]):
                if self.state == "death":
                    self.frame_index = len(self.frames["death"]) - 1
                elif self.state == "hurt":
                    self.change_state("idle")
                else:
                    self.frame_index = 0
            self.image = self.frames[self.state][self.frame_index]

    def take_damage(self,damage):
        if self.is_dead:
            return 0
        self.current_health -= damage
        print(f"{self.enemy_type} takes {damage} damage! Current health: {self.current_health}")
        if self.current_health <= 0:
            self.is_dead = True
            print(f"{self.enemy_type} is defeated! Reward: {self.reward}")
            return self.reward
        else:
            self.change_state("hurt")

    def attack(self):
        if not self.is_dead:
            print(f"{self.enemy_type} attacks!")
            self.change_state("attack")