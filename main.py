# Main program

import os
from src import file_handler as fh
from src.quant import index_calculator as ic
from src.qual import sentiment_analysis as sa

# Obtain main.py Absolute file path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define Path to secrets.json
secrets_path = os.path.join(current_dir, 'secrets.json')

# Asks for location of the survey output file.
# Creates a working copy. Leaves original intact.
fh.create_working_copy()

# Constructs a relative path to the working_copy.csv file.
working_copy_path = None
data_folder_path = os.path.join(current_dir, 'data')
for file_name in os.listdir(data_folder_path):
    if '_working_copy.csv' in file_name:
        working_copy_path = os.path.join(data_folder_path, file_name)
        break

if working_copy_path is None:
    print("No working copy file found in the data folder.")

# Opens working_data.csv
# Cleans the data. Saves an ISO dated copy.
fh.clean_data(working_copy_path)

# Constructs a new relative path to the working_copy_cleaned CSV file
# to pass on to index calculation functions.
working_copy_path = None
data_folder_path = os.path.join(current_dir, 'data')
for file_name in os.listdir(data_folder_path):
    if '_working_copy_cleaned.csv' in file_name:
        working_copy_path = os.path.join(data_folder_path, file_name)
        break

if working_copy_path is None:
    print("No working copy file found in the data folder.")

# Performs Effort, Reward, ERI Index, and Over-Commitment calculations
# and saves to an ISO dated _ERI_data.csv file ready for further analysis.
ic.eri_index(working_copy_path)

# Constructs a new relative path to the ERI_data.csv file
# to pass on to quantitative and qualitative analysis functions.
working_copy_path = None
data_folder_path = os.path.join(current_dir, 'data')
for file_name in os.listdir(data_folder_path):
    if 'ERI_data.csv' in file_name:
        working_copy_path = os.path.join(data_folder_path, file_name)
        break

# OpenAI API call to text-davinci-003 for sentiment analysis
# Costs $$$$ be careful
sa.gpt_sentiment(working_copy_path, secrets_path)

# TODO: Call to word_cloud_generator.py functions
# TODO: Call to hallucination checker.py function
# TODO: Call to analyses.py functions for quantitive analyses
