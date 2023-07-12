# Recode data and calculate Effort-Reward Imbalance Index
import pandas as pd
from datetime import datetime
import os
import numpy as np

def rearrange(data):
    # Create a list of the columns in the DataFrame
    cols = list(data.columns)

    # Identify the position of each specified column and add empty columns
    pos_ERI6 = cols.index(next(col for col in cols if 'ERI6' in col)) + 1
    cols.insert(pos_ERI6, 'Effort')

    pos_ERI15 = cols.index(next(col for col in cols if 'ERI15' in col)) + 1
    cols.insert(pos_ERI15, 'Esteem')

    pos_ERI17 = cols.index(next(col for col in cols if 'ERI17' in col)) + 1
    cols.insert(pos_ERI17, 'Promotion')

    pos_ERI13 = cols.index(next(col for col in cols if 'ERI13' in col)) + 1
    cols.insert(pos_ERI13, 'Reward')
    cols.insert(pos_ERI13, 'Security')

    pos_OC6 = cols.index(next(col for col in cols if 'OC6' in col)) + 1
    cols.insert(pos_OC6, 'ERI')
    cols.insert(pos_OC6, 'Over-commitment')

    # Rearrange the DataFrame with the new column order
    data = data.reindex(columns=cols)

    return data


def recode_rewards(data):
    # Define the columns related to Esteem, Promotion, and Security
    esteem_cols = ['ERI7 (I receive the respect I deserve from my superiors.)',
                   'ERI8 (I receive the respect I deserve from my colleagues.)',
                   'ERI9 (I experience adequate support in difficult situations.)',
                   'ERI10 (I am treated unfairly at work.)',
                   'ERI15 (Considering all my efforts and achievements, I receive the respect and prestige I deserve at work.)']

    promotion_cols = ['ERI11 (My job promotion prospects are poor.)',
                      'ERI14 (My current occupational position adequately reflects my education and training.)',
                      'ERI16 (Considering all my efforts and achievements, my work prospects are adequate.)',
                      'ERI17 (Considering all my efforts and achievements, my salary/income is adequate.)']

    security_cols = [
        'ERI12 (I have experienced or I expect to experience an undesirable change in my work situation.)',
        'ERI13 (My job security is poor.)']

    # List of all the columns to be recoded
    reward_cols = esteem_cols + promotion_cols + security_cols

    # Recode the columns
    data[reward_cols] = 6 - data[reward_cols]

    print("Reward scores recoded ...")

    return data


def effort(data):
    # Define the columns related to Effort
    effort_cols = [
        'ERI1 (I have constant time pressure due to a heavy work load.)',
        'ERI2 (I have many interruptions and disturbances in my job.)',
        'ERI3 (I have a lot of responsibility in my job.)',
        'ERI4 (I am often pressured to work overtime.)',
        'ERI6 (Over the past few years, my job has become more and more demanding.)']

    # Sum the coded answer values and create the 'Effort' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Effort'] = data[effort_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("Effort scores calculated ...")

    return data


def esteem(data):
    # Define the columns related to Esteem
    esteem_cols = ['ERI7 (I receive the respect I deserve from my superiors.)',
                   'ERI8 (I receive the respect I deserve from my colleagues.)',
                   'ERI9 (I experience adequate support in difficult situations.)',
                   'ERI10 (I am treated unfairly at work.)',
                   'ERI15 (Considering all my efforts and achievements, I receive the respect and prestige I deserve at work.)']

    # Sum the coded answer values and create the 'Esteem' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Esteem'] = data[esteem_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("Esteem scores calculated ...")

    return data


def promotion(data):
    # Define the columns related to Promotion
    promotion_cols = ['ERI11 (My job promotion prospects are poor.)',
                      'ERI14 (My current occupational position adequately reflects my education and training.)',
                      'ERI16 (Considering all my efforts and achievements, my work prospects are adequate.)',
                      'ERI17 (Considering all my efforts and achievements, my salary/income is adequate.)']

    # Sum the coded answer values and create the 'Promotion' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Promotion'] = data[promotion_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("Promotion scores calculated ...")

    return data


def security(data):
    # Define the columns related to Security

    security_cols = [
        'ERI12 (I have experienced or I expect to experience an undesirable change in my work situation.)',
        'ERI13 (My job security is poor.)']

    # Sum the coded answer values and create the 'Security' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Security'] = data[security_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("(Job) Security scores calculated ...")

    return data


def reward(data):
    # Define the columns related to Esteem, Promotion, and Security
    esteem_cols = ['ERI7 (I receive the respect I deserve from my superiors.)',
                   'ERI8 (I receive the respect I deserve from my colleagues.)',
                   'ERI9 (I experience adequate support in difficult situations.)',
                   'ERI10 (I am treated unfairly at work.)',
                   'ERI15 (Considering all my efforts and achievements, I receive the respect and prestige I deserve at work.)']

    promotion_cols = ['ERI11 (My job promotion prospects are poor.)',
                      'ERI14 (My current occupational position adequately reflects my education and training.)',
                      'ERI16 (Considering all my efforts and achievements, my work prospects are adequate.)',
                      'ERI17 (Considering all my efforts and achievements, my salary/income is adequate.)']

    security_cols = ['ERI12 (I have experienced or I expect to experience an undesirable change in my work situation.)',
                     'ERI13 (My job security is poor.)']

    # List of all the columns to be summed
    reward_cols = esteem_cols + promotion_cols + security_cols

    # Sum the coded answer values and create the 'Reward' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Reward'] = data[reward_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("(Total) Reward scores calculated ...")

    return data


def over_commitment(data):
    # Define the columns related to Over-commitment
    oc_cols = ['OC1 (I get easily overwhelmed by time pressures at work.)',
               'OC2 (As soon as I get up in the morning I start thinking about work problems.)',
               'OC3 (When I get home, I can easily relax and ‘switch off’ work.)',
               'OC4 (People close to me say I sacrifice too much for my job.)',
               'OC5 (Work rarely lets me go, it is still on my mind when I go to bed.)',
               'OC6 (If I postpone something that I was supposed to do today I’ll have trouble sleeping at night.)']

    # Sum the coded answer values and create the 'Over-commitment' column
    # Use all() to check if all questions were answered, and only then perform the sum
    data['Over-commitment'] = data[oc_cols].apply(
        lambda row: row.sum() if row.notna().all() else np.nan, axis=1)

    print("Over-commitment scores calculated ...")

    return data


def eri(data):
    # Define the correction factor
    c = 0.454545

    # Calculate the effort-reward imbalance index according to the new formula ER = e/(r*c)
    # Check if both Effort and Reward are not NaN, and only then perform the calculation
    data['ERI'] = data.apply(lambda row: row['Effort'] / (row['Reward'] * c) if pd.notna(row['Effort']) and pd.notna(row['Reward']) else np.nan, axis=1)

    print("Effort-Reward Imbalance Indices calculated for each respondent.")

    return data

# Index Calculator main function
def eri_index(wcc):
    # Read the working_copy_cleaned.csv data
    data = pd.read_csv(wcc)

    # Rearrange columns to accommodate calculation results
    data = rearrange(data)  # Update 'data' with the rearranged DataFrame

    # Recode reward components
    data = recode_rewards(data)

    # Call the calculation functions
    data = effort(data)
    data = esteem(data)
    data = promotion(data)
    data = security(data)
    data = reward(data)
    data = over_commitment(data)
    data = eri(data)

    # Construct the recoded file name with an ISO date stamp
    datestamp = datetime.now().strftime("%Y%m%d")
    recoded_file_name = f"{datestamp}_ERI_data.csv"

    # Save recoded file to data folder with appropriate name and format
    recoded_file_path = os.path.join("data", recoded_file_name)
    data.to_csv(recoded_file_path, index=False)

    print("'YYYYMMDD_ERI_data.csv' saved in the data folder, ready for analysis.")

