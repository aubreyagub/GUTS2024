from agent import Agent
from building import Building
from map import Map
from enum import Enum
import random
from degrees import *

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

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
        BuildingName.ASBS: Building(BuildingName.ASBS, (55.870739, -4.295667), 10),
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, (55.873323, -4.288474), 25),
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM,(), math.inf)
    }

    agents = [generate_student(buildings) for i in range(30)]

    map = Map(agents, buildings)
    # MATPLOTLIB STUFF BELOW
    # Scatter Map Visualisation 

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Agent Movement Simulation")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    
    # Set plot boundaries (adjust based on actual coordinates)
    ax.set_xlim(-4.297, -4.285)
    ax.set_ylim(55.870, 55.875)
    
    # Plot buildings as fixed points
    for building in buildings.values():
        print(building.name)
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


    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.set_xlim(-1, len(buildings))
    # ax.set_ylim(-1, len(agents))
    # ax.set_xticks(range(len(buildings)))
    # ax.set_xticklabels(
    #     [f"{building.name.value}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings.values()])
    # ax.set_yticks(range(len(agents)))
    # ax.set_yticklabels([agent.name for agent in agents])
    # ax.set_xlabel("Buildings")
    # ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")

    # # Secondary y-axis for bar chart of stink levels
    # ax2 = ax.twinx()
    # ax2.set_ylim(0, 1)
    # ax2.set_ylabel("Building Stink Level")
    # bars = ax2.bar(range(len(buildings)), [
    #                building.stink for building in buildings.values()], color='red', alpha=0.6, width=0.4)

    # # Initialize scatter plot for agents
    # agent_scatter = ax.scatter([], [], s=50, c='blue', label='Agents')

    # # Update function for animation
    # def plot_update(frame):
    #     if frame % 480 == 0:
    #         map.clean()

    #     map.update()
    #     # Move each agent to a new random building
    #     x_data = []
    #     y_data = []
    #     ax.set_xticklabels(
    #         [f"{building.name.value}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings.values()])
    #     ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")
    #     for i, agent in enumerate(agents):
    #         # Append the x and y positions for plotting
    #         x_data.append(list(buildings.keys()).index(agent.current_location.name))
    #         y_data.append(i)

    #     ax.set_xlabel(f"{frame}")

    #     # Update scatter plot data
    #     agent_scatter.set_offsets(list(zip(x_data, y_data)))

    #     # Update the bar heights to reflect current stink levels
    #     for j, building in enumerate(buildings.values()):
    #         bars[j].set_height(building.stink)

    #     return (agent_scatter, *bars)

    # map = Map(agents, buildings)

    # print("STARTING SIMULATION\n\n")

    # # Create animation
    # ani = animation.FuncAnimation(
    #     fig, plot_update, frames=480, interval=5, blit=False)

    # plt.legend(loc="lower left")
    # plt.show()

if __name__ == "__main__":
    main()
