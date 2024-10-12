from agent import Agent

def main():
    agents = []
    agents.append(Agent("Jordan", "CS", 0.7, 0.3, 1.0))
    agents.append(Agent("John", "History", 0.3, 0.7))
    agents.append(Agent("Jeb", "CS", 0.8, 0.1))
    agents.append(Agent("Jamie", "History", 0.2, 0.7))
    agents.append(Agent("Johan", "CS", 0.7, 0.1))

    print("STARTING SIMULATION\N\N")

    for i in range(10):
        for agent in agents:
            agent.update()
            print(f"{agent.name} is {round(agent.stink, 3)} stinky at {agent.current_location.name}")
        print("\nNext timestep\n")

if __name__ == "__main__":
    main()