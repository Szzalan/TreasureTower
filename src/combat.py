import math

import pygame
from assets.button import Button
from assets.dice import Dice
from assets.combat_enemy import CombatEnemy
from assets.combat_player import CombatPlayer
from assets.healthbar import HealthBar
from assets.playerstate import PlayerState

pygame.init()
clock = pygame.time.Clock()

def combat(screen, main_menu,enemy_type,player_state):
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    endgame_text = pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 100).render("GAME OVER!", False, (255, 255, 255))
    victory_text = pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 100).render("YOU WIN!", False, (255, 255, 255))

    endgame_state = False
    victory = False
    rolling = False
    running = True

    enemy_placements = {
        "skeleton" : [620,370],
        "zombie" : [640,410],
        "slime" : [700,500],
        "boss": [620,370]
    }
    placement_x,placement_y = enemy_placements.get(enemy_type)
    enemy = CombatEnemy(placement_x,placement_y,enemy_type)
    player = CombatPlayer(screen.get_width() / 2 - 250,150,player_state.current_health,10)

    health_bar_player = HealthBar(screen.get_width() / 2 - 250, 690, 150, 10,150,player.current_health)
    health_bar_enemy = HealthBar(screen.get_width()/2 + 100,690,150,10,enemy.max_health,enemy.current_health)
    font = pygame.font.Font("../assets/map_entities/Pixeltype.ttf", 20)

    bg = pygame.image.load("../assets/combat_elements/Old_dungeon/OldDungeon320X180.png").convert()
    bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    dice = Dice(200, 670)
    dice_sprites = pygame.sprite.Group(dice)
    player_attacked = False
    roll_button = Button((200, 690),"Roll")

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
                    rolling = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        enemy.update()
        player.update()

        if rolling and dice.has_landed:
            dice_roll_value = dice.roll_value()
            print(f"Dice has landed on {dice_roll_value}")
            if dice_roll_value is not None:
                print(f"Player rolled a {dice_roll_value}")
                player.attack(enemy,dice_roll_value,player_state.lucky_die_amount)
                player_attacked = True
            rolling = False

        if not enemy.is_dead and player_attacked:
            if player.animation_finished and enemy.animation_finished:
                current_time = pygame.time.get_ticks()
                attack_delay = 1000 if enemy.enemy_type == "zombie" else 500
                if current_time - enemy.attack_timer >= attack_delay:
                    enemy.attack(player,dice.roll_value())
                    player_attacked = False

        elif player.state == "death":
            endgame_state = True
            current_time = pygame.time.get_ticks()
            death_delay = 1500
            if current_time - player.death_timer >= death_delay:
                main_menu()
                running = False

        elif enemy.is_dead and enemy_type == "boss":
            victory = True
            current_time = pygame.time.get_ticks()
            death_delay = 2500
            if current_time - enemy.death_timer >= death_delay:
                main_menu()
                running = False

        elif enemy.is_dead:
            current_time = pygame.time.get_ticks()
            death_delay = 2500
            if current_time - enemy.death_timer >= death_delay:
                player_state.current_health = player.current_health
                player_state.gold += enemy.reward
                return "ENEMY_DEFEATED"

        health_bar_player.hp = player.current_health
        health_bar_enemy.hp = enemy.current_health

        screen.blit(bg, (0, 0))
        back_button.draw(screen)
        dice_sprites.update()
        dice_sprites.draw(screen)
        roll_button.draw(screen)
        health_bar_player.draw(screen)
        health_bar_player.health_value_display(screen,font)
        health_bar_enemy.draw(screen)
        health_bar_enemy.health_value_display(screen,font)
        screen.blit((pygame.transform.flip(enemy.image,flip_x=1,flip_y=0)), enemy.rect.topleft)
        screen.blit(player.image, player.rect.topleft)
        if victory:
            screen.blit(victory_text, (screen.get_width() / 2 - endgame_text.get_width() / 2, screen.get_height() / 2 - 250))
        if endgame_state:
            screen.blit(endgame_text, (screen.get_width() / 2 - endgame_text.get_width() / 2, screen.get_height() / 2 - 250))
        pygame.display.flip()
        clock.tick(60)