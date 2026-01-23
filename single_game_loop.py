from blackjack import Blackjack
from players import Player, Dealer
import time

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