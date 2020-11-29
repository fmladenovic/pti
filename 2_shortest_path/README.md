# 🚩Najkraći put

Posmatrajmo problem pronalačenja najkraćeg puta kroz graf. Modifikovati rešenje razmatrano na vežbama na sledeće načine:
1. Napisati funkciju koja za dati graf (datu matricu susedstva) i dati ulazni i izlazni čvor generiše najkraću putanju od ulaza do izlaza.
2. Modifikovati algoritam prikazan na vežbama tako da radi i za usmerene grafove.
3. Modifikovati rešenje tako da se dozvoli veći broj terminalnih čvorova.
4. Modifikovati rešenje tako da se uzme u obzir i nejednaka cena prelaza, odnosno tako da se i ivicama pridruže težine koje odgovaraju ceni prelaza preko te ivice. Do sada su cene svih ivica bile jednake jedinici.

## Zadatak 1
#### Imlementacija algoritama za ocenjivanje čvorova
Od algoritma sa vežbi je napravljena metoda koja kao ulazne parametre prima matricu susedstva (*adjacency matrix*) i krajnji čvor.

	def  calculate_state_values(environment, end):
		assert(0 < end  and  end <= len(environment), 'Idex out of bound!')
		
		v = [-math.inf  if  i != end  else  0  for  i  in  range(len(environment))]
		
		nodes_to_check = [end]
		while( len(nodes_to_check) != 0 ):
			current_node = nodes_to_check.pop()
			neighbors = non_zero_indexes(environment[current_node])
			for  n  in  neighbors:
				new_value = v[current_node] - 1
				if  new_value > v[n]:
					v[n] = new_value
					nodes_to_check.append(n)
		return  v
> NAPOMENA: non_zero_idexes -> np.nonzero(array)[0].tolist()
> 
Vodeći se logikom dinamičkog programiranja kojom nas je naučio dr Richard E. Bellman vrednost odredišnog čvora se postavlja na 0. U odnsu na taj čvor se dodeljuju vrednosti ostalim čvorovima. Prvi, njemu sustedni, čvorovi dobijaju vrednost -1, a ostali čvorvi dobijaju vrednosti tim poretkom gde je vrednost svakog čvora zapravo najkraće rastojanje od odredišnog (krajnjeg) čvora.

#### Imlementacija algoritama za pronalaženje najkraćeg puta

	def  shortest_path(environment, start, end):
		assert(0 < end  and  end <= len(environment), 'END out of bound!')
		assert(0 < start  and  start <= len(environment), 'START out of bound!')
		
		state_values = calculate_state_values(environment, end)
		path = [start]
		current_node = start
		while( current_node != end ):
			possible_nodes = non_zero_indexes(environment[current_node])
			possible_nodes_values = np.take(state_values, possible_nodes)
			current_node = possible_nodes[np.argmax( possible_nodes_values )] 
			path.append(current_node)
		return  path
Ocenjuju se čvorovi (stanja)  objašnjenim algoritmom. U putanju kretanja se dodaje početni čvor i taj čvor se postavlja za čvor u kome se trenutno nalazimo. Izvršavamo postupak sve dok se ne nađemo u krajnjem čvoru. Preuzimamo susedne čvorove (čvorove u koje možemo da idemo iz trenutnog čvora) i ocene tih čvorova. Biramo čvor koji je najbliži krajnjem čvoru, a potom prelazimo u taj čvor. Dodajemo čvor u kome smo u našu putanju. Nakon završetka petlje imamo našu putanju od zadatog početnog čvora, do krajnjeg čvora.

### Primeri
<table>
<tr> 
<td> <i>states</i> </td>
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549017-c05d5480-3270-11eb-8059-2bfe9bcf12fc.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549029-d23ef780-3270-11eb-8300-dd1b99856b87.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549032-d5d27e80-3270-11eb-9a1a-06204ae8bc9c.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549035-d9fe9c00-3270-11eb-9cee-4301f6a47ec9.png" alt="Graph" width="300px"> </td> 
 </tr>
<tr> 
<td> <i>paths</i>  </td>
<td> A -> B -> E </td> 
<td>C -> D -> E</td> 
<td> B -> E</td> 
<td> D -> E </td> 
</tr>
</table>


## Zadatak 2
Da bi se primenilo dinamičko programiranje u ovom slučaju potrebno je naći inverzni graf. Logika je sledeća: Ako sam ja krajnji čvor - ja ne znam ko su susedi koji upučuju na mene, ali susedi koji upućuju na mene znaju za mene. Za algoritam koji je baziran na logici dinamičkog programiranja stvari se posmatraju sa kraja ka 'početku'.
Naš algoritam za ocenjivanje čvorova u ovom slučaju treba da rukuje sa invertovanim grafom.

#### Imlementacija algoritama za invertovanje grafa
	def  generate_inverse_graph( graph ):
		inverse_graph = [ [0]*len(graph[0]) for  _  in  range( len(graph)) ]
		for (pointed_from, node) in  enumerate(graph):
			point_to_nodes = non_zero_indexes(node)
			for  pointed_node  in  point_to_nodes:	
				inverse_graph[pointed_node][pointed_from] = node[pointed_node]
		return  inverse_graph
Novi graf je inicijalno napunjen nepovezanim čvorovima (nova matrica susedstva). Za svaki čvor uzmi čvorove na koje pokazuje i tim čvorovima postavi da pokazuju na njega. U interpretaciji: Umesto da ja pokazujem na njih, oni pokazuju na mene.

## Zadatak 3
#### Implementacija algoritma za ocenjivanje čvorova sa više terminalnih čvorova

	def  calculate_state_values_for_multiple_terminal_nodes(environment, ends):
		assert(len(environment) != 0, 'You should add at least 1 state!')
		assert(len(ends) != 0, 'You should add at least 1 terminal state!')
		for  end  in  ends:
			assert(0 < end  and  end <= len(environment), 'END out of bound!')
		
		inverse_environment = generate_inverse_graph(environment)
		v = [-math.inf  if  i  not  in  ends  else  0  for  i  in  range(len(environment))]
		for  end  in  ends:
			nodes_to_check = [end]
			while( len(nodes_to_check) != 0 ):
				current_node = nodes_to_check.pop()
				neighbors = non_zero_indexes(inverse_environment[current_node])
				for  n  in  neighbors:
					new_value = v[current_node] - 1
					if  new_value > v[n]:
						v[n] = new_value
						nodes_to_check.append(n)
		return  v
Ovaj algoritam se razlikuje od prethodnog u tome što je potrebno oceniti čvorove za svaki terminalni čvor jer se čvorovi ocenjuju u odnosu na najbliži terminalni čvor. I, naravno, svaki terminalni čvor ima svoju '0' (najbolju) ocenu.

#### Implementacija algoritma za pronalaženje najkraćeg puta sa više terminalnih čvorova

  
	def  shortest_path_for_multiple_terminal_nodes(environment, start, ends):
		assert(len(environment) != 0, 'You should add at least 1 state!')
		assert(len(ends) != 0, 'You should add at least 1 terminal state!')
		for  end  in  ends:
			assert(0 < end  and  end <= len(environment), 'END out of bound!')

		state_values = calculate_state_values_for_multiple_terminal_nodes(environment, ends)
		path = [start]
		current_node = start
		while( current_node  not  in  ends ):
			possible_nodes = non_zero_indexes(environment[current_node])
			possible_nodes_values = np.take(state_values, possible_nodes) 
			current_node = possible_nodes[np.argmax( possible_nodes_values )] 
			path.append(current_node)

		return  path
Razlika između ovog i prošlog algoritma je u algoritmu ocenjivanja čvorova i u uslovu *while* petlje - bitno da stignemo u bilo koji krajnji čvor.

### Primeri
<table>
<tr> 
<td> <i>states</i> </td>
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549090-2a75f980-3271-11eb-8185-2b6d59fe0110.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549094-2f3aad80-3271-11eb-86f3-c5685f1b6d03.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549092-2cd85380-3271-11eb-8670-0dce5e5d255f.png" alt="Graph" width="300px"> </td> 
 <td> <img src="https://user-images.githubusercontent.com/30222786/100549096-33ff6180-3271-11eb-9264-a0a932959573.png" alt="Graph" width="300px"> </td> 
 </tr>
<tr> 
<td> <i>paths</i>  </td>
<td> A -> B -> E </td> 
<td>B -> E</td> 
<td> C -> G</td> 
<td> F -> G </td> 
</tr>
</table>

## Zadatak 4
Cena prelaza utiče na ocenu stanja. Njome možemo da modelujemo da li je neki prvi susedni čvor krajnjeg čvora 'bliži' ili 'dalji' krajnjem čvoru.

#### Implementacija algoritma za ocenjivanje čvorova sa nejednakim cenama prelaza
	def  weighted_calculate_state_values(environment, ends):
		...
		new_value = v[current_node] - inverse_environment[current_node][n]
		...
Ovaj algoritam se razlikuje od prethodnog samo u tome što je potrebno pronaći cenu prilikom prelaza iz jednog čvora u drugi i njome zameniti konstantu koju smo koristili do sada.

#### Implementacija algoritma za pronalaženje najkraćeg puta sa nejednakim cenama prelaza
	def  weighted_shortest_path(environment, start, ends):
		assert(len(environment) != 0, 'You should add at least 1 state!')
		assert(len(ends) != 0, 'You should add at least 1 terminal state!')
		for  end  in  ends:
			assert(0 < end  and  end <= len(environment), 'END out of bound!')

		state_values = weighted_calculate_state_values(environment, ends)
		path = [start]
		current_node = start
		while( current_node  not  in  ends ):
			possible_nodes = non_zero_indexes(environment[current_node])
			possible_nodes_values = np.take(state_values, possible_nodes) 
			
			for (i, possible_node) in  enumerate(possible_nodes): 
				possible_nodes_values[i] -= environment[current_node][possible_node]
				
			current_node = possible_nodes[np.argmax( possible_nodes_values )] 
			path.append(current_node)
		return  path

*For* petlja koja iterira kroz enumeraciju mogućih čvorova uračunava cenu prelaza u vrednost odredišnog čvora. Bilo je potrebno označiti kojim bi putem trebalo ići ako su sve ocene susednih čvorova jednake, a cena prelaza do nekog od njih manja od cene prelaza ka ostalim (više o tome u primeru).

### Primeri

<img src="https://user-images.githubusercontent.com/30222786/100549206-dae3fd80-3271-11eb-9865-eb27e4b45543.png" alt="Graph" width="100%">

Bez pomenute *for* petlje kada bismo krenuli iz čvora 'A', starom algoritmu bi bilo sve jedno koji čvor uzima za sledeći jer su svi čvorovi ocenjeni jednako, ali kada od svakog čvora dodatno oduzme cenu prelaska u taj čvor, onda postaje jasnije koji je čvor optimalno izabrati. Zbog toga je putanja u ovom slučaju A -> C -> G.

> NAPOMENA: Vizualizacije u ovom dokumentu su pravljene ručno, ali su u skladu sa implementiranim algoritmima.

> NAPOMENA: Imlementirana je jednostavnija vizualizacija koja je trenuntno isključena u kodu. Potrebno je instalirati *networkx* biblioteku:
> pip install networkx

## ✨Dodatni zadatak 
<img src="https://user-images.githubusercontent.com/30222786/100549522-a07b6000-3273-11eb-868b-2084455f6e68.png" alt="Graph" width="100%">

Čvorovi su označeni krugovima, a kapije punim kružićima na njihovim ivicama. Svaka isprekidana linija predtsavlja jedan mogući prelaz iz kapije u čvor. Smerovi prelaza nisu naznačeni strelicama, pošto se svaki prelaz vrši od kapije do čvora, nikada u suprotnu stranu. Tako recimo, u čvoru A imamo mogućnost izbora između dve kapije: 'donje' i 'gornje'. 'Donja' kapija nas vodi sa verovatnoćom 0,8 u čvor C, a sa verovatnoćom 0,2 u čvor D. Kapije kod kojih verovatnoća nije specificirana imaju podjednaku verovatnoću svih prelaza. Primetite da u čvoru B, 'gornja' kapija nas sa 50% verovatnoće vraća u polazni čvor.

#### Rešenje
<img src="https://miro.medium.com/max/5032/1*CiDCpUjj_3mGm3vdGrxu4g.png" alt="equ" width="100%"> 
Primena ove varjante Belmanove jednačine bi nam iterativno mogla odrediti vrednosti stanja gde bi te vrednosti posle dovoljnog broja iteracija konvergirale i jasno definisale optimalnu politiku. U ovom konkretnom slučaju nama samo *gama* figuriše 'kaznu' pa je iz toga zaključak sledeći: Mislim da nam za čvor A nije bitno koju kapiju biramu zato što iz bilo koje dve kapije dolazimo u čvor iz kog možemo stići direktno do cilja sa istom verovatnoćom (50%), a što se čvorova B, C i D tiče mislim da uvek treba birati kapiju koja nas može odvesti do čvora E. U najgorem slučaju završićemo u čvoru B gde ćemo posle dovoljnog broja pokušaja ipak stići do odredišta E.
