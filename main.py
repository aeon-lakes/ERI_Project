# Main program loop

import os
from src import file_handler as fh
from src.quant import index_calculator as ic

# Prompts for access to survey output file
# Creates a working copy leaving original intact
fh.create_working_copy()

# Obtain main.py Absolute file path
current_dir = os.path.dirname(os.path.abspath(__file__))

import os

# Construct the relative path to the working_copy CSV file
working_copy_path = None
data_folder_path = os.path.join(current_dir, 'data')
for file_name in os.listdir(data_folder_path):
    if '_working_copy.csv' in file_name:
        working_copy_path = os.path.join(data_folder_path, file_name)
        break

if working_copy_path is None:
    print("No working copy file found in the data folder.")


# Opens working_data.csv
# Cleans the data
# Saves a copy.
fh.clean_data(working_copy_path)

# # Construct the relative path to the working_copy_cleaned CSV file
# working_copy_cleaned_path = os.path.join(current_dir, 'data', 'working_copy_cleaned.csv')

# Construct the relative path to the working_copy_cleaned CSV file
working_copy_path = None
data_folder_path = os.path.join(current_dir, 'data')
for file_name in os.listdir(data_folder_path):
    if '_working_copy_cleaned.csv' in file_name:
        working_copy_path = os.path.join(data_folder_path, file_name)
        break

if working_copy_path is None:
    print("No working copy file found in the data folder.")

ic.eri_index(working_copy_path)