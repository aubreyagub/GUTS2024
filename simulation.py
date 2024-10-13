from agent import Agent
from building import Building
from map import Map
from degrees import *
import random
from copy import deepcopy
import requests
import names

from frontend.maptiler_key import MAPTILER_KEY

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

import json

import time

STUDENT_COUNT = 50
simulation = []

buildings = {
        BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR,(55.873498, -4.292804), 15),  # , has_shower=True),
        BuildingName.JMS: Building(BuildingName.JMS, (55.873150, -4.292460), 10),
        BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING,(55.873218, -4.288445), 10),
        BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, (55.872346, -4.288193), 10),
        BuildingName.ASBS: Building(BuildingName.ASBS, (55.870739, -4.295667), 10),
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, (55.873323, -4.288474), 25),
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM, (0, 0), math.inf)
    }

def generate_student(buildings, name=""):
    if name == "":
        name = names.get_full_name()
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)

agents = [generate_student(buildings) for i in range(STUDENT_COUNT-1)]

def generate(student: Agent):
    agents.append(student)

    map = Map(agents, buildings)

    # SEND POST REQUESTS
    # tick_count = int(input("How many ticks? "))
    tick_count = 480
    print(f"Simulating {tick_count} ticks")

    for i in range(tick_count):
        map.update()
        simulation.append({"agents": deepcopy(agents), 
                            "buildings": deepcopy(buildings),
                            "tick_count": i,
                            "total_study_time": deepcopy(map.total_study_time)
                            })

    print(f"Simulation complete. {len(simulation)} ticks recorded")


def run():
    agent_json = []
    for agent in agents:
        agent_json.append({
            "current_coordinate": agent.current_coordinate,
            "name": agent.name,
            "stink": agent.stink,
            "poi": agent.poi
        })

    time.sleep(5)

    requests.post(
        'http://127.0.0.1:5000/add_students',
        json=agent_json
    )

    for tick in simulation[1:]:
        agent_json = []
        for agent in tick.get("agents", []):
            agent_json.append({
                "current_coordinate": agent.current_coordinate,
                "name": agent.name,
                "stink": agent.stink,
                "poi": agent.poi,
                "time_studied": agent.time_studied
            })
        requests.post(
        'http://127.0.0.1:5000/update_students',
        json=agent_json
        )

        building_json = []
        for building in tick.get("buildings", []).values():
            building_json.append({
                "name": building.name,
                "coordinate": building.coordinate,
                "stink": building.stink,
                "capacity": building.capacity,
                "tick": tick
            })

        time.sleep(0.25)