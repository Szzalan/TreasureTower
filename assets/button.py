import pygame

class Button:
    pygame.init()
    def __init__(self, pos, text_input, font=pygame.font.Font("../assets/Pixeltype.ttf",50), base_color=(169,169,169),rect_color=(0,0,0),rect_size=None,hover_color=(112,128,144)):
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
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect_color = self.hover_color
        else:
            self.rect_color = self.default_rect_color
        pygame.draw.rect(screen, self.rect_color, self.rect,border_radius=10)
        screen.blit(self.text, self.text_rect)
