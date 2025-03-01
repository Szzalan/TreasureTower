import math

import pygame
from assets.button import Button

pygame.init()
clock = pygame.time.Clock()


def how_to_play(screen, main_menu):
    text = "Your goal is to collect the treasure on top of the tower."
    text2 = "You can move using the W, A, S and D keys."
    text3 = "To claim the final treasure,you need to reach the end of the tower and kill the boss."
    text4 = "To overcome all of this you will use a magic dice to defeat your enemies."
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    informations = pygame.font.Font("../assets/Pixeltype.ttf", 30).render(text,False, (255, 255, 255))
    informations2 = pygame.font.Font("../assets/Pixeltype.ttf", 30).render(text2, False, (255, 255, 255))
    informations3 = pygame.font.Font("../assets/Pixeltype.ttf", 30).render(text3, False, (255, 255, 255))
    informations4 = pygame.font.Font("../assets/Pixeltype.ttf", 30).render(text4, False, (255, 255, 255))
    running = True
    bg = pygame.image.load("../assets/background/fallen_kingdom_1280x720.png").convert()
    scroll = 0
    tiles = math.ceil(screen.get_width() / bg.get_width()) + 1

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

        for i in range(tiles):
                screen.blit(bg, (i * bg.get_width() + scroll, 0))

        scroll -= 3
        if abs(scroll) > bg.get_width():
            scroll = 0
        pygame.draw.rect(screen, (0, 0, 0), (390,100, 740, 100),border_radius=10)
        screen.blit(informations, (screen.get_width()/2-informations.get_width()/2, screen.get_height()/2-250))
        screen.blit(informations2, (screen.get_width()/2-informations.get_width()/2, screen.get_height()/2-230))
        screen.blit(informations3, (screen.get_width()/2-informations.get_width()/2, screen.get_height()/2-210))
        screen.blit(informations4, (screen.get_width()/2-informations.get_width()/2, screen.get_height()/2-190))


        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)