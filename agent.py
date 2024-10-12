from building import Building
from distributions import *
import numpy as np
import random

PERSON_SPEED = 2.0

class Agent():
    def __init__(self, name: str, course: str, building_preferences: tuple, stink=0.0):
        self.name = name
        self.course = course
        self.stink_threshold = generate_stink_threshold(course)
        self.natural_stink_rate = generate_natural_stink_rate(course)
        self.max_natural_stink = generate_max_natural_stink(course)
        self.stink_factor = generate_stink_factor(course)

        self.time_studied = 0.0
        self.stink = stink

        self.building_preferences = building_preferences

        starting_location = self.get_next_location()
        self.target_location = starting_location
        self.current_location = starting_location
        self.time_in_building = 0
        self.walk_time_remaining = 0

    def update(self):
        self.time_in_building += 1

        # Update natural stink
        self.stink = min(self.stink + self.natural_stink_rate, self.max_natural_stink)

        if self.time_in_building > 18:
            self.target_location = self.get_next_location()

        if self.current_location != self.target_location:
            self.move()
            return
        else:
            self.stink += self.stink_factor * self.current_location.stink

            # Keep stink capped between 0 and 1
            self.stink = min(self.stink, 1.0)


            # Check if the agent perceives the building stink as unpleasant
            perceived_stink = self.current_location.stink - self.stink

            # If the building stink is higher than the agent's stink, they notice it
            if perceived_stink > 0 and self.current_location.stink > self.stink_threshold and self.time_in_building > self.stink_threshold*10:
                self.target_location = self.get_next_location()
                return
            else:
                self.time_studied +=1
                return

    def get_next_location(self) -> Building:
        return random.choices(self.building_preferences[0], self.building_preferences[1], k=1)[0]

    def move(self):
        self.current_location = self.target_location
        self.time_in_building = 0