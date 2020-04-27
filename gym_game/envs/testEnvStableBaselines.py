import gym
import numpy as np
from gym_game.envs.gameEnv import GameEnv
from stable_baselines import PPO2, A2C
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.env_checker import check_env

env = gym.make('game-v0')
def train_agent():
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=20000)
    model.save("agentname")

def load_agent():
    model = A2C.load("a2c_agent.zip")
    obs = env.reset()
    for _ in range(10000):
        action, _states = model.predict(obs)
        obs, done, reward, info = env.step(action)
        if done:
            obs = env.reset()
        env.render()
    env.close()

#train_agent()
load_agent()