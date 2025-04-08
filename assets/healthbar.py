import pygame

class HealthBar:
    def __init__(self,x,y,w,h,max_hp,hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_hp = max_hp
        self.hp = max_hp
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self,screen):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen,"red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(screen,"green",(self.x,self.y,self.w*ratio,self.h))

    def health_value_display(self,screen,font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            health_text = f"{self.hp}/{self.max_hp}"
            text_surface = font.render(health_text,False,(255,255,255))
            screen.blit(text_surface,(self.x + self.w // 2 - text_surface.get_width() // 2,self.y - 25))
