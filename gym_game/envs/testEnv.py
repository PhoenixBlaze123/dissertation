import gym
import numpy as np
from gym_game.envs.gameEnv import GameEnv

env = gym.make('game-v0')

obs = env.reset()

for _ in range(100000):
    action = env.action_space.sample()
    obs, done, reward, info = env.step(action)
    if done:
        obs = env.reset()
    env.render(mode='human')
env.close()


