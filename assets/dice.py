import pygame
import random
pygame.init()

class Dice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.starting_x = x
        self.starting_y = y
        self.image = pygame.image.load("../assets/dice_faces/front-6.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.gravity = 0
        self.jumped = False
        self.bounced = False
        self.has_landed = False
        self.start = True
        self.x_offset = 0
        self.jump_strength = 20
        self.angled_frames = self.scale_frames(self.angled_dice(),2)
        self.front_frames = self.scale_frames(self.front_dice(), 2)
        self.current_frame_index = 0
        self.frame_counter = 0
        self.ground_level = y
        self.landed_index = None

    @staticmethod
    def scale_frames(frames, scale_factor):
        return [pygame.transform.scale(frame, (frame.get_width() * scale_factor,frame.get_height() * scale_factor))
                for frame in frames]
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

        return [dice_front_1_surf, dice_front_2_surf, dice_front_3_surf, dice_front_4_surf, dice_front_5_surf, dice_front_6_surf]

    def roll_dice_start(self):
        print("Roll started: Reset has_landed and landed_index")
        if self.start and self.rect.bottom >= self.ground_level:
            self.rect.midbottom = (self.starting_x, self.starting_y)
            self.x_offset = 0
            self.gravity = -self.jump_strength
            self.jumped = True
            self.bounced = False
            self.start = False
            self.has_landed = False
            self.landed_index = None

    def roll_animation(self):
        if self.rect.bottom < self.ground_level and self.frame_counter % 2 == 0:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.angled_frames)
            self.image = self.angled_frames[self.current_frame_index]

        elif self.bounced or self.jumped:
            if self.frame_counter % 5 == 0:
                 self.image = random.choice(self.front_frames)
        elif self.has_landed:
            if self.landed_index is None:
                self.landed_index = random.randint(1, 6)
            self.image = self.front_frames[self.landed_index - 1]

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
                self.has_landed = True

    def update(self):
        self.frame_counter += 1
        self.apply_gravity()
        self.roll_animation()


    def roll_value(self):
        if self.has_landed and self.landed_index is not None:
            if self.landed_index == 6:
                return self.landed_index * 2
            return self.landed_index
        return None
