import math

import pygame
from assets.button import Button
import random

pygame.init()
clock = pygame.time.Clock()


def game(screen, main_menu):
    dice_angled_1_surf = pygame.image.load("./dice/angled-left&right-1.png").convert_alpha()
    dice_angled_left_2_surf = pygame.image.load("./dice/angled-left-2.png").convert_alpha()
    dice_angled_right_2_surf = pygame.image.load("./dice/angled-right-2.png").convert_alpha()
    dice_angled_left_3_surf = pygame.image.load("./dice/angled-left-3.png").convert_alpha()
    dice_angled_right_3_surf = pygame.image.load("./dice/angled-right-3.png").convert_alpha()
    dice_angled_left_right_4_surf = pygame.image.load("./dice/angled-left&right-4.png").convert_alpha()
    dice_angled_left_right_5_surf = pygame.image.load("./dice/angled-left&right-5.png").convert_alpha()
    dice_angled_left_6_surf = pygame.image.load("./dice/angled-left-6.png").convert_alpha()
    dice_angled_right_6_surf = pygame.image.load("./dice/angled-right-6.png").convert_alpha()

    dice_front_1_surf = pygame.image.load("./dice/front&side-1.png").convert_alpha()
    dice_front_2_surf = pygame.image.load("./dice/front-2.png").convert_alpha()
    dice_front_3_surf = pygame.image.load("./dice/front-3.png").convert_alpha()
    dice_front_4_surf = pygame.image.load("./dice/front&side-4.png").convert_alpha()
    dice_front_5_surf = pygame.image.load("./dice/front-5.png").convert_alpha()
    dice_front_6_surf = pygame.image.load("./dice/front-6.png").convert_alpha()

    dice_front_frames = [dice_front_4_surf, dice_front_1_surf, dice_front_2_surf, dice_front_3_surf, dice_front_5_surf, dice_front_6_surf]

    dice_angled_frames = [dice_angled_1_surf, dice_angled_left_2_surf, dice_angled_right_2_surf, dice_angled_left_3_surf,
                          dice_angled_right_3_surf, dice_angled_left_right_4_surf, dice_angled_left_right_5_surf,
                          dice_angled_left_6_surf, dice_angled_right_6_surf]
    gravity = 0
    frame_counter = 0
    current_frame_index = 0
    jumped = False
    has_landed = False
    jump_strength = 20
    bounced = False
    start = True
    x_offset = 0
    dice_surf = pygame.image.load("./dice/front-6.png").convert_alpha()
    dice_rect = dice_surf.get_rect(midbottom=(screen.get_width()/2, 350))
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    roll_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60),"Roll")
    running = True
    while running:
        screen.fill((0, 0, 0))
        frame_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False

                if roll_button.rect.collidepoint(event.pos) and start:
                    if dice_rect.bottom >= 350:
                        gravity = -jump_strength
                        jumped = True
                        bounced = False
                        start = False
                    dice_rect.midbottom = (screen.get_width() / 2, 350)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if dice_rect.bottom < 350 and frame_counter % 8 == 0:
            current_frame_index = (current_frame_index + 1) % len(dice_angled_frames)
            dice_surf = dice_angled_frames[current_frame_index]

        elif not has_landed:
            dice_surf = random.choice(dice_front_frames)
            has_landed = True

        if jumped or bounced:
            gravity += 1
            dice_rect.y += gravity
            x_offset -= 0.1
            dice_rect.x += x_offset
            has_landed = False
        if dice_rect.bottom >= 350:
            dice_rect.bottom = 350
            if jumped:
                gravity = -15
                jumped = False
                bounced = True
                x_offset = 0
            elif bounced:
                gravity = 0
                bounced = False
                x_offset = 0
                start = True
        screen.blit(dice_surf, dice_rect)
        roll_button.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)