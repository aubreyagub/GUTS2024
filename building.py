import random
from typing import List

DECAY_MULTIPLIER = 0.1
class Building:
    def __init__(self, name):
        self.name = name
        self.stink = 0

        self.agents = set()

    def set_stink(self, stink):
        self.stink = stink

    def update(self):
        self.stink -= self.stink_decay()

    def stink_decay(self):
        stink_decay = DECAY_MULTIPLIER * self.stink
        return stink_decay