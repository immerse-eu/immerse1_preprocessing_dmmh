import os
import pandas as pd

def add_sitecode_from_filename(base_path, save_path):
    """
    Adds a SiteCode column to each CSV file in base_path based on center name in filename,
    and saves the updated CSV to save_path.
    """
    site_mapping = {
        "Lothian": 1,
        "CAMSH": 2,
        "Mannheim": 3,
        "Wiesloch": 4,
        "Leuven": 5,
        "Bierbeek": 6,
        "Bratislava": 7,
        "Kosice": 8
    }

    os.makedirs(save_path, exist_ok=True)

    for file_name in os.listdir(base_path):
        if file_name.endswith(".csv") and "merged_output_" in file_name:
            matched = False
            for site, code in site_mapping.items():
                if site in file_name:
                    site_code = code
                    matched = True
                    break

            if not matched:
                print(f"❌ No matching site found in filename: {file_name}")
                continue

            file_path = os.path.join(base_path, file_name)
            try:
                df = pd.read_csv(file_path, sep=";", low_memory=False)
                df["SiteCode"] = site_code

                save_file_path = os.path.join(save_path, file_name)
                df.to_csv(save_file_path, sep=";", index=False)
                print(f"✅ SiteCode added and saved: {save_file_path}")
            except Exception as e:
                print(f"❌ Error processing {file_name}: {e}")
