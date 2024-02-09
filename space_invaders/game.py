import pygame
from ship import Ship
import conf
from alien import Alien
from testo import Testo
from time import sleep
import colors

pygame.init()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT))
        pygame.display.set_caption("Space invaders")
        self.setta_valori_iniziali()
        self.ship = Ship(self.display)
        self.aliens = pygame.sprite.Group()
        self.bombe = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.testo = Testo(self.display)
        self.inizia_livello()

    def setta_valori_iniziali(self):
        self.running = True
        self.livello = 0
        self.punti = 0
        self.vite = conf.VITE
        self.alien_velocity = conf.ALIEN_VELOCITY
        self.fleet_direction = 1
        self.game_over_sound = pygame.mixer.Sound("asset/gameover.wav")
        self.lostlive_sound = pygame.mixer.Sound("asset/lostlive.wav")
        self.hit_sound = pygame.mixer.Sound("asset/hit.wav")
        self.win_sound = pygame.mixer.Sound("asset/win.wav")

    def background(self):
        img = pygame.image.load("asset/bg.jpg")
        img_rect = img.get_rect()
        img_rect.topleft = (0, 0)
        self.display.blit(img, img_rect)

    def schiera_flotta(self):
        for i in range(conf.RIGHE_FLOTTA):
            left = conf.ALIEN_WIDTH
            while left < conf.WINDOW_WIDTH - conf.ALIEN_WIDTH * 2:
                alien = Alien(
                    self.display,
                    left,
                    (conf.INTESTAZIONE_HEIGHT + 10) + i * conf.ALIEN_WIDTH,
                    self.alien_velocity,
                )

                self.aliens.add(alien)
                left += round(conf.ALIEN_WIDTH * 1.5)

    def shift_flotta(self):
        for alien in self.aliens.sprites():
            alien.shift(self.fleet_direction)

    def controlla_flotta(self):
        if not self.aliens.sprites():
            self.inizia_livello()
            return
        for alien in self.aliens.sprites():
            if alien.rect.bottom > conf.WINDOW_HEIGHT - conf.SHIP_HEIGHT:
                self.lose_life()
                break
            if alien.rect.right >= conf.WINDOW_WIDTH or alien.rect.left <= 0:
                self.fleet_direction = -self.fleet_direction
                self.shift_flotta()
                break

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.ship.bullets, self.aliens, True, True
        )
        if len(collisions):
            self.punti += len(collisions) * (self.livello * 10)
            self.hit_sound.play()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.lose_life()

        if pygame.sprite.spritecollideany(self.ship, self.bombe):
            self.lose_life()

    def lose_life(self):
        self.lostlive_sound.play()
        self.vite -= 1
        if self.vite == 0:
            self.gameover()
        else:
            self.inizia_livello(False)

    def gameover(self, finito=False):
        is_paused = True
        self.display.fill(colors.Black)
        if finito:
            self.win_sound.play()
            ##Bonus di punti per la fine del gioco (3000 punti per ogni vita rimasta)
            for i in range(self.vite):
                self.punti += 3000

            self.testo.gameover(self.punti, True)
        else:
            self.game_over_sound.play()
            self.testo.gameover(self.punti)

        pygame.display.update()

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        is_paused = False
                        self.running = False
                    if event.key == pygame.K_s:
                        is_paused = False
                        self.setta_valori_iniziali()
                        self.inizia_livello()

    def inizia_livello(self, nuovo=True):
        if nuovo:
            self.livello += 1

        ## Ho vinto il gioco
        if self.livello > conf.LIVELLO_FINALE:
            self.gameover(True)

        self.aliens.empty()
        self.bombe.empty()
        self.ship.bullets.empty()
        self.ship.pos_center()
        self.alien_velocity = self.alien_velocity + (
            (self.livello - 1) * conf.ALIEN_VELOCITY_INCREMENT
        )
        self.schiera_flotta()
        sleep(1)

    def loop(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False

            self.display.fill((0, 0, 0))
            self.background()
            self.testo.intestazione(self.livello, self.punti, self.vite)

            self.controlla_flotta()

            self.check_collisions()

            self.ship.update(events)
            self.aliens.update(self.fleet_direction, self.bombe)
            self.bombe.update()
            self.aliens.draw(self.display)
            self.bombe.draw(self.display)
            pygame.display.update()
            self.clock.tick(conf.FPS)


if __name__ == "__main__":
    game = Game()
    game.loop()


pygame.quit()
