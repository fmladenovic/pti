# 🎮 TIC-TAC-TOE ( XO )
Iks oks je popularna igra za dva igrača. Igra se na tabli od 3x3 polja. Igrači naizmenično upisuju karaktere unutar polja koji mogu da budu X ili O. Svakom igraču je dodeljen jedan karakter - često je igraču koji prvi igra dodeljen X, a drugom O. Prvi igrač koji poveže tri ista uzastopna karaktera po vertikali, dijagonali ili horizontali pobeđuje.

## *Minimax* algoritam
Za automatizaciju poteznih igara koristi se minimax algoritam. Njegova najprostija primena je upravu u igrici XO. Ostale primene su u micama ([nine men's morris](https://en.wikipedia.org/wiki/Nine_men%27s_morris)), u šahu ([chess](https://en.wikipedia.org/wiki/Chess))... Igrica XO predstavlja najprostiju primenu ovog algoritma zato što igrica ima konačno mogućih slučajeva i tih slučajeva nema veliki broj. Konkretno, algoritam teži da minimizuje mogući gubitak u najboljim slučajevima. Alternativno, može se posmatrati i kao maksimizovanje minimalne dobiti.

<img src = "https://i.stack.imgur.com/lrXqH.png" alt= "xo" width="100%">

### Implementacija *minimax* algoritma
	def  minimax(table, depth, is_maximizing, computer_sign, player_sign):
		last_move = PLAYER  if  is_maximizing  else  COMPUTER
		result = announce_victory(table, last_move)
		if  not  result == NOONE:
			return  result
			
		if  is_maximizing:
			bestScore = -math.inf
			for  i  in  range(len(table)):
				for  j  in  range(len(table[i])):
					if(table[i][j] == EMPTY):
						table[i][j] = computer_sign
						score = minimax(table, depth + 1, False, computer_sign, player_sign)
						table[i][j] = ''
						bestScore = max(score, bestScore)
			return  bestScore
		
		else:
			bestScore = math.inf
			for  i  in  range(len(table)):
				for  j  in  range(len(table[i])):
					if(table[i][j] == EMPTY):
						table[i][j] = player_sign
						score = minimax(table, depth + 1, True, computer_sign, player_sign)
						table[i][j] = ''
						bestScore = min(score, bestScore)
			return  bestScore

## Primeri partija
U nastavku se nalaze dve partije gde je prilikom pokretanja druge partije blago poboljšan minimax algoritam tako da slabije ocenjuje poteze koji kasnije dovode do pobede.

	def  minimax(table, depth, is_maximizing, computer_sign, player_sign):
			last_move = PLAYER  if  is_maximizing  else  COMPUTER
			result = announce_victory(table, last_move)
			if  not  result == NOONE:
				return  result / depth
		...

Primeri partija:
<table>
<tr> 
<td> <i>Bez poboljšanja</i> </td>  
<td> <i>Sa poboljšanjem</i></td> 
</tr>
<tr> 
<td> <img src = "https://user-images.githubusercontent.com/30222786/99910025-26376280-2cec-11eb-8c2a-f58539506ca0.png" alt ="Partija 1"> </td>  
<td> <img src = "https://user-images.githubusercontent.com/30222786/99910021-246d9f00-2cec-11eb-8cb1-430a1c35ff03.png" alt ="Partija 2"> </td> 
</tr>
</table>
