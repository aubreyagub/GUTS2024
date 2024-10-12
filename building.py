import random
from typing import List

DECAY_MULTIPLIER = 0.1
class Building:
    def __init__(self, name, stink_accumulation_rate: float, stink_dissipation_rate: float, coordinate):
        self.name = name
        self.stink = 0
        self.internal_stinks = []
        self.agents = set()
        self.stink_accumulation_rate = stink_accumulation_rate
        self.stink_dissipation_rate = stink_dissipation_rate
        self.coordinate = coordinate

    def set_stink(self, stink):
        self.stink = stink

    def set_internal_stinks(self, stinks_list):
        self.internal_stinks = stinks_list

    def update(self):
        print(self.internal_stinks)
        # Calculate the contribution of each agent to the building stink
        accumulated_stink = sum(stink for stink in self.internal_stinks) * self.stink_accumulation_rate
        
        # Update building stink
        self.stink = max(0, self.stink * (1 - self.stink_dissipation_rate) + accumulated_stink)
        
        # Cap building stink between 0 and 1
        self.stink = min(self.stink, 1.0)

    def stink_decay(self):
        stink_decay = DECAY_MULTIPLIER * self.stink
        return stink_decay