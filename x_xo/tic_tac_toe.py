import time
import random
import math
from numpy.random import randint

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
NOONE = -1000



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

# Minimax algoritam gradi (bez otpimizacije - alfa/beta rezanja...) celo stablo stanja.
#  Na svakom nivou teži da izabere najbolji potez iz ugla osobe koja je trenutno na potezu.
#  To uspeva da postigne tako što, na osnovu terminalnih čvorova, propagira vrednosti do krajnjih 
#  čvorova koji predstavljaju naš sledeći potez i bira onaj koji ima maksimalni pozitivan ishod po
#  korisnika algoritma.
def minimax(table, depth, is_maximizing, computer_sign, player_sign):
    last_move = PLAYER if is_maximizing else COMPUTER
    result = announce_victory(table, last_move)
    if not result == NOONE:
        return result/depth # Ovim postupkom sam naterao kompjuter da brže pobedi

    if is_maximizing:
        bestScore = -math.inf
        for i in range(len(table)):
            for j in range(len(table[i])):
                if(table[i][j] == EMPTY):
                    table[i][j] = computer_sign
                    score = minimax(table, depth + 1, False, computer_sign, player_sign)
                    table[i][j] = ''
                    bestScore = max(score, bestScore)
        return bestScore

    else: 
        bestScore = math.inf
        for i in range(len(table)):
            for j in range(len(table[i])):
                if(table[i][j] == EMPTY):
                    table[i][j] = player_sign
                    score = minimax(table, depth + 1, True, computer_sign, player_sign)
                    table[i][j] = ''
                    bestScore = min(score, bestScore)
        return bestScore


# Kompjuter se oslanja na minimax algoritam kako bi odredio najpovoljniju poziciju po njega.
def computer_move( table, computer_sign, player_sign ):
    bestScore = -math.inf
    for i in range(len(table)):
        for j in range(len(table[i])):
            if(table[i][j] == EMPTY):
                table[i][j] = computer_sign
                score = minimax(table, 1, False, computer_sign, player_sign)
                table[i][j] = ''
                if score > bestScore:
                    bestScore = score
                    field = (i, j)   
    return field



############################## GAME LOGIC ###################################


def game():
    table = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

    first_move = COMPUTER if random.uniform(0, 1) <= 0.5 else PLAYER  # Odabira na slučajan način ko ima prvi potez
    last_move = PLAYER if first_move == COMPUTER else COMPUTER
    winner = NOONE

    if first_move == PLAYER:
        player_sign = X
        computer_sign = O
    else:
        player_sign = O
        computer_sign = X
    
    print_table(table)
    while winner == NOONE:
        
        if( last_move == COMPUTER ):
            last_move = PLAYER
            print(LINE)
            print('Player move!')
            field = get_field( table )
            table[field[0]][field[1]] = player_sign

        else:
            last_move = COMPUTER
            print(LINE)
            print('Computer move!')
            field = computer_move( table, computer_sign, player_sign )
            table[field[0]][field[1]] = computer_sign

        winner = announce_victory(table, last_move)
        game_datails( table, winner )
    
    return winner




if __name__ == "__main__":
    game()