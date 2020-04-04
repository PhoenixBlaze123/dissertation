import gym
from gym_game.envs.gameMap import Map

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = gym.make('game-v0')
game_map = Map(game_type)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
for _ in range(10000):
    action, _states = model.predict(obs)
    reward = env.step(action, game_map, "solo_play")
    env.render()
env.close()