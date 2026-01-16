# Reinforcement Learning for Non-Stationary Blackjack

## Abstract

This project implements a Reinforcement Learning (RL) agent capable of mastering the game of Blackjack. Unlike standard implementations that utilise an infinite deck (drawing with replacement), this project focuses on the complexity of a "One Shoe" (finite deck) environment. This constraint introduces non-stationarity to the state transition probabilities, requiring the agent to develop policies that account for card depletion (i.e., card counting) to maximise expected returns against the dealer.

## Project Scope & Objectives

The primary objective is to demonstrate the efficacy of Temporal Difference (TD) learning and Monte Carlo methods in stochastic environments. The project is divided into two distinct phases of complexity:

1.  **Phase I: Infinite Deck (Baseline):** implementing an agent using the standard `gymnasium` environment to master Basic Strategy.
2.  **Phase II: Finite Deck (Advanced):** Implementing a custom environment wrapper that simulates card depletion. This alters the problem from a Markov Decision Process (MDP) based solely on visible cards to a Partially Observable MDP (POMDP) where the history of played cards dictates future probabilities.

## Theoretical Background

### Markov Decision Process (MDP)
The standard game of Blackjack is modelled as an MDP where the state $S$ is defined as a tuple:
$$S = (C_{sum}, D_{card}, A_{usable})$$
Where:
* $C_{sum}$: The current sum of the player's hand (4-21).
* $D_{card}$: The dealer's visible face-up card.
* $A_{usable}$: A boolean indicating the presence of a usable Ace (soft hand).

### The Non-Stationary Challenge
In a finite deck scenario, the probability $P(s' | s, a)$ changes as cards are removed from the shoe. To solve this without exploring the entire history space (which would be computationally intractable), the state space is augmented to include a "Running Count" or "True Count" heuristic, allowing the agent to adjust its betting and playing strategy based on the richness of the remaining deck.

## Implementation Details

### Tech Stack
* **Language:** Python 3.10+
* **Libraries:** `gymnasium`, `numpy`, `matplotlib` (for policy visualisation)

### Architecture
* `BlackjackAgent`: A class encapsulating the Q-Table and learning logic (supports both Q-Learning and Monte Carlo update rules).
* `OneShoeEnv`: A custom environment inheriting from `gymnasium.Env` that manages the deck state, reshuffling only when the "cut card" is reached.
* `PolicyEvaluator`: Utilities for visualising the learned state-value function $V(s)$ and comparing the learned policy against mathematically optimal Basic Strategy.

## Usage

### Installation
Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

### Training the Agent
To train the agent on the baseline environment (Infinite Deck):

```bash
python main.py --mode train --episodes 100000 --algorithm q_learning
```

To run the advanced finite deck simulation:

```bash
python main.py --mode train --episodes 500000 --env custom --shoe_size 1
```

## References

1.  Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press. (Specifically Chapter 5: Monte Carlo Methods).
2.  Thorp, E. O. (1966). *Beat the Dealer: A Winning Strategy for the Game of Twenty-One*. Random House.