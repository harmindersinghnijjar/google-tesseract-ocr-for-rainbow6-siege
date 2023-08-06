import pandas as pd
import sqlite3
import re

# Read the CSV file
csv_file = 'mysql_r6maps_com.csv'  # Replace with the path to your CSV file
data = pd.read_csv(csv_file, usecols=['map', 'location'])

# Connect to SQLite
conn = sqlite3.connect('maps.db')
cursor = conn.cursor()

# Iterate through unique maps
for map_name in data['map'].unique():
    # Sanitize the table name
    table_name = re.sub(r'\W+', '_', map_name)

    # Create a table for the map
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            location TEXT
        )
    ''')

    # Insert locations for the map
    locations = data[data['map'] == map_name]['location']
    for location in locations:
        cursor.execute(f'''
            INSERT INTO "{table_name}" (location)
            VALUES (?)
        ''', (location,))

    conn.commit()

# Close the connection
conn.close()
