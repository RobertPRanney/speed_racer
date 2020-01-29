"""
File: human_game.py
Descr: play a racecar game with human as the controller
Usage: python human_game.py
Notes:
"""
# IMPORT STATMENTS
import time

import pygame

import constants
from game import Game


def play_game():
    game = Game(drawing=True, displaying=True)
    while not game.is_finished:
        # Handle actions
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = constants.ACTION_FORWARD
        elif keys[pygame.K_DOWN]:
            action = constants.ACTION_BACKWARD
        elif keys[pygame.K_RIGHT]:
            action = constants.ACTION_RIGHT
        elif keys[pygame.K_LEFT]:
            action = constants.ACTION_LEFT
        else:
            action = constants.ACTION_NOTHING
        game.step(action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.end_game()


if __name__ == '__main__':
    play_game()
    time.sleep(2)
