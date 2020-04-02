import gym
import gym_game

from gym_game.envs.gameMap import Map
game_type = "solo_play"
env = gym.make('game-v0')
game_map = Map(game_type)

env.reset()
for _ in range(10000):
    env.render(mode= 'human')
    action = env.action_space.sample()
    #observation, reward, done, info = env.step(action)
    reward = env.step(action, game_map, game_type)
env.close()