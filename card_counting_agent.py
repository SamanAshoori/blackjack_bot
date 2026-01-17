import numpy as np
from collections import defaultdict
import random
import pickle
from one_shoe_blackjack import BlackjackEnv

class CardCountingAgent:
    #changed learning rate to be more aggresive
    def __init__(self, learning_rate=0.1, gamma=0.95, epsilon=1.0):
        self.q_table = defaultdict(float)
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        # Slower decay because our state space is larger (buckets)
        self.epsilon_decay = 0.99999 
        self.min_epsilon = 0.01

    def get_true_count_bucket(self, true_count):
        """
        Discretize the true count into buckets to reduce state space.
        Buckets:
        0: Very Negative (<= -2)
        1: Negative (-2 < TC < -1)
        2: Neutral (-1 <= TC < 1)
        3: Positive (1 <= TC < 2)
        4: Very Positive (>= 2)
        """
        if true_count <= -2:
            return 0
        elif true_count < -1:
            return 1
        elif true_count < 1:
            return 2 # Neutral
        elif true_count < 2:
            return 3
        else:
            return 4

    def get_state(self, obs, info):
        """
        Construct the state tuple from observation and info.
        We ignore the 'encoded_count' in obs and use the more accurate
        'true_count' from info to create our buckets.
        
        State: (player_sum, dealer_card, usable_ace, tc_bucket)
        """
        player_sum, dealer_card, usable_ace, _ = obs
        tc_bucket = self.get_true_count_bucket(info['true_count'])
        return (player_sum, dealer_card, usable_ace, tc_bucket)

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1])  # 0: Stick, 1: Hit
        
        # Get Q-values for both actions
        q_stick = self.q_table[(state, 0)]
        q_hit = self.q_table[(state, 1)]
        
        # Break ties (default to Stick if equal, or random? Stick is safer)
        return 0 if q_stick >= q_hit else 1

    def update(self, episode_memory):
        G = 0
        for state, action, reward in reversed(episode_memory):
            G = reward + self.gamma * G
            old_q = self.q_table[(state, action)]
            self.q_table[(state, action)] = old_q + self.lr * (G - old_q)
        
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def get_bet_size(self, true_count):
        confidence = 1.0 - (self.epsilon - self.min_epsilon) / (1.0 - self.min_epsilon)
        """
        Determine bet size based on the True Count.
        Standard Hi-Lo betting spread (1-10 units).
        """
        if true_count >= 4:
            base_bet = 10 # Max bet
        elif true_count >= 3:
            base_bet = 8
        elif true_count >= 2:
            base_bet = 4
        elif true_count >= 1:
            base_bet = 2
        else:
            base_bet = 1

        return max(1, int(base_bet * (0.2 + 0.8 * confidence)))

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = defaultdict(float, pickle.load(f))

def train(episodes=5_000_000):
    env = BlackjackEnv(natural=False, sab=False)
    agent = CardCountingAgent()
    
    wins = 0
    losses = 0
    draws = 0
    bankroll = 0.0
    
    # Track performance by count bucket
    performance_by_count = defaultdict(lambda: {'wins': 0, 'total': 0, 'profit': 0})
    
    # Track the true count from the previous episode to decide the bet
    # for the upcoming episode (before cards are dealt).
    last_true_count = 0.0

    for i in range(episodes):
        # 1. Place Bet based on previous count
        bet = agent.get_bet_size(last_true_count)
        
        # 2. Start Episode
        obs, info = env.reset()
        
        # Shuffle Detection:
        # If the deck has > 45 cards, a shuffle likely happened in reset().
        # If so, our high bet was based on a stale count. In a real casino,
        # we would see the shuffle and lower our bet.
        start_of_hand_tc = last_true_count
        bet = agent.get_bet_size(info['true_count'])

        if info['cards_remaining'] > 45:
            bet = 1
            start_of_hand_tc = 0.0
        else:
            start_of_hand_tc = info['true_count']
        
        state = agent.get_state(obs, info)
        done = False
        episode_memory = []
        
        while not done:
            action = agent.get_action(state)
            next_obs, reward, terminated, truncated, next_info = env.step(action)
            done = terminated or truncated
            
            # Scale reward by bet size. This teaches the agent that 
            # mistakes during high-bet hands are more costly.
            scaled_reward = reward * bet
            
            episode_memory.append((state, action, scaled_reward))
            
            state = agent.get_state(next_obs, next_info)
            info = next_info
            
        agent.update(episode_memory)
        
        # Update stats (using raw reward for win/loss, scaled for bankroll)
        if reward > 0:
            wins += 1
            bankroll += bet * reward # reward is 1 or 1.5
        elif reward < 0:
            losses += 1
            bankroll += bet * reward # reward is -1
        else:
            draws += 1
            
        # Update performance stats by bucket
        tc_bucket = agent.get_true_count_bucket(start_of_hand_tc)
        performance_by_count[tc_bucket]['total'] += 1
        performance_by_count[tc_bucket]['profit'] += bet * reward
        if reward > 0:
            performance_by_count[tc_bucket]['wins'] += 1
            
        # Update true count for next hand's betting decision
        last_true_count = info['true_count']

        if (i + 1) % 50_000 == 0:
            print(f"Episode {i + 1}: Epsilon {agent.epsilon:.4f} | "
                  f"Win Rate: {wins / 50_000:.2%} | "
                  f"Bankroll: {bankroll:.1f}")
            wins = losses = draws = 0

    print("\nPerformance by True Count Bucket:")
    for bucket in sorted(performance_by_count.keys()):
        stats = performance_by_count[bucket]
        win_rate = stats['wins'] / stats['total'] if stats['total'] > 0 else 0
        avg_profit = stats['profit'] / stats['total'] if stats['total'] > 0 else 0
        print(f"Bucket {bucket}: WR={win_rate:.2%} | Avg Profit={avg_profit:.3f} | Hands={stats['total']}")

    agent.save("card_counting_model.pkl")
    print("Model saved to card_counting_model.pkl")
    print("Training completed.")

if __name__ == "__main__":
    train()