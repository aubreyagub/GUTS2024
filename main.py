from flask import Flask, render_template, jsonify, request
from degrees import *
from copy import deepcopy
from flask_socketio import SocketIO, emit, join_room
import time
import math
import random
from agent import Agent
import simulation
import threading

from frontend.maptiler_key import MAPTILER_KEY

DEBUG = False
STUDENT_COUNT = 50
PORT = 5000

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'your_secret_key'

agents = []  # Start with an empty list

@app.route('/')
def index():
    return render_template('landing.html', maptiler_key=MAPTILER_KEY, active_page='landing')


@app.route('/formulae')
def formulae():
    return render_template('formulae.html', active_page='formulae')

@app.route("/add_students", methods=["POST"])
def add_students():
    agents = request.get_json()
    for i,agent in enumerate(agents):
        socketio.emit('new_student', {
            'student_id': i, 
            'lat': agent.get("current_coordinate")[0], 
            'lng': agent.get("current_coordinate")[1], 
            'name': agent.get("name"), 
            'stinkLevel': agent.get("stink"), 
            'poi': agent.get("poi", False)
        })
    return jsonify({"status": f"{len(agents)} agents data emitted"}), 200

@app.route("/update_students", methods=["POST"])
def update_student():
    agents = request.get_json()
    for i,agent in enumerate(agents):
        socketio.emit('update_student', {
            'student_id': i, 
            'lat': agent.get("current_coordinate")[0], 
            'lng': agent.get("current_coordinate")[1], 
            'stinkLevel': agent.get("stink"), 
            'poi': agent.get("poi", False),
            'time_studied': agent.get("time_studied")
        })
    return jsonify({"status": f"{len(agents)} agents were updated"}), 200

@app.route("/update_buildings", methods=["POST"])
def update_buildings():
    buildings = request.get_json()
    for i,building in enumerate(buildings):
        socketio.emit('update_building', {
            'building_id': i,
            'buildingName': building.name.value,
            'lat': building.coordinate[0],
            'lng': building.coordinate[1],
            'stinkLevel': building.stink,
            'capacity': building.capacity,
            'tick' : building.tick
        })
    return jsonify({"status": f"{len(buildings)} buildings were updated"}), 200

@app.route('/simulation')
def simulation_page():
    # Start the simulation in a separate thread
    simulation_thread = threading.Thread(target=simulation.run)
    simulation_thread.start()
    return render_template('simulation.html', maptiler_key=MAPTILER_KEY, active_page='simulation')


@socketio.on('join')
def on_join(data):
    session_id = data['sessionId']
    join_room(session_id)
    print(f"Client joined room: {session_id}")


@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    data = request.get_json()
    name = data.get('name')
    stink_score = data.get('stink_score')
    session_id = data.get('session_id')

    # Convert stink_score to float
    stink_score = float(stink_score)

    # Create a new Agent with the provided name and stink score
    degree = random.choice(list(DegreeTitle))
    new_agent = Agent(name, degree.value, simulation.buildings,
                      stink=stink_score, poi=True)
    
    simulation.generate(new_agent)

    socketio.emit('simulation_complete', {
                  'message': 'Simulation is complete.'}, room=session_id)

    return jsonify({'status': 'Simulation started with new agent'}), 200
    


def generate_student(buildings):
    name = "Student"
    degree = random.choice(list(DegreeTitle))
    return Agent(name, degree.value, buildings)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=PORT)
