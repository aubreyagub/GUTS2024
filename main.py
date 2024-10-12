from agent import Agent
from building import Building
from map import Map

import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():

    buildings = []
    boyd_orr = Building("boyd orr", (55.873498, -4.292804))
    library = Building("library", (55.873323, -4.288474))
    reading_room = Building("reading room", (55.872346, -4.288193))
    buildings.append(boyd_orr)
    buildings.append(library)
    buildings.append(reading_room)

    STUDENT_PREFERENCES = {
    "CS": ([boyd_orr, library, reading_room], [0.6, 0.3, 0.1]),
    "History": ([boyd_orr, library, reading_room], [0.1, 0.3, 0.6]),
}

    agents = []
    agents.append(Agent("Jordan", "CS", 0.7, 0.3, STUDENT_PREFERENCES["CS"], 1.0))
    agents.append(Agent("John", "History", 0.3, 0.7, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Jeb", "CS", 0.8, 0.1, STUDENT_PREFERENCES["CS"]))
    agents.append(Agent("Jamie", "History", 0.2, 0.7, STUDENT_PREFERENCES["History"]))
    agents.append(Agent("Johan", "CS", 0.7, 0.1, STUDENT_PREFERENCES["CS"]))

    ### MATPLOTLIB STUFF BELOW

    fig,ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-1, len(buildings))
    ax.set_ylim(-1, len(agents))
    ax.set_xticks(range(len(buildings)))
    ax.set_xticklabels([building.name for building in buildings])
    ax.set_yticks(range(len(agents)))
    ax.set_yticklabels([agent.name for agent in agents])
    ax.set_xlabel("Buildings")
    ax.set_title("Agent Movement Simulation")

    # Secondary y-axis for bar chart of stink levels
    ax2 = ax.twinx()
    ax2.set_ylim(0, 10)
    ax2.set_ylabel("Building Stink Level")
    bars = ax2.bar(range(len(buildings)), [building.stink for building in buildings], color='red', alpha=0.6, width=0.4)

    # Initialize scatter plot
    scat = ax.scatter([], [], s=100, c='blue')

    # Update function for animation
    def plot_update(frame):
        map.update()
        # Move each agent to a new random building
        x_data = []
        y_data = []
        for i, agent in enumerate(agents):
            # Append the x and y positions for plotting
            x_data.append(buildings.index(agent.current_location))
            y_data.append(i)

        # Update scatter plot data
        scat.set_offsets(list(zip(x_data, y_data)))

        # Update the bar heights to reflect current stink levels
        for j, building in enumerate(buildings):
            bars[j].set_height(building.stink)

        return (scat, *bars)

    map = Map(agents, buildings)

    print("STARTING SIMULATION\n\n")

    # Create animation
    ani = animation.FuncAnimation(fig, plot_update, frames=1000, interval=100, blit=True)

    plt.show()

    # fig, ax = plt.subplots(figsize=(8, 8))
    # ax.set_title("Agent Movement Simulation")
    # ax.set_xlabel("Longitude")
    # ax.set_ylabel("Latitude")
    
    # # Set plot boundaries (adjust based on actual coordinates)
    # ax.set_xlim(-4.295, -4.285)
    # ax.set_ylim(55.870, 55.875)
    
    # # Plot buildings as fixed points
    # for building in buildings:
    #     ax.plot(building.coordinate[1], building.coordinate[0], "ro", markersize=8, label=building.name)

    # # Initialize scatter plot for agents
    # agent_scatter = ax.scatter([], [], s=50, c='blue', label='Agents')

    # # Update function for animation
    # def plot_update(frame):
    #     map.update()
        
    #     # Get agent locations for this frame
    #     x_data, y_data = [], []
    #     for agent in agents:
    #         lon, lat = agent.current_coordinate[1], agent.current_coordinate[0]
    #         x_data.append(lon)
    #         y_data.append(lat)
        
    #     # Update scatter plot data
    #     agent_scatter.set_offsets(list(zip(x_data, y_data)))
        
    #     return agent_scatter,

    # map = Map(agents, buildings)

    # print("STARTING SIMULATION\n\n")

    # # Create animation
    # ani = animation.FuncAnimation(fig, plot_update, frames=1000, interval=100, blit=True)

    # plt.legend(loc="lower left")
    # plt.show()

if __name__ == "__main__":
    main()