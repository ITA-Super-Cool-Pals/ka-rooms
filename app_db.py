import sqlite3, os, csv

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-db', 'rooms.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create database with roomId, type columns
def db_create():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        # Create table if it doesn't exist
        cur.execute("""CREATE TABLE IF NOT EXISTS rooms (
                    roomId INTEGER PRIMARY KEY,
                    type TEXT
                    )""")

        # Read and insert data from CSV file
        with open('roomsDatabase.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header row if present
            rows = [(int(row[0]), row[1]) for row in reader]
            # Insert rows into the database table
            cur.executemany('INSERT INTO rooms (roomId, type) VALUES (?, ?)', rows)

    print(f'Database created and populated at {db_path}')

# Get list of all rooms
def get_all():
    rooms = []

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM rooms')

        # Get column names from cursor description
        columns = [column[0] for column in cur.description]

        # Fetch all rows and map each row to a column
        for row in cur.fetchall():
            rooms.append(dict(zip(columns, row)))

    return rooms

# Get specific room
def get_room(id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM rooms WHERE roomId = ?', (id,))

        # Fetch the room
        row = cur.fetchone()

        if row:
            columns = [column[0] for column in cur.description]
            room = dict(zip(columns, row))
            return room
        else:
            return None

# Add room
def add_room(data):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO rooms (roomId, type) VALUES (?, ?)', (data['roomId'], data['type']))
        conn.commit()

# Update a room type
def update_room(id, data):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE rooms SET type = ? WHERE roomId = ?', (data['type'], id))
        conn.commit()

# Delete a room
def delete_room(id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM rooms WHERE roomId = ?', (id,))
        conn.commit()
