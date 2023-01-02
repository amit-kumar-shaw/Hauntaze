import pygame
from os import walk, listdir

def import_frames(folder, scale):
    frames = []

    for image in sorted(listdir(folder)):
        full_path = folder + '/' + image
        frame = pygame.image.load(full_path).convert_alpha()
        if scale != 1:
            frame = pygame.transform.rotozoom(frame, 0, scale)
        frames.append(frame)

    return frames