import pygame
import conf
from bullet import Bullet


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.velocity = conf.SHIP_VELOCITY
        self.image = pygame.image.load("asset/ship.png")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.pos_center()
        self.bullets = pygame.sprite.Group()

    def pos_center(self):
        self.rect.bottom = conf.WINDOW_HEIGHT - 10
        self.rect.centerx = conf.WINDOW_WIDTH // 2
        self.screen.blit(self.image, self.rect)

    def spara(self):
        if len(self.bullets) < conf.SHIP_BULLETS:
            bullet = Bullet(self.screen)
            bullet.sparato(self.rect.centerx)
            self.bullets.add(bullet)

    def update(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < conf.WINDOW_WIDTH:
            self.rect.x += self.velocity

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spara()

        self.screen.blit(self.image, self.rect)
        self.bullets.update()
