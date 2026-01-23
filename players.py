from numpy import np
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