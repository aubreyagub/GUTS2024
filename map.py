import time
from typing import List
from building import Building
from agent import Agent

BUILDING_STINK_MULTIPLIER = 0.5

class Map:
    def __init__(self, agents: list[Agent], buildings: list[Building]):
        self.agents = agents
        self.buildings = buildings

    def update(self):
        building_occupancy = {}

        for agent in self.agents:
            if agent.current_location in building_occupancy.keys():
                building_occupancy[agent.current_location].append(agent)
            else:
                building_occupancy[agent.current_location] = [agent]

        for building in self.buildings:
            stinks_inside = [agent.stink for agent in building_occupancy.get(building, [])]
            building.set_internal_stinks(stinks_inside)
            building.update()

        for agent in self.agents:
            agent.update()