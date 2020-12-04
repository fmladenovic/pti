from random import randint, uniform

import json


CARDS = [ 
    '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', '12♥', '13♥', '14♥',
    '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', '12♦', '13♦', '14♦',
    '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', '12♣', '13♣', '14♣',
    '1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', '12♠', '13♠', '14♠'
]

LAMBDA = 0.1

PLAYERS_VICTORY = +1
DEALERS_VICTORY = -1
TIE = CONTINUE = 0

HIT = 'hit'
HOLD = 'hold'
EMPTY = 'empty'

ACTIONS = [HIT, HOLD]



# def hit(self):
#     card_value = get_card_by_value()
#     self.player_sum, self.useable_ace = sum_and_useable_ace(self.player_sum, self.useable_ace, card_value)

class State:
    def __init__(self):
        self.player_sum = 0
        self.useable_ace = 0
        self.dealer_sum = 0





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

    def update_q(self, s, a, r, l  = LAMBDA):
        key = self._convert_to_key(s, a)

        old_q = self.q(s, a)
        new_q = old_q + l * ( r - old_q)
        self.sa_q[key] = new_q


    def _convert_to_key(self, s, a):
        s_str = [str(part) for part in s]
        return '[({}, {}, {}), {}]'.format(s_str[0], s_str[1], s_str[2], a)

    def save_qs(self):
        with open('data.json', 'w') as fp:
            json.dump(self.sa_q, fp)



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
    while dealer_sum <= 17:
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

    return state_action_pairs[i][0][0]


def game(iterations):
    game_memory = GameMemory()
    my_final_reverd = 0
    for _ in range(iterations):
        game_state_actions, reverd = game_round(game_memory)
        my_final_reverd += reverd
        for game_state_action in game_state_actions:
            if(game_state_action[1] != EMPTY):
                game_memory.update_q(game_state_action[0], game_state_action[1], reverd)
    
    print('\nEND', str(my_final_reverd))
    game_memory.save_qs()


if __name__ == "__main__":
    game(1000000)
















def hit():
    return CARDS[ randint(0, len(CARDS)-1)]






def calculate_sum(cards):
    
    card_values = [get_value(card) for card in cards]

    if 1 not in card_values:
        return sum(card_values), False # sum, usefull ace
    else:
        card_values_sum = sum(card_values) - 1
        if card_values_sum + 11 > 21:
            return card_values_sum + 1, False # sum, usefull ace
        else:
            return card_values_sum + 11, True # sum, usefull ace


