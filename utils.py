"""
File: utils.py
Descr: Good place to store random functions
Usuage: Import Only
Notes:
"""
# IMPORT STATEMENTS
import imageio

def make_video(file_path, fps, policy, tf_env, env):
    env.enable_rendering()
    with imageio.get_writer(file_path, fps=fps) as video:
        time_step = tf_env.reset()
        while not time_step.is_last():
            action = policy.action(time_step)
            time_step = tf_env.step(action)
            video.append_data(env.render())
