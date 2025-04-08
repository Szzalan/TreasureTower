import math

import pygame
from assets.button import Button
from assets.dice import Dice
from assets.combat_enemy import CombatEnemy
from assets.combat_player import CombatPlayer
from assets.healthbar import HealthBar

pygame.init()
clock = pygame.time.Clock()


def combat(screen, main_menu,enemy_type):
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    running = True
    enemy_placements = {
        "skeleton" : [620,370],
        "zombie" : [640,410],
        "slime" : [700,500]
    }
    placement_x,placement_y = enemy_placements.get(enemy_type)
    enemy = CombatEnemy(placement_x,placement_y,enemy_type)
    player = CombatPlayer(screen.get_width() / 2 - 250,150,150,10)

    health_bar_player = HealthBar(screen.get_width() / 2 - 250, 690, 150, 10,player.max_health,player.current_health)
    health_bar_enemy = HealthBar(screen.get_width()/2 + 100,690,150,10,enemy.max_health,enemy.current_health)
    font = pygame.font.Font("../assets/Pixeltype.ttf", 20)

    bg = pygame.image.load("../assets/combat_elements/Old_dungeon/OldDungeon320X180.png").convert()
    bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    dice = Dice(200, 670)
    dice_sprites = pygame.sprite.Group(dice)
    player_attacked = False
    roll_button = Button((200, 690),"Roll")
    victory = False
    victory_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False

                if roll_button.rect.collidepoint(event.pos):
                    dice.roll_dice_start()
                    if dice.has_landed:
                        dice_roll_value = dice.roll_value()
                        player.attack(enemy,dice_roll_value)
                        player_attacked = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not enemy.is_dead and player_attacked:
            enemy.attack(player,dice.roll_value())
            player_attacked = False
            if player.current_health <= 0:
                player.change_state("death")
                print("Game Over!")
                main_menu()
                running = False

        elif enemy.is_dead:
            print(f"The {enemy_type} has been defeated! You win!")
            return "ENEMY_DEFEATED"

        health_bar_player.hp = player.current_health
        health_bar_enemy.hp = enemy.current_health

        screen.blit(bg, (0, 0))
        back_button.draw(screen)
        dice_sprites.update()
        dice_sprites.draw(screen)
        roll_button.draw(screen)
        enemy.update()
        player.update()
        health_bar_player.draw(screen)
        health_bar_player.health_value_display(screen,font)
        health_bar_enemy.draw(screen)
        health_bar_enemy.health_value_display(screen,font)
        screen.blit((pygame.transform.flip(enemy.image,flip_x=1,flip_y=0)), enemy.rect.topleft)
        screen.blit(player.image, player.rect.topleft)
        pygame.display.flip()
        clock.tick(60)