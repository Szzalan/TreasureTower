import pygame
import random
pygame.init()

class Dice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.starting_x = x
        self.starting_y = y
        self.image = pygame.image.load("../assets/dice_faces/front-6.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.gravity = 0
        self.jumped = False
        self.bounced = False
        self.has_landed = False
        self.start = True
        self.x_offset = 0
        self.jump_strength = 20
        self.angled_frames = self.angled_dice()
        self.front_frames = self.front_dice()
        self.current_frame_index = 0
        self.frame_counter = 0
        self.ground_level = y
        self.landed_index = None

    @staticmethod
    def angled_dice():
        dice_angled_1_surf = pygame.image.load("../assets/dice_faces/angled-left&right-1.png").convert_alpha()
        dice_angled_left_2_surf = pygame.image.load("../assets/dice_faces/angled-left-2.png").convert_alpha()
        dice_angled_right_2_surf = pygame.image.load("../assets/dice_faces/angled-right-2.png").convert_alpha()
        dice_angled_left_3_surf = pygame.image.load("../assets/dice_faces/angled-left-3.png").convert_alpha()
        dice_angled_right_3_surf = pygame.image.load("../assets/dice_faces/angled-right-3.png").convert_alpha()
        dice_angled_left_right_4_surf = pygame.image.load("../assets/dice_faces/angled-left&right-4.png").convert_alpha()
        dice_angled_left_right_5_surf = pygame.image.load("../assets/dice_faces/angled-left&right-5.png").convert_alpha()
        dice_angled_left_6_surf = pygame.image.load("../assets/dice_faces/angled-left-6.png").convert_alpha()
        dice_angled_right_6_surf = pygame.image.load("../assets/dice_faces/angled-right-6.png").convert_alpha()

        return [dice_angled_1_surf, dice_angled_left_2_surf, dice_angled_right_2_surf, dice_angled_left_3_surf,
                          dice_angled_right_3_surf, dice_angled_left_right_4_surf, dice_angled_left_right_5_surf,
                          dice_angled_left_6_surf, dice_angled_right_6_surf]
    @staticmethod
    def front_dice():
        dice_front_1_surf = pygame.image.load("../assets/dice_faces/front&side-1.png").convert_alpha()
        dice_front_2_surf = pygame.image.load("../assets/dice_faces/front-2.png").convert_alpha()
        dice_front_3_surf = pygame.image.load("../assets/dice_faces/front-3.png").convert_alpha()
        dice_front_4_surf = pygame.image.load("../assets/dice_faces/front&side-4.png").convert_alpha()
        dice_front_5_surf = pygame.image.load("../assets/dice_faces/front-5.png").convert_alpha()
        dice_front_6_surf = pygame.image.load("../assets/dice_faces/front-6.png").convert_alpha()

        return [dice_front_4_surf, dice_front_1_surf, dice_front_2_surf, dice_front_3_surf, dice_front_5_surf, dice_front_6_surf]

    def roll_dice_start(self):
        if self.start and self.rect.bottom >= self.ground_level:
            self.rect.midbottom = (self.starting_x, self.starting_y)
            self.x_offset = 0
            self.gravity = -self.jump_strength
            self.jumped = True
            self.bounced = False
            self.start = False

    def roll_animation(self):
        if self.rect.bottom < self.ground_level and self.frame_counter % 2 == 0:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.angled_frames)
            self.image = self.angled_frames[self.current_frame_index]

        elif not self.has_landed:
            self.image = random.choice(self.front_frames)
            self.landed_index = self.front_frames.index(self.image)
            self.has_landed = True

    def apply_gravity(self):
        if self.jumped or self.bounced:
            self.gravity += 1
            self.rect.y += self.gravity

            self.x_offset -= 0.1
            self.rect.x += self.x_offset
            self.has_landed = False

        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            if self.jumped:
                self.gravity = -15
                self.jumped = False
                self.bounced = True
                self.x_offset = 0
            elif self.bounced:
                self.gravity = 0
                self.bounced = False
                self.x_offset = 0
                self.start = True

    def update(self):
        self.frame_counter += 1
        self.roll_animation()
        self.apply_gravity()

    def roll_value(self):
        if self.landed_index is not None:
            if self.landed_index == 5:
                return (self.landed_index + 1) * 2
            return self.landed_index + 1
        return None
