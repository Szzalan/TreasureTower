import math

import pygame
from assets.button import Button
import random

from assets.dice import Dice

pygame.init()
clock = pygame.time.Clock()

def game(screen, main_menu):
    dice = Dice(screen.get_width()/2, 350)
    all_sprites = pygame.sprite.Group(dice)
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    roll_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60),"Roll")
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False

                if roll_button.rect.collidepoint(event.pos):
                    dice.roll_dice_start()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        all_sprites.update()
        all_sprites.draw(screen)
        roll_button.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)