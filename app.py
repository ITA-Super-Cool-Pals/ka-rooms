import os, json, app_db
from flask import Flask, request, Response

app = Flask(__name__)

# List of fields the API accepts
ROOM_FIELDS = ['roomId', 'type']
ROOM_TYPES = ['Standard Single', 'Grand Lit', 'Standard Double', 'Superior Double', 'Junior Suite', 'Spa Executive', 'Suite', 'LOFT Suite']

# Show result function, sorted by column order
def show_result(data, status=200):
    return Response(json.dumps(data, sort_keys=False), status=status, mimetype='application/json')

# Check if DB exists, if not create empty new DB
if not os.path.exists(app_db.db_path):
    print('rooms db not found, creating new')
    app_db.db_create()
else:
    print(f'rooms db found, using it at {app_db.db_path}')

# Routes
# Return all rooms
@app.route('/rooms', defaults={'id': None})
@app.route('/rooms/<int:id>')
def get_rooms(id):
    if id is None:
        rooms = app_db.get_all()
        return show_result(rooms)
    else:
        room = app_db.get_room(id)

        if room:
            return show_result(room)
        else:
            return show_result({'error': 'Room ID not found'}, status=404)

# Create new room
@app.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()

    # Check if room Id is already used
    if app_db.get_room(data['roomId']):
        return show_result({'error': 'Room ID already exists'}, status=409)

    # Check if only roomId (integer) and type (string) are provided
    if all(field in data for field in ROOM_FIELDS) and isinstance(data['roomId'], int) and data['type'] in ROOM_TYPES:
        app_db.add_room(data)
        return show_result(data, status=201)
    else:
        return show_result({'error': 'Invalid data'}, status=400)

# Update existing room
@app.route('/rooms/<int:id>', methods=['PATCH'])
def update_room(id):
    data = request.get_json()

    # Check if room exists
    if app_db.get_room(id):
        # Check if only type is provided
        if 'type' in data and data['type'] in ROOM_TYPES:
            app_db.update_room(id, data)
            return show_result(data)
        else:
            return show_result({'error': 'Invalid data'}, status=400)
    else:
        return show_result({'error': 'Room ID not found'}, status=404)

# Delete existing room
@app.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    if app_db.get_room(id):
        app_db.delete_room(id)
        return show_result({'message': 'Room deleted'})
    else:
        return show_result({'error': 'Room ID not found'}, status=404)

app.run(host="0.0.0.0")
