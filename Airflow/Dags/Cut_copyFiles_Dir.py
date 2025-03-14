import os
import shutil
import threading
import streamlit as st

# Fixed source and destination paths
FIXED_SOURCE_PATH = r"E:\Testing_folder"
FIXED_DESTINATION_PATH = r"E:\Target_Testing_folder"

# Streamlit UI
st.title("Auto Move: All .bak Files")

# User input for source and target folders
source_folder = st.text_input("📁 Source Folder:", FIXED_SOURCE_PATH)
target_folder = st.text_input("📁 Target Folder:", FIXED_DESTINATION_PATH)



# Function to move .bak files
def move_bak_files():
    moved = []


    try:
        for file_name in os.listdir(source_folder):
            if file_name.endswith(".bak"):
                source_path = os.path.join(source_folder, file_name)
                target_path = os.path.join(target_folder, file_name)

                if os.path.isfile(source_path):
                    shutil.move(source_path, target_path)
                    moved.append(file_name)

        # Update status inside the thread (not recommended for Streamlit)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to run the move_bak_files function in a separate thread
def start_monitoring():
    thread = threading.Thread(target=move_bak_files)
    thread.start()

if st.button("🚀 Execute"):
    start_monitoring()
    st.info("Operation Started.*")

    