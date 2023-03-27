import pygame
from tiles import Tile, StaticTile, Coin
from settings import tile_size, screen_width, screen_height
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics
from enemy import Enemy
from decoration import Sky, Water, Clouds
from game_data import levels
from pause import Pause

class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, reset_coins, change_health, game, game_instance, user_id):

        # level setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        self.current_x_pos = 0
        self.game_instance = game_instance
        self.game = game_instance
        self.user_id = user_id
        self.pause_menu = Pause(surface, self, game_instance, self.resume_level, self.return_to_overworld, self.return_to_overworld)
        self.level_complete_sound = pygame.mixer.Sound('sounds/level_complete.wav')

        # overworld conn
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # user interface
        self.change_coins = change_coins
        self.reset_coins = reset_coins

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        # kill particles
        self.kill_sprites = pygame.sprite.Group()

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        self.coin_sound = pygame.mixer.Sound('sounds/pickupCoin.wav')

        # bg_trees
        tree_layout = import_csv_layout(level_data['bg trees'])
        self.tree_sprites = self.create_tile_group(tree_layout, 'bg trees')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        self.enemy_hurt_sound = pygame.mixer.Sound('sounds/hitHurt.wav')
        self.enemy_kill_sound = pygame.mixer.Sound('sounds/enemyKill.wav')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # background
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 25, level_width)
        self.clouds = Clouds(300, level_width, 25)

    def resume_level(self):
        self.game_instance.set_menu_status()

    def return_to_overworld(self):
        self.create_overworld(self.current_level, self.new_max_level, self.user_id)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('sprites/terrain/Tileset.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('sprites/decoration/grass_tiles.png')
                        tile_index = row_index
                        tile_surface = grass_tile_list[tile_index]
                        tile_position = pygame.math.Vector2(x, y + 1)
                        sprite = StaticTile(tile_size, tile_position.x, tile_position.y, tile_surface)

                    if type == 'crates':
                        crate_tile_list = import_cut_graphics('sprites/decoration/boxes_tiles.png')
                        tile_surface = crate_tile_list[int(value)]
                        tile_position = pygame.math.Vector2(x, y + 2)
                        sprite = StaticTile(tile_size, tile_position.x, tile_position.y, tile_surface)

                    if type == 'coins':
                        if value == '0':
                            sprite = Coin(tile_size, x, y, 'sprites/coins/gold', 3)
                        if value == '1':
                            sprite = Coin(tile_size, x, y, 'sprites/coins/silver', 1)

                    if type == 'bg trees':
                        tree_tile_list = import_cut_graphics('sprites/decoration/willows_tileset.png')
                        tile_surface = tree_tile_list[int(value)]
                        tile_position = pygame.math.Vector2(x, y + 1)
                        sprite = StaticTile(tile_size, tile_position.x, tile_position.y, tile_surface)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if value == '1':
                    hat_surface = pygame.image.load('sprites/character/finish.png').convert_alpha()
                    sprite = StaticTile(tile_size,x , y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(0, 9)
        else:
            position += pygame.math.Vector2(0, -9)

        jump_particle_sprite = ParticleEffect(position, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0, 7)
            else:
                offset = pygame.math.Vector2(0, 7)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
            self.current_x_pos -= 1
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0 and self.current_x_pos < 510:
            self.world_shift = -5
            player.speed = 0     
            self.current_x_pos += 1
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right + 1.5
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left - 1.5
                    player.direction.x = 0
                    player.on_right = True
                    self.current_x = sprite.rect.right 

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top 
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom 
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.game_instance.current_health = 0
            self.game_instance.check_game_over()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.game.move_to_next_level()
            self.level_complete_sound.play()

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.coin_sound.play()

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -10
                    kill_sprite = ParticleEffect(enemy.rect.center, 'kill')
                    self.kill_sprites.add(kill_sprite)
                    enemy.kill()
                    self.enemy_kill_sound.play()
                else:
                    self.player.sprite.get_damage()
                    self.enemy_hurt_sound.play()

    def update(self):

        # background
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
            
        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

         # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # trees
        self.tree_sprites.update(self.world_shift)
        self.tree_sprites.draw(self.display_surface)

        # enemies
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.kill_sprites.update(self.world_shift)
        self.kill_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
            
        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
            
        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface, self.world_shift)