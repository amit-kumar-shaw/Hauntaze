import pygame
from os import walk

def import_frames(folder, scale):
    frames = []

    for _, __, images in walk(folder):
        for image in images:
            full_path = folder + '/' + image
            frame = pygame.image.load(full_path).convert_alpha()
            frame = pygame.transform.rotozoom(frame, 0, scale)
            frames.append(frame)

    return frames