import pygame
from settings import *
import sys
from highscore import Highscores
from database import get_user_highscore_and_level


class Menu:
    def __init__(self, screen, title, options, create_overworld, option_functions, user_id, is_new_account=False, current_level=None):
        self.screen = screen
        self.title = title
        self.options = options
        self.option_functions = option_functions
        self.create_overworld = create_overworld
        self.user_id = user_id
        self.is_new_account = is_new_account
        self.current_level = current_level
        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 80)
        self.font2 = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
        self.title_text = self.font.render(self.title, True, (0, 0, 0))
        self.option_text = []
        for option in self.options:
            self.option_text.append(self.font2.render(option, True, (0, 0, 0)))
        self.selected = 0
        self.options_colors = [('white' if i != self.selected else 'gold') for i in range(len(self.options))]
        self.background = pygame.image.load('sprites/menu.jpg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.sound = pygame.mixer.Sound('sounds/change_selection.wav')

    def show_highscore(self):
        highscore, _ = get_user_highscore_and_level(self.user_id)
        highscores_screen = Highscores(self.screen, highscore, self.run)
        highscores_screen.run()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_text, (screen_width / 2 - self.title_text.get_size()[0] / 2, 100))
        for i in range(len(self.options)):
            option_text = self.font2.render(self.options[i], True, pygame.Color(self.options_colors[i]))
            option_text_pos = (screen_width / 2 - option_text.get_size()[0] / 2, 320 + i * 70)
            self.screen.blit(option_text, option_text_pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.selected -= 1
                        self.sound.play()
                    if event.key == pygame.K_s:
                        self.selected += 1
                        self.sound.play()
                    if event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            _, max_level = get_user_highscore_and_level(self.user_id)
                            return self.create_overworld(0, max_level, self.user_id)
                        elif self.selected == 1:
                            print('Options')
                        elif self.selected == 2:
                            pygame.quit()
                            sys.exit()
            self.selected %= len(self.options)
            for i in range(len(self.options)):
                self.options_colors[i] = 'white' if i != self.selected else 'gold'
            self.draw()
            pygame.display.update()
            pygame.time.Clock().tick(60)
