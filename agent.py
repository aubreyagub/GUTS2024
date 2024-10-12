from building import Building
from degrees import Degree
import numpy as np
import random
import math
from enums import BuildingName

PERSON_SPEED = 2.0

def clamp(n, min=0, max=1):
        if n < min:
            return min
        elif n > max:
            return max
        else:
            return n
class Agent():
    def __init__(self, name: str, degree: Degree, buildings, stink=0.0):
        self.name = name
        self.degree = degree
        self.buildings = buildings

        self.stink_threshold = self.generate_stink_threshold()
        self.natural_stink_rate = self.generate_natural_stink_rate()
        self.stink_factor = self.generate_stink_factor()

        self.time_studied = 0.0
        self.stink = stink

        self.building_preferences = degree.BUILDING_PREFERENCE

        starting_location = self.get_next_location()
        self.target_location = starting_location
        self.current_location = starting_location
        self.time_in_building = 0
        self.walk_time_remaining = 0

    
    def take_a_shower(self):
        self.stink = 0

    def update(self):
        self.time_in_building += 1
        self.stink += self.natural_stink_rate

        # If you are in the shadow realm...
        if self.current_location.name == BuildingName.SHADOW_REALM:
            self.walk_time_remaining -= 1
            # If you have now finished walking, and your destination isn't full
            if self.walk_time_remaining <= 0 and self.target_location.fullness < 1:
                self.current_location = self.target_location
        # You are not in your target location but not in the shadow realm
        elif self.current_location != self.target_location:
            self.move()
        # You are in your target location
        else:
            # Get stinkier if you are less stinky than the building
            if self.current_location.stink > self.stink:
                self.stink += self.stink_factor * (1 / (1 + math.exp(self.stink - self.current_location.stink)))
            self.stink = min(self.stink, 1.0)

            # Check if the agent perceives the building stink as unpleasant
            perceived_stink = self.current_location.stink - self.stink
            if perceived_stink > 0 and self.current_location.stink > self.stink_threshold and self.time_in_building > self.stink_threshold*20:
                # TODO: if capacities don't add up this will crash!!!!!
                self.target_location = self.get_next_location()
                while self.target_location.fullness == 1:
                    self.target_location = self.get_next_location()
            else:
                self.time_studied += 1

            shower_p = random.randrange(1, 20)
            if shower_p == 1 and self.current_location.has_shower:
                self.stink = 0

    def get_next_location(self) -> Building:
        building_name = random.choices(list(self.buildings.keys()), self.building_preferences.values(), k=1)[0]
        return self.buildings[building_name]
    
    def move(self):
        self.current_location = self.buildings[BuildingName.SHADOW_REALM]
        self.time_in_building = 0
        self.walk_time_remaining = 10


    # Functions to randomly generate attributes
    def generate_stink_factor(self):
        stink_factor = np.random.normal(
            self.degree.STINK_FACTOR_DISTRIBUTION[0], self.degree.STINK_FACTOR_DISTRIBUTION[1])
        return clamp(stink_factor)

    def generate_natural_stink_rate(self):
        natural_stink_rate = np.random.normal(
            self.degree.NATURAL_STINK_RATE_DISTRIBUTION[0], self.degree.NATURAL_STINK_RATE_DISTRIBUTION[1])
        return clamp(natural_stink_rate)

    def generate_stink_threshold(self):
        stink_threshold = np.random.normal(
            self.degree.STINK_THRESHOLD_DISTRIBUTION[0], self.degree.STINK_THRESHOLD_DISTRIBUTION[1])
        return clamp(stink_threshold)
