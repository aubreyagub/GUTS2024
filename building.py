import random
from typing import List

DECAY_MULTIPLIER = 0.1
class Building:
    def __init__(self, name):
        self.name = name
        self.stink = 0

        self.agents = set()

    def add_stink(self, stink_increase):
        self.stink = self.stink + stink_increase 

    def update(self):
        self.stink -= self.stink_decay()
        pass

    def stink_decay(self):
        stink_decay = DECAY_MULTIPLIER * self.stink
        return stink_decay