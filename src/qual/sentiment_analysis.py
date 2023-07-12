# Reads responses to free text questions and uses GPT to analyse sentiment
# Writes output to file

import openai
import json
import pandas as pd

# Load API key from secrets.json
with open('secrets.json') as f:
    secrets = json.load(f)
openai.api_key = secrets['openai_api_key']


def sentiment(data):
    # Columns to analyze
    columns_to_analyze = [
        'What are things that make your work enjoyable and fulfilling? Have these things become more or less common in your recent experience? Are there factors that make your role eu-stressful (stressful and challenging, but in a good way)? Are these factors more or less present in your recent experience?',
        'What do you experience in your work that makes it (dis)stressful, unpleasant, and/or unfulfilling to perform your role? How commonplace are these experiences?',
        'Do you have any thoughts about how your work could be redesigned to be less (dis)stressful?',
        'If you could make one single positive improvement to your work or workplace; one that would make the most difference to you, what would it be?',
        'Do you have any other comments about your work situation or role? Is there anything previous questions failed to allow you to express regarding workplace stressors?'
    ]

    # Iterate through each row
    for i, row in data.iterrows():
        # Iterate through each column
        for column in columns_to_analyze:
            text = row[column]
            if pd.isnull(text):
                continue

            # Generate the sentiment
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Classify the sentiment in: {text}",
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            sentiment = response.choices[0].text.strip()

            # Update the cell with the sentiment
            data.at[i, column] = f"({sentiment}). {text}"



    return data
