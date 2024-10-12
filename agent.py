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
        self.stink += self.natural_stink_rate

        if self.current_location != self.target_location:
            self.move()
        else:
            self.stink += self.stink_factor * self.current_location.stink

            # Keep stink capped between 0 and 1
            self.stink = min(self.stink, 1.0)

            # Check if the agent perceives the building stink as unpleasant
            perceived_stink = self.current_location.stink - self.stink

            # If the building stink is higher than the agent's stink, they notice it
            if perceived_stink > 0 and self.current_location.stink > self.stink_threshold and self.time_in_building > self.stink_threshold*20:
                self.target_location = self.get_next_location()
            else:
                self.time_studied +=1

            shower_p = random.randrange(1,10)
            if shower_p == 1 and self.current_location.has_shower:
                self.stink = 0

    def get_next_location(self) -> Building:
        return random.choices(self.building_preferences[0], self.building_preferences[1], k=1)[0]

    def move(self):
        self.current_location = self.target_location
        self.time_in_building = 0