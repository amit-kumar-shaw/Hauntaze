import pygame
from os import listdir

def import_frames(folder, scale):
    """load all images in a particular folder"""

    frames = []
    for image in sorted(listdir(folder)):
        full_path = folder + '/' + image
        frame = pygame.image.load(full_path).convert_alpha()
        if scale != 1:
            frame = pygame.transform.rotozoom(frame, 0, scale)
        frames.append(frame)

    return frames
