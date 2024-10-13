from enums import BuildingName
from enum import Enum

class Degree:
    STINK_THRESHOLD_DISTRIBUTION = NotImplementedError
    NATURAL_STINK_RATE_DISTRIBUTION = NotImplementedError
    STINK_FACTOR_DISTRIBUTION = NotImplementedError
    BUILDING_PREFERENCE = NotImplementedError

class ComputerScience(Degree):
    STINK_THRESHOLD_DISTRIBUTION = (0.5, 0.2)
    NATURAL_STINK_RATE_DISTRIBUTION = (0.002, 0.0002)
    STINK_FACTOR_DISTRIBUTION = (0.002, 0.0001)
    BUILDING_PREFERENCE = {
        BuildingName.BOYD_ORR: 0.6,
        BuildingName.JMS: 0.0,
        BuildingName.FRASER_BUILDING: 0.0,
        BuildingName.READING_ROOM: 0.1,
        # BuildingName.ASBS: 0.0,
        BuildingName.LIBRARY: 0.3,
        BuildingName.SHADOW_REALM: 0.0
    }

    def __str__(self):
        return "Computer Science"

class Business(Degree):
    STINK_THRESHOLD_DISTRIBUTION = (0.2, 0.1)
    NATURAL_STINK_RATE_DISTRIBUTION = (0.0002, 0.0001)
    STINK_FACTOR_DISTRIBUTION = (0.001, 0.0001)
    BUILDING_PREFERENCE = {
        BuildingName.BOYD_ORR: 0.1,
        BuildingName.JMS: 0.0,
        BuildingName.FRASER_BUILDING: 0.0,
        BuildingName.READING_ROOM: 0.6,
        # BuildingName.ASBS: 0.0,
        BuildingName.LIBRARY: 0.3,
        BuildingName.SHADOW_REALM: 0.0
    }

    def __str__(self):
        return "Business"

class History(Degree):
    STINK_THRESHOLD_DISTRIBUTION = (0.3, 0.1)
    NATURAL_STINK_RATE_DISTRIBUTION = (0.0003, 0.0001)
    STINK_FACTOR_DISTRIBUTION = (0.001, 0.0001)
    BUILDING_PREFERENCE = {
        BuildingName.BOYD_ORR: 0.0,
        BuildingName.JMS: 0.2,
        BuildingName.FRASER_BUILDING: 0.1,
        BuildingName.READING_ROOM: 0.4,
        BuildingName.READING_ROOM: 0.6,
        # BuildingName.ASBS: 0.0,
        BuildingName.LIBRARY: 0.3,
        BuildingName.SHADOW_REALM: 0.0
    }

    def __str__(self):
        return "History"

class DegreeTitle(Enum):
    # MATHS = "Mathematics"
    COMPUTER_SCIENCE = ComputerScience
    BUSINESS = Business
    # BIO = "Biology"
    # PHYSICS = "Physics"
    HISTORY = History
    # ENGLISH = "English"
    # MANDARIN = "Mandarin"
    # ENG = "Engineering"