import pygame
import assets.spritesheet as spritesheet
from assets.items import Item

pygame.init()
class BuyMenu:
    def __init__(self,items,font,screen,x,y,width,height,player_state):
        self.items = items
        self.font = font
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected_index = 0
        self.is_open = True
        self.player_state = player_state

    def render(self):
        menu_background_color = (50,50,50)
        pygame.draw.rect(self.screen,menu_background_color,(self.x,self.y,self.width,self.height))
        for i, item in enumerate(self.items):
            border_color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            image_x = self.x + 40 + i * 100
            image_y = self.y + 30
            text_y = image_y + 60
            pygame.draw.rect(self.screen, border_color, (image_x-5, image_y-5, 60, 60), 2)
            if item.image:
                self.screen.blit(item.image,(image_x,image_y))
            name_text = self.font.render(item.name, False, border_color)
            cost_text = self.font.render(f"{item.cost} Gold", False, border_color)
            self.screen.blit(name_text, (image_x, text_y))
            self.screen.blit(cost_text, (image_x, text_y + 20))


    def handle_input(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_d:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                selected_item = self.items[self.selected_index]
                if self.player_state.gold >= selected_item.cost:
                    self.player_state.gold -= selected_item.cost
                    if selected_item.name == "Potion":
                        self.player_state.potion_amount += 1
                    elif selected_item.name == "Lucky_die":
                        self.player_state.lucky_die_amount += 1
                    print(f"You bought {selected_item.name}")
                else:
                    print("Not enough gold")
            elif event.key == pygame.K_ESCAPE:
                self.is_open = False

class Merchant(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite_sheet = None
        self.image = None
        self.rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.load_sprite_sheet()
        self.load_img()

    def load_sprite_sheet(self):
        self.sprite_sheet = pygame.image.load("../assets/map_entities/NPCS.png").convert_alpha()

    def load_img(self):
        sprite_loader = spritesheet.HandleSpriteSheet(self.sprite_sheet)
        self.image = sprite_loader.get_image(1, 0, 16, 16)

    def check_interact(self, player):
        merchant_x, merchant_y = self.x, self.y
        player_x, player_y = player.x // 16, player.y // 16
        if merchant_x == player_x and merchant_y == player_y - 1:  # Above
            return True
        if merchant_x == player_x and merchant_y == player_y + 1:  # Below
            return True
        if merchant_x == player_x - 1 and merchant_y == player_y:  # Left
            return True
        if merchant_x == player_x + 1 and merchant_y == player_y:  # Right
            return True
        return False

    def interact(self,event,player,player_state):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.check_interact(player):
                potion = Item(0,0,"Potion")
                lucky_die = Item(0,0,"Lucky_die")
                items = [potion,lucky_die]
                font = pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 32)
                screen = pygame.display.get_surface()
                screen_height = pygame.display.get_surface().get_height()
                screen_width = pygame.display.get_surface().get_width()
                buy_menu = BuyMenu(items,font,screen,((screen_width-250) // 2),((screen_height-250) // 2),250,150,player_state)
                while buy_menu.is_open:
                    for event in pygame.event.get():
                        buy_menu.handle_input(event)
                    buy_menu.render()
                    pygame.display.update()
                return True
        else:
            return False