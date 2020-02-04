"""
File: human_game.py
Descr: play a racecar game with human as the controller
Usage: python human_game.py
Notes:
"""
# IMPORT STATMENTS
import time
import pickle
import argparse

import pygame

from speed_racer import constants
from speed_racer.game import Game


def setup_args():
    parser = argparse.ArgumentParser(description='Car Game with human control')
    parser.add_argument('track_name', nargs='?', default='hard', choices=['easy', 'hard'])
    parser.add_argument('--record', nargs=1, default=None)
    return parser.parse_args()


def play_game():
    args = setup_args()

    game = Game(args.track_name, drawing=True, displaying=True)
    actions = []
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
        actions.append(action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.end_game()

    if args.record:
        with open(f'action_recordings/{args.record[0]}.pkl', 'wb') as out_pickle:
            pickle.dump(actions, out_pickle)



if __name__ == '__main__':
    play_game()
    time.sleep(2)
