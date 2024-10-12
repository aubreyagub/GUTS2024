from agent import Agent
from building import Building
from map import Map

# import matplotlib.pyplot as plt

def main():


    buildings = []
    boyd_orr = Building("boyd orr")
    library = Building("library")
    reading_room = Building("reading room")
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

    map = Map(agents, buildings)

    print("STARTING SIMULATION\n\n")

    for i in range(100):
        map.update()
        print("\nNext timestep\n")
    
    for agent in agents:
        print(f"{agent.name} studied for {agent.time_studied} mins")

if __name__ == "__main__":
    main()