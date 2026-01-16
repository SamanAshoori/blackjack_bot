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
        self.epsilon = epsilon 
        self.epsilon_decay = 0.99995 # Decay factor
        self.min_epsilon = 0.01 # Minimum epsilon value


    def get_action(self, state):
        if random.uniform(0,1) < self.epsilon:
            return env.action_space.sample()
        else:
            qs = [self.q_table[(state, a)] for a in range(env.action_space.n)]
            return np.argmax(qs)


    def update(self, episode_memory):
        G = 0
        for state, action, reward in reversed(episode_memory):
            G = reward + self.gamma * G
            
            # Standard MC Update formula
            old_value = self.q_table[(state, action)]
            self.q_table[(state, action)] = old_value + self.lr * (G - old_value)
            
        # Decay epsilon after learning from the episode
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)  
    
    def decay_epsilon(self):
        self.epsilon = max(0.01,self.epsilon * 0.9995)

def train(episodes=100_000): # Needed 100k episodes to see good convergence
    agent = BlackjackAgent()
    
    # Just for tracking our progress
    wins = 0
    losses = 0
    draws = 0
    
    
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
            
            if done and reward > 0:
                wins += 1
            elif done and reward < 0:
                losses += 1
            elif done and reward == 0:
                draws += 1
                

        agent.update(episode_memory)
        
        if (i+1) % 5000 == 0:
            print(f"Episode {i+1}: Epsilon {agent.epsilon:.4f} | Win rate (last 5k): {wins/5000:.2%}")
            wins = 0



if __name__ == "__main__":
    train()