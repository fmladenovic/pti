import matplotlib.pyplot as plt
import math

DISTANCE_COALITION = 10
MAX_V = 10

VISON_DISTANCE = 100


class Agent:
    def __init__(self, start, finish, color):
        self.start = start
        self.finish = finish
        self.positions = [start]
        self.color = color

     
    def extract_positions(self):
        xs_comp = []
        ys_comp = []
        xs = []
        ys = []
        for (i, position) in enumerate (self.positions):
            xs_comp.append(position[0])
            ys_comp.append(position[1])
            if i != 0 and i != len(self.positions) - 1:
                xs.append(position[0])
                ys.append(position[1])
            
        return xs_comp, ys_comp, xs, ys



    def near(self, point, distance_for_check):
        distance = [point[0] - self.positions[-1][0], point[1] - self.positions[-1][1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        return norm <= distance_for_check

    def priority_advantage(self, agents):
        priority = agents.index(self)
        for i in range(priority):
            if self.near( agents[i].positions[-1], DISTANCE_COALITION ):
                return None

        distance = [self.finish[0] - self.positions[-1][0], self.finish[1] - self.positions[-1][1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = (distance[0]/norm, distance[1]/norm)

        for i in range(priority + 1, len(agents)):
           if self.near( agents[i].positions[-1], DISTANCE_COALITION ):
                return (self.positions[-1][0] + direction[1] * (MAX_V+0.1) , self.positions[-1][1] + direction[0] * (MAX_V+0.1)) 
        return (self.positions[-1][0] + direction[0] * MAX_V , self.positions[-1][1] + direction[1] * MAX_V) 




    def unhappiness(self, agent):
        distance = self.distance(agent.positions[-1])
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        return max( ( (VISON_DISTANCE ** 2 - norm**2)/(norm**2 - DISTANCE_COALITION**2 + 0.00000000001 )), 0)

    def distance(self, point):
        return [point[0] - self.positions[-1][0], point[1] - self.positions[-1][1]]

    def automatic_navigation(self, agents):
        rest_agents = [ agent for agent in agents if agent != self ]

        adaption_component = [ 0, 0 ]
        for agent in rest_agents:
            distance = self.distance(agent.positions[-1])
            unhappiness = self.unhappiness(agent)
            adaption_component = ( adaption_component[0] + (distance[0] * unhappiness), adaption_component[1] + (distance[1] * unhappiness) )
        
        finish_distance = self.distance(self.finish)
        dvi_dxi = [finish_distance[0] - adaption_component[0], finish_distance[1] - adaption_component[1]]
        norm = math.sqrt(dvi_dxi[0] ** 2 + dvi_dxi[1] ** 2)
        direction = (dvi_dxi[0]/norm, dvi_dxi[1]/norm)

        return (self.positions[-1][0] + direction[0] * MAX_V , self.positions[-1][1] + direction[1] * MAX_V) 



    def next_position(self, agents):
        if self.near(self.finish, MAX_V * 0.8):
            return 

        # position = self.priority_advantage( agents )
        position = self.automatic_navigation( agents )

        if position != None:
            self.positions.append(position)



def simulation(agents):
    plt.suptitle('Simulation')
    plt.xlim( -120, 120)
    plt.ylim( -120, 120)

    for agent in agents:
        xs_comp, ys_comp, xs, ys = agent.extract_positions()
        plt.plot(xs_comp, ys_comp, f'{agent.color}--')
        # plt.plot(xs, ys, f'{agent.color}o')
        plt.plot(agent.start[0], agent.start[1], f'{agent.color}s')
        plt.plot(agent.finish[0], agent.finish[1], f'{agent.color}x')
    plt.show()



def game():

    # agents = [Agent((-90, 0), (100, 0), 'b'), Agent((90, 0), (-100, 0), 'g')]
    # agents = [Agent((0,-90), (0, 100), 'b'), Agent((0, 90), (0, -100), 'g')]
    # agents = [Agent((-50, -50), (50, 50), 'b'), Agent((50, -50), (-50, 50), 'g')]


    agents = [Agent((-90, 4), (100, 0), 'b'), Agent((90, -4), (-100, 0), 'g')]
    # agents = [Agent((4,-90), (0, 100), 'b'), Agent((-4, 90), (0, -100), 'g')]
    # agents = [Agent((-50, -50), (50, 50), 'b'), Agent((50, -50), (-50, 50), 'g')]

    for _ in range(100):
        for agent in agents:
            agent.next_position(agents)
    simulation(agents)


if __name__ == "__main__":
    game()
    