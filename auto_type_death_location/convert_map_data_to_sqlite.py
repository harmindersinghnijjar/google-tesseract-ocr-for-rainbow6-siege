import sqlite3
import json

# Function to create tables
def create_tables(cursor):
    cursor.execute('''CREATE TABLE maps (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
    cursor.execute('''CREATE TABLE objectives (id INTEGER PRIMARY KEY, map_id INTEGER, name TEXT, FOREIGN KEY(map_id) REFERENCES maps(id))''')
    # Add more tables as needed

# Function to insert data
def insert_data(cursor, data):
    for map_data in data['maps']:
        cursor.execute("INSERT INTO maps (name, description) VALUES (?, ?)", (map_data['name'], map_data['description']))
        map_id = cursor.lastrowid
        for objective in map_data['objectives']:
            cursor.execute("INSERT INTO objectives (map_id, name) VALUES (?, ?)", (map_id, objective['name']))
        # Repeat for other tables and data

# Main function
def main():
    # Connect to SQLite3
    conn = sqlite3.connect('map_data.db')
    cursor = conn.cursor()

    # Create tables
    create_tables(cursor)

    # Load data from JSON (modify this part to match your data structure)
    with open('map_data.json', 'r') as file:
        data = json.load(file)

    # Insert data
    insert_data(cursor, data)

    # Commit and close
    conn.commit()
    conn.close()

    print("Data successfully inserted into SQLite3 database.")

if __name__ == "__main__":
    main()
