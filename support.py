import pygame
from os import walk

def import_folder(path, scale_factor=1):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            scaled_surf = pygame.transform.scale(image_surf, (int(image_surf.get_width() * scale_factor), int(image_surf.get_height() * scale_factor)))
            surface_list.append(scaled_surf)

    return surface_list

