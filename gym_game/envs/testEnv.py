import gym
from gym_game.envs.gameEnv import GameEnv

env = gym.make('game-v0')

obs = env.reset()
r = 0
for _ in range(10000):
    action = env.action_space.sample()
    obs, done, reward, info = env.step(action)
    r += reward
    if done:
        obs = env.reset()
    env.render(mode='human')
#print("Ovservation: ", obs.shape)
env.close()