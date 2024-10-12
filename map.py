import time
from typing import List
from building import Building
from agent import Agent

BUILDING_STINK_MULTIPLIER = 0.1

class Map:
    def __init__(self, agents: list[Agent], buildings: list[Building]):
        self.agents = agents
        self.buildings = buildings

    def update(self):
        for building in self.buildings:
            building.update()
            #print(f"{building.name} is {round(building.stink, 3)} stinky")

        for agent in self.agents:
            agent.current_location.add_stink(agent.stink*BUILDING_STINK_MULTIPLIER)
            agent.update()
            #print(f"{agent.name} is {round(agent.stink, 3)} stinky in {agent.current_location.name}")