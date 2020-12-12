import sys
from random import randint, uniform
import matplotlib.pyplot as plt
import json


CARDS = [ 
    '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', '12♥', '13♥', '14♥',
    '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', '12♦', '13♦', '14♦',
    '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', '12♣', '13♣', '14♣',
    '1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', '12♠', '13♠', '14♠'
]

LAMBDA = 0.1
GAMA = 0.5

PLAYERS_VICTORY = +1
DEALERS_VICTORY = -1
TIE = CONTINUE = 0

HIT = 'hit'
HOLD = 'hold'
EMPTY = 'empty'

EMPTY_STATE = [None, None, None]

ACTIONS = [HIT, HOLD]


MONTE_KARLO = 'monte_karlo'
SARSA = 'sarsa'
Q_LEARNING = 'q_learning'

ALGORITHAMS = [MONTE_KARLO, SARSA, Q_LEARNING ]

#               s       a    q
# sa_q = {
#     ([11, False, 5], HIT): 0
# }
class GameMemory:

    def __init__(self):
        self.sa_q = {}

    def q(self, s, a):
        key = self._convert_to_key(s, a)
        return  self.sa_q.get( key ) if key in self.sa_q.keys() else 0

    def update_q_monte_karlo(self, s, a, r, l  = LAMBDA):
        key = self._convert_to_key(s, a)

        old_q = self.q(s, a)
        new_q = old_q + l * ( r - old_q)
        self.sa_q[key] = new_q


    def update_q_sarsa(self, s, a, s_prim, a_prim, r, l  = LAMBDA, g = GAMA):
        key = self._convert_to_key(s, a)
        next_q = 0

        if key in self.sa_q.keys(): # Terminal value will be 0
            next_q = self.q(s_prim, a_prim)

        old_q = self.q(s, a)
        new_q = old_q + l * ( r + g * next_q - old_q)
        self.sa_q[key] = new_q

    def update_q_q_learning(self, s, a, s_prim, r, l  = LAMBDA, g = GAMA):
        key = self._convert_to_key(s, a)
        next_q = 0

        if key in self.sa_q.keys():
            max_a = greedy(self, s_prim)
            next_q = self.q(s_prim, max_a)

        old_q = self.q(s, a)
        new_q = old_q + l * ( r + g * next_q - old_q)
        self.sa_q[key] = new_q


    def _convert_to_key(self, s, a):
        s_str = [str(part) for part in s]
        return '[({}, {}, {}), {}]'.format(s_str[0], s_str[1], s_str[2], a)

    def save_qs(self, name):
        with open(name+'_data.json', 'w') as fp:
            json.dump(self.sa_q, fp)

    def read_qs(self, name):
        with open(name+'_data.json', 'r') as fp:
            self.sa_q = json.load(fp)



##################################### POLICIES ##################################################
def greedy(game_memory, state):
    q_hit = game_memory.q(state, HIT)
    q_hold = game_memory.q(state, HOLD)
    return HIT if q_hit >= q_hold else HOLD


def e_greedy(game_memory, state, e):
    rand = uniform(0, 1)
    if rand < e:
        return ACTIONS[randint(0, len(ACTIONS)-1)]
    else:
        return greedy(game_memory, state)

def learning( game_memory, state, e ):
    if(state[0] > 17):
        return HOLD
    else:
        return e_greedy(game_memory, state, e)

# TODO: SOFTMAX


######################################## UTILITY ##################################################
def plot_values( values ):
    plt.plot(range(1, len(values) + 1), values)
    plt.ylabel('reverds')
    plt.xlabel('parties')
    plt.show()


def get_value( card ):
    if len(card) == 3:
        return 10
    return int(card[0])


def get_card_by_value():
    return get_value(CARDS[ randint(0, len(CARDS)-1)])


def sum_and_useable_ace(old_sum, useable_ace, new_value):
    new_sum = old_sum + new_value

    if new_sum > 21 and useable_ace:
        new_sum -= 10
        return new_sum, False
    
    if new_sum <= 11 and new_value == 1:
        new_sum += 10
        return new_sum, True
    
    return new_sum, useable_ace



########################################## GAME LOGIC ##################################################
def begin_round():
    player_cards = []
    dealer_cards = []

    for i in range(3):
        card = CARDS[ randint(0, len(CARDS)-1)]
        if i % 2 == 0:
            player_cards.append(card)
        else:
            dealer_cards.append(card)

    return generate_state(player_cards, dealer_cards)

def generate_state(player_cards, dealer_cards):
    player_values = [get_value(card) for card in player_cards]
    
    value = get_value(dealer_cards[0])
    dealer_value = value if value != 1 else 11   # dealer will have only 1 card on start (we cant see another)
    
    useable_ace = 1 in player_values and sum(player_values) + 10 <= 21
    player_value = sum(player_values) if not useable_ace else sum(player_values) + 10
    return [player_value, useable_ace, dealer_value]


def game_round(game_memory):
    # [ [state, action], ....] = [ [[11, False, 5], 'hit'], [[18, True, 5], 'hold']]
    init_state = begin_round()
    state_action_pairs = [[init_state, EMPTY]]

    player_sum = player_turn(game_memory, state_action_pairs)

    if player_sum == 21:
        return state_action_pairs, PLAYERS_VICTORY
    elif player_sum > 21:
        return state_action_pairs, DEALERS_VICTORY

    dealer_sum = dealer_turn(state_action_pairs[0][0][2])

    if player_sum < dealer_sum:
        return state_action_pairs, DEALERS_VICTORY
    elif player_sum > dealer_sum:
        return state_action_pairs, PLAYERS_VICTORY
    else:
        return state_action_pairs, TIE

def dealer_turn( dealer_sum ):
    while dealer_sum < 17:
        value = get_card_by_value()
        dealer_sum += value if value != 1 else 11
    return dealer_sum

def player_turn( game_memory, state_action_pairs):
    action = ''
    i = 0

    while action != HOLD and state_action_pairs[i][0][0] < 21:
        action = learning(game_memory, state_action_pairs[i][0], 0.3) if len(game_memory.sa_q.keys()) > 360 else e_greedy(game_memory, state_action_pairs[i][0], 0.2)
        state_action_pairs[i][1] = action

        if action == HIT:
            old_state = state_action_pairs[i][0]
            new_state = [*sum_and_useable_ace(old_state[0], old_state[1], get_card_by_value()), old_state[2]]
            state_action_pairs.append([new_state, EMPTY])
            i+=1

    if state_action_pairs[-1][1] == EMPTY: # EMPTY is our 'exit' state that we won't count
        return state_action_pairs.pop()[0][0]
    return state_action_pairs[-1][0][0]


def game_learn(iterations):
    for aloritham in ALGORITHAMS:
        game_memory = GameMemory()

        for _ in range(iterations):
            game_state_actions, reverd = game_round(game_memory)

            if aloritham == MONTE_KARLO:
                for game_state_action in game_state_actions:
                    game_memory.update_q_monte_karlo(game_state_action[0], game_state_action[1], reverd)

            elif aloritham == SARSA:
                for (i, game_state_action) in enumerate(game_state_actions):
                    if i+1 < len(game_state_actions):
                        game_next_state_action = game_state_actions[i+1]
                        game_memory.update_q_sarsa(game_state_action[0], game_state_action[1], game_next_state_action[0], game_next_state_action[1], 0)
                    else:
                        game_memory.update_q_sarsa(game_state_action[0], game_state_action[1], EMPTY_STATE, EMPTY, reverd)

            elif aloritham == Q_LEARNING:
                for (i, game_state_action) in enumerate(game_state_actions):
                    if i+1 < len(game_state_actions):
                        game_next_state_action = game_state_actions[i+1]
                        game_memory.update_q_q_learning(game_state_action[0], game_state_action[1], game_next_state_action[0], 0)
                    else:
                        game_memory.update_q_q_learning(game_state_action[0], game_state_action[1], EMPTY_STATE, reverd)

                   

        if(iterations != 0):
            print('END LEARNING ' + aloritham)
            game_memory.save_qs(aloritham)


def game_play(play_iterations):
    game_memory = GameMemory()
    for aloritham in ALGORITHAMS:

        game_memory.read_qs(aloritham)
        win_tie_def = [0, 0, 0]

        for _ in range(play_iterations):

            _, reverd = game_round(game_memory)

            if(reverd == TIE):
                win_tie_def[1] += 1
            elif(reverd == PLAYERS_VICTORY):
                win_tie_def[0] += 1
            else:
                win_tie_def[2] += 1
                
        print('\n {:^11} result: '.format(aloritham), win_tie_def)


if __name__ == "__main__":
    game_learn(int(sys.argv[1]))
    game_play(int(sys.argv[2]))







