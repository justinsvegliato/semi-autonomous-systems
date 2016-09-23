import json

id = 0

def update_id():
    global id
    id += 1

def get_control_request(action):
    request = json.dumps({
        'id': id,
        'type': 'control',
        'action': action
    });

    update_id()

    return request

def get_location_request():
    request = json.dumps({
        'id': id,
        'type': 'location'
    });

    update_id()

    return request