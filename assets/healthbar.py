import pygame

class HealthBar:
    """
    Represents a graphical health bar for a game entity.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the health bar.
        y (int): The y-coordinate of the top-left corner of the health bar.
        w (int): The width of the health bar.
        h (int): The height of the health bar.
        max_hp (int): The maximum health of the entity.
        hp (int): The current health of the entity.
        rect (pygame.Rect): The rectangle representing the health bar's position and size.
    """
    def __init__(self,x,y,w,h,max_hp,hp):
        """
        Initializes a HealthBar object.

        Args:
            x (int): The x-coordinate of the top-left corner of the health bar.
            y (int): The y-coordinate of the top-left corner of the health bar.
            w (int): The width of the health bar.
            h (int): The height of the health bar.
            max_hp (int): The maximum health of the entity.
            hp (int): The current health of the entity.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_hp = max_hp
        self.hp = max_hp
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self,screen):
        """
        Draws a health bar on the screen indicating the current health status relative
        to the maximum health. The maximum health is displayed as a red bar and the
        current health is displayed as a green bar.

        Args:
            screen (pygame.Surface): The surface on which the health bar is drawn.
        """
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen,"red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(screen,"green",(self.x,self.y,self.w*ratio,self.h))

    def health_value_display(self,screen,font):
        """
        Displays the current health to maximum health ratio on the screen when hovered over
        the health bar.

        Args:
            screen (pygame.Surface): The surface on which the health ratio is displayed.
            font (pygame.font.Font): The font used for rendering the health ratio.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            health_text = f"{self.hp}/{self.max_hp}"
            text_surface = font.render(health_text,False,(255,255,255))
            screen.blit(text_surface,(self.x + self.w // 2 - text_surface.get_width() // 2,self.y - 25))
