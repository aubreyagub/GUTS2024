from agent import Agent
from flask import Flask, render_template, jsonify, request
from building import Building
from map import Map
from enum import Enum
import random
from degrees import *
import requests
from copy import deepcopy
from flask import Flask
from flask_socketio import SocketIO, emit
import threading

from frontend.maptiler_key import MAPTILER_KEY

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

import time

DEBUG = False
STUDENT_COUNT = 50
PORT = 5000
student_id_counter = 0

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('simulation.html', maptiler_key=MAPTILER_KEY, active_page='simulation')

@app.route('/formulae')
def formulae():
    return render_template('formulae.html', active_page='formulae')

def generate_student(buildings):
    name = "A"
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)

def main():
    buildings = {
        BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR,(55.873498, -4.292804), 15),  # , has_shower=True),
        BuildingName.JMS: Building(BuildingName.JMS, (55.873150, -4.292460), 10),
        BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING,(55.873218, -4.288445), 10),
        BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, (55.872346, -4.288193), 10),
        # BuildingName.ASBS: Building(BuildingName.ASBS, (), 10),
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, (55.873323, -4.288474), 25),
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM, (0, 0), math.inf)
    }

    agents = [generate_student(buildings) for i in range(STUDENT_COUNT-1)]
    agents.append(Agent("STINKY MCGEE", ComputerScience, buildings, stink=0.5, poi=True))

    map = Map(agents, buildings)
    # MATPLOTLIB STUFF BELOW
    if DEBUG:
        # Scatter Map Visualisation 

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title("Agent Movement Simulation")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        
        # Set plot boundaries (adjust based on actual coordinates)
        ax.set_xlim(-4.295, -4.285)
        ax.set_ylim(55.870, 55.875)
        
        # Plot buildings as fixed points
        for building in buildings.values():
            # print(building.name)
            if building.name != BuildingName.SHADOW_REALM: # do not display shadow realm on map as it is not a single point
                ax.plot(building.coordinate[1], building.coordinate[0], "ro", markersize=8, label=building.name)

        # Initialize scatter plot for agents
        agent_scatter = ax.scatter([], [], s=50, c='blue', label='Agents')

        # Update function for animation
        def plot_update(frame):
            map.update()
            
            # Get agent locations for this frame
            x_data, y_data = [], []
            for agent in agents:
                lon, lat = agent.current_coordinate[1], agent.current_coordinate[0]
                x_data.append(lon)
                y_data.append(lat)
            
            # Update scatter plot data
            agent_scatter.set_offsets(list(zip(x_data, y_data)))
            
            return agent_scatter,

        map = Map(agents, buildings)

        print("STARTING SIMULATION\n\n")

        # Create animation
        ani = animation.FuncAnimation(fig, plot_update, frames=1000, interval=100, blit=True)

        plt.legend(loc="lower left")
        plt.show()

    else:
        # SEND POST REQUESTS
        # tick_count = int(input("How many ticks? "))
        tick_count = 480
        print(f"Simulating {tick_count} ticks")
        simulation = []

        for i in range(tick_count):
            map.update()
            simulation.append({"agents": deepcopy(agents), "buildings": deepcopy(buildings), "tick_count": i})

        print(f"Simulation complete. {len(simulation)} ticks recorded")

        time.sleep(5)

        for i in range(len(agents)):
            agent = simulation[0]["agents"][i]
            socketio.emit('new_student', {
                'student_id': int(i), 
                'lat': float(agent.current_coordinate[0]), 
                'lng': float(agent.current_coordinate[1]), 
                'name': str(agent.name), 
                'stinkLevel': float(round(agent.stink, 3)), 
                'poi': bool(agent.poi)
            })

        for tick in simulation[1:]:
            # do post requests
            for i, agent in enumerate(tick["agents"]):
                socketio.emit('update_student', {
                    'student_id': int(i), 
                    'lat': float(agent.current_coordinate[0]), 
                    'lng': float(agent.current_coordinate[1]), 
                    'stinkLevel': float(round(agent.stink, 3)), 
                    'poi': bool(agent.poi)
                })

            for i,building in enumerate(tick["buildings"].values()):
                print(f"Emitting building update for {building.name.value}, Stink Level: {building.stink}")

                socketio.emit('update_building', {
                    'building_id': i,
                    'buildingName': str(building.name.value),
                    'lat': float(building.coordinate[0]),
                    'lng': float(building.coordinate[1]),
                    'stinkLevel': float(round(building.stink, 3)),
                    'capacity': str(building.capacity),
                    'tick' : int(tick["tick_count"]),
                    'fullness' : float(building.fullness)
                })

            time.sleep(0.5)

if __name__ == "__main__":
    simulation_thread = threading.Thread(target=main)
    simulation_thread.daemon = True  # Ensures thread exits when main program exits
    simulation_thread.start()

    socketio.run(app, debug=False, port=PORT)