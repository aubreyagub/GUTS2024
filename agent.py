from building import Building
from degrees import Degree
import numpy as np
import random
import math
from enums import BuildingName
import paths

PERSON_SPEED = 2.0

def clamp(n, min=0, max=1):
        if n < min:
            return min
        elif n > max:
            return max
        else:
            return n
class Agent():
    def __init__(self, name: str, degree: Degree, buildings, stink=0.0, poi = False):
        self.name = name
        self.degree = degree
        self.buildings = buildings
        self.poi = poi

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
        # self.walk_time_remaining = 0

        self.path = []
        self.target_coordinate = starting_location.coordinate
        self.current_coordinate = starting_location.coordinate
    
    def take_a_shower(self):
        self.stink = 0

    def update(self):
        self.time_in_building += 1
        self.stink += self.natural_stink_rate

        if self.current_location != self.target_location:
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
                self.path = self.get_path(self.current_location.name, self.target_location.name)
                # print(f"{self.name} is moving from {self.current_location.name} to {self.target_location.name}")
                while self.target_location.fullness == 1:
                    self.target_location = self.get_next_location()
            else:
                self.time_studied += 1

    def get_next_location(self) -> Building:
        building_name = random.choices(list(self.buildings.keys()), self.building_preferences.values(), k=1)[0]
        return self.buildings[building_name]
    
    # def move(self):
    #     self.current_location = self.buildings[BuildingName.SHADOW_REALM]
    #     self.time_in_building = 0
    #     self.walk_time_remaining = 10

    def move(self):
        self.current_location = self.buildings[BuildingName.SHADOW_REALM]
        if len(self.path) > 1:
            self.current_coordinate = self.path.pop(0)
        elif len(self.path) == 1:
            self.current_coordinate = self.path.pop()
        else:
            # place agent in a random location in the building
            building_entrance_coord = self.target_location.coordinate
            self.current_coordinate = self.randomise_coordinate(building_entrance_coord)
            self.current_location = self.target_location

    def get_path(self, start, end):
        path_key = (start,end)
        if path_key in paths.paths:  
            return paths.paths[path_key].copy()
        else:
            # print(f"Path not found between {start} and {end}")
            return []

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

    def randomise_coordinate(self,coord):
        # Unpack latitude and longitude
        lat, lon = coord
        
        # Modify the last two decimal places directly
        new_lat = round(lat + random.uniform(-0.0003, 0.0003), 6)
        new_lon = round(lon + random.uniform(-0.0005, 0.0005), 6)
        
        return (new_lat, new_lon)