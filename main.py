from agent import Agent
from flask import Flask, render_template, jsonify, request
from building import Building
from map import Map
from enum import Enum
import random
from degrees import *
from copy import deepcopy
from flask_socketio import SocketIO, emit, join_room
import threading
import time
import math

from frontend.maptiler_key import MAPTILER_KEY

DEBUG = False
STUDENT_COUNT = 50
PORT = 5000

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize buildings and agents globally
buildings = {
    BuildingName.BOYD_ORR: Building(BuildingName.BOYD_ORR, (55.873498, -4.292804), 15),
    BuildingName.JMS: Building(BuildingName.JMS, (55.873150, -4.292460), 10),
    BuildingName.FRASER_BUILDING: Building(BuildingName.FRASER_BUILDING, (55.873218, -4.288445), 10),
    BuildingName.READING_ROOM: Building(BuildingName.READING_ROOM, (55.872346, -4.288193), 10),
    BuildingName.LIBRARY: Building(BuildingName.LIBRARY, (55.873323, -4.288474), 25),
    BuildingName.SHADOW_REALM: Building(
        BuildingName.SHADOW_REALM, (0, 0), math.inf)
}

agents = []  # Start with an empty list
simulation_thread = threading.Thread(target=lambda: None)
simulation_thread_started = False
agent_lock = threading.Lock()
simulation_complete = threading.Event()


@app.route('/')
def index():
    return render_template('landing.html', maptiler_key=MAPTILER_KEY, active_page='landing')


@app.route('/formulae')
def formulae():
    return render_template('formulae.html', active_page='formulae')


@app.route('/simulation')
def simulation():
    return render_template('simulation.html', maptiler_key=MAPTILER_KEY, active_page='simulation')


@socketio.on('join')
def on_join(data):
    session_id = data['sessionId']
    join_room(session_id)
    print(f"Client joined room: {session_id}")


@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    global simulation_thread, simulation_thread_started
    data = request.get_json()
    name = data.get('name')
    stink_score = data.get('stink_score')
    session_id = data.get('session_id')

    # Convert stink_score to float
    stink_score = float(stink_score)

    # Create a new Agent with the provided name and stink score
    degree = random.choice(list(DegreeTitle))
    new_agent = Agent(name, degree.value, buildings,
                      stink=stink_score, poi=True)

    # Add the new agent to the agents list
    with agent_lock:
        agents.append(new_agent)

    # If the simulation hasn't started yet, start it
    if not simulation_thread_started:
        simulation_thread = threading.Thread(target=main, args=(session_id,))
        simulation_thread.daemon = True  # Ensures thread exits when main program exits
        simulation_thread.start()
        simulation_thread_started = True
    else:
        # If simulation is already running, you may decide how to handle it
        pass

    return jsonify({'status': 'Simulation started with new agent'}), 200


def generate_student(buildings):
    name = "Student"
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)


def main(session_id):
    global agents, buildings
    # Initialize other agents
    with agent_lock:
        if len(agents) < STUDENT_COUNT:
            for i in range(STUDENT_COUNT - len(agents)):
                agents.append(generate_student(buildings))

    # Map and simulation logic
    map = Map(agents, buildings)
    tick_count = 480
    print(f"Simulating {tick_count} ticks")

    for tick in range(tick_count):
        map.update()

        # Send updates to clients via SocketIO
        with agent_lock:
            current_agents = agents.copy()

        # For each agent
        for i, agent in enumerate(current_agents):
            socketio.emit('update_student', {
                'student_id': i,
                'lat': agent.current_coordinate[0],
                'lng': agent.current_coordinate[1],
                'stinkLevel': agent.stink,
                'poi': agent.poi
            })

        # For each building
        for i, building in enumerate(buildings.values()):
            socketio.emit('update_building', {
                'building_id': i,
                'buildingName': building.name.value,
                'lat': building.coordinate[0],
                'lng': building.coordinate[1],
                'stinkLevel': building.stink,
                'capacity': building.capacity
            })

        time.sleep(0.05)  # Adjust as needed

    # Simulation complete
    # Emit 'simulation_complete' event to the specific client
    socketio.emit('simulation_complete', {
                  'message': 'Simulation is complete.'}, room=session_id)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=PORT)
