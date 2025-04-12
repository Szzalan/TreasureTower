import pygame
import random
pygame.init()

class Dice(pygame.sprite.Sprite):
    """
    Represents a die object in the game's combat state.
    Attributes:
        starting_x (int): The x-coordinate of the die's starting position.
        starting_y (int): The y-coordinate of the die's starting position.
        image (pygame.Surface): The die's image surface.
        rect (pygame.Rect): The die's rectangle.
        gravity (int): The current gravity applied to the dice.
        jumped (bool): Indicates whether the die is in jump motion.
        bounced (bool): Indicates whether the dice is in bounce motion.
        has_landed (bool): Indicates whether the dice has landed.
        start (bool): Indicates whether the die has stopped the animation.
        x_offset (int): The current x-offset applied to the dice.
        jump_strength (int): The strength of the jump applied to the dice.
        angled_frames (list): A list of surfaces representing the die's angled frames.
        front_frames (list): A list of surfaces representing the die's front frames.
        current_frame_index (int): The index of the current frame.
        frame_counter (int): The counter used to determine when to change frames.
        ground_level (int): The y-coordinate of the ground level.
        landed_index (int): The index of the last frame which has the die landed on.
    """
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
        """
        Scales a list of surfaces by a specified factor.

        Args:
            frames (list): List of surface objects representing the frames to scale.
            scale_factor (float): The factor by which the frame dimensions should be scaled.

        :returns list: List of scaled frames.
        """
        return [pygame.transform.scale(frame, (frame.get_width() * scale_factor,frame.get_height() * scale_factor))
                for frame in frames]
    @staticmethod
    def angled_dice():
        """
        Loads and returns a list of surfaces representing all angled die face images.

        :returns list: A list representing all the die's angled face images.
        """
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
        """
        Loads and returns a list of images representing all front faces.

        :returns list: A list representing all the die's front face images.
        """
        dice_front_1_surf = pygame.image.load("../assets/dice_faces/front&side-1.png").convert_alpha()
        dice_front_2_surf = pygame.image.load("../assets/dice_faces/front-2.png").convert_alpha()
        dice_front_3_surf = pygame.image.load("../assets/dice_faces/front-3.png").convert_alpha()
        dice_front_4_surf = pygame.image.load("../assets/dice_faces/front&side-4.png").convert_alpha()
        dice_front_5_surf = pygame.image.load("../assets/dice_faces/front-5.png").convert_alpha()
        dice_front_6_surf = pygame.image.load("../assets/dice_faces/front-6.png").convert_alpha()

        return [dice_front_1_surf, dice_front_2_surf, dice_front_3_surf, dice_front_4_surf, dice_front_5_surf, dice_front_6_surf]

    def roll_dice_start(self):
        """
        Starts the dice roll animation. Resets the die into it's starting position.
        Initiates the jump motion.
        """
        if self.start and self.rect.bottom == self.ground_level:
            self.rect.midbottom = (self.starting_x, self.starting_y) # reset to starting position
            self.x_offset = 0
            self.gravity = -self.jump_strength #applies gravity for jump
            self.jumped = True
            self.bounced = False
            self.start = False
            self.has_landed = False
            self.landed_index = None

    def roll_animation(self):
        """
        Cycles through the dice frames immitating a rolling dice.
        If it touches the ground it chooses from front facing frames instead.
        If the animation has ended, it generates a random index and set it as the last frame.
        """
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
        """
        Controls the die's movement during the animation depending on the motion.
        """
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
        """
        Controls the speed of the die's frame switching.
        Controls the motion of the die and updates the animation to reflect
        the motion.
        """
        self.frame_counter += 1
        self.apply_gravity()
        self.roll_animation()


    def roll_value(self):
        """
        Computes the last frame's value for combat purposes.

        :returns int or None: Returns an integer value based on the last frame of the animation or None if the
            object has not landed.
        """
        if self.has_landed and self.landed_index is not None:
            if self.landed_index == 6:
                return self.landed_index * 2
            return self.landed_index
        return None
