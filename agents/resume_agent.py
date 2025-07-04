# agents/resume_agent.py

from pathlib import Path
from docx import Document
import openai
import os
import json

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)

def get_embedding(text, model="text-embedding-3-large"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def save_embedding_to_json(embedding, output_path):
    with open(output_path, "w") as f:
        json.dump(embedding, f)
    print(f"✅ Embedding saved to {output_path}")

if __name__ == "__main__":
    resume_path = Path("data/resumes/example_resume.docx")
    output_path = Path("data/resumes/example_resume_embedding.json")

    if resume_path.exists():
        print("🔍 Extracting text...")
        text = extract_text_from_docx(resume_path)

        print("🧠 Generating embedding...")
        embedding = get_embedding(text)

        print("💾 Saving embedding...")
        save_embedding_to_json(embedding, output_path)

    else:
        print(f"❌ Resume not found at {resume_path}")

