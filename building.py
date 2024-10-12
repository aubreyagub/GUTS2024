import random

class Building:
    def __init__(self, name):
        self.name = name
        self.stink = 0

    def update_building_stink(self, stink_increase):
        self.stink += stink_increase