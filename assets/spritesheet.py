import pygame


class HandleSpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_h, frame_v, width, height,offset_v=0,offset_h=0):
        image = pygame.Surface((width, height),pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_h * width)+offset_h, (frame_v * height)+offset_v, width, height))
        return image