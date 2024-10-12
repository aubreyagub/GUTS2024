from building import Building
import random

boyd_orr = Building("boyd orr")
library = Building("library")
reading_room = Building("reading room")

PERSON_SPEED = 2.0
STINK_INCREASE = 0.001
BUILDING_STINK_MULTIPLIER = 0.1
STUDENT_PREFERENCES = {
    "CS": ([boyd_orr, library, reading_room], [0.6, 0.3, 0.1]),
    "History": ([boyd_orr, library, reading_room], [0.1, 0.3, 0.6]),

}

class Agent:
    def __init__(self, name: str, course: str, stink_threshold: float, stink_awareness: float, stink=0.0):
        self.name = name
        self.course = course
        self.stink_threshold = stink_threshold
        self.stink_awareness = stink_awareness

        self.time_studied = 0.0
        self.stink = stink

        starting_location = self.get_next_location()
        self.target_location = starting_location
        self.current_location = starting_location

    def update(self):
        temp_stink = self.stink
        self.stink = self.stink + (STINK_INCREASE + (self.current_location.stink*BUILDING_STINK_MULTIPLIER))
        self.current_location.update_building_stink(temp_stink*BUILDING_STINK_MULTIPLIER)

        if self.current_location != self.target_location:
            self.move()
            return
        else:
            # consider stink level
            if self.current_location.stink > self.stink_threshold:
                self.target_location = self.get_next_location()
                return
            else:
                self.time_studied += 1

    def get_next_location(self):
        return random.choices(STUDENT_PREFERENCES[self.course][0], STUDENT_PREFERENCES[self.course][1], k=1)[0]

    def move(self):
        self.current_location = self.target_location