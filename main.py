from agent import Agent
from building import Building
from map import Map
from enum import Enum
import random
from degrees import *
import requests
from copy import deepcopy

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

DEBUG = False
STUDENT_COUNT = 250
URL = "192.168.1.253"
PORT = "3069"

def generate_student(buildings):
    name = "A"
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)

def main():
    buildings = {
        BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR, 0.15*STUDENT_COUNT),  # , has_shower=True),
        BuildingName.JMS: Building(BuildingName.JMS, 0.2*STUDENT_COUNT, rate=0.00001, has_shower=True),
        BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING, 0.1*STUDENT_COUNT),
        BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, 0.1*STUDENT_COUNT),
        BuildingName.ASBS: Building(BuildingName.ASBS, 0.15*STUDENT_COUNT),
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, 0.3*STUDENT_COUNT),
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM, math.inf)
    }

    agents = [generate_student(buildings) for i in range(STUDENT_COUNT-1)]
    agents.append(Agent("STINKY MCGEE", ComputerScience, buildings, stink=0.0))

    map = Map(agents, buildings)

    # MATPLOTLIB STUFF BELOW
    if DEBUG:

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(-1, len(buildings))
        ax.set_ylim(-1, len(agents))
        ax.set_xticks(range(len(buildings)))
        ax.set_xticklabels(
            [f"{building.name.value}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings.values()])
        ax.set_yticks(range(len(agents)))
        ax.set_yticklabels([agent.name for agent in agents])
        ax.set_xlabel("Buildings")
        ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")

        # Secondary y-axis for bar chart of stink levels
        ax2 = ax.twinx()
        ax2.set_ylim(0, 1)
        ax2.set_ylabel("Building Stink Level")
        bars = ax2.bar(range(len(buildings)), [
                    building.stink for building in buildings.values()], color='red', alpha=0.6, width=0.4)

        # Initialize scatter plot
        scat = ax.scatter([], [], s=100, c='blue')

        # Update function for animation
        def plot_update(frame):
            if frame % 480 == 0:
                map.clean()

            map.update()
            # Move each agent to a new random building
            x_data = []
            y_data = []
            ax.set_xticklabels(
                [f"{building.name.value}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings.values()])
            ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")
            for i, agent in enumerate(agents):
                # Append the x and y positions for plotting
                x_data.append(list(buildings.keys()).index(agent.current_location.name))
                y_data.append(i)

            ax.set_xlabel(f"{frame}")

            # Update scatter plot data
            scat.set_offsets(list(zip(x_data, y_data)))

            # Update the bar heights to reflect current stink levels
            for j, building in enumerate(buildings.values()):
                bars[j].set_height(building.stink)

            return (scat, *bars)

        print("STARTING SIMULATION\n\n")

        # Create animation
        ani = animation.FuncAnimation(
            fig, plot_update, frames=480, interval=100, blit=False)

        plt.show()

    else:
        # SEND POST REQUESTS
        tick_count = int(input("How many ticks? "))
        print(f"Simulating {tick_count} ticks")
        simulation = []

        for i in range(tick_count):
            map.update()
            simulation.append({"agents": deepcopy(agents), "buildings": deepcopy(buildings)})

        print(f"Simulation complete. {len(simulation)} ticks recorded")

        # do post requests
        endpoint = f"{URL}:{PORT}"
        data = {

        }
        requests.post(endpoint, json=data)

if __name__ == "__main__":
    main()
