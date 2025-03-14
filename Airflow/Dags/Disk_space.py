import os
import psutil
import streamlit as st

def check_disk_space(server, drives):
    st.title(f"Disk Space Checker for {server}")
    
    for drive in drives:
        try:
            # Construct the path for the remote drive
            path = f"\\\\{server}\\{drive}$"
            if not os.path.exists(path):
                st.error(f"Drive {drive} does not exist on {server}.")
                continue

            # Get disk usage statistics
            usage = psutil.disk_usage(path)
            st.write(f"**Drive:** {drive}")
            st.write(f"  **Total:** {usage.total // (2**30):.2f} GB")
            st.write(f"  **Used:** {usage.used // (2**30):.2f} GB")
            st.write(f"  **Free:** {usage.free // (2**30):.2f} GB")
            st.write(f"  **Usage:** {usage.percent}%")
            st.write("-" * 30)
        except Exception as e:
            st.error(f"Error accessing drive {drive} on {server}: {e}")

# List of servers and their respective drives to check
servers = {
    "192.168.43.146": ["C", "D", "E"]
}

# Streamlit app
for server, drives in servers.items():
    check_disk_space(server, drives)