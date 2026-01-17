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
    
    def set_state(self, dealer, player,deck, seed = 25):
        self.dealer = dealer
        self.player = player
        self.deck = deck
        random.seed(seed)
        random.shuffle(self.deck)

    def draw_player(self):
        #Draw a card for the player
        self.player.append(self.deck.pop(0))
    
    def draw_dealer(self):
        #Draw a card for the dealer
        self.dealer.append(self.deck.pop(0))

bj = Blackjack()
print(bj.deck)
bj.draw_player()
print(bj.player)
bj.draw_dealer()
print(bj.dealer)