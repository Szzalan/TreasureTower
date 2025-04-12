import pygame


class HandleSpriteSheet:
    """
    Handles operations related to a sprite sheet.
    This class is designed to extract individual sprites from a
    sprite sheet.

    Attributes:
        sheet (pygame.Surface): The sprite sheet containing the sprites.
    """
    def __init__(self, image):
        """
        Initializes the sprite sheet.

        Args:
            image: The sprite sheet containing the sprites.
        """
        self.sheet = image

    def get_image(self, frame_h, frame_v, width, height,offset_v=0,offset_h=0,scale = 1):
        """
        Extracts an image from the sprite sheet and scales it according to the provided parameters.

        Args:
            frame_h (int): The horizontal index of the frame to extract.
            frame_v (int): The vertical index of the frame to extract.
            width (int): The width of the extracted image.
            height (int): The height of the extracted image.
            offset_v (int, optional): The vertical offset of the frame to extract. Defaults to 0.
            offset_h (int, optional): The horizontal offset of the frame to extract. Defaults to 0.
            scale (int, optional): The scale factor for the extracted image. Defaults to 1.

        :return: The extracted image.
        """
        image = pygame.Surface((width, height),pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_h * width)+offset_h, (frame_v * height)+offset_v, width, height))
        image = pygame.transform.scale(image,(width*scale,height*scale))
        return image