from database import init_db, add_package, get_all_packages

def main():
    #Step 1: Initialize the database and ensure table exists 
    init_db()

    #Step 2: Dummy package data to insert
    package = {
        'id': 'pkg002',
        'sender': 'Alice',
        'receiver': 'Bob',
        'origin': 'New York',
        'destination': 'Los Angeles',
        'weight': 3.2,
        'status': 'In Transit',
        'eta': '2025-07-01',
        'created_at': '2025-06-24'
    }


    #Step 3: Add the dummy package

    add_package(package)
    print("Package Added!")

    packages = get_all_packages()
    print(packages)

if __name__ == '__main__':
    main()