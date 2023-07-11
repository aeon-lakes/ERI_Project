# Main program loop

import os
from src import file_handler as fh
from src.quant import index_calculator as ic

# Prompts for access to survey output file
# Creates a working copy leaving original intact
fh.create_working_copy()

# Obtain main.py Absolute file path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the working_copy CSV file
working_copy_path = os.path.join(current_dir, 'data', 'working_copy.csv')

# Opens working_data.csv
# Cleans the data
# Saves a copy.
fh.clean_data(working_copy_path)

# Construct the relative path to the working_copy_cleaned CSV file
working_copy_cleaned_path = os.path.join(current_dir, 'data', 'working_copy_cleaned.csv')

ic.eri_index(working_copy_cleaned_path)