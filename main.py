import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyzeData(all_data):
    json_string = json.dumps(all_data, indent=2)

    prompt = f"""
    You are analyzing hackathon participants from DevPost.
    Here is the participant dataset in JSON format:

    {json_string}

    Using this data:
    1. RANK the participants by how impressive their hackathon performance is.
       Consider: win count and competition size (winning a 500 person hackathon 
       is more impressive than a 50 person one).
    2. EXTRACT TRENDS across all participants.

    Respond only in JSON with keys "rankings" (list) and "trends" (list of strings).
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ← updated model
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"Raw response: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        raw = response.choices[0].message.content
        print(f"Raw Groq response: {raw}")
        return raw
    