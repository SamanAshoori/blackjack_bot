#Blackack.py
#Outcomes (1 = win , 0 = draw , -1 if lose)
import random

class Blackjack:
    def __init__(self, seed = 25):
        self.deck = [i for i in range(52)]
        random.seed(seed)
        random.shuffle(self.deck)

        self.dealer = []
        self.player = []
    
    def set_state(self, state):
        (dealer , player , deck , seed) = state
        self.seed = seed
        self.dealer = dealer
        self.player = player
        self.deck = deck
        random.seed(seed)
        random.shuffle(self.deck)
    
    def get_state(self):
        return self.dealer, self.player, self.deck, self.seed
    

    def draw_player(self):
        #Draw a card for the player
        self.player.append(self.deck.pop(0))
    
    def draw_dealer(self):
        #Draw a card for the dealer
        self.dealer.append(self.deck.pop(0))

    def display_game(self):
        print(f"Remaining cards: {len(self.deck)}")
        print(f"Dealer: {self.dealer}")
        print(f"Player: {self.player}")



bj = Blackjack(seed = 20)
print(bj.display_game())