import pygame, sys
from settings import *
from database import register_user, login_user

class Registration:
    def __init__(self, screen, title, create_menu, create_selection_menu):
        self.screen = screen
        self.title = title
        self.create_menu = create_menu
        self.create_selection_menu = create_selection_menu
        self.error_message = ""
        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
        self.font2 = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 30)
        self.title_text = self.font.render(self.title, True, (0, 255, 255))
        self.username_text = self.font2.render("Username:", True, (255, 255, 255))
        self.password_text = self.font2.render("Password:", True, (255, 255, 255))
        self.submit_text = self.font2.render("Submit", True, (255, 255, 255))
        self.background = pygame.image.load('sprites/menu.jpg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        self.username_input = ""
        self.password_input = ""
        self.focus = "username"

    def draw_error_message(self, message):
        error_message_surface = self.font2.render(message, True, (255, 0, 0))
        self.screen.blit(error_message_surface, (screen_width / 2 - error_message_surface.get_size()[0] / 2, 550))


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_text, (screen_width / 2 - self.title_text.get_size()[0] / 2, 100))
        self.screen.blit(self.username_text, (screen_width / 2 - 200, 250))
        self.screen.blit(self.password_text, (screen_width / 2 - 200, 350))
        self.screen.blit(self.submit_text, (screen_width / 2 - self.submit_text.get_size()[0] / 2, 450))

        username_input_surface = self.font2.render(self.username_input, True, (255, 255, 255))
        password_input_surface = self.font2.render("*" * len(self.password_input), True, (255, 255, 255))

        self.screen.blit(username_input_surface, (screen_width / 2, 250))
        self.screen.blit(password_input_surface, (screen_width / 2, 350))
        self.draw_error_message(self.error_message)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.create_selection_menu()
                        running = False
                    if event.key == pygame.K_RETURN:
                        if self.focus == "username":
                            self.focus = "password"
                        elif self.focus == "password":
                            result = register_user(self.username_input, self.password_input)
                            if result:
                                self.create_menu()
                                running = False
                            else:
                                self.error_message = "Username already exists"

                    if event.key == pygame.K_BACKSPACE:
                        if self.focus == "username":
                            self.username_input = self.username_input[:-1]
                        elif self.focus == "password":
                            self.password_input = self.password_input[:-1]

                    if event.key == pygame.K_TAB:
                        if self.focus == "username":
                            self.focus = "password"
                        elif self.focus == "password":
                            self.focus = "username"

                    if event.unicode.isalnum():
                        if self.focus == "username":
                            self.username_input += event.unicode
                        elif self.focus == "password":
                            self.password_input += event.unicode

            self.draw()
            pygame.display.update()
            pygame.time.Clock().tick(60)


class Login:
    def __init__(self, screen, title, create_menu_with_user_id, create_registration, create_selection_menu):
        self.screen = screen
        self.title = title
        self.create_menu_with_user_id = create_menu_with_user_id
        self.create_registration = create_registration
        self.create_selection_menu = create_selection_menu
        self.error_message = ""
        self.font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
        self.font2 = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 30)
        self.title_text = self.font.render(self.title, True, (0, 255, 255))
        self.username_text = self.font2.render("Username:", True, (255, 255, 255))
        self.password_text = self.font2.render("Password:", True, (255, 255, 255))
        self.submit_text = self.font2.render("Submit", True, (255, 255, 255))
        self.background = pygame.image.load('sprites/menu.jpg')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        self.username_input = ""
        self.password_input = ""
        self.focus = "username"

    def draw_error_message(self, message):
        error_message_surface = self.font2.render(message, True, (255, 0, 0))
        self.screen.blit(error_message_surface, (screen_width / 2 - error_message_surface.get_size()[0] / 2, 550))


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_text, (screen_width / 2 - self.title_text.get_size()[0] / 2, 100))
        self.screen.blit(self.username_text, (screen_width / 2 - 200, 250))
        self.screen.blit(self.password_text, (screen_width / 2 - 200, 350))
        self.screen.blit(self.submit_text, (screen_width / 2 - self.submit_text.get_size()[0] / 2, 450))

        username_input_surface = self.font2.render(self.username_input, True, (255, 255, 255))
        password_input_surface = self.font2.render("*" * len(self.password_input), True, (255, 255, 255))

        self.screen.blit(username_input_surface, (screen_width / 2, 250))
        self.screen.blit(password_input_surface, (screen_width / 2, 350))
        self.draw_error_message(self.error_message)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.create_selection_menu()
                        running = False

                    if event.key == pygame.K_RETURN:
                        authenticated, user_id = login_user(self.username_input, self.password_input)

                        if authenticated:
                            self.create_menu_with_user_id(user_id)
                            return
                        else:
                            self.error_message = "Incorrect login credentials. Please try again."
                            self.username_input = ""
                            self.password_input = ""
                            self.selected = 0

                    if event.key == pygame.K_BACKSPACE:
                        if self.focus == "username":
                            self.username_input = self.username_input[:-1]
                        elif self.focus == "password":
                            self.password_input = self.password_input[:-1]

                    if event.key == pygame.K_TAB:
                        if self.focus == "username":
                            self.focus = "password"
                        elif self.focus == "password":
                            self.focus = "username"

                    if event.unicode.isalnum():
                        if self.focus == "username":
                            self.username_input += event.unicode
                        elif self.focus == "password":
                            self.password_input += event.unicode

            self.draw()
            pygame.display.update()
            pygame.time.Clock().tick