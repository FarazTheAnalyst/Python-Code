import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit Page Configuration
st.set_page_config(page_title="Daily Backups Management Tool", page_icon="💾", layout="wide")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["Backup Management", "Power BI Report", "Dashboard Overview"])

# Backup Management Tab
with tab1:
    st.title("💾 Daily Backups Management Tool")
    st.info("This tool helps you manage your daily backups by deleting older backups while keeping the latest one.")

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        backup_folder = st.text_input("📂 Enter Backup Folder Path:", r"E:\\bkps\\Daily_Partial_Backups")
    with col2:
        cutoff_date = st.date_input("📅 Enter Cutoff Date:", datetime.today().date())
    with col3:
        database_name = st.text_input("🔍 Enter Database Name (optional):", "").strip().lower()

    # Dictionary to store latest backup files
    latest_backups = {}
    deletion_results = []
    deleted_count = 0  # Counter for deleted backups

    # Step 1: Scan Backup Folder
    if os.path.exists(backup_folder) and os.path.isdir(backup_folder):
        with st.spinner("🔍 Scanning backup folder..."):
            for root, dirs, files in os.walk(backup_folder):
                dir_latest_backups = {}

                for file in files:
                    file_path = os.path.join(root, file)
                    if not file.endswith(".bak"):  # Skip non-backup files
                        continue
                    if database_name and database_name not in file.lower():
                        continue

                    # Get file date
                    mod_time = os.path.getmtime(file_path)
                    mod_datetime = datetime.fromtimestamp(mod_time)
                    file_date = mod_datetime.date()

                    # Keep track of the latest backup for each date
                    if file_date not in dir_latest_backups or mod_time > dir_latest_backups[file_date][1]:
                        dir_latest_backups[file_date] = (file_path, mod_time)

                latest_backups[root] = dir_latest_backups
    else:
        st.error("❌ Invalid backup folder path. Please check the path and try again.")

    # Step 2: Delete Old Backups
    if st.button("🗑️ Delete Old Backups", help="Click to delete backups older than the cutoff date"):
        if os.path.exists(backup_folder) and os.path.isdir(backup_folder):
            with st.spinner("🗑️ Deleting old backups..."):
                for root, dirs, files in os.walk(backup_folder):
                    dir_latest_backups = latest_backups.get(root, {})

                    for file in files:
                        file_path = os.path.join(root, file)
                        if not file.endswith(".bak"):
                            continue
                        if database_name and database_name not in file.lower():
                            continue

                        # Get file date
                        mod_time = os.path.getmtime(file_path)
                        mod_datetime = datetime.fromtimestamp(mod_time)
                        file_date = mod_datetime.date()

                        # Delete if older than cutoff and not the latest backup
                        if file_date < cutoff_date and file_path != dir_latest_backups.get(file_date, ("", None))[0]:
                            try:
                                os.remove(file_path)
                                deletion_results.append(f"✔️ 🗑️ Deleted: {file_path}")
                                deleted_count += 1
                            except Exception as e:
                                deletion_results.append(f"❌ Error deleting {file_path}: {e}")

            # Display results
            if deletion_results:
                st.subheader("🚮 💥 Deletion Results:")
                st.success(f"🧹 Total backups deleted: {deleted_count}")
                for result in deletion_results:
                    st.write(result)
            else:
                st.warning("⚠️ No files were deleted. Check folder contents or filters.")
        else:
            st.error("❌ Invalid backup folder path. Please check the path and try again.")

# Power BI Report Tab
with tab2:
    st.title("📊 Full Backups Power BI Report")
    st.info("Below is the embedded Full Backups Power BI report:")
    
    power_bi_Full_url = "https://app.powerbi.com/view?r=eyJrIjoiZjEyNmQyZTQtZTBhYi00OWZhLTk1NTMtMzEyNzlmNDE5NjlmIiwidCI6IjA2NDlhMjJhLWZmNmMtNDAyYy1hY2M3LWM1NGI5NWJhNTg0MCIsImMiOjl9"  
    st.components.v1.iframe(power_bi_Full_url, width=1450, height=750, scrolling=False)

    st.title("📊 Differential Backups Power BI Report")
    st.info("Below is the embedded Differential Backups Power BI report:")

    power_bi_Diff_url = "https://app.powerbi.com/view?r=eyJrIjoiOTBjZWE3MjEtZmU1MC00MWY2LTlkM2MtN2RhNzg4NmNmNWEzIiwidCI6IjA2NDlhMjJhLWZmNmMtNDAyYy1hY2M3LWM1NGI5NWJhNTg0MCIsImMiOjl9"
    st.components.v1.iframe(power_bi_Diff_url, width=1450, height=750, scrolling=False)

# Dashboard Overview Tab
with tab3:
    st.title("📈 Dashboard Overview")
    st.info("This section shows key metrics and insights related to backups.")

    # Example: Show some statistics
    st.metric("Total Backups Scanned", 150)
    st.metric("Backups Deleted Today", 20)
    st.metric("Storage Space Saved", "3.5 GB")

    # Example: Dummy chart (Can replace with real charts)
    data = pd.DataFrame({
        "Date": pd.date_range(start="2024-02-01", periods=10, freq="D"),
        "Backups Deleted": np.random.randint(5, 20, size=10)
    })

    # Line chart
    fig = px.line(data, x="Date", y="Backups Deleted", title="Backups Deleted Over Time")
    st.plotly_chart(fig)


"""The line latest_backups[root] = dir_latest_backups is storing the dictionary dir_latest_backups in another dictionary called latest_backups, using the root directory path as the key.

Explanation:
latest_backups: This is a dictionary that will store the latest backup files for each directory (folder) encountered during the os.walk traversal. The key is the directory path (root), and the value is another dictionary (dir_latest_backups).

root: This is the current directory path being processed by os.walk. It acts as the key in the latest_backups dictionary.

dir_latest_backups: This is a dictionary that stores the latest backup file for each date within the current directory (root). The key is the date (file_date), and the value is a tuple containing the file path and modification time of the latest backup for that date.

latest_backups[root] = dir_latest_backups: This line associates the dir_latest_backups dictionary (which contains the latest backups for the current directory) with the root directory path in the latest_backups dictionary. Essentially, it maps the directory path to its corresponding latest backups.

Example:
Suppose:

root = "/backups/folder1"

dir_latest_backups = {"2023-10-01": ("/backups/folder1/file1.bak", 1696108800), "2023-10-02": ("/backups/folder1/file2.bak", 1696195200)}

Then:

latest_backups[root] = dir_latest_backups will result in:

python
Copy
latest_backups = {
    "/backups/folder1": {
        "2023-10-01": ("/backups/folder1/file1.bak", 1696108800),
        "2023-10-02": ("/backups/folder1/file2.bak", 1696195200)
    }
}
This structure allows you to easily look up the latest backup files for each directory by its path."""