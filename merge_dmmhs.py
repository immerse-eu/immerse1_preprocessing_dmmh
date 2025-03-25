import pandas as pd
import os

def merge_same_center_files(base_path, save_path):
    """
    Merges CSV files with the same name across all subfolders under the given base path.
    Creates a 'Timestamp' column and sorts data if relevant columns exist.

    Args:
        base_path (str): Root directory that contains subfolders with CSV files.
        save_path (str): Directory to save the merged CSV results.
    """
    file_groups = {}

    # 🔍 Recursively collect CSV files grouped by filename
    for root, dirs, files in os.walk(base_path):
        for file_name in files:
            if file_name.endswith(".csv"):
                file_path = os.path.join(root, file_name)
                file_groups.setdefault(file_name, []).append(file_path)

    # 📁 Ensure the save_path exists
    os.makedirs(save_path, exist_ok=True)

    # 🔄 Merge files with the same name
    for file_name, file_paths in file_groups.items():
        merged_df = pd.DataFrame()

        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path, low_memory=False)
                if "Unique_ID" in df.columns: #GH TODO: delete
                    df = df.drop(columns=["Unique_ID"])

                print(f">>> Read: {file_path}")
                merged_df = pd.concat([merged_df, df], ignore_index=True)
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")

        # 🧼 Clean column names
        merged_df.columns = merged_df.columns.str.strip()

        # If possible, create Timestamp column and sort
        if all(col in merged_df.columns for col in ["Participant", "Interaction_Trigger_Date", "Interaction_Trigger_Time"]):
            # merged_df["Timestamp"] = pd.to_datetime(
            #     merged_df["Interaction_Trigger_Date"] + " " + merged_df["Interaction_Trigger_Time"],
            #     errors="coerce"
            # )
            timestamp_col = pd.to_datetime(
                merged_df["Interaction_Trigger_Date"] + " " + merged_df["Interaction_Trigger_Time"],
                errors="coerce"
            )
            merged_df = pd.concat([merged_df, timestamp_col.rename("Timestamp")], axis=1)

            sort_cols = ["Participant", "Interaction_Counter", "Timestamp"]
            sort_cols = [col for col in sort_cols if col in merged_df.columns]
            merged_df = merged_df.sort_values(by=sort_cols)

        else:
            print(f"❌ Skipped {file_name}: missing required columns.")

        # 💾 Save the merged file
        output_file_path = os.path.join(save_path, f"merged_{file_name}")
        merged_df.to_csv(output_file_path, index=False, sep=";")
        print(f"✅ Merged file saved to: {output_file_path}")



def merge_all_data_across_centers(base_path, save_path, output_filename="merged_all_sites_dmmh.csv"):
    """
    Merges all CSV files in base_path into one, sorts the result, and saves it to save_path.

    Args:
        base_path (str): Folder containing the CSV files to merge.
        save_path (str): Folder where the merged result will be saved.
        output_filename (str): Name of the output merged CSV file.
    """
    all_dfs = []

    for file_name in os.listdir(base_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(base_path, file_name)
            try:
                df = pd.read_csv(file_path, sep=";", low_memory=False)
                all_dfs.append(df)
                print(f">>> Loaded: {file_name}")
            except Exception as e:
                print(f"❌ Failed to load {file_name}: {e}")

    if not all_dfs:
        print("❌ No CSV files to merge.")
        return

    merged_df = pd.concat(all_dfs, ignore_index=True)

    # 정렬 기준: Participant, Interaction_Counter, Timestamp가 있으면 기준으로 정렬
    sort_columns = [col for col in ["Participant", "Interaction_Counter", "Timestamp"] if col in merged_df.columns]
    if sort_columns:
        merged_df = merged_df.sort_values(by=sort_columns)

    os.makedirs(save_path, exist_ok=True)
    output_file_path = os.path.join(save_path, output_filename)
    merged_df.to_csv(output_file_path, index=False, sep=";")
    print(f"✅ Merged and sorted file saved to: {output_file_path}")
