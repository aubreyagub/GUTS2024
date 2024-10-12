from building import Building
import random

PERSON_SPEED = 2.0

bo_to_lib = [(55.873498, -4.292804), 
                (55.873311, -4.293180), 
                (55.873010, -4.292456),
                (55.872712, -4.291050), 
                (55.872530, -4.289391),
                (55.872807, -4.288762),
                (55.873128, -4.288531),
                (55.873323, -4.288474)]

lib_to_rr = [(55.873323, -4.288474), 
                (55.873102, -4.288537), 
                (55.873065, -4.288317), 
                (55.872884, -4.288315), 
                (55.872674, -4.288206), 
                (55.872346, -4.288193)]

rr_to_bo = [(55.872346, -4.288193),
            (55.872452, -4.289079),
            (55.872521, -4.289712),
            (55.872681, -4.290329),
            (55.872889, -4.290934),
            (55.873012, -4.291090),
            (55.873137, -4.291259),
            (55.873302, -4.291524),
            (55.873498, -4.292804)] 

bo_to_fraser = [(55.873498, -4.292804), 
                (55.873311, -4.293180), 
                (55.873010, -4.292456),
                (55.872712, -4.291050), 
                (55.872530, -4.289391),
                (55.872807, -4.288762),
                (55.873128, -4.288531),
                (55.873218, -4.288445)]

lib_to_fraser = [(55.873323, -4.288474),(55.873218, -4.288445)]  

fraser_to_rr =  [(55.873218, -4.288445),
                (55.873102, -4.288537), 
                (55.873065, -4.288317), 
                (55.872884, -4.288315), 
                (55.872674, -4.288206), 
                (55.872346, -4.288193)]


        
paths = {
    ("boyd orr", "library"): bo_to_lib,
    ("library", "boyd orr"): bo_to_lib[::-1],
    ("library", "reading room"): lib_to_rr,
    ("reading room", "library"): lib_to_rr[::-1],
    ("reading room", "boyd orr"): rr_to_bo,
    ("boyd orr", "reading room"): rr_to_bo[::-1],
    ("library", "fraser building"): lib_to_fraser,
    ("fraser building", "library"): lib_to_fraser[::-1],
    ("boyd orr", "fraser building"): bo_to_fraser,
    ("fraser building", "boyd orr"): bo_to_fraser[::-1],
    ("boyd orr", "boyd orr"): [(55.873498, -4.292804)],
    ("library", "library"): [(55.873323, -4.288474)],
    ("reading room", "reading room"): [(55.872346, -4.288193)],
    ("fraser building", "fraser building"): [(55.873218, -4.288445)]
}

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
                print(f"Path: {self.path}")
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
        if path_key in paths:  
            return paths[path_key].copy()
        else:
            print(f"Path not found between {start} and {end}")
            return []