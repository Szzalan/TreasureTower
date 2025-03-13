import pygame


class HandleSpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_h, frame_v, width, height):
        image = pygame.Surface((width, height),pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_h * width), (frame_v * height), width, height))
        return image