import os
import datetime
import streamlit as st

def delete_old_backups(directory, days_old, database_name):
    now = datetime.datetime.now()
    time_threshold = now - datetime.timedelta(days=days_old)

    delete_count = 0
    deleted_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if not file_path.endswith(".bak"):
                continue

            if database_name and database_name not in file.lower():
                continue

            file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified_time < time_threshold:
                deleted_files.append(file_path)
                os.remove(file_path)
                delete_count += 1

    if "Full" in directory:            
        st.title("🚮 💥Full Deletion Results")
        if delete_count > 0:
            st.success(f"🧹 Old files have been deleted. Total Backups deleted: {delete_count}")
        else:
            st.write("Deleting Partial Backups Files")
        
        for file in deleted_files:
            st.write(f"☑️ {file}")

    else:
        st.title("🚮 Partial Deletion Results")
        if delete_count > 0:
            st.success(f"🧹 Old files have been deleted. Total Backups deleted: {delete_count}")
        else:
            st.write("Deleting Partial Backups Files")

        for file in deleted_files:
            st.write(f"☑️ {file}") 

    if delete_count == 0:
        st.warning("No files were deleted.")   
        
    return delete_count

def main():
    st.title("💣 Delete Full Old Backup Files")

    st.info("This tool helps you Delete your Daily Full backups by deleting older backups more than 8 days.")
    # Input for directory paths

    col1, col2, col3 = st.columns(3)

    with col1:
        directory_to_clean_full = st.text_input("🗁📚 Enter the Full Backup directory path:", r"E:\Daily_Full_Backups")
    with col2:
        directory_to_clean_partial = st.text_input("🗁📚 Enter the Partial Backup directory path:", r"E:\Daily_Partial_Backups")
    with col3:
        days_old = st.number_input("8 ྀི 🔢 Enter the number of days:", min_value=8, value=8)

    database_name = st.text_input("🔍 Enter Database Name (optional):", "").strip().lower()

    if st.button("Delete Old Files"):
        if os.path.exists(directory_to_clean_full):
            delete_count_full = delete_old_backups(directory_to_clean_full, days_old, database_name)
        else:
            st.error(f"The specified Full Backup directory does not exist: {directory_to_clean_full}")

        if os.path.exists(directory_to_clean_partial):
            delete_count_partial = delete_old_backups(directory_to_clean_partial, days_old, database_name)
        else:
            st.error(f"The specified Partial Backup directory does not exist: {directory_to_clean_partial}")

if __name__ == "__main__":
    main()