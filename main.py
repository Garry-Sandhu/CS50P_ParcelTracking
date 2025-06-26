from database import init_db, add_package, get_all_packages
from tracker import create_package, update_package_status, delete_package_by_id, track_package_by_id
from datetime import datetime

def main():
    #Step 1: Initialize the database and ensure table exists 
    init_db()

    currentTime = datetime.now()

    #Step 2: Dummy package data to insert
    package = {
        'id': 'pkg002'+ currentTime.strftime("%Y-%m-%d"),
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

    """
    add_package(package)
    print("Package Added!")
    """

    
    while True:
        print("\n1. Create New Package")
        print("2. Update Package Status")
        print("3. Delete Package")
        print("4. Track Package")
        print("4. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_package()
        elif choice == "2":
            update_package_status()
        elif choice == "3":
            delete_package_by_id()
        elif choice == "4":
            track_package_by_id()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
    

    packages = get_all_packages()
    print(packages)


if __name__ == '__main__':
    main()