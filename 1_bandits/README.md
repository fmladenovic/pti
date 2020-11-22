# Bandits

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

	def  softmax(q, t):
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
			if(first < picker and picker < second):
				return i + 1
		return 0
#### Grafici *q-vrednosti* u zavisnosti od parametra *t*
...