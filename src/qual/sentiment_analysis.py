# Reads responses to free text questions and uses GPT to analyse sentiment
# Writes output to file

import openai
import json
import pandas as pd

from tqdm import tqdm


# Uses OpenAI API call to text-davinci-003 gpt model to perform sentiment
# classification on free text answers and add a requirement for human checking.
def gpt_sentiment(file_path, secrets_path):
    # Load API key from secrets.json
    with open(secrets_path) as f:
        secrets = json.load(f)
    openai.api_key = secrets['OPENAI_API_KEY']

    # Load the data
    data = pd.read_csv(file_path)

    # Check if 'gpt_sentiment' and 'human_checked' columns exist.
    # If not, add them with 'False' as the first and only entries.
    if 'human_checked' not in data.columns:
        data['human_checked'] = False

    if 'gpt_sentiment' not in data.columns:
        data['gpt_sentiment'] = False
    else:
        # If 'gpt_sentiment' column exists, check whether set to 'True'
        if data['gpt_sentiment'].iloc[0]:
            print("GPT Sentiment analysis has already been performed on this "
                  "file."
                  "/nExiting to main program without making changes.")
            return

    print("Analysing sentiment using GPT LLM AI."
          "\nThis may take some time ...")

    # Columns to analyze
    columns_to_analyze = [
        'What are things that make your work enjoyable and fulfilling? '
        'Have these things become more or less common in your recent experience? '
        'Are there factors that make your role eu-stressful (stressful and '
        'challenging, but in a good way)? Are these factors more or less present'
        ' in your recent experience?',
        'What do you experience in your work that makes it (dis)stressful, '
        'unpleasant, and/or unfulfilling to perform your role? How commonplace '
        'are these experiences?',
        'Do you have any other comments about your work situation or role? '
        'Is there anything previous questions failed to allow you to express '
        'regarding workplace stressors?'
    ]

    # Iterate through each row
    for i in tqdm(range(len(data)), desc="Progress"):  # Add progress bar here
        row = data.iloc[i]
        # Iterate through each column
        for column in columns_to_analyze:
            text = row[column]
            if pd.isnull(text):
                continue

            # Generate the sentiment
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"This is a sentiment classification task. "
                       f"The question was: '{column}'. "
                       f"The response was: '{text}'. "
                       f"Classify the sentiment of the response only "
                       f"using a single word from the following: "
                       f"Positive, "
                       f"Negative, or "
                       f"Neutral.",
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            sentiment = response.choices[0].text.strip()

            # Update the cell with the sentiment
            data.at[i, column] = f"({sentiment}). {text}"

            # Update the cell with the sentiment
            data.at[i, column] = f"({sentiment}). {text}"
            # Update 'gpt_sentiment' column
            data.at[i, 'gpt_sentiment'] = True

    # Save the updated data back to the CSV file
    data.to_csv(file_path, index=False)

    print("GPT sentiment analysis by text-davinci-003 complete."
          "\nHuman check of GPT sentiment entries essential."
          "\n1. Open YYYYMMDD_ERI_data.csv file in spreadsheet application."
          "\n2. Manually change 'human_checked' entry to 'True' "
          "\n   to continue analysis.")
