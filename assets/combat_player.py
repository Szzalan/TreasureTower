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
            self.sprite_sheet = pygame.image.load("../assets/combat_elements/Knight_1/Death.png").convert_alpha()

    def load_frames(self):
        sprite_loader = HandleSpriteSheet(self.sprite_sheet)
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