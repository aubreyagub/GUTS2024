from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import maptiler_key

app = Flask(__name__)
socketio = SocketIO(app)

PORT = 5000

students = {}
student_id_counter = 0

@app.route('/')
def index():
    return render_template('simulation.html', maptiler_key=maptiler_key.MAPTILER_KEY, active_page='simulation')

@app.route('/formulae')
def formulae():
    return render_template('formulae.html', active_page='formulae')

@app.route('/create_student', methods=['POST'])
def create_student():
    global student_id_counter
    
    data = request.json
    
    lat = data['lat']
    lng = data['lng']
    name = data.get('name', f'Student {student_id_counter}')
    stink_level = data.get('stinkLevel', 1)
    poi = data.get('poi', False)
    student_id = f"student-{student_id_counter}"
    
    students[student_id] = {'lat': lat, 'lng': lng, 'name': name, 'stinkLevel': stink_level, 'poi': poi}
    student_id_counter += 1
    
    socketio.emit('new_student', {'student_id': student_id, 'lat': lat, 'lng': lng, 'name': name, 'stinkLevel': stink_level, 'poi': poi})

    return jsonify({'student_id': student_id})

@app.route('/create_students', methods=['POST'])
def create_students():
    global student_id_counter
    
    data = request.json

    for student in data:
    
        lat = student['lat']
        lng = student['lng']
        name = student.get('name', f'Student {student_id_counter}')
        stink_level = student.get('stinkLevel', 1)
        poi = student.get('poi', False)
        student_id = f"student-{student_id_counter}"
        
        students[student_id] = {'lat': lat, 'lng': lng, 'name': name, 'stinkLevel': stink_level, 'poi': poi}
        student_id_counter += 1
        
        socketio.emit('new_student', {'student_id': student_id, 'lat': lat, 'lng': lng, 'name': name, 'stinkLevel': stink_level, 'poi': poi})

    return jsonify({'student_id': student_id})

@app.route('/update_student/<student_id>', methods=['POST'])
def update_student(student_id):
    if student_id not in students:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.json
    lat = data.get('lat', students[student_id]['lat'])
    lng = data.get('lng', students[student_id]['lng'])
    stink_level = data.get('stinkLevel', students[student_id]['stinkLevel'])
    poi = data.get('poi', students[student_id]['poi'])
    
    students[student_id]['lat'] = lat
    students[student_id]['lng'] = lng
    students[student_id]['stinkLevel'] = stink_level
    students[student_id]['poi'] = poi
    
    socketio.emit('update_student', {'student_id': student_id, 'lat': lat, 'lng': lng, 'stinkLevel': stink_level, 'poi': poi})
    
    return jsonify({'success': True})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=PORT)