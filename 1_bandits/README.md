# Banditi 🧨

Posmatrajmo problem resavanja problema bandita sa vise ruku. Modifikovati resenje razmatrano na vezbama na sledece nacine: 
1. Implementirati *softmax politiku odlucivanja*. 
2. U delimicno pohlepnoj politici izbora ispitati efikasnost resenja u zavisnosti od izabrane vrednosti parametra *epsilon*. 
3. U slucaju da se banditi menjaju tokom vremena, recimo tako sto se srednje vrednosti ocekivane dobiti naglo promene, ispitati kako se ponasa delimicno pohlepna politika odlucivanja za razlicite vrednosti parametra *epsilon*.

## Zadatak 1
Softmax politika je još jedan od načina da se uvede slučajnost u odabiru akcije. Dobijene *q-vrednosti* iz prethodne iteracije se skaliraju u opseg (0, 1) gde se svaka vrednost preslikava u broj. Za svaku akciju taj broj predstavlja verovatnoću da bude izabrana. Zbir novodobijenih vrednosti je 1.
> ![softmax](https://user-images.githubusercontent.com/30222786/99899523-49d9b900-2caa-11eb-9550-d668d6470976.png)
> Formula na kojoj se bazira *softmax politika odlučivanja*

Sa parametrom *t* (temperatura) se kontroliše raspodela verovatnoće po akciji.
#### Implementacija *softmax politike odlučivanja*

	def softmax(q, t):
		q = [x/t for x in q]
		softmax_values = np.exp(q) / np.sum(np.exp(q), axis=0)
		
		precalculated_values = []
		precalculated_values.append(softmax_values[0])
		
		for i in range(1, len(softmax_values)):
			precalculated_values.append(precalculated_values[i-1] + softmax_values[i])
		
		picker = rand()
		for i in range(len(precalculated_values) - 1):
			first = precalculated_values[i]
			second = precalculated_values[i+1]
			if(first < picker and picker <= second):
				return i + 1
		return 0
#### Grafici *q-vrednosti* i biranih akcija u zavisnosti od parametra *t*

<table>
<tr> <td> <i>t</i> </td>  <td> 1 </td> <td>2</td> <td>5</td> <td>10</td> </tr>
<tr> <td> <i>actions</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99906587-3b09fb00-2cd8-11eb-8e51-7858bfb7b862.png" alt="Actions" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99906711-e0bd6a00-2cd8-11eb-971f-04b11f2f8f7f.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99906792-5de8df00-2cd9-11eb-836c-55c2bc8e2c02.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99906795-5fb2a280-2cd9-11eb-8364-96ac8e878339.png" alt="Actions" width="150px"></td> </tr>
<tr> <td> <i>q-values</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99906644-8d4b1c00-2cd8-11eb-9ea0-2c11d15923dc.png" alt="q-values" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99906709-def3a680-2cd8-11eb-9e92-c5efc1e2efd8.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99906789-59bcc180-2cd9-11eb-9360-ab8751ef2df5.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99906791-5b868500-2cd9-11eb-92fa-2dcc902869de.png" alt="q-values" width="150px"></td> </tr>
</table>

## Zadatak 2
Delimično pohlepna politika ili *epsilon-greedy* politika u zavisnosti od parametra *epsilon* bira slučajnu akciju ili najbolju akciju. Tačnije, sa parametrom *epsilon* vršimo balansiranje između *eksploracije* i *eksploatacije* sistema. Bira se slučajan broj koji ako je manji od *epsilon* rezultuje slučajnom akcijom, a ako je veći od *epsilon* bira se najbolja akcija. *Epsilon* i slučajan broj se biraju iz opslega (0, 1).

#### Grafici *q-vrednosti* i biranih akcija u zavisnosti od parametra *epsilon*
<table>
<tr> <td> <i>epsilon</i> </td>  <td> 0.1 </td> <td>0.2</td> <td>0.5</td> <td>1</td> </tr>
<tr> <td> <i>actions</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99907586-f08b7d00-2cdd-11eb-9df0-36d96bc6d9ac.png" alt="Actions" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99907587-f2554080-2cdd-11eb-91de-cb0913ee2e80.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99907589-f3866d80-2cdd-11eb-8786-27068cf52c9f.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99907590-f4b79a80-2cdd-11eb-8d9f-58dd45b3a612.png" alt="Actions" width="150px"></td> </tr>
<tr> <td> <i>q-values</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99907592-f7b28b00-2cdd-11eb-8db7-73d41920ed0f.png" alt="q-values" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99907597-fda86c00-2cdd-11eb-9c29-b4fa5edd60fe.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99907598-ff722f80-2cdd-11eb-83e8-5d02028cf3da.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99907595-faad7b80-2cdd-11eb-9dfb-7332203a8f07.png" alt="q-values" width="150px"></td> </tr>
</table>

#### Zaključak
Na navedenim graficima može se videti kako algoritam u zavisnosti od parametra *epsilon* bira akcije. Kada je *epsilon* malo naš sistem bira, skoro uvek, najbolju akciju, a kako se *epsilon* povećava to više teži da istražuje. 


## Zadatak 3

#### Dodatak simulaciji
Odabrane su različite srednje vrednosti koje proizvodi okruženje gde se nakon 300 iteracija simulacije dešava prva promena celog okruženja, a nakon 700 te iteracije vraća se staro stanje.

    bandits = [(1, 1), (5, 10), (-3, 15), (15, 2), (-24, 3)]
    changed_bandits = [(8, 1), (10, 2), (-5, 2), (-30, 2), (12, 3)]
    old_bandits = [(1, 1), (5, 10), (-3, 15), (15, 2), (-24, 3)]
	...
	for k in range(1000):
		if k >= 300:
			bandits = changed_bandits
		if k >= 700:
			bandits = old_bandits
		a = eps_greedy(q, 0.2) #0.1, 0.2, 0.5, 1
		r = environment(a, bandits)
		q = learn(q, a, r)
		actions.append(a)
		rewards.append(r)
		qs.append(q)

#### Grafici *q-vrednosti* i biranih akcija u promenljivom okruženju u zavisnosti od parametra *epsilon*
<table>
<tr> <td> <i>epsilon</i> </td>  <td> 0.1 </td> <td>0.2</td> <td>0.5</td> <td>1</td> </tr>
<tr> <td> <i>actions</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99908378-a8bb2480-2ce2-11eb-9749-6179d59e9820.png" alt="Actions" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99908381-a9ec5180-2ce2-11eb-8ff3-815da7bfe735.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99908382-ab1d7e80-2ce2-11eb-9f1a-d5bacb1429f1.png" alt="Actions" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99908385-ac4eab80-2ce2-11eb-8c60-0e43a4b4c930.png" alt="Actions" width="150px"></td> </tr>
<tr> <td> <i>q-values</i>  <td> <img src="https://user-images.githubusercontent.com/30222786/99908386-ae186f00-2ce2-11eb-91ca-e1186417d2ac.png" alt="q-values" width="150px"> </td> <td><img src="https://user-images.githubusercontent.com/30222786/99908387-b1abf600-2ce2-11eb-9043-927320292d33.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99908388-b2448c80-2ce2-11eb-873b-6ef1027b2b42.png" alt="q-values" width="150px"></td> <td><img src="https://user-images.githubusercontent.com/30222786/99908391-b40e5000-2ce2-11eb-8837-f810a33f9b92.png" alt="q-values" width="150px"></td> </tr>
</table>

#### Zaključak
Što se više sistem menja to imamo manje koristi od ove klase algoritama jer bi se na kraju svelo na slučajno pogađanje. 