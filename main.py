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
        BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR, 10),  # , has_shower=True),
        BuildingName.JMS: Building(BuildingName.JMS, 10),
        BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING, 10),
        BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, 15),
        BuildingName.ASBS: Building(BuildingName.ASBS, 20),
        BuildingName.LIBRARY: Building(BuildingName.LIBRARY, 16),
        BuildingName.SHADOW_REALM: Building(BuildingName.SHADOW_REALM, math.inf)
    }

    agents = [generate_student(buildings) for i in range(50)]

    map = Map(agents, buildings)
    agents.append(Agent("Jordan", "CS", 0.7, STUDENT_PREFERENCES["CS"], 1.0))
    agents.append(Agent("John", "History", 0.3, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", 0.8, STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", 0.2, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", 0.7, STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Anna", "CS", 0.7, STUDENT_PREFERENCES["CS"], 1.0))
    agents.append(Agent("Amy", "History", 0.3, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Alex", "CS", 0.8, STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Arya", "History", 0.2, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Ali", "CS", 0.7, STUDENT_PREFERENCES["CS"]))

    # MATPLOTLIB STUFF BELOW

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

    # Initialize scatter plot for agents
    agent_scatter = ax.scatter([], [], s=50, c='blue', label='Agents')

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

    map = Map(agents, buildings)

    print("STARTING SIMULATION\n\n")

    # Create animation
    ani = animation.FuncAnimation(
        fig, plot_update, frames=480, interval=5, blit=False)

    plt.legend(loc="lower left")
    plt.show()

    # Bar Charts Visualisation

    # fig,ax = plt.subplots(figsize=(8, 6))
    # ax.set_xlim(-1, len(buildings))
    # ax.set_ylim(-1, len(agents))
    # ax.set_xticks(range(len(buildings)))
    # ax.set_xticklabels([building.name for building in buildings])
    # ax.set_yticks(range(len(agents)))
    # ax.set_yticklabels([agent.name for agent in agents])
    # ax.set_xlabel("Buildings")
    # ax.set_title("Agent Movement Simulation")

    # # Secondary y-axis for bar chart of stink levels
    # ax2 = ax.twinx()
    # ax2.set_ylim(0, 1)
    # ax2.set_ylabel("Building Stink Level")
    # bars = ax2.bar(range(len(buildings)), [building.stink for building in buildings], color='red', alpha=0.6, width=0.4)

    # Initialize scatter plot
    scat = ax.scatter([], [], s=100, c='blue')
    # # Update function for animation
    # def plot_update(frame):
    #     map.update()
    #     # Move each agent to a new random building
    #     x_data = []
    #     y_data = []
    #     for i, agent in enumerate(agents):
    #         # Append the x and y positions for plotting
    #         x_data.append(buildings.index(agent.current_location))
    #         y_data.append(i)

    #     # Update scatter plot data
    #     scat.set_offsets(list(zip(x_data, y_data)))

    #     # Update the bar heights to reflect current stink levels
    #     for j, building in enumerate(buildings):
    #         bars[j].set_height(building.stink)

    #     return (scat, *bars)

    # map = Map(agents, buildings)

    # print("STARTING SIMULATION\n\n")

    # # Create animation
    # ani = animation.FuncAnimation(fig, plot_update, frames=1000, interval=100, blit=True)

    # plt.show()

if __name__ == "__main__":
    main()
