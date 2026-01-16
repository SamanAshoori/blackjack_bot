import gymnasium as gym
import numpy as np
from collections import defaultdict
import random

# Phase 1: We use the standard env to test our Agent structure
# Later, we will replace this with 'CustomOneShoeBlackjackEnv'
env = gym.make('Blackjack-v1', natural=False, sab=False)

class BlackjackAgent:
    def __init__(self, learning_rate=0.01, gamma=0.95, epsilon=1.0):
        self.q_table = defaultdict(float)
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon # Exploration rate

    def get_action(self, state):
        """
        Input: state (tuple)
        Output: action (0 for Stick, 1 for Hit)
        Logic: Epsilon-Greedy. Random chance to explore, otherwise pick best Q-value.

        """
        random.uniform(0,1)
        if random.uniform(0,1) < self.epsilon:
            return env.action_space.sample()
        else:
            return np.argmax([self.q_table[(state, a)] for a in range(env.action_space.n)])


    def update(self, episode_memory):
        """
        Input: A list of (state, action, reward) tuples from the WHOLE game.
        Logic: Calculate Return (G) backwards, then update Q-table.
        """
        G = 0
        for state, action, reward in reversed(episode_memory):
            G = reward + self.gamma * G
            self.q_table[(state, action)] += self.lr * (G - self.q_table[(state, action)])  
    
    def decay_epsilon(self):
        self.epsilon = max(0.01,self.epsilon * 0.9995)

def train(episodes=1000):
    agent = BlackjackAgent()
    
    for i in range(episodes):
        episode_memory = []
        state, info = env.reset()
        done = False
        
        while not done:
            action = agent.get_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            episode_memory.append((state, action, reward))
            
            state = next_state
        agent.update(episode_memory)
        agent.decay_epsilon()



if __name__ == "__main__":
    train()