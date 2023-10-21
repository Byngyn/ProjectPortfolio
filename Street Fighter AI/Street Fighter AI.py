#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip freeze


# In[2]:


#!pip install gym==0.21.0


# In[3]:


import gym # used to create observation space
import retro # used to run Street Fighter
import time # used to slow down Street Fighter


# In[5]:


# create an environment with Street Fighter
env = retro.make(game='StreetFighterIISpecialChampionEdition-Genesis')


# In[6]:


# sample of the observation space
env.observation_space.sample()


# In[7]:


# sample of available actions
env.action_space


# In[8]:


# reset game
#obs = env.reset()
# set flag to false
#done = False
#for game in range(1):
#    while not done:
#        if done:
#            obs = env.reset()
#        env.render()
#        obs, reward, done, info = env.step(env.action_space.sample())
#        print(reward)


# In[9]:


# close any exisiting environment
env.close()


# In[10]:


#show game info
#info


# ## Preprocessing

# In[11]:


#!pip install opencv-python
#!pip install matplotlib


# In[12]:


# import environment base class for a wrapper
from gym import Env
from gym import spaces
# import space shapes for env
from gym.spaces import MultiBinary
from gym.spaces import Box
# import numpy to calculate frame delta
import numpy as np
# import opencv for grayscaling
import cv2
#import matplotlib for plotting image
from matplotlib import pyplot as plt


# In[13]:


# Create custom environment 
class StreetFighter(Env): 
    def __init__(self):
        super().__init__()
        # Specify action space and observation space 
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)
        self.action_space = gym.spaces.MultiBinary(12)
        # Startup and instance of the game 
        self.game = retro.make(game='StreetFighterIISpecialChampionEdition-Genesis', use_restricted_actions=retro.Actions.FILTERED)
    
    def reset(self):
        # Return the first frame 
        obs = self.game.reset()
        obs = self.preprocess(obs) 
        self.previous_frame = obs 
        
        # Create a attribute to hold the score delta 
        self.score = 0 
        return obs
    
    def preprocess(self, observation): 
        # Grayscaling to reduce data size
        gray = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
        # Resize to reduce data size
        resize = cv2.resize(gray, (84,84), interpolation=cv2.INTER_CUBIC)
        # Add the channels value
        channels = np.reshape(resize, (84,84,1))
        return channels 
    
    def step(self, action): 
        # Take a step 
        obs, reward, done, info = self.game.step(action)
        obs = self.preprocess(obs) 
        
        # Frame delta 
        frame_delta = obs - self.previous_frame
        self.previous_frame = obs 
        
        # Reshape the reward function
        reward = info['score'] - self.score 
        self.score = info['score'] 
        
        return frame_delta, reward, done, info
    
    def render(self, *args, **kwargs):
        self.game.render()
        
    def close(self):
        self.game.close()


# In[14]:


#plt.imshow(cv2.cvtColor(resize, cv2.COLOR_BGR2RGB))


# In[15]:


#gray = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
#resize = cv2.resize(gray, (84,84), interpolation=cv2.INTER_CUBIC)


# In[16]:


#env.close()


# In[17]:


#env = StreetFighter()


# In[18]:


#reset game
#obs = env.reset()
# set flag to false
#done = False
#for game in range(1):
#    while not done:
#        if done:
#            obs = env.reset()
#        env.render()
#        obs, reward, done, info = env.step(env.action_space.sample())
#        if reward > 0:
#            print(reward)


# In[19]:


#obs = env.reset()


# In[20]:


#obs, reward, done, info = env.step(env.action_space.sample())


# In[21]:


#plt.imshow(cv2.cvtColor(obs,cv2.COLOR_BGR2RGB))


# In[22]:


env.close()


# ## Hyperparameter Tuning

# In[23]:


#!pip install --user torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113


# In[24]:


#!pip install --user stable-baselines3[extra] optuna
#!pip install ipywidgets


# In[25]:


# Importing the optimzation frame - HPO
import optuna
# PPO algo for RL
from stable_baselines3 import PPO
# Bring in the eval policy method for metric calculation
from stable_baselines3.common.evaluation import evaluate_policy
# Import the sb3 monitor for logging 
from stable_baselines3.common.monitor import Monitor
# Import the vec wrappers to vectorize and frame stack
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
# Import os to deal with filepaths
import os


# In[26]:


# create folders to hold logs
LOG_DIR = './logs/'
OPT_DIR = './opt/'


# In[27]:


# Function to return test hyperparameters - define the object function
def optimize_ppo(trial): 
    return {
        'n_steps':trial.suggest_int('n_steps', 2048, 8192),
        'gamma':trial.suggest_loguniform('gamma', 0.8, 0.9999),
        'learning_rate':trial.suggest_loguniform('learning_rate', 1e-5, 1e-4),
        'clip_range':trial.suggest_uniform('clip_range', 0.1, 0.4),
        'gae_lambda':trial.suggest_uniform('gae_lambda', 0.8, 0.99)
    }


# In[28]:


# create a savepath to hold the best model from the trial
SAVE_PATH = os.path.join(OPT_DIR, 'trial_{}_best_model'.format(1))


# In[29]:


# Run a training loop and return mean reward 
def optimize_agent(trial):
    try:
        model_params = optimize_ppo(trial) 
        # Create environment 
        env = StreetFighter()
        
        env = Monitor(env, LOG_DIR)
        env = DummyVecEnv([lambda: env])
        env = VecFrameStack(env, 4, channels_order='last')

        # Create algo 
        model = PPO('CnnPolicy', env, tensorboard_log = LOG_DIR, verbose=0, **model_params)
        model.learn(total_timesteps=100000)

        # Evaluate model 
        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=5)
        env.close()

        SAVE_PATH = os.path.join(OPT_DIR, 'trial_{}_best_model'.format(trial.number))
        model.save(SAVE_PATH)

        return mean_reward

    except Exception as e:
        print(e)
        return -1000


# In[30]:


#close any existing environments
env.close()

# Creating the experiment 
study = optuna.create_study(direction='maximize')
#study.optimize(optimize_agent, n_trials=10, n_jobs=1)
study.optimize(optimize_agent, n_trials=100, n_jobs=1)


# In[31]:


# observe the best parameters
study.best_params


# In[32]:


# observe the best trial
study.best_trial


# In[33]:


# use the information above to load the best performing model
model = PPO.load(os.path.join(OPT_DIR, 'trial_85_best_model.zip'))


# In[34]:


# Import base callback 
from stable_baselines3.common.callbacks import BaseCallback

class TrainAndLoggingCallback(BaseCallback):
    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)
            
    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True


# In[35]:


CHECKPOINT_DIR = './train/'


# In[36]:


callback = TrainAndLoggingCallback(check_freq=10000, save_path=CHECKPOINT_DIR)


# In[37]:


# Create environment 
env = StreetFighter()
env = Monitor(env, LOG_DIR)
env = DummyVecEnv([lambda: env])
env = VecFrameStack(env, 4, channels_order='last')


# In[38]:


model_params = study.best_params


# In[39]:


model_params['n_steps'] = 7488  # set n_steps to 7488 or a factor of 64


# In[40]:


# model_params['learning_rate'] = 5e-7
model_params


# In[41]:


model = PPO('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1, **model_params)


# In[42]:


# Reload previous weights from HPO
model.load(os.path.join(OPT_DIR, 'trial_0_best_model.zip'))


# In[43]:


# Kick off training 
model.learn(total_timesteps=5000000, callback=callback)
# model.learn(total_timestep=5000000) 


# In[68]:


model = PPO.load('./train/best_model_5000000.zip')


# In[66]:


env.close()


# In[69]:


mean_reward, _ = evaluate_policy(model, env, render=True, n_eval_episodes=5)


# In[61]:


mean_reward


# In[54]:


obs = env.reset()


# In[62]:


obs.shape


# In[70]:


env.step(model.predict(obs)[0])


# In[71]:


env.close()
# Reset game to starting state
obs = env.reset()
# Set flag to flase
done = False
for game in range(1):
    print('Score:')
    while not done: 
        if done: 
            print('Game Finished')
            obs = env.reset()
        env.render()
        action = model.predict(obs)[0]
        obs, reward, done, info = env.step(action)
        time.sleep(0.01)
        print(reward)


# In[ ]:




