import pygame
import colors
import conf


class Testo:
    def __init__(self, screen):
        self.testo = pygame.font.Font("asset/SpaceQuest.ttf", conf.FONT_SIZE_LITTLE)
        self.screen = screen

    def intestazione(self, livello, punti, vite):
        livello = self.testo.render(f"Livello { livello }", True, colors.Green)
        livello_rect = livello.get_rect()
        livello_rect.left = 20
        livello_rect.top = 10

        punti = self.testo.render(f"Punti { punti }", True, colors.Green)
        punti_rect = punti.get_rect()
        punti_rect.top = 10
        punti_rect.right = conf.WINDOW_WIDTH - 20

        for i in range(vite):
            vita = pygame.image.load("asset/ship.png")
            vita_rect = vita.get_rect()
            vita_rect.left = (
                ((conf.WINDOW_WIDTH // 2) - conf.SHIP_HEIGHT)
                + (i * conf.SHIP_HEIGHT)
                + 10
            )
            vita_rect.top = 2
            self.screen.blit(vita, vita_rect)

        self.screen.blit(livello, livello_rect)
        self.screen.blit(punti, punti_rect)
        pygame.draw.line(
            self.screen,
            colors.Olive,
            (0, conf.INTESTAZIONE_HEIGHT),
            (conf.WINDOW_WIDTH, conf.INTESTAZIONE_HEIGHT),
            4,
        )

    def check_punteggio_massimo(self, punti):
        with open("punteggio_max", "r") as f:
            punti_max = int(f.read())

        if punti_max < punti:
            with open("punteggio_max", "w") as f:
                f.write(str(punti))
            testo = f"Complimenti hai fatto il nuovo punteggio massimo di {punti} punti"
        else:
            testo = f"Punteggio massimo {punti_max}, punti fatti da te {punti}"

        testo_punti_max = self.testo.render(testo, True, colors.Green)
        testo_punti_max_rect = testo_punti_max.get_rect()
        testo_punti_max_rect.center = (conf.WINDOW_WIDTH // 2, conf.WINDOW_HEIGHT // 2)
        self.screen.blit(testo_punti_max, testo_punti_max_rect)

    def gameover(self, punti, finito=False):
        testo = (
            f"Ci hai salvati dagli Alieni. Grazie per il tuo servizio."
            if finito
            else f"GAME OVER"
        )
        testo_gameover = self.testo.render(testo, True, colors.Green)
        testo_gameover_rect = testo_gameover.get_rect()
        testo_gameover_rect.center = (
            conf.WINDOW_WIDTH // 2,
            conf.WINDOW_HEIGHT // 2 - (conf.SHIP_HEIGHT * 2),
        )
        sottotesto = self.testo.render(
            f"Premi s per rigiocare, q per uscire", True, colors.Green
        )
        sottotesto_rect = sottotesto.get_rect()
        sottotesto_rect.center = (
            conf.WINDOW_WIDTH // 2,
            conf.WINDOW_HEIGHT // 2 + (conf.SHIP_HEIGHT * 2),
        )
        self.screen.blit(testo_gameover, testo_gameover_rect)
        self.screen.blit(sottotesto, sottotesto_rect)
        self.check_punteggio_massimo(punti)
