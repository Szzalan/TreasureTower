import math

import pygame
from assets.button import Button
from assets.dice import Dice
from assets.combat_enemy import CombatEnemy
from assets.combat_player import CombatPlayer

pygame.init()
clock = pygame.time.Clock()


def combat(screen, main_menu,enemy_type):
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    running = True

    enemy = CombatEnemy(screen.get_width() / 2 + 100,screen.get_height() / 2,enemy_type)
    player = CombatPlayer(screen.get_width / 2 - 100,screen.get_height() / 2,150,10)

    bg = pygame.image.load("../assets/combat_elements/Old_dungeon/OldDungeon320X180.png").convert()
    bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    dice = Dice(screen.get_width()/2, 350)
    dice_sprites = pygame.sprite.Group(dice)
    player_attacked = False
    roll_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60),"Roll")

    while running:
        current_time = pygame.time.get_ticks()
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

        if dice.has_landed and not player_attacked:
            dice_roll_value = dice.roll_value()
            player.attack(enemy,dice_roll_value)
            player_attacked = True

        if not enemy.is_dead and player_attacked:
            enemy.attack(player)
            if player.current_health <= 0:
                player.change_state("death")
                print("Game Over!")
        screen.blit(bg, (0, 0))
        back_button.draw(screen)
        dice_sprites.update()
        dice_sprites.draw(screen)
        roll_button.draw(screen)
        player.update(current_time)
        screen.blit(player.image, player.rect.topleft)
        pygame.display.flip()
        clock.tick(60)