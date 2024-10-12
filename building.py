import random
from typing import List


class Building:
    def __init__(self, name, capacity: int, rate=0.01, has_shower=False):
        self.name = name
        self.stink = 0
        self.internal_stinks = []
        self.agents = set()
        self.stink_accumulation_rate = rate
        self.stink_dissipation_rate = 3 * rate
        self.has_shower = has_shower
        self.capacity = capacity
        self.fullness = 0

    def clean(self):
        self.stink = 0

    def set_stink(self, stink):
        self.stink = stink

    def set_internal_stinks(self, stinks_list):
        self.internal_stinks = stinks_list

    def update(self):
        # 0-1 score of "how full" the building is
        self.fullness = len(self.internal_stinks) / self.capacity

        # Calculate the contribution of each agent to the building stink
        accumulated_stink = (
            sum(stink for stink in self.internal_stinks) * self.stink_accumulation_rate * self.fullness)

        # Update building stink
        self.stink = max(0, self.stink * (1 -
                         self.stink_dissipation_rate) + accumulated_stink)

        # Cap building stink between 0 and 1
        self.stink = min(self.stink, 1.0)
