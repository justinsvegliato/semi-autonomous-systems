import json

id = 0

def get_action_response(data):
    return {
        'id': id,
        'action': 'left'
    }

handlers = {
    'action': get_action_response
}

def handle(request):
    global id

    data = request['data']
    type = request['type']

    handler = handlers[type]
    response = handler(data)

    id += 1

    return json.dumps(response)