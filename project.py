import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, get_all_packages
from tracker import create_package, update_package_status, delete_package_by_id, track_package_by_id, view_status_history
from datetime import datetime


def show_dashboard():
    st.header("📊 Package Tracking Dashboard")
    
    packages = get_all_packages()
    if packages:
        df = pd.DataFrame(packages)
        
        # Status distribution chart
        st.subheader("Package Status Overview")
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig = px.pie(status_counts, values='Count', names='Status', 
                         title="Status Distribution", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Total Packages", len(packages))
            st.metric("Unique Senders", df['sender'].nunique())
            st.metric("Unique Destinations", df['destination'].nunique())
        
        # Recent packages table
        st.subheader("All Packages")
        st.dataframe(df[['id', 'sender', 'receiver', 'status', 'eta']])
    else:
        st.warning("No packages found in the database.")

def main():
    # Initialize the database
    init_db()
    
    st.set_page_config(
        page_title="Package Tracker",
        page_icon="📦",
        layout="wide"
    )
    
    st.title("📦 Package Tracking System")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Menu")
        menu_option = st.radio(
            "Select Option",
            ["Dashboard", "Create Package", "Update Status", 
             "Delete Package", "Track Package", "View History"]
        )
        
        st.divider()
        st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Main content
    if menu_option == "Dashboard":
        show_dashboard()
    elif menu_option == "Create Package":
        st.header("Create New Package")
        create_package()  # Uses existing function from tracker.py
    elif menu_option == "Update Status":
        st.header("Update Package Status")
        update_package_status()  # Uses existing function from tracker.py
    elif menu_option == "Delete Package":
        st.header("Delete Package")
        delete_package_by_id()  # Uses existing function from tracker.py
    elif menu_option == "Track Package":
        st.header("Track Package")
        track_package_by_id()  # Uses existing function from tracker.py
    elif menu_option == "View History":
        st.header("Package Status History")
        view_status_history()  # Uses existing function from tracker.py

if __name__ == '__main__':
    main()
