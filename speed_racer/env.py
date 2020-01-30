"""
File: speed_racer.py
Descr:
Usuage:
Notes:
"""


# IMPORT STATMENTS
import numpy as np
import tensorflow as tf
from tf_agents.specs import array_spec
from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts

from .game import Game
from . import constants


tf.compat.v1.enable_v2_behavior()


class SpeedRacer(py_environment.PyEnvironment):
    def __init__(self):
        self.game = Game(drawing=False, displaying=False)
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int64, minimum=0, maximum=4, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(10,), dtype=np.float32, minimum=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            maximum=[constants.TRACK_AREA_WIDTH, constants.TRACK_AREA_HEIGHT, constants.MAX_VEL, 360,
                     constants.SENSOR_MAX, 1, constants.SENSOR_MAX, 1, constants.SENSOR_MAX, 1],
            name='observation')
        self._state = np.array(self.game.car.current_state())
        self._episode_ended = False
        self._last_time_step = None


    def action_spec(self):
        return self._action_spec


    def observation_spec(self):
        return self._observation_spec


    def _reset(self):
        self.game.restart_game()
        self._state = np.array(self.game.car.current_state())
        self._episode_ended = False
        self._last_time_step = ts.restart(np.array(self._state, dtype=np.float32))
        return self._last_time_step


    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        reward = self.game.step(action)
        self._episode_ended = self.game.is_finished
        self._state = self.game.car.current_state()

        if self._episode_ended:
            self._last_time_step = ts.termination(
                np.array(self._state, dtype=np.float32),
                reward)
        else:
            self._last_time_step = ts.transition(
                np.array(self._state, dtype=np.float32),
                reward=reward,
                discount=1.0)
        return self._last_time_step

    def get_info(self):
        return self._last_time_step


    def enable_rendering(self):
        self.game.enabled_drawing()


    def enable_watching(self):
        self.game.enabled_displaying()


    def render(self, mode='rgb_array'):
        return self.game.render()
