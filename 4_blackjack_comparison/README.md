# 🎲Blackjack uporedjivanje algoritama

Uporediti Monte-Karlo algoritam sa SARSA i Q-LEARNING algoritmima.

## Implementacija rešenja
Budući da nam nije toliko bitno da odmah ažuriramo trenutne *q* vrednosti (nije moguće da nam se ponovi isto stanje dva puta u jednoj partiji) ažuriranje je vršeno na kraju svake partije sa odgovarajućim vrednostima - Nagrada za svaki potez koji nije naš krajnji potez u partiji je 0, a nagrada za krajnji potez je informacija o tome da li smo pobedili (+1), izgubili (-1) ili odigrali nerešeno (0).

### SARSA

Za stanje *s_prim* i akciju *a_prim* uzimaju se naredno stanje iz naše partije, a za akciju se bira ona 	akcija koju je proizvela naša politika odlučivanja. Terminalna stanja imaju vrednost 0, zato što mi ne donosimo odluku u njima. 
Ažuriranje *q* vrednosti se vrši sledećim algoritmom:

	def  update_q_sarsa(self, s, a, s_prim, a_prim, r, l = LAMBDA, g = GAMA):
		key = self._convert_to_key(s, a)
		next_q = 0

		if  key  in  self.sa_q.keys(): # Terminal value will be 0
			next_q = self.q(s_prim, a_prim)

		old_q = self.q(s, a)
		new_q = old_q + l * ( r + g * next_q - old_q)
		self.sa_q[key] = new_q
	

### Q learning

*Q learning* algoritam se razlikuje od *SARSA* algoritma samo po tome što težimo da u narednom stanju izaberemo najbolju akciju. 
Ažuriranje *q* vrednosti se vrši sledećim algoritmom:

	def  update_q_q_learning(self, s, a, s_prim, r, l = LAMBDA, g = GAMA):
		key = self._convert_to_key(s, a)
		next_q = 0

		if  key  in  self.sa_q.keys():
			max_a = greedy(self, s_prim)
			next_q = self.q(s_prim, max_a)

		old_q = self.q(s, a)
		new_q = old_q + l * ( r + g * next_q - old_q)
		self.sa_q[key] = new_q

## Rezultati
Nakon 2,000,000 iteracija učenja *q* vrednosti, rezultati partija su sledeći:
<table>
<tr> 
<td>  Parties </td>
 <td> 10,000 </td> 
 <td> 30,000 </td> 
 <td> 50,000 </td> 
 <td> 100,000</td> 
 </tr>
<tr> 
<td> Monte-Karlo  </td>
<td> w:2343 t:688 l:6969 </td> 
<td> w:7027 t:2075 l:20898 </td> 
<td>  w:11676 t:3390 l:34934</td> 
<td> w:233825 t:67141 l:699034 </td> 
</tr>
<tr> 
<td> SARSA  </td>
<td> w:2298 t:717 l:6985</td> 
<td> w:6931 t:2161 l:20908</td> 
<td>w:11474 t:3575 l:34951 </td> 
<td> w:229626 t:71132 l:699242 </td> 
</tr>
<tr> 
<td> Q-learning </td>
<td> w:2336 t:667 l:6997</td> 
<td>w:6898  t:2098 l:21004</td> 
<td> w:11656  t:3472 l:34872</td> 
<td> w:233468 t:68923 l:697609</td> 
</tr>
</table>

Poboljšanje algoritama je moguće uz pametnu  inicijalizaciju q-vrednosti i podešavanja hiper-parametara *lambda* i *gama*.