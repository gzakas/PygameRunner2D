import pygame 
from game_data import levels
from support import import_folder
from decoration import Sky
from menu import Menu
from pause import Pause

class Node(pygame.sprite.Sprite):
	def __init__(self,pos,status,icon_speed, path):
		super().__init__()
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		if status == 'available':
			self.status = 'available'
		else:
			self.status = 'locked'
		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)

	def animate(self):
		self.frame_index += 0.25
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self):
		if self.status == 'available':
			self.animate()
		else:
			tinted_surface = self.image.copy()
			tinted_surface.fill('black', None, pygame.BLEND_RGBA_MULT)
			self.image.blit(tinted_surface, (0, 0))

class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.Surface((20,20))
		self.image = pygame.image.load('sprites/overworld/character.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos


class Overworld:
	def __init__(self,start_level,max_level,surface,create_level, game, user_id):

		# setup 
		self.display_surface = surface 
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level
		self.game = game
		self.user_id = user_id

		# movement logic
		self.moving = False
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 8

		# sprites 
		self.setup_nodes()
		self.setup_icon()
		self.sky = Sky(8)

		# time
		self.start_time = pygame.time.get_ticks()
		self.allow_input = False
		self.timer_length = 500

		# menu
		self.menu = Menu(surface, "Paused", ['Resume', 'Quit'], self.resume_overworld, [self.resume_overworld, self.return_to_menu], self.user_id)
		self.overworld_pause = Pause(surface, self, self.game, self.resume_overworld, self.return_to_menu, self.game.quit_game)

	def resume_overworld(self):
		self.overworld_pause.update_paused_state(False)

	def return_to_menu(self):
		self.game.create_menu()
		self.overworld_pause.update_paused_state(False)

	def setup_nodes(self):
		self.nodes = pygame.sprite.Group()

		for index, node_data in enumerate(levels.values()):
			if index <= self.max_level:
				node_sprite = Node(node_data['node_pos'],'available',self.speed, node_data['node_sprites'])
			else:
				node_sprite = Node(node_data['node_pos'],'locked',self.speed, node_data['node_sprites'])
			self.nodes.add(node_sprite)

	def draw_paths(self):
		if self.max_level > 0:
			points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
			pygame.draw.lines(self.display_surface,'#a04f45',False,points,6)

	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.moving and self.allow_input:
			if keys[pygame.K_d] and self.current_level < self.max_level:
				self.move_direction = self.get_movement_data('next')
				self.current_level += 1
				self.moving = True
			elif keys[pygame.K_a] and self.current_level > 0:
				self.move_direction = self.get_movement_data('previous')
				self.current_level -= 1
				self.moving = True
			elif keys[pygame.K_RETURN]:
				self.create_level(self.current_level)
			elif keys[pygame.K_ESCAPE]:
				self.overworld_pause.is_paused = True
				self.overworld_pause.run()

	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		
		if target == 'next': 
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

		return (end - start).normalize()

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)

	def input_timer(self):
		if not self.allow_input:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.timer_length:
				self.allow_input = True

	def run(self):
		self.input_timer()
		result = self.input()
		if result == 'menu':
			return 'menu'
		self.update_icon_pos()
		self.icon.update()
		self.nodes.update()
		self.sky.draw(self.display_surface)
		self.draw_paths()
		self.nodes.draw(self.display_surface)
		self.icon.draw(self.display_surface)
		if self.overworld_pause.is_paused:
			self.overworld_pause.run()

