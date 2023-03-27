import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from menu import Menu
from pause import Pause
from death_screen import DeathScreen
from highscore import Highscores
from authentication import Registration, Login
from database import create_database, get_user_highscore_and_level, update_user_highscore_and_level

create_database()

class Game:
	def __init__(self):

		# game attributes
		self.max_level = 0
		self.max_health = 100
		self.current_health = 100
		self.coins = 0
		self.menu = None
		self.current_level = 0

		# user interface
		self.ui = UI(screen)

		# authentication
		self.auth_font = pygame.font.Font('sprites/ui/ARCADEPI.ttf', 50)
		self.auth_options = ["Login", "Register"]
		self.auth_selected = 0
		self.auth_option_colors = [('white' if i != self.auth_selected else 'gold') for i in range(len(self.auth_options))]
		self.auth_background = pygame.image.load('sprites/menu.jpg')
		self.auth_background = pygame.transform.scale(self.auth_background, (screen_width, screen_height))
		self.auth_sound = pygame.mixer.Sound('sounds/change_selection.wav')

	def draw_auth_menu(self):
		screen.blit(self.auth_background, (0, 0))
		for i, option in enumerate(self.auth_options):
			option_text = self.auth_font.render(option, True, pygame.Color(self.auth_option_colors[i]))
			option_text_pos = (screen_width / 2 - option_text.get_size()[0] / 2, 320 + i * 70)
			screen.blit(option_text, option_text_pos)
		pygame.display.update()

	def create_selection_menu(self):
		self.status = 'auth'
		self.run()

	def create_auth_menu(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						self.auth_selected -= 1
						self.auth_sound.play()
					if event.key == pygame.K_s:
						self.auth_selected += 1
						self.auth_sound.play()
					if event.key == pygame.K_RETURN:
						if self.auth_selected == 0:  # Login
							self.create_login()
							return
						elif self.auth_selected == 1:  # Register
							self.create_registration()
							return

			self.auth_selected %= len(self.auth_options)
			for i in range(len(self.auth_options)):
				self.auth_option_colors[i] = 'white' if i != self.auth_selected else 'gold'
			self.draw_auth_menu()
			pygame.time.Clock().tick(60)

	def set_menu_status(self):
		self.status = 'menu'

	def resume_game(self):
		if self.status == 'level':
			self.level.resume_level()
		elif self.status == 'overworld':
			self.overworld.resume_overworld()

	def create_pause_menu(self, screen):
		self.pause = Pause(screen, self, self, self.resume_game, self.return_to_menu, self.quit_game)
		self.status = 'pause'

	def create_level(self,current_level):
		self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.reset_coins, self.change_health, self, self, self.user_id)
		self.status = 'level'

	def create_registration(self):
		registration = Registration(screen, "Register", self.create_login, self.create_selection_menu)
		registration.run()

	def create_login(self):
		login = Login(screen, "Login", lambda user_id: self.create_menu(user_id), self.create_registration, self.create_selection_menu)
		login.run()

	def create_overworld(self, current_level, new_max_level, user_id):
		self.user_id = user_id
		highscore, max_level = get_user_highscore_and_level(self.user_id)
		if new_max_level > self.max_level:
			self.max_level = new_max_level
			self.max_level = max_level
			self.highscore = highscore
		self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self, self.user_id)
		self.status = 'overworld'

	def show_highscores(self):
		highscore, _ = get_user_highscore_and_level(self.user_id)
		highscores_screen = Highscores(screen, highscore, self.show_menu)
		highscores_screen.run()
		self.status = 'highscores'

	def create_menu(self, user_id=None):
		self.user_id = user_id
		self.menu = Menu(screen, "Menu", ['Start', 'Options', 'Quit'], self.create_overworld, [self.start_game, self.show_options, self.quit_game], self.user_id)
		self.status = 'menu'
		self.menu.run()

	def start_game(self):
		self.create_overworld(0, 0, self.user_id)

	def show_options(self):
		print('Options')

	def quit_game(self):
		pygame.quit()
		sys.exit()


	def reset_coins(self):
		self.coins = 0

	def change_coins(self, amount):
		self.coins += amount

	def change_health(self, amount):
		self.current_health += amount

	def move_to_next_level(self):
		update_user_highscore_and_level(self.user_id, self.coins, self.max_level)
		self.current_level += 1
		self.create_level(self.current_level)

	def check_game_over(self):
		if self.current_health <= 0:
			update_user_highscore_and_level(self.user_id, self.coins, self.max_level)
			death_screen = DeathScreen(screen, self.restart_level, self.return_to_menu)
			death_screen.run()

	def restart_level(self):
		self.current_health = 100
		self.coins = 0
		self.create_level(self.level.current_level)

	def return_to_menu(self):
		self.current_health = 100
		self.coins = 0
		self.status = 'menu'

	def handle_key_events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if self.status == 'level':
					self.level.pause_menu.run()
				elif self.status == 'overworld':
					self.create_menu()


	def run(self):
		for event in pygame.event.get():
			self.handle_key_events(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		if not hasattr(self, 'status') or self.status == 'auth':
			self.create_auth_menu()
		elif self.status == 'overworld':
			self.overworld.run()
		elif self.status == 'menu':
			self.create_menu()
		elif self.status == 'paused':
			pause_menu = Pause(screen, self)
			pause_menu.run()
		elif self.status == 'highscores':
			self.show_highscores()
		elif self.status == 'level':
			self.level.update()
			self.ui.show_health(self.current_health, self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()
		else:
			print("Warning: Invalid status. Resetting to authentication menu.")
			self.create_auth_menu()
			self.status = 'auth'




pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2DRunner')
clock = pygame.time.Clock()


game = Game()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_key_events(event)

    screen.fill(('silver'))
    game.run()

    pygame.display.update()
    clock.tick(60)
