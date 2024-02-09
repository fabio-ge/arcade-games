import pygame
import colors
import conf


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.velocity = conf.BULLET_VELOCITY
        self.rect = pygame.draw.line(
            self.screen,
            colors.Lime,
            (0, conf.WINDOW_HEIGHT - 10),
            (0, conf.WINDOW_HEIGHT - 5),
            3,
        )

    def sparato(self, x):
        altezza = conf.WINDOW_HEIGHT - conf.SHIP_HEIGHT
        self.rect = pygame.draw.line(
            self.screen,
            colors.Lime,
            (x, altezza),
            (x, altezza - 5),
            3,
        )

    def update(self):
        nuova_base = self.rect.bottom - self.velocity
        self.rect = pygame.draw.line(
            self.screen,
            colors.Lime,
            (self.rect.centerx, nuova_base),
            (self.rect.centerx, nuova_base - 5),
            3,
        )

        if self.rect.top < 0:
            self.kill()
