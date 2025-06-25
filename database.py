import sqlite3

db_name = "data/packages.db"

def connect(db_name = "data/packages.db"):
    """
    Connect to specific SQLite database and return the connection and cursor"

    Parameters:
        db_Name (str): Name of the SQLite database file (default is 'package.db').

    Returns:
        tuple: (connection, cursor)
    """

    #Connect to the SQLite database file
    #file it doesn't exit, SQLite will create it automatically
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row #return it as a special object that behaves like a dictionary

    #Create a cursor object to interact with database
    cursor = conn.cursor()

    return conn, cursor

def init_db():
    #Initialize the database by creating the 'packages' table if it doesn't exist.

    conn, cursor = connect()

    #Create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            id TEXT PRIMARY KEY,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            weight REAL NOT NULL,
            status TEXT NOT NULL,
            eta TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    #Commit changes and close the connection

    conn.commit()
    conn.close()
    

def add_package(package_dict: dict):
    '''
    Insert a new package record into the 'packages' table

    Parameters:
    package_dict (dict): Dictionary with keys matching the table columns:
        {
            'id': '123'
            'sender': "Manjeet Singh',
            'receiver': 'Gursharan Sandhu',
            'origin': 'St Adolphe',
            'destination': 'Winnipeg',
            'weight': 2.5
            'status': 'In Transit';
            'eta': '2025-06-28';
            'created_at": '2025-06-24'
        }
    '''

    conn, cursor = connect()

    cursor.execute("""
                   INSERT INTO packages (id, sender, receiver, origin, destination, weight, status, eta, created_at)
                   VALUES (:id, :sender, :receiver, :origin, :destination, :weight, :status, :eta, :created_at)
    """, package_dict)

    conn.commit()

    conn.close()



def update_status(packages_id: str, new_status: str):
    """
    Updated the status of a package given its ID/

    Parameters:
        package_id (str): The unique ID of the package.
        new_status (str): The new status to set.
    """

    conn, cursor = connect()

    cursor.execute("""
        UPDATE packages
        SET status = ?
        WHERE id = ?
    """, (new_status, packages_id))

    conn.commit()
    conn.close()
    


def get_all_packages():
    """
    Fetch all packages from the database.

    Returns:
        list of tuples: Each tuple represents a row from the package table.
    """    

    conn, cursor = connect()

    cursor.execute('SELECT * FROM packages')

    rows = cursor.fetchall() #Fetch all results 

    conn.close()

    return [dict(row) for row in rows]