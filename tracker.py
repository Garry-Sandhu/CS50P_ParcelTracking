import uuid
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from database import add_package, update_status, get_package, delete_package, get_status_history

def create_package():
    with st.form("create_package"):
        st.subheader("Create New Package")
        col1, col2 = st.columns(2)
        
        with col1:
            sender = st.text_input("Sender Name").strip().title()
            receiver = st.text_input("Receiver Name").strip().title()
            weight = st.number_input("Package Weight (kg)", min_value=0.1, step=0.1)
        
        with col2:
            origin = st.text_input("Origin").strip().title()
            destination = st.text_input("Destination").strip().title()
            shipping_option = st.selectbox(
                "Shipping Option",
                ["Standard Shipping (5 Days)", "Priority Shipping (3 Days)", 
                 "Expedited Shipping (2 Days)", "Over-Night Delivery"]
            )
        
        if st.form_submit_button("Create Package"):
            if not all([sender, receiver, origin, destination, weight]):
                st.error("Please fill in all fields")
                return
            
            # Generate unique tracking ID
            tracker_id = str(uuid.uuid4())
            
            # Set status 
            status = "New Shipment"
            
            # Calculate ETA
            shipping_days = {
                "Standard Shipping (5 Days)": 5,
                "Priority Shipping (3 Days)": 3,
                "Expedited Shipping (2 Days)": 2,
                "Over-Night Delivery": 1
            }
            
            eta = datetime.now() + timedelta(days=shipping_days[shipping_option])
            
            package = {
                "id": tracker_id,
                "sender": sender,
                "receiver": receiver,
                "origin": origin,
                "destination": destination,
                "weight": weight,
                "status": status,
                "eta": eta.strftime("%Y-%m-%d"),
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            
            add_package(package)
            st.success(f'Package created successfully! Tracking ID: {tracker_id}')

def update_package_status():
    tracking_id = st.text_input("Enter Tracking ID").strip()
    
    if tracking_id:
        package = get_package(tracking_id)
        if package:
            st.subheader(f"Update Status for Package {tracking_id}")
            st.write(f"Current Status: **{package['status']}**")
            
            new_status = st.selectbox(
                "Select New Status",
                ["In Transit", "Out for Delivery", "Delivered", "Returned"]
            )
            
            if st.button("Update Status"):
                update_status(tracking_id, new_status)
                st.success(f"Status updated to {new_status}")
        else:
            st.error("Package not found")

def delete_package_by_id():
    
    
    tracking_id = st.text_input(
        "Enter Tracking ID to Delete",
        help="Enter the exact tracking ID shown on your receipt",
        placeholder="e.g. PKG12345"
    ).strip()
    
    if tracking_id:
        package = get_package(tracking_id)
        if package:
            # Enhanced package display
            with st.container(border=True):
                st.warning(f"⚠️ You are about to delete package: **{tracking_id}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Sender Info")
                    st.markdown(f"""
                    **Name**: {package['sender']}  
                    **Origin**: {package['origin']}  
                    **Created**: {package['created_at']}
                    """)
                    
                with col2:
                    st.subheader("Recipient Info")
                    st.markdown(f"""
                    **Name**: {package['receiver']}  
                    **Destination**: {package['destination']}  
                    **ETA**: {package['eta']}
                    """)
                
                st.divider()
                
                st.subheader("Shipping Details")
                st.markdown(f"""
                 **Status**: `{package['status']}`  
                **Weight**: {package['weight']} kg  
                **Tracking ID**: `{package['id']}`
                """)
            
            # Confirmation button
            if st.button(
                "Confirm Deletion",
                type="primary",
                help="This action cannot be undone",
                key=f"delete_confirm_{tracking_id}"
            ):
                if delete_package(tracking_id):
                    st.success(f"✅ Package {tracking_id} deleted successfully")
                    #st.balloons()
                else:
                    st.error("Failed to delete package")
        else:
            st.error("❌ Package not found. Please verify the Tracking ID")


def track_package_by_id():
    st.header("📡 Track Package")
    
    with st.form("track_package_form"):
        tracking_id = st.text_input("Enter Tracking ID",
                                  placeholder="e.g. PKG12345",
                                  help="Enter your package tracking number")
        
        if st.form_submit_button("Track Package"):
            if tracking_id:
                package = get_package(tracking_id)
                if package:
                    st.success("Package Found!")
                    
                    # Visual status indicator
                    status_emoji = {
                        "In Transit": "🚚",
                        "Out for Delivery": "📦",
                        "Delivered": "✅",
                        "Returned": "↩️"
                    }.get(package['status'], "ℹ️")
                    
                    with st.container(border=True):
                        st.markdown(f"""
                        ### {status_emoji} Current Status: **{package['status']}**
                        
                        **Tracking ID**: {package['id']}
                        **Estimated Delivery**: {package['eta']}
                        """)
                    
                    # Package journey visualization
                    st.subheader("Package Journey")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"""
                        🏢 **From**: {package['origin']}
                        🏠 **To**: {package['destination']}
                        ⚖️ **Weight**: {package['weight']} kg
                        """)
                    
                    with col2:
                        st.map()  # Would integrate with real map API in production
                else:
                    st.error("Package not found. Please check your Tracking ID")


def view_status_history():
    tracking_id = st.text_input("Enter Tracking ID to View History").strip()
    
    if tracking_id:
        history = get_status_history(tracking_id)
        if history:
            st.subheader(f"Status History for Package {tracking_id}")
            
            for record in history:
                st.write(f"- {record['changed_at']}: {record['status']}")
        else:
            st.error("No history found for this package")











# import uuid
# from datetime import datetime, timedelta
# from database import add_package, update_status, get_package, delete_package, get_status_history

# def create_package():
#     #prompt user for input 
#     sender = input("Enter sender name: ").strip().title()
#     receiver = input("Enter receiver name: ").strip().title()
#     origin = input("Enter origin: ").strip().title()
#     destination = input("Enter destination: ").strip().title()
#     try:
#         weight = float(input("Enter package weight (kg): "))
#     except ValueError:
#         print("Invalid weight. Please enter a number")
#         return
    
#     created_at = datetime.now()


#     #Generate unique tracking ID
#     tracker_id = str(uuid.uuid4())
#     print(tracker_id)

#     #Set status 
#     status = "New Shipment"

#     #Set ETA (e.g., 5 days from now)

#     print("Choose a shipping option: ")
#     print("1. Standard Shipping - 5 Days")
#     print("2. Priority Shipping - 3 Days")
#     print("3. Expedited Shipping - 2 Days")
#     print("4. Over-Night Delivery")

#     shipping_selection = input("Enter Choice: ").strip()

#     shipping_option = {
#         "1": 5,
#         "2": 3,
#         "3": 2,
#         "4": 1
#     }


#     eta = datetime.now() + timedelta(days=shipping_option[shipping_selection])


#     #Build package dictionary

#     package = {
#         "id": tracker_id,
#         "sender": sender,
#         "receiver": receiver,
#         "origin": origin,
#         "destination": destination,
#         "weight": weight,
#         "status": status,
#         "eta": eta.strftime("%Y-%m-%d"),
#         "created_at":created_at.strftime("%Y-%m-%d")
#     }

#     #Call the add_package function to store package 
#     add_package(package)

#     print(f'Package created successfully with Tracking ID: {tracker_id} with expected delivery date as {eta.strftime("%Y-%m-%d")}')



# def update_package_status():
#     tracking_id = input("Enter the Tracking ID: ")
#     package = get_package(tracking_id)
#     print(f'Current Package status: {package['status']}')
#     print("Choose new status:")
#     print("1. In Transit")
#     print("2. Out for Delivery")
#     print("3. Delivered")
#     choice = input("Enter choice:")

#     status_option = {
#         "1": "In Transit",
#         "2": "Out for Delivery",
#         "3": "Delivered"
#     }

#     update_status(tracking_id, status_option[choice])

#     print(f'Status for package {tracking_id} updated to {status_option[choice]}')

# def delete_package_by_id():
#     tracking_id = input("Enter the Tracking ID to delete: ").strip()

#     confirm = input(f'Are you sure you want to delete package {tracking_id}? (y/n): ').lower()

#     if confirm != 'y':
#         print("Cancelled.")
#         return
    
#     if delete_package(tracking_id):
#         print(f'package {tracking_id} has been deleted successfully')
#     else:
#         print("Package not found or already deleted.")

# def track_package_by_id():
#     tracking_id = input("Enter the Tracking ID: ").strip()

#     if get_package(tracking_id):
#         package = get_package(tracking_id)
#         print(f'Package {tracking_id} is {package["status"]} and expected to be deliverd by {package["eta"]}')
#     else:
#         print("Package not found.")

# def view_status_history():
#     tracking_id = input("Enter the Tracking ID to view status history: ").strip()
#     history = get_status_history(tracking_id)

#     if not history:
#         print("No history found for this package")
#         return
    
#     print(f'\n📦 Status history for {tracking_id}:\n')

#     for row in history:
#         print(f' - {row["changed_at"]} -> {row["status"]}')
    
