from agent import Agent
from building import Building
from map import Map
from degrees import *
import random
from copy import deepcopy
import requests

from frontend.maptiler_key import MAPTILER_KEY

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

import json

import time

STUDENT_COUNT = 50

def generate_student(buildings):
    name = "A"
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)

def main():
    buildings = {
        BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR,(55.8736, -4.2929), 15),  # , has_shower=True), #
        BuildingName.JMS: Building(BuildingName.JMS, (55.873204, -4.292221), 10), #
        BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING,(55.873109, -4.287863), 10), #
        BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, (55.872737, -4.287961), 10), # 
        BuildingName.ASBS: Building(BuildingName.ASBS, (55.870620, -4.296032), 10), #
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, (55.873611, -4.292889), 25), # 
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM, (0, 0), math.inf)
    }

    agents = [generate_student(buildings) for i in range(STUDENT_COUNT-1)]
    agents.append(Agent("STINKY MCGEE", ComputerScience, buildings, stink=0.5, poi=True))

    map = Map(agents, buildings)

    # SEND POST REQUESTS
    # tick_count = int(input("How many ticks? "))
    tick_count = 480
    print(f"Simulating {tick_count} ticks")
    simulation = []

    for i in range(tick_count):
        map.update()
        simulation.append({"agents": deepcopy(agents), 
                            "buildings": deepcopy(buildings),
                            "tick_count": i,
                            "total_study_time": deepcopy(map.total_study_time)
                            })

    print(f"Simulation complete. {len(simulation)} ticks recorded")

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


    # for tick in simulation[1:]:
    #     # do post requests
    #     for i, agent in enumerate(tick["agents"]):
    #         socketio.emit('update_student', {
    #             'student_id': i, 
    #             'lat': agent.current_coordinate[0], 
    #             'lng': agent.current_coordinate[1], 
    #             'stinkLevel': agent.stink, 
    #             'poi': agent.poi,
    #             'time_studied': agent.time_studied
    #         })

    #     for i,building in enumerate(tick["buildings"].values()):
    #         socketio.emit('update_building', {
    #             'building_id': i,
    #             'buildingName': building.name.value,
    #             'lat': building.coordinate[0],
    #             'lng': building.coordinate[1],
    #             'stinkLevel': building.stink,
    #             'capacity': building.capacity,
    #             'tick' : tick["tick_count"]
    #         })

        #time.sleep(0.25)

if __name__ == "__main__":
    main()