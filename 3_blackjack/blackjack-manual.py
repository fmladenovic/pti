from random import randint

PLAYER = 10
DEALER = -10

CONTINUE = 2

PLAYERS_VICTORY = 1
DEALERS_VICTORY = -1

# PLAYERS_BLACKJACK = 4
# DEALERS_BLACKJACK = -4

TIE = 0


CARDS = [ 
    '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', '12♥', '13♥', '14♥',
    '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', '12♦', '13♦', '14♦',
    '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', '12♣', '13♣', '14♣',
    '1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', '12♠', '13♠', '14♠'
]


HIT = 5
HOLD = -2



################################################################################### VIEW #################################################################################
def print_state( player_cards, dealer_cards, show_card = False ):
    player_state = 'PLY:' + 4*' '
    for card in player_cards:
        player_state += '{:^4}'.format(card) + ' '

    dealer_state = 'DLR:' + 4*' '
    for (i,card) in enumerate(dealer_cards):
        if i == 1 and not show_card:
            dealer_state += '{:^4}'.format('X') + ' '
        else:
            dealer_state += '{:^4}'.format(card) + ' '

    delimiter =  '-' * len(player_state) if len(player_state) > len(dealer_state)  else '-' * len(dealer_state)

    to_print = '\n' + dealer_state + '\n' + delimiter + '\n' + player_state + '\n'

    print(to_print)


def print_victory( end ):
    if end == CONTINUE:
        print( 'It is TIE! \n' )
    elif end == PLAYERS_VICTORY:
        print( 'It is PLAYERS victory! \n' )
    elif end == DEALERS_VICTORY:
        print( 'It is DEALERS victory!')


def input_action():
    print('1 -> HIT')
    print('0 -> HOLD')
    action = input('Enter action: ')
    if action == '1':
        return hit()
    else:
        return hold()


################################################################################### UTIL #################################################################################


def get_value( card ):
    if len(card) == 3:
        return 10
    return int(card[0])

def get_card():
    return CARDS[ randint(0, len(CARDS)-1)]


def calculate_sum(cards):
    
    card_values = [get_value(card) for card in cards]

    if 1 not in card_values:
        return sum(card_values)
    else:
        card_values_sum = sum(card_values) - 1
        if card_values_sum + 11 > 21:
            return card_values_sum + 1
        else:
            return card_values_sum + 11

def check_end(player_cards, dealer_cards, move):

    dealer_sum = calculate_sum(dealer_cards)
    player_sum = calculate_sum(player_cards)

    if move == PLAYER:

        if player_sum > 21:
            return DEALERS_VICTORY
        elif player_sum == 21:
            return PLAYERS_VICTORY if player_sum != dealer_sum else TIE
        else:
            return CONTINUE

    else:

        if dealer_sum > 21:
            return PLAYERS_VICTORY
        elif dealer_sum == 21:
            return DEALERS_VICTORY if player_sum != dealer_sum else TIE
        else:
            if dealer_sum >= 17:
                if dealer_sum > player_sum:
                    return DEALERS_VICTORY
                elif dealer_sum < player_sum:
                    return PLAYERS_VICTORY
                else:
                    return TIE
            else:
                return CONTINUE


################################################################################### GAME PLAY #################################################################################

def hit():
    return get_card()

def hold():
    return HOLD

def begin_round():
    player_cards = []
    dealer_cards = []

    for i in range(4):
        card = get_card()
        if i % 2 == 0:
            player_cards.append(card)
        else:
            dealer_cards.append(card)

    return player_cards, dealer_cards


def dealer_moves( player_cards, dealer_cards ):
    print_state(player_cards, dealer_cards, True)
    while True:
        
        end = check_end(player_cards, dealer_cards, DEALER)
        if end != CONTINUE: return end
        
        dealer_cards.append(get_card())
        print_state(player_cards, dealer_cards, True)


def player_moves( player_cards, dealer_cards ):

    print_state(player_cards, dealer_cards, False)

    while True:
        dealer_cards.append(get_card())
        print_state(player_cards, dealer_cards, False)
        check = check_end(player_cards, dealer_cards, PLAYER)

        if check != CONTINUE: return check


def human_moves( player_cards, dealer_cards ):
    print_state(player_cards, dealer_cards, False)
    while True:

        end = check_end(player_cards, dealer_cards, PLAYER)
        if end != CONTINUE: return end

        action = input_action()
        if action == HOLD: 
            return HOLD
        else:
            player_cards.append(get_card())
            print_state(player_cards, dealer_cards, False)



def game_round():

    player_cards, dealer_cards = begin_round()

    player_move_end = human_moves( player_cards, dealer_cards ) # human_moves( player_cards, dealer_cards )
    if player_move_end != HOLD:
        print_victory(player_move_end)
        return player_move_end

    dealer_move_end = dealer_moves( player_cards, dealer_cards )
    print_victory(dealer_move_end)
    return dealer_move_end
    
    




def game():
    scores = []
    for _ in range(10):
        end = game_round()
        scores.append( end )
    print('TOTAL SCORE -> ', str(sum(scores)), scores, len(scores))
    

if __name__ == "__main__":
    game()