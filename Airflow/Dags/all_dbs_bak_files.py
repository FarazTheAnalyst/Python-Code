import os
import pandas as pd
import streamlit as st
from datetime import datetime

def format_file_size(size_bytes):
    """
    Convert file size in bytes to a human-readable format (GB, MB, KB, or B).
    """
    if size_bytes >= 1024 ** 3:  
        return f"{size_bytes / (1024 ** 3):,.2f} GB"
    elif size_bytes >= 1024 ** 2:  
        return f"{size_bytes / (1024 ** 2):,.2f} MB"
    elif size_bytes >= 1024:  
        return f"{size_bytes / 1024:,.2f} KB"
    else:  
        return f"{size_bytes:,} B"

def get_bak_files(directory):
    """
    Recursively find all .bak files in the given directory and its subdirectories.
    """
    bak_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = os.path.getmtime(file_path)
            modified_date = datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")
            file_size = os.path.getsize(file_path)
            formatted_size = format_file_size(file_size)
            
            if file.endswith('.bak'):
                bak_files.append((file_path, modified_date, formatted_size))
    return bak_files

def main():
    st.title("Backup Files Viewer")
    
    # Default directories
    default_directory_1 = r"E:\bkps\Daily_Partial_Backups"  
    default_directory_2 = r"E:\Daily_Partial_Backups"

    root_directory_1 = st.text_input("🗀 Enter the first root directory path:", value=default_directory_1)
    root_directory_2 = st.text_input("🗀 Enter the second root directory path:", value=default_directory_2)

    all_bak_files = []

    if root_directory_1:
        if not os.path.exists(root_directory_1):
            st.error(f"The specified directory does not exist: {root_directory_1}")
        else:
            bak_files_1 = get_bak_files(root_directory_1)
            all_bak_files.extend(bak_files_1, )

    if root_directory_2:
        if not os.path.exists(root_directory_2):
            st.error(f"The specified directory does not exist: {root_directory_2}")
        else:
            bak_files_2 = get_bak_files(root_directory_2)
            all_bak_files.extend(bak_files_2)

    if not root_directory_1 and not root_directory_2:
        st.info("Please provide at least one directory path.")
        return

    if not all_bak_files:
        st.info("No .bak files found in the specified directories.")
        return
    
    df = pd.DataFrame(all_bak_files, columns=["Backup Files", "Date modified", "Size"])
    st.write("### List of .bak files from the specified directories")
    st.dataframe(df, use_container_width=True, 
                 column_config = {"Date modified": st.column_config.TextColumn(width="small"),
                                    "Size": st.column_config.TextColumn(width="small"), "Backup Files": st.column_config.TextColumn(width="large")}
                                    )

if __name__ == "__main__":
    main()

    