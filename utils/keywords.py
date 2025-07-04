# utils/keywords.py

import docx2txt
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_docx(path):
    return docx2txt.process(path)

def extract_keywords(text):
    prompt = f"""
You are an expert career assistant. Analyze this resume text and extract:

1. 3 to 5 job titles this person is qualified for
2. 5 to 10 relevant skills, tools, or technologies they specialize in

Resume:
{text[:3000]}

Respond in JSON like:
{{"titles": [...], "skills": [...]}}
Only return JSON.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        return parsed.get("titles", []), parsed.get("skills", [])
    except json.JSONDecodeError:
        print("⚠️ Could not parse GPT response:")
        print(content)
        return [], []
