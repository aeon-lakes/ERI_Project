# Open original Survey Monkey file and parse into
import pandas as pd
import numpy as np
import os
import shutil
from tkinter import Tk, filedialog
from datetime import datetime

# Creates ISO dated working_copy.csv file of selected .csv
# Allows debugging using eri555_test_data.csv file
# TODO: Make test files for 4 point Likert versions of ERI:
#  eri544_test_data.csv for white collar workers,
#  eri644_test_data.csv for blue collar workers.
# TODO: Low priority. Make test file for standard 5 point Likert version of ERI
#  with 4 point scale Over-Commitment. ie. eri554_test_data.csv
# TODO: Define function to identify type of ERI questionnaire and
#  add id_code to file. Currently defaults to eri555.
def create_working_copy():
    # Define the directory paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    tests_dir = os.path.join(parent_dir, 'tests')

    # File path for reference eri555_test_data.csv
    reference_file_path = os.path.join(tests_dir, 'eri555_test_data.csv')

    # Load the reference data from eri555_test_data.csv
    reference_data = pd.read_csv(reference_file_path, nrows=1)

    # Check if 'data' directory exists
    if os.path.exists(data_dir):
        # Check if 'data' directory has contents
        if os.listdir(data_dir):
            choice = input("The 'data' directory already exists and contains "
                           "files.\nDo you want to delete them and analyse new "
                           "data? (Y/N): ")
            if choice.upper() == 'Y':
                # Delete contents of 'data' directory
                for filename in os.listdir(data_dir):
                    file_path = os.path.join(data_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            else:
                print("Analysis continues with current working copy.")
                return
    else:
        # Create the 'data' directory if it doesn't exist
        os.makedirs(data_dir)

    # Prompt user for choice
    choice = ""
    while choice.upper() not in ["F", "T"]:
        choice = input("Do you wish to open a [F]ile or run the [T]est data?"
                       "\nInput F or T: ")

    if choice.upper() == "F":
        # Open file dialog to select a file
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        if file_path:
            # Check if the selected file is a CSV file
            if not file_path.lower().endswith('.csv'):
                print("Invalid file type. Please select a .csv file.")
                return  # Exit the function if an invalid file type is selected

            # Check if the selected file's top line matches the reference data
            data = pd.read_csv(file_path, nrows=1)
            if not data.columns.tolist() == reference_data.columns.tolist():
                print("The selected file does not have the appropriate data "
                      "structure.")
                return  # Exit the function if the data structure doesn't match

            # Create a working copy by copying the file
            output_file_path = os.path.join(data_dir, 'working_copy.csv')
            shutil.copy(file_path, output_file_path)
            print("The file has been duplicated as 'working_copy.csv' in the"
                  " 'data' directory.")
        else:
            print("No file selected. Exiting.")



    elif choice.upper() == "T":

        # File path for test data
        file_path = os.path.join(tests_dir, 'eri555_test_data.csv')

        # Create a working copy by copying the test data
        datestamp = datetime.now().strftime("%Y%m%d")
        output_file_name = f"{datestamp}_working_copy.csv"
        output_file_path = os.path.join(data_dir, output_file_name)
        shutil.copy(file_path, output_file_path)
        print(
            f"The test data have been duplicated as '{output_file_name}"
            f"' in the 'data' directory.")

# Data cleaning functions
# TODO: Add functions for 4 point Likert scoring

# Read raw data from the working copy
def read_data(filepath):
    data = pd.read_csv(filepath)
    return data

# Remove Survey Monkey response descriptor row cruft:
def remove_descriptor_row(data):
    descriptor_row_index = # logic to identify row
    data = data.drop(descriptor_row_index)
    return data

# Remove un-needed columns
# Collector ID, Start Date, End Date, IP Address, Email Address, First Name,
# Last Name, Custom Data 1, I am a SMO, RMO ... , Consent
def remove_columns(data):
    data = data.drop(columns=data.columns[1:11])
    return data

# Reset index
def reset_index(data: object) -> object:
   data.reset_index(drop=True, inplace=True)
   return data

# Remove empty columns
def remove_empty_columns(data):
   unnamed_columns = # logic to identify empty columns
   data = data.drop(columns=unnamed_columns)
   return data

# Rename columns
def rename_columns(data):
   # renaming logic
   return data

# Code responses
def code_responses(data):
   # response recoding logic
   return data

# Replace question code with follow-up code if appropriate
def merge_followups(data):
   # logic to replace questions with follow up responses
   return data

# Remove now un-needed follow-up columns
def remove_followups(data):
   follow_up_columns = # logic to identify follow up columns
   data = data.drop(columns=follow_up_columns)
   return data

# Further cleaning
def final_polish(data):
   # additional cleaning logic
   return data

def save_cleaned(data):

def clean_data(filepath):
   data = read_data(filepath) # load file into DataFrame
   data = remove_descriptor_row(data) # removes Survey Monkey cruft row
   data = remove_columns(data) # removes unnecessary data columns
   data = remove_empty_columns(data) # removes empty column cruft
   data = rename_columns(data)  # add ER and OC question numbers
   data = code_responses(data)    # to ER, OC, and followup questions
   data = merge_followups(data)   # merge ER, OC, and followup data
   data = remove_followups(data) # now duplicate followup data removed
   data = final_polish(data)
   data = reset_index(data)
   save_cleaned(data)

