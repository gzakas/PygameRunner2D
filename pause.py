import pygame, sys
from settings import *

class Pause:
    def __init__(self, surface, game, game_instance, resume_function, main_menu_function, quit_function):
        self.surface = surface
        self.game = game
        self.game_instance = game_instance
        self.resume_function = resume_function
        self.main_menu_function = main_menu_function
        self.quit_function = quit_function
        self.is_paused = False
        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
        self.options = ['Resume', 'Main Menu', 'Quit']
        self.selected = 0
        self.options_colors = [('white' if i != self.selected else 'gold') for i in range(len(self.options))]
        self.sound = pygame.mixer.Sound('sounds/change_selection.wav')
        self.background = pygame.image.load('sprites/menu.jpg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

    def draw(self):
        self.surface.blit(self.background, (0, 0))
        for index, option in enumerate(self.options):
            option_surface = self.font.render(option, True, pygame.Color(self.options_colors[index]))
            x = self.surface.get_width() // 2 - option_surface.get_width() // 2
            y = self.surface.get_height() // 2 - option_surface.get_height() // 2 + 70 * index
            self.surface.blit(option_surface, (x, y))

    def update_paused_state(self, new_state):
        self.is_paused = new_state

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] and self.selected < len(self.options) - 1:
            self.selected += 1
            self.sound.play()
            self.options_colors[self.selected] = 'gold'
            self.options_colors[self.selected - 1] = 'white'
        elif keys[pygame.K_w] and self.selected > 0:
            self.selected -= 1
            self.sound.play()
            self.options_colors[self.selected] = 'gold'
            self.options_colors[self.selected + 1] = 'white'
        elif keys[pygame.K_RETURN]:
            if self.selected == 0:
                self.resume_function()
                self.is_paused = False
            elif self.selected == 1:
                self.main_menu_function()
                self.is_paused = False
            elif self.selected == 2:
                pygame.quit()
                sys.exit()


    def run(self):
        while self.is_paused:
            self.surface.fill('black')
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    result = self.input()
                    if result == 'menu':
                        return 'menu'
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            pygame.time.Clock().tick(60)
