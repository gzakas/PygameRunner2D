import pygame, sys
from settings import *

class Highscores:
    def __init__(self, screen, highscore, back_func):
        self.screen = screen
        self.highscore = highscore
        self.back_func = back_func

        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
        self.background = pygame.image.load('sprites/menu.jpg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        title_text = self.font.render("Highscore", True, pygame.Color('white'))
        title_text_pos = (screen_width // 2 - title_text.get_size()[0] // 2, 100)
        self.screen.blit(title_text, title_text_pos)

        score_text = self.font.render(str(self.highscore), True, pygame.Color('gold'))
        score_text_pos = (screen_width // 2 - score_text.get_size()[0] // 2, 200)
        self.screen.blit(score_text, score_text_pos)

        back_text = self.font.render("Back", True, pygame.Color('white'))
        back_text_pos = (screen_width // 2 - back_text.get_size()[0] // 2, 300)
        self.screen.blit(back_text, back_text_pos)

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return self.back_func()
            self.draw()
            pygame.display.update()
            pygame.time.Clock().tick(60)
