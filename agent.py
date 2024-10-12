from building import Building
import random
import map 

PERSON_SPEED = 2.0
STINK_INCREASE = 0.001
BUILDING_STINK_MULTIPLIER = 0.01

bo_to_lib = [(55.873498, -4.292804), 
                (55.873311, -4.293180), 
                (55.873010, -4.292456), 
                (55.872712, -4.291050), 
                (55.872530, -4.289391),
                (55.872807, -4.288762),
                (55.873128, -4.288531),
                (55.873342, -4.288400)]

lib_to_rr = [(55.873323, -4.288474), 
                (55.873102, -4.288537), 
                (55.873065, -4.288317), 
                (55.872884, -4.288315), 
                (55.872674, -4.288206), 
                (55.872520, -4.288044)]

rr_to_bo = [(55.872346, -4.288193),
            (55.872452, -4.289079),
            (55.872521, -4.289712),
            (55.872681, -4.290329),
            (55.872889, -4.290934),
            (55.873012, -4.291090),
            (55.873137, -4.291259),
            (55.873302, -4.291524),
            (55.873751, -4.292348)]   
        
paths = {
    "boyd orr library": bo_to_lib,
    "library boyd orr": bo_to_lib.reverse(),
    "library reading room": lib_to_rr,
    "reading room library": lib_to_rr.reverse(),
    "rr bo": rr_to_bo,
    "bo rr": rr_to_bo.reverse()
}

class Agent():
    def __init__(self, name: str, course: str, stink_threshold: float, stink_awareness: float, building_preferences: tuple, stink=0.0, path=[]):
        self.name = name
        self.course = course
        self.stink_threshold = stink_threshold
        self.stink_awareness = stink_awareness

        self.time_studied = 0.0
        self.stink = stink
        self.path = []

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
            perceieved_stink = max(self.current_location.stink - self.stink, 0)
            print(f"stink of {self.current_location.name}: {self.current_location.stink}")
            print(f"perceived stink: {perceieved_stink}")
            if perceieved_stink > self.stink_threshold:
                self.target_location = self.get_next_location()
                self.path = self.get_path(self.current_location, self.target_location)
                # walk along path to location
                return
            else:
                self.time_studied += 1

    def get_next_location(self) -> Building:
        return random.choices(self.building_preferences[0], self.building_preferences[1], k=1)[0]

    def move(self):
        self.current_location = self.target_location

    def get_path(self, start, end):
        path_key = start + " " + end  
        return paths[path_key]
