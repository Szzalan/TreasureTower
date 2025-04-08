import pygame
from assets.spritesheet import HandleSpriteSheet

class CombatPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y,health,damage,frame_delay=250):
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
        self.load_sprite_sheet()
        self.load_frames()

    def load_sprite_sheet(self):
        if self.state == "idle":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Idle.png").convert_alpha()
        if self.state == "attack":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Attack_1.png").convert_alpha()
        if self.state == "hurt":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Hurt.png").convert_alpha()
        if self.state == "death":
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Dead.png").convert_alpha()

    def load_frames(self):
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
        if new_state != self.state:
            self.state = new_state
            self.load_sprite_sheet()
            self.load_frames()
            self.frame_index = 0
            self.frame_timer = pygame.time.get_ticks()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.frame_timer > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.state])
            self.image = self.frames[self.state][self.frame_index]
            self.frame_timer = current_time

    def update(self):
        if self.state in self.frames:
            self.animate()
        if self.current_health <= 0 and self.state != "death":
            self.change_state("death")

    def take_damage(self,damage):
        self.current_health -= damage
        print(f"Player takes {damage} damage! Current health: {self.current_health}")
        if self.current_health > 0:
            self.change_state("hurt")
        else:
            self.change_state("death")
            print("Player has died!")

    def attack(self,enemy,dice_roll_value):
        if self.state in ["attack","death"]:
            return
        self.change_state("attack")
        attack_damage = self.damage + dice_roll_value
        print(f"Dice roll value {dice_roll_value}, damage {self.damage}")
        print(f"Player attacks for {attack_damage} damage!")
        enemy.take_damage(attack_damage)