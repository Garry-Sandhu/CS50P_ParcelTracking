import uuid
from datetime import datetime, timedelta
from database import add_package, update_status, get_package, delete_package

def create_package():
    #prompt user for input 
    sender = input("Enter sender name: ").strip().title()
    receiver = input("Enter receiver name: ").strip().title()
    origin = input("Enter origin: ").strip().title()
    destination = input("Enter destination: ").strip().title()
    try:
        weight = float(input("Enter package weight (kg): "))
    except ValueError:
        print("Invalid weight. Please enter a number")
        return
    
    created_at = datetime.now()


    #Generate unique tracking ID
    tracker_id = str(uuid.uuid4())
    print(tracker_id)

    #Set status 
    status = "New Shipment"

    #Set ETA (e.g., 5 days from now)
    eta_days = 5
    eta = datetime.now() + timedelta(days=eta_days)


    #Build package dictionary

    package = {
        "id": tracker_id,
        "sender": sender,
        "receiver": receiver,
        "origin": origin,
        "destination": destination,
        "weight": weight,
        "status": status,
        "eta": eta.strftime("%Y-%m-%d"),
        "created_at":created_at.strftime("%Y-%m-%d")
    }

    #Call the add_package function to store package 
    add_package(package)

    print(f'Package created successfully with Tracking ID: {tracker_id}')



def update_package_status():
    tracking_id = input("Enter the Tracking ID: ")
    package = get_package(tracking_id)
    print(f'Current Package status: {package['status']}')
    print("Choose new status:")
    print("1. In Transit")
    print("2. Out for Delivery")
    print("3. Delivered")
    choice = input("Enter choice:")

    status_option = {
        "1": "In Transit",
        "2": "Out for Delivery",
        "3": "Delivered"
    }

    update_status(tracking_id, status_option[choice])

    print(f'Status for package {tracking_id} updated to {status_option[choice]}')

def delete_package_by_id():
    tracking_id = input("Enter the Tracking ID to delete: ").strip()

    confirm = input(f'Are you sure you want to delete package {tracking_id}? (y/n): ').lower()

    if confirm != 'y':
        print("Cancelled.")
        return
    
    if delete_package(tracking_id):
        print(f'package {tracking_id} has been deleted successfully')
    else:
        print("Package not found or already deleted.")

def track_package_by_id():
    tracking_id = input("Enter the Tracking ID: ").strip()

    if get_package(tracking_id):
        package = get_package(tracking_id)
        print(f'Package {tracking_id} is {package["status"]} and expected to be deliverd by {package["eta"]}')
    else:
        print("Package not found.")