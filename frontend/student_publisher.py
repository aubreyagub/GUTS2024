import requests
import time
from app import PORT

def create_student(lat, lng, name, stink_level, poi):
    response = requests.post(f'http://127.0.0.1:{PORT}/create_student', json={
        'lat': lat,
        'lng': lng,
        'name': name,
        'stinkLevel': stink_level, 
        'poi': poi
    })

    if response.status_code == 200:
        student_id = response.json()['student_id']
        print(f'student created with ID: {student_id}')
        return student_id
    else:
        print('failed to create student')

def update_student(student_id, lat, lng, stink_level):
    response = requests.post(f'http://127.0.0.1:{PORT}/update_student/{student_id}', json={
        'lat': lat,
        'lng': lng,
        'stinkLevel': stink_level  
    })

    if response.status_code == 200:
        print(f'student {student_id} updated')
    else:
        print('failed to update student')

if __name__ == '__main__':
    
    jim = create_student(55.872706, -4.290885, 'Jim', 5, True)
    
    if jim:
        update_student(jim, 55.873100, -4.291100, 7) 
        time.sleep(1)
        update_student(jim, 55.873200, -4.291000, 8)  
        time.sleep(1)
        update_student(jim, 55.873000, -4.291200, 9)  
        time.sleep(1)
        update_student(jim, 55.872900, -4.291100, 10)  

    time.sleep(1)
    jamie = create_student(55.872716, -4.290885, 'Jamie', 15, True)  
    time.sleep(1)
    update_student(jamie, 55.872900, -4.291115, 5)  

    anon = create_student(55.872716, -4.2909, 'Anon', 300, False)  
