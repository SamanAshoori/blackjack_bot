#Blackack.py
#Outcomes (1 = win , 0 = draw , -1 if lose)
import random
import time
import numpy as np
from datetime import datetime


class Blackjack:
    def __init__(self, state = None, seed = datetime.now().microsecond):
        if state is None:
            self.deck = [i for i in range(52)]
            random.seed(seed)
            random.shuffle(self.deck)

            self.dealer = []
            self.player = []
        else:
            self.set_state(state, seed = seed)
    
    def set_state(self, state, seed = datetime.now().microsecond):
        (dealer , player , deck) = state

        self.dealer = dealer
        self.player = player
        self.deck = deck
        random.seed(seed)
        random.shuffle(self.deck)
    
    def get_state(self):
        return (self.dealer, self.player, self.deck)
    
    def convert_cards(self,card):
        #Convert a card
        value = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'][card%13]
        suit = 'CDHS'[card//13]
        return value + suit

        
    def calc(self,player = True):
        #Calculate the value of the player
        mydeck = self.player if player else self.dealer
        has_ace = False
        value = 0
        for card in mydeck:
            index = card%13
            if index == 0:
                value += 1
                has_ace = True
            else:
                value += min(index,10)
        if has_ace and value <= 11:
            value += 10
        
        if value > 21:
            return -1

        return value


    def draw_player(self):
        #Draw a card for the player
        self.player.append(self.deck.pop(0))
    
    def draw_dealer(self):
        #Draw a card for the dealer
        self.dealer.append(self.deck.pop(0))

    def get_result(self):
        #Get the result of the game
        dealer_value = self.calc(player = False)
        player_value = self.calc()
        return np.sign(player_value - dealer_value)
        

    def display_game(self, move = '', elapsed_time = 1):
        time.sleep(elapsed_time)
        print("------ ------ ------ ----- ----- ------ ------ ------ ------ ------")
        print(f"Remaining cards: {len(self.deck)}")
        if move != '':
            print(move)
        print(f"Dealer: {list(map(self.convert_cards,self.dealer))}, Value: {self.calc(player = False)}")
        print(f"Player: {list(map(self.convert_cards,self.player))}, Value: {self.calc()}")



def Player(env):
    #In MC - player does random action
    if env.calc() == 21:
        return 'Stick'
    return np.random.choice(['Hit','Stick'])

def Dealer(env):
    #Dealer will keep drawing untill he busts or beats player
    if env.get_result() > 0 and env.calc(player = False) != -1:
        return 'Hit'
    else:
        return 'Stick'


def SingleGameLoop(verbose = True, state = None):
    #Play a single game
    
    bj = Blackjack(state)
    bj.draw_player()
    bj.draw_dealer()
    bj.draw_dealer()

    bj.display_game()


    while bj.calc(player= True) != -1:
        action = Player(bj)
        if action == 'Hit':
            bj.draw_player()
            if verbose:
                bj.display_game(move = 'Player Hits')
        else:
            if verbose:
                bj.display_game(move = 'Player Sticks')
            break


    #dealer will draw second card
    bj.draw_dealer()
    if verbose:
        bj.display_game(move='Dealer shows second card')

    while bj.calc(player= False) != -1:
        action = Dealer(bj)
        if action == 'Hit':
            bj.draw_dealer()
            if verbose:
                bj.display_game(move = 'Dealer Hits')
        else:
            if verbose:
                bj.display_game(move = 'Dealer Sticks')
            break


    result = bj.get_result()
    bj.display_game()
    if result == 0:
        print("Draw")
    elif result == 1:
        print("Player Wins")
    else:
        print("Dealer Wins")


env = Blackjack()



SingleGameLoop(state = env.get_state(), verbose= False)
