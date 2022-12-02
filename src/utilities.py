import pygame
from os import walk, listdir

def import_frames(folder, scale):
    frames = []

    # for _, __, images in walk(folder, topdown=True):
    #     for image in images:
    #         full_path = folder + '/' + image
    #         print(full_path)
    #         frame = pygame.image.load(full_path).convert_alpha()
    #         frame = pygame.transform.rotozoom(frame, 0, scale)
    #         frames.append(frame)
    for image in sorted(listdir(folder)):
        full_path = folder + '/' + image
        frame = pygame.image.load(full_path).convert_alpha()
        frame = pygame.transform.rotozoom(frame, 0, scale)
        frames.append(frame)

    return frames