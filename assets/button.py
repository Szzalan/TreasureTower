from email.mime import image

import pygame

class Button:
    """
    Button class for creating a button in a pygame window.

    Attributes:
        x_pos (int): The x-coordinate of the button's position.
        y_pos (int): The y-coordinate of the button's position.
        font (pygame.font.Font): The font used for rendering the button's text.
        default_rect_color (tuple): Used for storing the default color of the button's rectangle.
        text_input (str): The text displayed on the button.
        base_color (tuple): The color of the button's text.
        rect_color (tuple): The color of the button's rectangle.
        hover_color (tuple): The color of the button's rectangle when hovered over.
        text (pygame.Surface): The rendered text surface for the button.
        rect_size (tuple): The size of the button's rectangle.
        rect (pygame.Rect): The rectangle representing the button's position and size.
        text_rect (pygame.Rect): The rectangle representing the button's text position.
    """
    pygame.init()
    def __init__(self, pos, text_input, font=pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 50),
                 base_color=(169,169,169), rect_color=(0,0,0), rect_size=None, hover_color=(112,128,144)):
        """
        Initializes a Button object.

        Args:
            pos (tuple): The position of the button as a tuple (x, y).
            text_input (str): The text displayed on the button.
            font (pygame.font.Font, optional): The font used for rendering the button's text.
            base_color (tuple, optional): The color of the button's text.
            rect_color (tuple, optional): The color of the button's rectangle.
            rect_size (tuple, optional): The size of the button's rectangle.
            hover_color (tuple, optional): The color of the button's rectangle when hovered over.
        """
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.default_rect_color = rect_color
        self.text_input = text_input
        self.base_color = base_color
        self.rect_color = rect_color
        self.hover_color = hover_color
        self.text = self.font.render(self.text_input, False, self.base_color)
        text_width = self.text.get_width()
        text_height = self.text.get_height()

        if rect_size is None:
            padding = 5
            self.rect_size = (text_width + padding * 2, text_height + padding * 2)

        else:
            self.rect_size = rect_size

        self.rect = pygame.Rect(0, 0, self.rect_size[0], self.rect_size[1])
        self.rect.center = (self.x_pos, self.y_pos)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self,screen):
        """
        Draws the button on the screen and handles color change.

        Args:
            screen (pygame.Surface): The surface on which the button is drawn.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect_color = self.hover_color

        else:
            self.rect_color = self.default_rect_color

        pygame.draw.rect(screen, self.rect_color, self.rect,border_radius=10)
        screen.blit(self.text, self.text_rect)
