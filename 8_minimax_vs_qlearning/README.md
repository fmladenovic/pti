
# 🎮 TIC-TAC-TOE ( XO )

U ovoj implementaciji bota za igranje xo-a korišćen je *q-learning* algoritam. Treniran je da igra protiv minimax algoritma i pokazao je da u malo više od 50% slučajeva može da odigra nerešeno sa minimax algoritmom.

  

## Rezultati

Nakon 1,000,000 iteracija učenja *q* vrednosti, rezultati partija su sledeći:

<table>
<tr>
<td> Parties </td>
<td> 10 </td>
<td> 100 </td>
<td> 1000 </td>
<td> 10000</td>
</tr>
<tr>
<td> Results </td>
<td> w:0 t:5 l:5</td>
<td> w:0 t:58 l:42 </td>
<td> w:0 t:559 l:441</td>
<td> w:0 t:5716 l:4284 </td>
</tr>
</table>

  

**Zaključak**: Potrebno je koristiti neki manje pametn algoritam za treniranje zato što u ovom slučaju naš bot ne ume da kreira pobedničku strategiju (politiku).