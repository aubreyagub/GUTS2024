from building import Building
import random

PERSON_SPEED = 2.0
STINK_INCREASE = 0.001
BUILDING_STINK_MULTIPLIER = 0.01

class Agent():
    def __init__(self, name: str, course: str, stink_threshold: float, stink_awareness: float, building_preferences: tuple, stink=0.0):
        self.name = name
        self.course = course
        self.stink_threshold = stink_threshold
        self.stink_awareness = stink_awareness

        self.time_studied = 0.0
        self.stink = stink

        self.building_preferences = building_preferences

        starting_location = self.get_next_location()
        self.target_location = starting_location
        self.current_location = starting_location

    def update(self):
        self.stink = self.stink + (STINK_INCREASE + (self.current_location.stink*BUILDING_STINK_MULTIPLIER))

        if self.current_location != self.target_location:
            self.move()
            return
        else:
            # consider stink level
            perceieved_stink = self.current_location.stink - self.stink*BUILDING_STINK_MULTIPLIER
            if perceieved_stink > self.stink_threshold:
                self.target_location = self.get_next_location()
                return
            else:
                self.time_studied += 1

    def get_next_location(self) -> Building:
        return random.choices(self.building_preferences[0], self.building_preferences[1], k=1)[0]

    def move(self):
        print(f"{self.name} has decided to move to {self.target_location.name}")
        self.current_location = self.target_location