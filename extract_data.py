import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def extract_profile_info(text):
    prompt = f"""
    Extract the following details from the text: name, spouse, birthdate, nationality, and keywords (separated by commas).
    For keywords, select the most relevant ones and maximum 5 keywords in total.
    Please format your response in JSON format like this:
    {{
        "name": "Name of the person",
        "spouse": "Spouse's name",
        "birthdate": "Birthdate of the person",
        "nationality": "Nationality of the person",
        "keywords": "keyword1, keyword2, etc."
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user", "content": text[:10000]}
        ],
        temperature=0.5
    )

    extracted_info = response["choices"][0]["message"]["content"]

    try:
        extracted_data = json.loads(extracted_info)
    except json.JSONDecodeError:
        extracted_data = {"error": "Failed to extract data in JSON format"}

    return json.dumps(extracted_data, indent=4)