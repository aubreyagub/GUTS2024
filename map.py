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
        building_occupancy = {}

        for building in self.buildings:
            building.update()

        for agent in self.agents:
            if agent.current_location in building_occupancy.keys():
                building_occupancy[agent.current_location].append(agent)
            else:
                building_occupancy[agent.current_location] = [agent]
            agent.update()

        # SET AVG STINK FOR EACH BUILDING
        for building in building_occupancy:
            total_stink = 0
            agent_count = 0
            for agent in building_occupancy[building]:
                total_stink += agent.stink
                agent_count += 1
            avg_stink = total_stink/agent_count
            building.set_stink(avg_stink)



    def get_path(self, start, end):
        bo_to_lib = []
        lib_to_rr = []
        rr_to_bo = []
        
        match start:
                case "boyd orr":
                    match end:
                        case "library":
                            return 
                        case "reading room":
                            return 
                case "library":
                    match end:
                        case "boyd orr":
                            return 
                        case "reading room":
                            return
                case "reading room":
                    match end:
                        case "boyd orr":
                            return 
                        case "library":
                            return