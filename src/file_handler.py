# Open original Survey Monkey file and parse into
import pandas as pd
import numpy as np
import os
import shutil
from tkinter import Tk, filedialog

def create_working_copy():
    # Define the directory paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    tests_dir = os.path.join(parent_dir, 'tests')

    # File path for reference eri_test_data.csv
    reference_file_path = os.path.join(tests_dir, 'eri_test_data.csv')

    # Load the reference data from eri_test_data.csv
    reference_data = pd.read_csv(reference_file_path, nrows=1)

    # Check if 'data' directory exists
    if os.path.exists(data_dir):
        # Check if 'data' directory has contents
        if os.listdir(data_dir):
            choice = input("The 'data' directory already exists and contains files.\nDo you want to delete them and analyse new data? (Y/N): ")
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
        choice = input("Do you wish to open a [F]ile or run the [T]est data? Input F or T: ")

    if choice.upper() == "F":
        # Open file dialog to select a file
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        if file_path:
            # Check if the selected file is a CSV file
            if not file_path.lower().endswith('.csv'):
                print("Invalid file type. Please select a CSV file.")
                return  # Exit the function if an invalid file type is selected

            # Check if the selected file's top line matches the reference data
            data = pd.read_csv(file_path, nrows=1)
            if not data.columns.tolist() == reference_data.columns.tolist():
                print("The selected file does not have the appropriate data structure.")
                return  # Exit the function if the data structure doesn't match

            # Create a working copy by copying the file
            output_file_path = os.path.join(data_dir, 'working_copy.csv')
            shutil.copy(file_path, output_file_path)
            print("The file has been duplicated as 'working_copy.csv' in the 'data' directory.")
        else:
            print("No file selected. Exiting.")

    elif choice.upper() == "T":
        # File path for test data
        file_path = os.path.join(tests_dir, 'eri_test_data.csv')

        # Create a working copy by copying the test data
        output_file_path = os.path.join(data_dir, 'working_copy.csv')
        shutil.copy(file_path, output_file_path)
        print("The test data have been duplicated as 'working_copy.csv' in the 'data' directory.")



def clean_data(wk):
    # Read the working copy data from CSV
    data = pd.read_csv(wk)

    # Identify the "response descriptor row"
    descriptor_row_index = data.index[(data == 'Response').any(axis=1) |
                                      (data == 'Other (please specify)').any(
                                          axis=1) |
                                      (data == 'Open-Ended Response').any(
                                          axis=1)][0]

    # Remove the "response descriptor row"
    data = data.drop(descriptor_row_index, axis=0)

    # Remove Columns B through K (indices 1 through 10 in 0-based indexing)
    data = data.drop(data.columns[1:11], axis=1)

    # Reset the index
    data.reset_index(drop=True, inplace=True)

    # Remove columns that are unnamed and completely empty
    unnamed_columns = [col for col in data.columns if
                       'Unnamed' in col and data[col].isna().all()]
    data = data.drop(columns=unnamed_columns)

    # Define new column names
    new_column_names = {
        'Throughout this survey the word \'stress\' is used in its negative sense; and the words \'distress\' and \'distressed\' are used in a lay, non-clinical sense. With that in mind: Do you find your day-to-day clinical work stressful? You will have opportunities to explain your answer through responses to subsequent questions.': 'Stressed',
        'I am:': 'Sex',
        'I am:.1': 'Grade',
        'Use the pull-down menu to select your age bracket:': 'Age bracket',
        'I graduated from:': 'Registerable degree',
        'What specialty do you work in? If an RMO, use your current rotation specialty.': 'Specialty group',
        'I attend to patients in person during normal sleep hours (2230 - 0630)': 'Broken sleep frequency',
        'When I am called to attend patients during sleep hours (2230 - 0630)': 'Nighttime junior support'
    }

    # Rename the columns
    data.rename(columns=new_column_names, inplace=True)

    # Define question number key
    question_number_key = {
        'I have constant time pressure due to a heavy work load.': 'ERI1 (I have constant time pressure due to a heavy work load.)',
        'I have many interruptions and disturbances in my job.': 'ERI2 (I have many interruptions and disturbances in my job.)',
        'I have a lot of responsibility in my job.': 'ERI3 (I have a lot of responsibility in my job.)',
        'I am often pressured to work overtime.': 'ERI4 (I am often pressured to work overtime.)',
        'Over the past few years, my job has become more and more demanding.': 'ERI6 (Over the past few years, my job has become more and more demanding.)',
        'I receive the respect I deserve from my superiors.': 'ERI17 (I receive the respect I deserve from my superiors.)',
        'I receive the respect I deserve from my colleagues.': 'ERI18 (I receive the respect I deserve from my colleagues.)',
        'I experience adequate support in difficult situations.': 'ERI19 (I experience adequate support in difficult situations.)',
        'I am treated unfairly at work.': 'ERI10 (I am treated unfairly at work.)',
        'Considering all my efforts and achievements, I receive the respect and prestige I deserve at work.': 'ERI15 (Considering all my efforts and achievements, I receive the respect and prestige I deserve at work.)',
        'My job promotion prospects are poor.': 'ERI11 (My job promotion prospects are poor.)',
        'My current occupational position adequately reflects my education and training.': 'ERI14 (My current occupational position adequately reflects my education and training.)',
        'Considering all my efforts and achievements, my work prospects are adequate.': 'ERI16 (Considering all my efforts and achievements, my work prospects are adequate.)',
        'Considering all my efforts and achievements, my salary/income is adequate.': 'ERI17 (Considering all my efforts and achievements, my salary/income is adequate.)',
        'I have experienced or I expect to experience an undesirable change in my work situation.': 'ERI12 (I have experienced or I expect to experience an undesirable change in my work situation.)',
        'My job security is poor.': 'ERI13 (My job security is poor.)',
        'I get easily overwhelmed by time pressures at work.': 'OC1 (I get easily overwhelmed by time pressures at work.)',
        'As soon as I get up in the morning I start thinking about work problems.': 'OC2 (As soon as I get up in the morning I start thinking about work problems.)',
        'When I get home, I can easily relax and ‘switch off’ work.': 'OC3 (As soon as I get up in the morning I start thinking about work problems.)',
        'People close to me say I sacrifice too much for my job.': 'OC4 (People close to me say I sacrifice too much for my job.)',
        'Work rarely lets me go, it is still on my mind when I go to bed.': 'OC5 (Work rarely lets me go, it is still on my mind when I go to bed.)',
        'If I postpone something that I was supposed to do today I’ll have trouble sleeping at night.': 'OC6 (If I postpone something that I was supposed to do today I’ll have trouble sleeping at night.)'
    }

    # Rename the columns with question numbers
    data.rename(columns=question_number_key, inplace=True)

    # Define a list of columns to apply reverse coding
    reverse_coding = ['ERI17', 'ERI18', 'ERI19', 'ERI15', 'ERI14', 'ERI16',
                      'OC3']

    question_numbers = ['ERI1', 'ERI2', 'ERI3', 'ERI4', 'ERI6', 'ERI7', 'ERI18',
                        'ERI19', 'ERI10', 'ERI15', 'ERI11',
                        'ERI14', 'ERI16', 'ERI17', 'ERI12', 'ERI13', 'OC1',
                        'OC2', 'OC3', 'OC4', 'OC5', 'OC6']

    # Define the response recoding keys
    normal_response_recoding_key = {
        'Disagree': 1,
        'Agree': 2,
        'Skip [this question and the remainder of this question block]': np.nan
    }

    reverse_response_recoding_key = {
        'Disagree': 2,
        'Agree': 1,
        'Skip [this question and the remainder of this question block]': np.nan
    }

    # Recode the responses
    for col in data.columns:
        for question_number in question_numbers:
            if question_number in col:
                # Extract the shortened form of the question number from the column name
                shortened_question_number = col.split(' ')[0]

                if shortened_question_number in reverse_coding:
                    data[col] = data[col].replace(reverse_response_recoding_key)
                else:
                    data[col] = data[col].replace(normal_response_recoding_key)

    follow_up_recoding_key = {
        'Not distressed': 2,
        'Somewhat distressed': 3,
        'Distressed': 4,
        'Very distressed': 5,
        'Skip [this question and the remainder of this question block]': np.nan
    }

    # Get a list of all column names
    column_names = data.columns.tolist()

    # Recode the follow-up responses
    for i, col in enumerate(column_names):
        # Extract the shortened form of the question number from the column name
        shortened_question_number = col.split(' ')[0]

        # Check if the shortened question number is in the question numbers list
        if shortened_question_number in question_numbers:
            # Check if this is not the last column to avoid index out of range
            if i != len(column_names) - 1:
                # The follow-up column is the column to the right of the current column
                follow_up_col = column_names[i + 1]

                # Recode the follow-up column
                data[follow_up_col] = data[follow_up_col].replace(
                    follow_up_recoding_key)

    # Iterate through the DataFrame columns and replace question cells values with follow-up values if required
    for i, col in enumerate(column_names):
        # Extract the shortened form of the question number from the column name
        shortened_question_number = col.split(' ')[0]

        # Check if the shortened question number is in the question numbers list
        if shortened_question_number in question_numbers:
            # Check if this is not the last column to avoid index out of range
            if i != len(column_names) - 1:
                # The follow-up column is the column to the right of the current column
                follow_up_col = column_names[i + 1]

                # Compare values in the question and follow-up columns
                data[col] = data[[col, follow_up_col]].max(axis=1)

        # Iterate through the DataFrame columns
        for i, col in enumerate(column_names):
            # Extract the shortened form of the question number from the column name
            shortened_question_number = col.split(' ')[0]

            # Check if the shortened question number is in the question numbers list
            if shortened_question_number in question_numbers:
                # Check if this is not the last column to avoid index out of range
                if i != len(column_names) - 1:
                    # The follow-up column is the column to the right of the current column
                    follow_up_col = column_names[i + 1]

                    # Check if the data types are numeric
                    if np.issubdtype(data[col].dtype,
                                     np.number) and np.issubdtype(
                            data[follow_up_col].dtype, np.number):
                        # Compare values in the question and follow-up columns
                        data[col] = data[[col, follow_up_col]].max(axis=1)

        #def clean_data(wk):
    # ... All previous steps remain the same ...

    # List to keep track of follow-up columns
    follow_up_columns = []

    # Iterate through the DataFrame columns
    for i, col in enumerate(column_names):
        # Extract the shortened form of the question number from the column name
        shortened_question_number = col.split(' ')[0]

        # Check if the shortened question number is in the question numbers list
        if shortened_question_number in question_numbers:
            # Check if this is not the last column to avoid index out of range
            if i != len(column_names) - 1:
                # The follow-up column is the column to the right of the current column
                follow_up_col = column_names[i + 1]

                # Check if the data types are numeric
                if np.issubdtype(data[col].dtype, np.number) and np.issubdtype(data[follow_up_col].dtype, np.number):
                    # Compare values in the question and follow-up columns
                    data[col] = data[[col, follow_up_col]].max(axis=1)

                # Add the follow-up column to the list
                follow_up_columns.append(follow_up_col)

    # Remove follow-up columns
    data = data.drop(columns=follow_up_columns)

    # Remove any remaining unnamed and completely empty columns
    unnamed_columns = [col for col in data.columns if 'Unnamed' in col and data[col].isna().all()]
    data = data.drop(columns=unnamed_columns)

    # Define the recoding key for Grade and apply
    grade_key = {
        'A Resident Medical Officer (RMO)': 'RMO',
        'A Senior Medical Officer (SMO)': 'SMO',
        'A Registrar': 'Reg'
    }

    data['Grade'] = data['Grade'].replace(grade_key)

    # Define the recoding key for place of medical degree and recode
    degree_key = {
        'An overseas university, I am an International Medical Graduate (IMG)': 'International',
        'A New Zealand university, I am a local graduate': 'Local'
    }

    data['Registerable degree'] = data['Registerable degree'].replace(
        degree_key)

    # Define a simplified name recoding for specialty and apply
    specialty_key = {
        'Medical Specialty (mainly ward and clinic based practice, few procedures)': 'Medical',
        'Surgical Specialty (mainly procedural practice)': 'Surgical',
        'Other patient-facing role (use the free text entry box)': 'Other'
    }

    data['Specialty group'] = data['Specialty group'].replace(specialty_key)

    # Clean 'Other' specialties to ensure consistency

    # Get a list of all column names
    column_names = data.columns.tolist()

    # Find the index of 'Specialty group' column
    specialty_group_index = column_names.index('Specialty group')

    # Iterate through 'Specialty group' column
    for i, specialty in enumerate(data['Specialty group']):
        if specialty == 'Other':
            next_cell_value = data.loc[
                i, 'More precisely, my specialty / subspecialty is:'].lower()  # Convert to lower case
            if next_cell_value in ['paed', 'paediatric', 'paeds', 'paediatrics',
                                   'kids', 'ped']:  # Lower case search terms
                data.loc[i, 'Specialty group'] = 'Medical'
            elif next_cell_value in ['o&g', 'obs & gynae',
                                     'obgyn', 'o+g', 'obs & gyne', 'obs + gyne', 'obs and gyne'
                                     'obs and gynae', 'obs + gynae',
                                     'obstetrics and gynaecology', 'obstetrics & gynaecology',
                                     'obstetrics + gynaecology']:  # Lower case search terms
                data.loc[i, 'Specialty group'] = 'Surgical'

    # Simplify junior support during sleep hours
    # Define key
    sleep_hours_key = {
        'I am the first doctor in my specialty to be called. There is no junior support in my specialty.': 'No junior support',
        'There are doctors junior to me, working in my specialty, already on site': 'Junior support',
    }

    # Apply the recoding
    data[
        'When I am called to attend patients during sleep hours (2230 - 0630):'] = \
    data[
        'When I am called to attend patients during sleep hours (2230 - 0630):'].replace(
        sleep_hours_key)

    # Save the cleaned data back to CSV
    cleaned_file_path = wk.replace('.csv', '_cleaned.csv')
    data.to_csv(cleaned_file_path, index=False)

    print(
        "Data are now cleaned and saved as 'working_copy_cleaned.csv' in the 'data' directory")
