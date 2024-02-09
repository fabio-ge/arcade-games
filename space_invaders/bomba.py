import pygame
import conf


class Bomba(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("asset/bomb.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        if self.rect.top >= conf.WINDOW_HEIGHT:
            self.kill()

        self.rect.top += conf.BOMB_VELOCITY
