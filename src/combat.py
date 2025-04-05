import math

import pygame
from assets.button import Button

pygame.init()
clock = pygame.time.Clock()


def combat(screen, main_menu,enemy_type):
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    running = True
    bg = pygame.image.load("../assets/combat_elements/Old_dungeon/OldDungeon320X180.png").convert()
    bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(bg, (0, 0))
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)