"""
File: utils.py
Descr: Good place to store random functions
Usuage: Import Only
Notes:
"""
# IMPORT STATEMENTS
import base64
import imageio
import IPython
from collections import deque

import numpy as np


# FUNCTION DEFINITIONS
def make_video(file_path, fps, policy, tf_env, env):
    env.enable_rendering()
    with imageio.get_writer(file_path, fps=fps) as video:
        time_step = tf_env.reset()
        while not time_step.is_last():
            action = policy.action(time_step)
            time_step = tf_env.step(action)
            video.append_data(env.render())


def embed_video(file_path):
    video = open(file_path,'rb').read()
    b64 = base64.b64encode(video)
    tag = '''
    <video width="640" height="480" controls>
    <source src="data:video/mp4;base64,{0}" type="video/mp4">
    Your browser does not support the video tag.
    </video>'''.format(b64.decode())
    return IPython.display.HTML(tag)


def smooth_list(alist, window=10):
    runner = deque(maxlen=window)
    smoothed = []
    for val in alist:
        runner.append(val)
        smoothed.append(np.mean(runner))
    return smoothed


def compute_avg_return(env, policy, num_episodes=5):
    total_return = 0.0
    for _ in range(num_episodes):
        time_step = env.reset()
        episode_return = 0.0
        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = env.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return
    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]
