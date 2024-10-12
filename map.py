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
        bo_to_lib = [(55.873498, -4.292804), 
                     (55.873311, -4.293180), 
                     (55.873010, -4.292456), 
                     (55.872712, -4.291050), 
                     (55.872530, -4.289391),
                     (55.872807, -4.288762),
                     (55.873128, -4.288531),
                     (55.873342, -4.288400)
                    ]
        
        lib_to_rr = [(55.873323, -4.288474), 
                     (55.873102, -4.288537), 
                     (55.873065, -4.288317), 
                     (55.872884, -4.288315), 
                     (55.872674, -4.288206), 
                     (55.872520, -4.288044)]
        
        rr_to_bo = [(55.872346, -4.288193),
                    (55.872452, -4.289079),
                    (55.872521, -4.289712),
                    (55.872681, -4.290329),
                    (55.872889, -4.290934),
                    (55.873012, -4.291090),
                    (55.873137, -4.291259),
                    (55.873302, -4.291524),
                    (55.873751, -4.292348) ]   
        
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