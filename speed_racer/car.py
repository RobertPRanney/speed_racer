"""
File: car.py
Descr: Holds the information needed for a pygame car
Usage: Import Only
Notes:
"""

# IMPORT STATMENTS
import os
import math

import pygame

from . import colors
from . import constants


# CONSTANT DECLARATIONS
CAR_SCALE_DIMS = (150, 75)

CAR_NAME = "s_car"
SENSOR_NAMES = ['up', 'forward', 'down']

MODULE_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-1])
CAR_IMG = pygame.transform.scale(pygame.image.load(f"{MODULE_DIR}/imgs/{CAR_NAME}_none.png"), CAR_SCALE_DIMS)



class Sensor:
    sensor_max = constants.SENSOR_MAX

    def  __init__(self, name):
        self.name = name
        self.img = pygame.transform.scale(pygame.image.load(f"{MODULE_DIR}/imgs/{CAR_NAME}_sensor_{self.name}.png"), CAR_SCALE_DIMS)
        self.orig_img = pygame.transform.scale(pygame.image.load(f"{MODULE_DIR}/imgs/{CAR_NAME}_sensor_{self.name}.png"), CAR_SCALE_DIMS)
        self.overlap = None
        self.dist = self.sensor_max
        self.active = 0


    def rotate(self, angle):
        self.img = pygame.transform.rotate(self.orig_img, angle)
        self.mask = pygame.mask.from_surface(self.img, 50)


    def draw(self, win, topleft):
        win.blit(self.img, topleft)
        if self.overlap:
            pygame.draw.circle(win, colors.SENSOR_YELLOW, self.overlap, 5)


    def update(self, track, rect):
        offset_x = rect[0] - track.rect[0]
        offset_y = rect[1] - track.rect[1]
        self.overlap = track.mask.overlap(self.mask, (offset_x, offset_y))
        if self.overlap:
            self.dist = math.sqrt((rect.centerx - self.overlap[0])**2 + (rect.centery - self.overlap[1])**2)
            self.active = 1
        else:
            self.dist = self.sensor_max
            self.active = 0


class Car:
    max_vel = constants.MAX_VEL
    min_vel = constants.MIN_VEL
    turn_rate = constants.TURN_RATE
    forward_accel = constants.FORWARD_ACCEL
    backward_accel = constants.BACKWARD_ACCEL

    def __init__(self, starting_x, starting_y):
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.center_x = starting_x
        self.center_y = starting_y
        self.angle = 0
        self.vel = 0

        self.img = CAR_IMG
        self.orig_img = CAR_IMG
        self.rect = self.img.get_rect(center=(self.center_x, self.center_y))
        self.mask = pygame.mask.from_surface(self.img, 50)

        self.sensors = [Sensor(sensor_name) for sensor_name in SENSOR_NAMES]

        self.in_finish_area = False
        self.score = 0


    def crash(self):
        self.center_x = self.starting_x
        self.center_y = self.starting_y
        self.angle = 0
        self.vel = 0
        self.in_finish_area = False


    def reset(self):
        self.center_x = self.starting_x
        self.center_y = self.starting_y
        self.angle = 0
        self.vel = 0
        self.in_finish_area = False
        self.score = 0


    def _turn(self, action):
        if action == constants.ACTION_LEFT:
            self.angle += self.turn_rate
        elif action == constants.ACTION_RIGHT:
            self.angle -= self.turn_rate
        self.angle = round(self.angle % 360, 1)


    def _accel(self, action):
        if action == constants.ACTION_FORWARD:
            self.vel += self.forward_accel
        elif action == constants.ACTION_BACKWARD:
            self.vel -= self.backward_accel
        self.vel = max(min(self.max_vel, self.vel), self.min_vel)


    def move(self, action):
        # Handle Action
        if action in [constants.ACTION_LEFT, constants.ACTION_RIGHT]:
            self._turn(action)
        elif action in [constants.ACTION_BACKWARD, constants.ACTION_FORWARD]:
            self._accel(action)
        elif action == constants.ACTION_NOTHING:
            pass

        # Handle Displacement
        rads = math.radians(self.angle)
        displ_x = (self.vel * math.cos(rads))
        displ_y = (self.vel * math.sin(rads))
        self.center_x += displ_x
        self.center_y -= displ_y
        self.rect.center = (self.center_x, self.center_y)

        # Handle Rotation
        self.img = pygame.transform.rotate(self.orig_img, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.img, 50)
        for sensor in self.sensors:
            sensor.rotate(self.angle)


    def draw(self, win):
        win.blit(self.img, self.rect.topleft)
        for sensor in self.sensors:
            sensor.draw(win, self.rect.topleft)


    def update_sensors(self, track):
        for sensor in self.sensors:
            sensor.update(track, self.rect)


    def current_state(self):
        state = [self.center_x,
                 self.center_y,
                 self.vel,
                 self.angle
                ]
        for sensor in self.sensors:
            state.append(sensor.dist)
            state.append(sensor.active)
        return state


    def __str__(self):
        empty = "X: {:0.2f}    Y: {:0.2f}\nVel: {:0.2f}\nAngle: {:0.2f}\nUp: {:0.2f}:{:}\nForward: {:0.2f}:{:}\nDown: {:0.2f}:{:}"
        return empty.format(*self.current_state())
