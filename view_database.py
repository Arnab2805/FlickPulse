# view_database.py
import sqlite3

def view_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Query all entries in the users table
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Print out the entries
    if rows:
        print("ID | Username | Password")
        print("------------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    else:
        print("No entries found in the database.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    view_database()
