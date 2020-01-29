"""
File: trainer.py
Descr:
Usuage:
Notes:
"""


# IMPORT STATMENTS
import tensorflow as tf
from tf_agents.utils import common
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import tf_py_environment

import utils
from speed_racer import SpeedRacer

tf.compat.v1.enable_v2_behavior()




if __name__ == '__main__':
    num_iterations = 20000 # @param {type:"integer"}

    initial_collect_steps = 1000  # @param {type:"integer"}
    collect_steps_per_iteration = 1  # @param {type:"integer"}
    replay_buffer_max_length = 100000  # @param {type:"integer"}

    batch_size = 64  # @param {type:"integer"}
    learning_rate = 1e-3  # @param {type:"number"}
    log_interval = 200  # @param {type:"integer"}

    num_eval_episodes = 10  # @param {type:"integer"}
    eval_interval = 1000  # @param {type:"integer"}
    video_filename = 'test_render.mp4'
    env = SpeedRacer()
    tf_env = tf_py_environment.TFPyEnvironment(env)
    fc_layer_params = (100,)

    q_net = q_network.QNetwork(
        tf_env.observation_spec(),
        tf_env.action_spec(),
        fc_layer_params=fc_layer_params)


    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

    train_step_counter = tf.Variable(0)

    agent = dqn_agent.DqnAgent(
        tf_env.time_step_spec(),
        tf_env.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)

    agent.initialize()
    utils.make_video('videos/test_render.mp4', 60, agent.policy, tf_env, env)
