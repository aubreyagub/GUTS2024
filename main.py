from flask import Flask, render_template, jsonify, request
from degrees import *
from copy import deepcopy
from flask import Flask
from flask_socketio import SocketIO, emit

from frontend.maptiler_key import MAPTILER_KEY

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

if __name__ == "__main__":
    socketio.run(app, debug=True, log_output=True, port=PORT)