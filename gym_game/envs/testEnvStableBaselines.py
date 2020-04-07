import gym
from gym_game.envs.gameEnv import GameEnv
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv


env = gym.make('game-v0')

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
for _ in range(10000):
    action, _states = model.predict(obs)
    obs, done, reward, info = env.step(action)
    if done:
        obs = env.reset()
    env.render()
env.close()