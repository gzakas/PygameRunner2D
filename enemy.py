import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'sprites/enemy/minotaur1/walking', 1.4)
        self.rect.y += size - self.image.get_size()[(1)] + 4
        self.speed = randint(1, 3)

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def move(self):
        self.rect.x += self.speed

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()