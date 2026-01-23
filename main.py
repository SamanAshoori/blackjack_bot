
from blackjack import Blackjack
from single_game_loop import SingleGameLoop

env = Blackjack()
SingleGameLoop(state = env.get_state(), verbose= False)