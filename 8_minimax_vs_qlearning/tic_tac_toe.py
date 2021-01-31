import time
import json
import random
import math
from numpy.random import randint, uniform

from copy import deepcopy

WIDTH = 3
HEIGHT = 3

EMPTY = ''
X = 'x'
O = 'o'
LINE = '---------------------------------------------------------------\n'

# Konstanta COMPUTER i njena vrednost +1 označavaju potez kompjutera i u minimax algoritmu
#  se njome iskazuje pozitivan ishod za kompjuter - kompjuter je igrač koji maksimizuje vrednost
COMPUTER = 1 

# Knstanta TIE označava nerešeno
TIE = 0

# Konstanta PLAYER i njena vrednost -1 označavaju potez igrača i u minimax algoritmu
#  se njome iskazuje negativan ishod za kompjuter - 'player' је igrač koji minimizuje vrednost
PLAYER = -1

# Konstanta NONE označava da je igra još u toku
NOONE = 'noone'

EPSILON = 0.3
LAMBDA = 0.1
GAMA = 0.9


EMPTY_STATE = [ ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
EMPTY_ACTION = ('-', '-')

#################################### VIEW #########################################
def print_table( table ):
    break_row = '  -+-+-\n'
    row0 = '  0 1 2\n\n'
    row1 = '0 {:^1}|{:^1}|{:^1}\n'.format(table[0][0], table[0][1], table[0][2])
    row2 = '1 {:^1}|{:^1}|{:^1}\n'.format(table[1][0], table[1][1], table[1][2])
    row3 = '2 {:^1}|{:^1}|{:^1}\n'.format(table[2][0], table[2][1], table[2][2])
    view =  row0 + row1 + break_row + row2 + break_row + row3
    print(view)

def game_datails(table, winner):
    print_table( table )

    if winner == PLAYER:
        print('Player is winner!')
    elif winner == COMPUTER:
        print('Computer is winner!')
    elif winner == TIE:
        print('Game is unresolved!')




############################## KEYBOARD INPUT ###################################
def get_field( table ):
    while( True ):   
        x = int_input('x')
        y = int_input('y')
        print('\n')
        if( check_field(x) and check_field(y) ):
            print( 'Values should be in interval [0,2].\n' )
        elif( check_available_field( table, (x, y) ) ):
            print( 'Field is already taken, choose another one.\n' )
        else:
            return (x, y)

def int_input( value_name ):
    while True:
        value_str = input('{}: '.format(value_name))
        try:
            return int(value_str)
        except Exception:
            print('{} must be integer!'.format(value_name))

def check_field( value ):
    return 0 > value or value > 2 

def check_available_field( table, field ):
    return table[field[0]][field[1]] != EMPTY




############################## END GAME ###################################
# Proverava se da li se desila pobeda u poslednjem potezu i onaj koji je poslednji
#  odigrao potez se proglašava pobednikom
def announce_victory(table, last_move):
    if is_tie(table):
        return TIE
    if is_victory(table):
        return last_move
    return NOONE

# Ako je nerešeno sva polja na tabeli više nisu prazni stringovi
def is_tie(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == EMPTY:
                return False
    return True

# Pobeda je ako se tri ista znaka prostiru u nekom od pravaca
def is_victory(table):
    for i in range(3):
        if not table[1][i] == EMPTY and table[0][i] == table[1][i] and table[1][i] == table[2][i]:
            return True
        if not table[i][1] == EMPTY and table[i][0] == table[i][1] and table[i][1] == table[i][2]:
            return True
    main_daig_victory = not table[1][1] == EMPTY and table[0][0] == table[1][1] and table[1][1] == table[2][2]
    other_diag_victory = not table[1][1] == EMPTY and table[0][2] == table[1][1] and table[1][1] == table[2][0]
    return main_daig_victory or other_diag_victory
    



############################## COMPUTER MOVE ###################################
class MinimaxMemory:

    def __init__(self, player_sign = X, computer_sign = O):
        self.computer_sign = computer_sign
        self.player_sign = player_sign
        self.s_a = {}

    def __to_key(self, s):
        return '[[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]]'.format(s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2], s[2][0], s[2][1], s[2][2])


    def minimax(self, table, depth, is_maximizing):
        last_move = PLAYER if is_maximizing else COMPUTER
        result = announce_victory(table, last_move)
        if not result == NOONE:
            return result/depth

        if is_maximizing:
            bestScore = -math.inf
            for i in range(len(table)):
                for j in range(len(table[i])):
                    if(table[i][j] == EMPTY):
                        table[i][j] = self.computer_sign
                        score = self.minimax(table, depth + 1, False)
                        table[i][j] = ''
                        bestScore = max(score, bestScore)
            return bestScore

        else: 
            bestScore = math.inf
            for i in range(len(table)):
                for j in range(len(table[i])):
                    if(table[i][j] == EMPTY):
                        table[i][j] = self.player_sign
                        score = self.minimax(table, depth + 1, True)
                        table[i][j] = ''
                        bestScore = min(score, bestScore)
            return bestScore


    def computer_move(self, table ):
        key = self.__to_key(table)
        if key in self.s_a.keys():
            return self.s_a[key]

        field = (0,0)
        bestScore = -math.inf
        for i in range(len(table)):
            for j in range(len(table[i])):
                if(table[i][j] == EMPTY):
                    table[i][j] = self.computer_sign
                    score = self.minimax(table, 1, False)
                    table[i][j] = ''
                    if score > bestScore:
                        bestScore = score
                        field = (i, j) 

        self.s_a[key] = field
        return field

    def save_qs(self):
        with open('minimax.json', 'w') as fp:
            json.dump(self.s_a, fp)

    def read_qs(self):
        with open('minimax.json', 'r') as fp:
            self.s_a = json.load(fp)


############################## Q LEARNING ###################################
class GameMemory:

    def __init__(self, player_sign = X):
        self.player_sign = player_sign
        self.sa_q = {}

        self.party = []

    def __to_key(self, s, a):
        return '([[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]], ({}, {}))'.format(s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2], s[2][0], s[2][1], s[2][2], a[0], a[1])


    def q(self, s, a):
        key = self.__to_key(s,a)
        if key not in self.sa_q.keys(): self.sa_q[key] = 0
        return self.sa_q[key] 


    def update_qs(self, r):
        for i in range( len(self.party) ):
            s = self.party[i][0]
            a = self.party[i][1]
            
            s_prim = EMPTY_STATE
            reverd = r
            if i != len(self.party) - 1:
                reverd = 0
                s_prim = self.party[i+1][0]

            self._update_q(s, a, s_prim, reverd)


    def _update_q(self, s, a, s_prim, r, l  = LAMBDA, g = GAMA):

        if s_prim != EMPTY_STATE:
            max_a = self.greedy(s_prim)
            max_q = self.q(s_prim, max_a)
        else:
            max_q = 0

        old_q = self.q(s, a)
        new_q = old_q + l * ( r + g * max_q - old_q)

        self.sa_q[self.__to_key(s, a)] = new_q
    

    def __generate_available_actions(self, state):
        actions = []
        for (i, row) in enumerate(state):
            for (j, sign) in enumerate(row):
                if sign == EMPTY:
                    actions.append((i, j))
        return actions

    def play_move(self, table):

        action = game_memory.e_greedy( table )
        self.party.append( [deepcopy(table), deepcopy(action)] )

        return action

    def greedy(self, state):
        max_action = (-1, -1)
        max_q = -math.inf
        
        for (i, row) in enumerate(state):
            for (j, sign) in enumerate(row):
                if sign == EMPTY:
                    q = self.q(state, (i,j))
                    if max_q < q:
                        max_q = q
                        max_action = (i, j)
        return max_action

    def e_greedy(self, state, e = EPSILON):
        rand = uniform(0, 1)
        if rand < e:
            actions = self.__generate_available_actions(state)
            return actions[randint(0, len(actions)-1)] if len(actions) != 1 else actions[0]
        else:
            return self.greedy(state)

    def save_qs(self):
        with open('data.json', 'w') as fp:
            json.dump(self.sa_q, fp)

    def read_qs(self):
        with open('data.json', 'r') as fp:
            self.sa_q = json.load(fp)

############################## GAME LOGIC ###################################


def game(game_memory, minimax_memory, parties):

    results = [0, 0, 0]

    for _ in range(parties):
        game_memory.party = []
        table = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]

        first_move = COMPUTER if random.uniform(0, 1) <= 0.5 else PLAYER  # Odabira na slučajan način ko ima prvi potez
        last_move = PLAYER if first_move == COMPUTER else COMPUTER
        winner = NOONE

        if first_move == PLAYER:
            game_memory.player_sign = minimax_memory.player_sign = player_sign = X
            minimax_memory.computer_sign = computer_sign = O
        else:
            game_memory.player_sign = minimax_memory.player_sign = player_sign = O
            minimax_memory.computer_sign = computer_sign = X
        
        # print_table(table)
        while winner == NOONE:
            
            if last_move == COMPUTER:
                last_move = PLAYER
                field = game_memory.play_move(table)
                table[field[0]][field[1]] = player_sign
                
            else:
                last_move = COMPUTER
                field = minimax_memory.computer_move( table )

                # print(LINE)
                # print('Computer move!')
                # field = get_field( table )

                table[field[0]][field[1]] = computer_sign

            winner = announce_victory(table, last_move)
            # game_datails( table, winner )

        game_memory.update_qs(-winner)
        if winner == PLAYER:
            results[0] += 1
        elif winner == TIE:
            results[1] += 1
        elif winner == COMPUTER:
            results[2] += 1

    return results




if __name__ == "__main__":
    game_memory = GameMemory()
    minimax_memory = MinimaxMemory()

    learning_iterations = 0
    play_iterations = 10000

    print('END LEARNING: ', game(game_memory, minimax_memory, learning_iterations) )
    if learning_iterations != 0:
        game_memory.save_qs()
        minimax_memory.save_qs()


    game_memory.read_qs()
    minimax_memory.read_qs()
    print('END: ', game(game_memory, minimax_memory, play_iterations) )

