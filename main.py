import pandas as pd
import numpy as np
import os
import yaml
import merge_dmmhs
import base_variables


# Read configuration file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Get paths from config
base_path_dmmh = config['dmmhPath']['base_path']
save_path_merged_center = config['dmmhPath']['save_path_merged_center']
save_path_baseVar = config['dmmhPath']['save_path_baseVar']
reference_file_path = os.path.join(config['maganamedPath']['base_path'], 'Kind-of-participant.csv')
save_path_merged_all = config['dmmhPath']['save_path_merged_all']

# Call the processing function
# (0) merge data for each center (only if it is needed!)
merge_dmmhs.merge_same_center_files(base_path_dmmh, save_path_merged_center)
# (1) add base variable (SiteCode)
base_variables.add_sitecode_from_filename(save_path_merged_center, save_path_baseVar)
# (2) merge all dmmh data across centers (Only if it is needed. Too big!)
# merge_dmmhs.merge_all_data_across_centers(save_path_baseVar, save_path_merged_all)

print("✅✅✅ ----- DMMH data is ready for the next process ----- ")




