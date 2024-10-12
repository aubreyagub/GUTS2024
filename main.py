from agent import Agent
from building import Building
from map import Map

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


def main():

    buildings = []
    boyd_orr = Building("boyd orr", 10)  # , has_shower=True)
    library = Building("library", 16)
    reading_room = Building("reading room", 15)
    shadow_realm = Building("shadow_realm", math.inf)
    buildings.append(boyd_orr)
    buildings.append(library)
    buildings.append(reading_room)
    buildings.append(shadow_realm)

    STUDENT_PREFERENCES = {
        "CS": ([boyd_orr, library, reading_room, shadow_realm], [0.6, 0.3, 0.1, 0.0]),
        "History": ([boyd_orr, library, reading_room, shadow_realm], [0.1, 0.3, 0.6, 0.0]),
    }

    agents = []
    agents.append(Agent("Jordan", "CS", STUDENT_PREFERENCES["CS"], 1.0))
    agents.append(Agent("John", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Johan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jordan2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("John2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb2", "CS", STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie2", "History", STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan2", "CS", STUDENT_PREFERENCES["CS"]))

    map = Map(agents, buildings)

    # MATPLOTLIB STUFF BELOW

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-1, len(buildings))
    ax.set_ylim(-1, len(agents))
    ax.set_xticks(range(len(buildings)))
    ax.set_xticklabels(
        [f"{building.name}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings])
    ax.set_yticks(range(len(agents)))
    ax.set_yticklabels([agent.name for agent in agents])
    ax.set_xlabel("Buildings")
    ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")

    # Secondary y-axis for bar chart of stink levels
    ax2 = ax.twinx()
    ax2.set_ylim(0, 1)
    ax2.set_ylabel("Building Stink Level")
    bars = ax2.bar(range(len(buildings)), [
                   building.stink for building in buildings], color='red', alpha=0.6, width=0.4)

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
            [f"{building.name}: {len(map.get_building_occupancies().get(building, []))}" for building in buildings])
        ax.set_title(f"TOTAL STINK: {round(map.get_total_stink(), 3)}")
        for i, agent in enumerate(agents):
            # Append the x and y positions for plotting
            x_data.append(buildings.index(agent.current_location))
            y_data.append(i)

        ax.set_xlabel(f"{frame}")

        # Update scatter plot data
        scat.set_offsets(list(zip(x_data, y_data)))

        # Update the bar heights to reflect current stink levels
        for j, building in enumerate(buildings):
            bars[j].set_height(building.stink)

        return (scat, *bars)

    print("STARTING SIMULATION\n\n")

    # Create animation
    ani = animation.FuncAnimation(
        fig, plot_update, frames=480, interval=5, blit=False)

    plt.show()


if __name__ == "__main__":
    main()
