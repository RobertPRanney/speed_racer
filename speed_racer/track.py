"""
File: track.py
Descr: Holds the information needed for a pygame track
Usuage: Import
Notes:
"""

# IMPORT STATMENTS
import os
from statistics import median

import pygame

from . import constants
from . import colors

MODULE_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-1])

class Track:
    def __init__(self, screen_size, name):
        self.track_name = name
        self.img = pygame.transform.scale(pygame.image.load(f'{MODULE_DIR}/imgs/tracks/{self.track_name}/track_outline.png'), screen_size)
        self.img_display = pygame.transform.scale(pygame.image.load(f'{MODULE_DIR}/imgs/tracks/{self.track_name}/track_fill.png'), screen_size)
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self._find_finish()


    def collided(self, some_object):
        offset_x = some_object.rect[0] - self.rect[0]
        offset_y = some_object.rect[1] - self.rect[1]
        overlap = self.mask.overlap(some_object.mask, (offset_x, offset_y))
        return overlap


    def draw(self, win):
        win.blit(self.img_display, constants.TOP_LEFT)


    def _find_finish(self):
        img_width, img_height = self.img_display.get_size()
        finish_points = []
        for i in range(img_width):
            for j in range(img_height):
                if self.img_display.get_at((i, j))[:3] == colors.FINISH_RED:
                    finish_points.append((i, j))
        x_coords = [x[0] for x in finish_points]
        y_coords = [x[1] for x in finish_points]

        finish_x = median(x_coords)
        y_top = min(y_coords)
        y_bottom = max(y_coords)
        length = y_bottom - y_top

        self.car_start_point = (finish_x + 50, y_top + length / 2)
        self.finish_surf = pygame.Surface((10, length))
        self.finish_rect = self.finish_surf.get_rect(midtop=(finish_x, y_top))
        self.finish_mask = pygame.mask.from_surface(self.finish_surf)
