# 🎲Blackjack
**Pravila:** 
Igra ima dva igrača (nas i delitelja). Na početku igre, Igrač i Delitelj dobijaju po dve karte. Pri tome, jedna Deliteljeva karta sakrivena od Igrača. Prvi na potezu je Igrač, koji ima opcu da zahteva novu kartu (*hit*) ili da stane (*hold*). Svaka 'obojena' karta (kralj, dama ili žandar) se broji kao 10, a svaka karta sa brojem (2 - 10) se broji spram svog broja. 'Kec' se može brojati kao 11 ili kao 1. Cilj je dostići ukupan zbir što bliži ili idealno jednak 21. Ukoliko je ukupan zbir iznad 21, tada igrač automatski gubi. Ukoliko ni jedan igrač ije izgubio, pobedio je onaj koji u ukupnom zbiru ima veći broj.
**Strategija delitelja:**
Zahtevaj novu kartu sve dok u ukupnom zbiru ne dostigneš 17 ili više. Stani, čim je ukupan zbir bar 17.
**Pitanje špila:**
U ovom slučaju špil će se smatrati beskonačnim, što znači da je podjednako moguće izvući bilo koju od karata u svakom trenutku (eliminišemo takozvano 'brojenje karata').

## Postavka problema
Pre same implementacije bitno je definisati elemente kojima se rukuje. Elementi od interesa su nam stanja (*s*), akcije (*a*) i nagrade (*r*).

 - Stanje bi bila trojka: suma karata Igrača, da li je u toj sumi figurisao iskoristiv 'kec' (iskoristiv je ako se računao kao 11) i vidljiva karta delitelja.
 - Akcije su: *hit* i *hold*.
 - Nagrade su: +1 ako je Igrač pobedio, -1 ako je Delitelj pobedio i 0 ako je nerešeno.

## Logika rešenja
Budući da se naš protivnik ponaša deterministički (mi ne možemo predvideti koja je njegova skrivena karta ili koju će kartu on izvući) najbolje što možemo da uradimo jeste da računamo do koje nas dobiti u srednjem vode stanja u kojim se nalazimo i akcije koje koristimo. Ovaj postupak se naziva *q-learning*. Da bismo 'sagradili' naše *q* potrebno je odigrati značajan broj partija gde bismo mi u *q* ugrađivali naše iskustvo, a samim tim bi nam te vrednosti *q*-a gradile politiku, odnsono - govorile bi nam koja je akcija najoptimalnija za stanje u kome se nalazimo.

## Implementacija rešenja

### Konstante

Karte koje je moguće izvući iz špila karta:

	CARDS = [
		'1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', '12♥', '13♥', '14♥',
		'1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', '12♦', '13♦', '14♦',
		'1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', '12♣', '13♣', '14♣',
		'1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', '12♠', '13♠', '14♠'
	]

Lambda figuriše u ažuriranju *q* vrednosti - u interpretaciji govori koliko ćemo priznati nove promene:
	
	LAMBDA = 0.1

 
Nagrade - krajnji ishodi partije:
	
	PLAYERS_VICTORY = +1
	DEALERS_VICTORY = -1
	TIE = CONTINUE = 0

  
Moguće akcije i EMPTY vrednost koja je pomoćna konstanta:

	HIT = 'hit'
	HOLD = 'hold'
	ACTIONS = [HIT, HOLD]
	EMPTY = 'empty'

### Pomoćne funckije

Ako karta ima 3 karaktera (zbog znaka karte) onda je to neka obojena karta ili desetka tako da je njena vrednost 10, u suprotnom je vrednost prvog karaktera:

	def  get_value( card ):
		if  len(card) == 3:
			return  10
		return  int(card[0])

Vrednost slučajne karte iz špila (prilikom izvlačenja bira se slučajna karta i uzima se njena vrednost):

	def  get_card_by_value():
		return  get_value(CARDS[ randint(0, len(CARDS)-1)])


Metoda koja određuje da li se u sumi može koristiti iskoristivi kec i dodaje na staru sumu novu vrednost:

	def  sum_and_useable_ace(old_sum, useable_ace, new_value):
		new_sum = old_sum + new_value
		if  new_sum > 21  and  useable_ace:
			new_sum -= 10
			return  new_sum, False
		if  new_sum <= 11  and  new_value == 1:
			new_sum += 10
			return  new_sum, True
		return  new_sum, useable_ace

### Memorija *q* vrednosti

U ovoj klasi se nalazi sama srž logike.  Ideja je da se prate stanja, akcije primenjene u tim stanjima i koja je njihova prosečna dobit. Da se ne bi čuvale sve dobiti pa računala q vrednost, ona se ažurira po sledećoj formuli:

	q(s, a) = q(s, a) + lambda*(r − q(s,a))
	
U ovom slučaju memoriju predstavlja jedan rečnik (*dictionary*) ili json objkeat u kome su ključevi parovi stanja akcija, gde je stanje opisano objašnjenim tripletom, a gde je akcija jedna od dve pomenute. 
Primer stanja u memoriju:

	{
		...
		"[(18, False, 10), hit]": -0.5264860690000001,
		"[(18, False, 10), hold]": -0.7367800069828581,
		...
	}
 
	
Pored metoda koje rukuju *q* vrednostima nalaze se i pomoćne metode. Jedna služi da kreira string ključ od stanja i ackije, a drug da sačuva celokupni rečnik kao JSON dokument nakon treniranja kako bi se *q* vrednosti mogle analizirati i eventualno ponovo učitale.

	class  GameMemory:

		def  __init__(self):
			self.sa_q = {}

		def  q(self, s, a):
			key = self._convert_to_key(s, a)
			return  self.sa_q.get( key ) if  key  in  self.sa_q.keys() else  0
			
		def  update_q(self, s, a, r, l = LAMBDA):
			key = self._convert_to_key(s, a)
			old_q = self.q(s, a)
			new_q = old_q + l * ( r - old_q)
			self.sa_q[key] = new_q

		def  _convert_to_key(self, s, a):
			s_str = [str(part) for  part  in  s]
			return  '[({}, {}, {}), {}]'.format(s_str[0], s_str[1], s_str[2], a)
			
		def  save_qs(self):
			with  open('data.json', 'w') as  fp:
				json.dump(self.sa_q, fp)

### Politike odlučivanja
Pored standardnih politika implementirana je *learning* politika čiji je zadatak da se ponaša 'sigurnije' dok se parovi stanja i ackija ne istraže dovoljno, odnosno dok ne budemo imali dovoljno iskustva.

	def  learning( game_memory, state, e ):
		if(state[0] > 17):
			return  HOLD
		else:
			return  e_greedy(game_memory, state, e)
U slučaju da nam je suma karta 17 ili više (pošto Diler igra do 17) naša akcija će biti *hold*, a u slučaju da imamo ispod 17 koristiće se *epsilon greedy* politika.

	def  greedy(game_memory, state):
		q_hit = game_memory.q(state, HIT)
		q_hold = game_memory.q(state, HOLD)
		return  HIT  if  q_hit >= q_hold  else  HOLD

	def  e_greedy(game_memory, state, e):
		rand = uniform(0, 1)
		if  rand < e:
			return  ACTIONS[randint(0, len(ACTIONS)-1)]
		else:
			return  greedy(game_memory, state)

### Implementacija igre
Na početku partije dele se karte:

	def  begin_round():
		player_cards = []
		dealer_cards = []
		for  i  in  range(3):
			card = CARDS[ randint(0, len(CARDS)-1)]
			if  i % 2 == 0:
				player_cards.append(card)
			else:
				dealer_cards.append(card)
		return  generate_state(player_cards, dealer_cards)
Na osnovu karata generiše se početno stanje:

	def  generate_state(player_cards, dealer_cards):
		player_values = [get_value(card) for  card  in  player_cards]
		value = get_value(dealer_cards[0])
		dealer_value = value  if  value != 1  else  11  # dealer will have only 1 card on start (we cant see another)
		useable_ace = 1  in  player_values  and  sum(player_values) + 10 <= 21
		player_value = sum(player_values) if  not  useable_ace  else  sum(player_values) + 10
		return [player_value, useable_ace, dealer_value]

Igra se runda u kojoj se pamte parovi stanja i akcije u tim stanjima kako bi se njihove q vrednosti na kraju partije mogle ažurirati i određuje se ishod partije:

	def  game_round(game_memory):
		init_state = begin_round()
		state_action_pairs = [[init_state, EMPTY]]
		
		player_sum = player_turn(game_memory, state_action_pairs)

		if  player_sum == 21:
			return  state_action_pairs, PLAYERS_VICTORY
		elif  player_sum > 21:
			return  state_action_pairs, DEALERS_VICTORY

		dealer_sum = dealer_turn(state_action_pairs[0][0][2])

		if  player_sum < dealer_sum:
			return  state_action_pairs, DEALERS_VICTORY
		elif  player_sum > dealer_sum:
			return  state_action_pairs, PLAYERS_VICTORY
		else:
			return  state_action_pairs, TIE

Prvi na potezu je igrač koji na osnovu *q* vrednosti uz pomoć određene politike bira akciju za stanje u kome se trenutno nalazi i to radi sve dok ne prepusti potez dileru akcijom *hold*:

	def  player_turn( game_memory, state_action_pairs):
		action = ''
		i = 0

		while  action != HOLD  and  state_action_pairs[i][0][0] < 21:
			action = learning(game_memory, state_action_pairs[i][0], 0.3) if  len(game_memory.sa_q.keys()) > 360  else  e_greedy(game_memory, state_action_pairs[i][0], 0.2)
			state_action_pairs[i][1] = action

			if  action == HIT:
				old_state = state_action_pairs[i][0]
				new_state = [*sum_and_useable_ace(old_state[0], old_state[1], get_card_by_value()), old_state[2]]
				state_action_pairs.append([new_state, EMPTY])
				i+=1

		if  state_action_pairs[-1][1] == EMPTY: 
			return  state_action_pairs.pop()[0][0]
		return  state_action_pairs[-1][0][0]

Drugi na potezu je diler i on ima fiksnu politiku kojom bira akcije:

	def  dealer_turn( dealer_sum ):
		while  dealer_sum < 17:
			value = get_card_by_value()
			dealer_sum += value  if  value != 1  else  11
		return  dealer_sum

Nakon odigrane partije ažuriramo q vrednosti u našoj memoriji za sve parove stanja i akcija u protekloj partiji i krajnjim ishodom:

	def  game(iterations):
		game_memory = GameMemory()
		my_final_reverd = 0
		reverds = []

		for  _  in  range(iterations):
			game_state_actions, reverd = game_round(game_memory)

			reverds.append(my_final_reverd + reverd)
			my_final_reverd += reverd

			for  game_state_action  in  game_state_actions:
				game_memory.update_q(game_state_action[0], game_state_action[1], reverd)

		print('\nEND', str(my_final_reverd))
		plot_values(reverds)
		game_memory.save_qs()
	
Na kraju se vrši ispis krajnjeg skora, prikazuje grafik naših dobitaka (gubitaka)
 i čuvaju se q-vrednosti.

    

> NAPOMENA: Program se pokreće sa jednim argumentom koji predstavlja broj partija.
> Primer: python blackjack.py 1000

## Diskusija
Ako se pogledaju q vrednosti u data.json dokumentu koje su dobijene nakon 1,000,000 iteracija može se videti da vrlo malo kombinacija (stanja, akcija) zapravo imaju pozitivnu q vrednost. Što bi u interpretaciji značilo da mi nemamo mnogo šansi za pobedom. Svega u 30tak stan sa adekvatnim akcijama imamo nekakve šanse za pobedom. Među tim stanjima se ističu situacije kada mi imamo sumu karata preko 18.
**Zaključak je:** Nije isplativo igrati Blackjack!