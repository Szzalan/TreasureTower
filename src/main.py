import sys

import pygame
from assets.button import Button
import math
from assets.playerstate import PlayerState
from src.how_to_play import how_to_play
from src.game import game

# pygame setup
pygame.init()
player_state = PlayerState(150, 50,potion_amount = 3,lucky_die_amount = 1)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Treasure Tower')

def main_menu():
    """
    Displays the main menu for the game enabling the player to choose between playing or quitting.
    """
    clock = pygame.time.Clock()
    title = pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 100).render("Treasure Tower", False, (255, 255, 255))
    quit_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 180), "Quit")
    info_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120), "How to play")
    play_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60), "Play")
    bg = pygame.image.load("../assets/background/fallen_kingdom_1280x720.png").convert()

    scroll = 0
    tiles = math.ceil(screen.get_width() / bg.get_width()) + 1

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    game(screen, main_menu)

                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if info_button.rect.collidepoint(event.pos):
                    how_to_play(screen, main_menu)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for i in range(tiles):
            screen.blit(bg, (i * bg.get_width() + scroll, 0))

        scroll -= 3
        if abs(scroll) > bg.get_width():
            scroll = 0

        screen.blit(title, (screen.get_width()/2-title.get_width()/2, screen.get_height()/2-250))
        quit_button.draw(screen)
        info_button.draw(screen)
        play_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

main_menu()