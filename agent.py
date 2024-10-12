from building import Building
import random
import paths

PERSON_SPEED = 2.0

class Agent():
    def __init__(self, name: str, course: str, stink_threshold: float, building_preferences: tuple, stink=0.0):
        self.name = name
        self.course = course
        self.stink_threshold = stink_threshold
        self.natural_stink_rate = 0.03
        self.max_natural_stink = 0.3
        self.stink_factor = 0.5

        self.time_studied = 0.0
        self.stink = stink

        self.building_preferences = building_preferences

        starting_location = self.get_next_location()
        self.target_location = starting_location
        self.current_location = starting_location

        self.path = []
        self.target_coordinate = starting_location.coordinate
        self.current_coordinate = starting_location.coordinate

    def update(self):
        # Update natural stink
        self.stink = min(self.stink + self.natural_stink_rate, self.max_natural_stink)

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
            if perceived_stink > 0 and self.current_location.stink > self.stink_threshold:
                self.target_location = self.get_next_location()
                self.path = get_path(self.current_location.name, self.target_location.name)
                print(f"{self.name} is moving from {self.current_location.name} to {self.target_location.name}")
                return
            else:
                self.time_studied +=1
                return

    def get_next_location(self) -> Building:
        return random.choices(self.building_preferences[0], self.building_preferences[1], k=1)[0]

    def move(self):
        if len(self.path) > 1:
            self.current_coordinate = self.path.pop(0)
        elif len(self.path) == 1:
            self.current_coordinate = self.path.pop()
            self.current_location = self.target_location
        else:
            print("Path is empty")
            return


def get_path(start, end):
        path_key = (start,end)
        if path_key in paths.paths:  
            return paths.paths[path_key].copy()
        else:
            print(f"Path not found between {start} and {end}")
            return []