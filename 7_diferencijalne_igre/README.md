# 🐾 Diferencijalne igre

 1. Simulirati kretanje većeg broja agenata po ravni, tako da svaki agent nastoji stići do svog cilja, a da pri tome ne izazove sudar sa drugim agentima. Koristi strategiju izbora brzine do koje smo došli na vežbama: dati prioritet svakom agentu, agenti koji se nađu u blizini agenata višeg prioriteta ne smeju da se kreću.
 2. Ista simulacija za poboljšani zakon kretanja.

## Implementacija rešenja
I za prvi i za drugi deo zadatka koristi se isti kod za simulaciju. Rešenja se razlikuju samo u funkciji koja generiše narednu poziciju agenta.

	class  Agent:
		def  __init__(self, start, finish, color):
			self.start = start
			self.finish = finish
			self.positions = [start]
			self.color = color
Agenta definišu početna i odredišna tačka, boja koja pomaže u simulaciji i njegove pozicije (kretanje) kako bi se mogao rekonstruisati grafik.
### Prvi zadatak
Za prvi zadatak zakon kretanja je definisan tako da letelice koje su manjeg prioriteta stoje u mestu dok ih letelice višeg prioriteta zaobilaze. Zaobilaženje se vrši tako što se letalice pomeraju za 90 stepeni u odnosu na njihov pravac kretanja u levo kada letelica nižeg prioriteta uđe u njihovu zonu kolizije, a ako je u kolizionoj zoni letelica višeg prioriteta onda se letelica nižeg prioriteta zaustavlja.

	def  near(self, point, distance_for_check):
		distance = [point[0] - self.positions[-1][0], point[1] - self.positions[-1][1]]
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		return  norm <= distance_for_check

	def  priority_advantage(self, agents):
		priority = agents.index(self)
		for  i  in  range(priority):
			if  self.near( agents[i].positions[-1], DISTANCE_COALITION ):
				return  None

		distance = [self.finish[0] - self.positions[-1][0], self.finish[1] - self.positions[-1][1]]
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		direction = (distance[0]/norm, distance[1]/norm)  

		for  i  in  range(priority + 1, len(agents)):
			if  self.near( agents[i].positions[-1], DISTANCE_COALITION ):
				return (self.positions[-1][0] + direction[1] * (MAX_V+0.1) , self.positions[-1][1] + direction[0] * (MAX_V+0.1))

		return (self.positions[-1][0] + direction[0] * MAX_V , self.positions[-1][1] + direction[1] * MAX_V)

### Drugi zadatak
U drugom zadatku uvodimo novu zonu - zonu vidlivosti. Ona pomaže letelicama da uopšte ne dolaze u kritične situacije.

	def  unhappiness(self, agent):
		distance = self.distance(agent.positions[-1])
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		return  max( ( (VISON_DISTANCE ** 2 - norm**2)/(norm**2 - DISTANCE_COALITION**2 + 0.00000000001 )), 0)

	def  distance(self, point):
		return [point[0] - self.positions[-1][0], point[1] - self.positions[-1][1]]

	def  automatic_navigation(self, agents):
		rest_agents = [ agent  for  agent  in  agents  if  agent != self ]

		adaption_component = [ 0, 0 ]
		for  agent  in  rest_agents:
			distance = self.distance(agent.positions[-1])
			unhappiness = self.unhappiness(agent)
			adaption_component = ( adaption_component[0] + (distance[0] * unhappiness), adaption_component[1] + (distance[1] * unhappiness) )
		
		finish_distance = self.distance(self.finish)
		dvi_dxi = [finish_distance[0] - adaption_component[0], finish_distance[1] - adaption_component[1]]
		norm = math.sqrt(dvi_dxi[0] ** 2 + dvi_dxi[1] ** 2)
		direction = (dvi_dxi[0]/norm, dvi_dxi[1]/norm)

		return (self.positions[-1][0] + direction[0] * MAX_V , self.positions[-1][1] + direction[1] * MAX_V)

Funkcija nesreće (nezadovoljstva) kaže da ako letelice nisu u vidnom polju ne uzimati ih u obzir, a ako jesu proveriti koliko su blizu. Razlomak je dizajniran tako da proizvodi broj koji je jako veliki ako su letelice u zoni kolizije, a manji ako su u zoni vidljivosti - odnosno sve manji što su letelice dalje.
Sama funkcija automatske navigacije se sastoji iz dve komponente. Jedna komponenta tera letelicu da stremi ka cilju, a druga da izbegava ostale letelice. Funkcija nesreće praktično oceni naše rastojanje od drugih letelica i sa snažnom ili blagom promenom utiče na ugao pod kojim stremimo ka cilju izbegavajući celokupno koliziono polje drugih letelica.


## Rezultati

#### Prvi zadatak

<table>
<tr> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128343-6075c580-5367-11eb-855c-9b8b2131b951.png" alt="Vodoravno">  </td>
<td> <img src="https://user-images.githubusercontent.com/30222786/104128344-610e5c00-5367-11eb-877e-e4d66d5c973c.png" alt="Horizontalno"> </td> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128345-610e5c00-5367-11eb-8539-cd5bdd27d230.png" alt="Ukrsteno"> </td> 
</tr>
</table>


#### Drugi zadatak

<table>
<tr> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128392-931fbe00-5367-11eb-889f-de40ecc1c1ff.png" alt="Vodoravno">  </td>
<td> <img src="https://user-images.githubusercontent.com/30222786/104128393-931fbe00-5367-11eb-88e7-af0f0221a4c9.png" alt="Horizontalno"> </td> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128394-93b85480-5367-11eb-9b58-9464c8b1d127.png" alt="Ukrsteno"> </td> 
</tr>
</table>

<table>
<tr> 
<td>  Vison field </td>
<td> 20 </td> 
<td> 100 </td> 
<td> 200</td> 
</tr>
<tr> 
<td> Simulation </td> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128470-06293480-5368-11eb-99a1-1b9704182f16.png" alt="Vidno polje 20">  </td>
<td> <img src="https://user-images.githubusercontent.com/30222786/104128392-931fbe00-5367-11eb-889f-de40ecc1c1ff.png" alt="Vidno polje 100"> </td> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128471-06c1cb00-5368-11eb-9114-7a74ff585396.png" alt="Vidno polje 200"> </td> 
</tr>
</table>

<table>
<tr> 
<td> Ako su tačke tačno na liniji neće doći do mimoilaženja u diskretnom sistemu.</td> 
<td> <img src="https://user-images.githubusercontent.com/30222786/104128539-67e99e80-5368-11eb-8a0b-93e2726cec58.png" alt="Bez mimoilaženja">  </td>
</tr>
</table>