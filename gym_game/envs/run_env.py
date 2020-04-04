import gym
from gym_game.envs.gameEnv import GameEnv

env = gym.make('game-v0')

env.reset()

for _ in range(10000):
    action = env.action_space.sample()
    #observation, reward, done, info = env.step(action)
    reward = env.step(action)
    env.render(mode='human')

env.close()