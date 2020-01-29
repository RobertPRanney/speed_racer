"""
File: game.py
Descr: Holds all elements needed for a game including a car, track and scoring
       logic. Can be used as human playable or trainable.
Usuage: Import Only
Notes:
"""

# IMPORT STATMENTS
import pygame

import colors
import constants
from car import Car
from track import Track

pygame.init()


class Game:
    def __init__(self, drawing=False, displaying=False):
        self.screen_size = (constants.TRACK_AREA_WIDTH, constants.TRACK_AREA_HEIGHT)
        self.track = Track(self.screen_size)
        self.car = Car(*self.track.car_start_point)
        self.frame = 0
        self.last_reward = 0
        self.drawing = drawing
        self.displaying = displaying
        self.is_finished = False

        if self.drawing:
            self.screen = pygame.display.set_mode(self.screen_size)
            self.font = pygame.font.SysFont("comicsans", 30)

        if self.displaying:
            self.clock = pygame.time.Clock()


    def enabled_drawing(self):
        if not self.drawing:
            self.drawing = True
            self.screen = pygame.display.set_mode(self.screen_size)
            self.font = pygame.font.SysFont("comicsans", 30)


    def enabled_displaying(self):
        self.enabled_drawing()
        if not self.enabled_displaying:
            self.enabled_displaying = True
            self.clock = pygame.time.Clock()


    def step(self, action):
        self.car.move(action)
        self.car.update_sensors(self.track)
        self.last_reward = self._get_reward()
        self.car.score += self.last_reward
        self.frame += 1

        if self.drawing:
            self.screen.fill(colors.WHITE)
            self.track.draw(self.screen)
            self.car.draw(self.screen)
            self._draw_info()
        if self.displaying:
            pygame.display.flip()
            self.clock.tick(constants.FRAME_RATE)

        if self.frame == constants.GAME_LENGTH:
            self.is_finished = True

        return self.last_reward


    def _get_reward(self):
        if self.track.collided(self.car):
            self.car.crash()
            reward = -50
        elif self.track.finish_rect.collidepoint(self.car.center_x, self.car.center_y):
            if not self.car.in_finish_area:
                self.car.in_finish_area = True
                if self.car.center_x < self.track.finish_rect.centerx:
                    reward = 100
                else:
                    reward = -100
            else:
                reward = -0.01
        else:
            self.car.in_finish_area = False
            reward = -0.01
        return reward


    def _draw_info(self):
        y_loc = constants.TRACK_AREA_HEIGHT - 180
        for chunk in self.car.__str__().split('\n'):
            text = self.font.render(chunk, 1, colors.BLACK)
            self.screen.blit(text, (10, y_loc))
            y_loc += 20

        text = self.font.render(f"Score: {self.car.score:0.0f}", 1, colors.BLACK)
        self.screen.blit(text, (10, y_loc))
        y_loc += 20

        if self.displaying:
            fps = self.clock.get_fps()
            text = self.font.render(f"FPS: {fps:0.0f}", 1, colors.BLACK)
            self.screen.blit(text, (10, y_loc))


    def end_game(self):
        self.is_finished = True


    def restart_game(self):
        self.car.reset()


    def render(self):
        if self.drawing:
            return pygame.surfarray.array3d(self.screen).swapaxes(0, 1)
        raise Exception("Drawing must be enabled")
