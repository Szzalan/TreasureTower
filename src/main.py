import sys

import pygame
from assets.button import Button
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Treasure Tower')

def main_menu():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

        screen.fill("purple")
        title = pygame.font.Font("../assets/Pixeltype.ttf", 100).render("Treasure Tower", False, (255, 255, 255))
        quit_button = Button((screen.get_width()/2,screen.get_height()/2+180),"Quit")
        info_button = Button((screen.get_width()/2,screen.get_height()/2+120),"How to play")
        play_button = Button((screen.get_width()/2,screen.get_height()/2+60),"Play")
        screen.blit(title, (screen.get_width()/2-title.get_width()/2, screen.get_height()/2-100))
        quit_button.draw(screen)
        info_button.draw(screen)
        play_button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()
main_menu()