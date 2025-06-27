import streamlit as st
from database import init_db
from tracker import create_package, update_package_status, delete_package_by_id, track_package_by_id, view_status_history
from datetime import datetime

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
        #st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Main content
    if menu_option == "Dashboard":
        show_dashboard()
    elif menu_option == "Create Package":
        st.header("Create New Package")
        create_package()
    elif menu_option == "Update Status":
        st.header("Update Package Status")
        update_package_status()
    elif menu_option == "Delete Package":
        st.header("Delete Package")
        delete_package_by_id()
    elif menu_option == "Track Package":
        st.header("Track Package")
        track_package_by_id()
    elif menu_option == "View History":
        st.header("Package Status History")
        view_status_history()

def show_dashboard():
    st.header("📊 Package Tracking Dashboard")
    
    from database import get_status_distribution, get_recent_packages
    import plotly.express as px
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    
    # Status distribution
    st.subheader("Package Status Overview")
    status_df = get_status_distribution()
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        if not status_df.empty:
            fig = px.pie(status_df,values='Count', names='Status',title="Status Distribution")
            fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,textposition='inside',marker=dict(colors=colors, line=dict(color='#000000', width=2)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No package data available")
    
    with col2:
        st.metric("Total Packages", len(status_df))
        # Add more metrics as needed
    
    # Recent packages
    st.subheader("Recent Packages")
    recent_df = get_recent_packages()
    if not recent_df.empty:
        st.dataframe(recent_df)
    else:
        st.warning("No recent packages found")

if __name__ == '__main__':
    main()