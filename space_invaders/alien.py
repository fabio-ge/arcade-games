import pygame
import conf
import random
from bomba import Bomba


class Alien(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, velocity):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("asset/alien.png")
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.velocity = velocity

    def shift(self, direction):
        self.rect.top += conf.ALIEN_SHIFT
        self.rect.x += direction * self.velocity

    def update(self, direction, bombe):
        """Muovo l' alieno"""
        self.rect.x += direction * self.velocity
        rand_number = random.randint(1, 1000)
        if rand_number < 3:
            self.sgancia_bomba(bombe)

    def sgancia_bomba(self, bombe):
        if len(bombe) == conf.MAX_BOMBE:
            return

        bomba = Bomba(self.rect.centerx, self.rect.bottom + 10)
        bombe.add(bomba)
