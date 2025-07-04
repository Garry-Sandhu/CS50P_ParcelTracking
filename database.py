import sqlite3
from datetime import datetime
import pandas as pd

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

    #Create a table for order status history tracking

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS package_status_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id TEXT NOT NULL,
            status TEXT NOT NULL,
            changed_at TEXT NOT NULL,
            FOREIGN KEY (package_id) REFERENCES packages(id)
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



def update_status(package_id: str, new_status: str):
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
    """, (new_status, package_id))

    conn.commit()
    conn.close()

    log_status_change(package_id, new_status)
    


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

def get_package(tracking_id):
    """
    Fetch a single package by its tracking ID.

    Args: 
        tracking_id (str): The ID of the package to fetch.
    
    Returns:
        dict or None: A dictionary representing the package, or None if not found.
    """

    conn, cursor = connect()

    cursor.execute('SELECT * FROM packages WHERE id = ?', (tracking_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    else:
        return None
    
def delete_package(tracking_id):
    """
    Delete a package from the database by its Tracking ID/

    Args:
        tracking_id (str): The ID of the package to delete

    Returns:
        bool: True if the package was deleted, False if no such package exists.
    """

    conn, cursor = connect()

    cursor.execute('DELETE FROM packages WHERE id =?', (tracking_id,))
    deleted = cursor.rowcount > 0 # Check if any row was deleted 

    conn.commit()
    conn.close()

    return deleted


def log_status_change(package_id: str, status: str):
    conn, cursor = connect()
    changed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO package_status_log (package_id, status, changed_at)
        VALUES (?, ?, ?)
    """, (package_id, status, changed_at))

    conn.commit()
    conn.close()

def get_status_history(package_id: str):
    conn, cursor = connect()
    cursor.execute("""
        SELECT status, changed_at FROM package_status_log
        WHERE package_id = ?
        ORDER BY changed_at ASC
    """, (package_id,))
    
    history = cursor.fetchall()
    conn.close()
    return history

def get_status_distribution():
    """Get package status counts for dashboard"""
    conn, cursor = connect()
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM packages 
        GROUP BY status
    """)
    result = cursor.fetchall()
    conn.close()
    return pd.DataFrame(result, columns=['Status', 'Count'])

def get_recent_packages(limit=10):
    """Get recent packages for dashboard"""
    conn, cursor = connect()
    cursor.execute("""
        SELECT id, sender, receiver, status, eta 
        FROM packages 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    result = cursor.fetchall()
    conn.close()
    return pd.DataFrame(result, columns=['ID', 'Sender', 'Receiver', 'Status', 'ETA'])