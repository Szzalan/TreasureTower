import pygame
import random
pygame.init()
import assets.spritesheet as spritesheet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y