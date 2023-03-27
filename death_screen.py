import pygame, sys
from settings import *


class DeathScreen:
    def __init__(self, screen, restart_level, return_to_menu):
        self.screen = screen
        self.restart_level = restart_level
        self.return_to_menu = return_to_menu

        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 30)
        self.options = ['Hell no! (Restart)', "You're right... (Main Menu)"]
        self.selected = 0
        self.sound = pygame.mixer.Sound('sounds/change_selection.wav')

    def run(self):
        while True:
            self.screen.fill(('black'))
            death_text = self.font.render("Not so good, are we?", True, (255, 0, 0))
            death_x = screen_width // 2 - death_text.get_width() // 2
            death_y = screen_height // 4 - death_text.get_height() // 2
            self.screen.blit(death_text, (death_x, death_y))

            for i, option in enumerate(self.options):
                option_text = self.font.render(option, True, (0, 255, 255))
                x = screen_width // 2 - option_text.get_width() // 2
                y = screen_height // 2 - option_text.get_height() // 2 + 60 * i
                self.screen.blit(option_text, (x, y))

                if i == self.selected:
                    pointer_img = pygame.image.load('sprites/arrow.png')
                    self.screen.blit(pointer_img, (x - pointer_img.get_width() - 10, y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.selected = (self.selected - 1) % len(self.options)
                        self.sound.play()
                    elif event.key == pygame.K_s:
                        self.selected = (self.selected + 1) % len(self.options)
                        self.sound.play()
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            self.restart_level()
                            return
                        elif self.selected == 1:
                            self.return_to_menu()
                            return

            pygame.display.update()
            pygame.time.Clock().tick(60)
