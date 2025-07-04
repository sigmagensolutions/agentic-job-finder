# agents/match_agent.py

import os
import json
from dotenv import load_dotenv
from utils.keywords import extract_text_from_docx
from sklearn.metrics.pairwise import cosine_similarity as cosine_sim
import numpy as np
from openai import OpenAI

# Load environment variables and initialize client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_resume_embedding(resume_path):
    text = extract_text_from_docx(resume_path)
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def get_job_embedding(job):
    job_text = f"{job.get('title', '')}\n\n{job.get('snippet', '')}"
    response = client.embeddings.create(
        input=[job_text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return float(cosine_sim([a], [b])[0][0])

def rank_jobs(resume_path, job_data_list, output_path):
    print("📂 Loading resume embedding...")
    resume_embedding = get_resume_embedding(resume_path)

    print("📂 Processing job results...")
    scored_jobs = []
    resume_text = extract_text_from_docx(resume_path)

    for job in job_data_list:
        job_embedding = get_job_embedding(job)
        similarity = cosine_similarity(resume_embedding, job_embedding)

        prompt = f"""
Compare the following resume and job description. Give a score from 0 to 1 for how well the resume matches the job (0 = no match, 1 = perfect match). Then briefly explain your reasoning.

Resume:
{resume_text}

Job Title: {job.get('title', '')}
Job Description: {job.get('snippet', '')}

Return result in JSON like:
{{
  "score": float,
  "summary": string
}}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            result = response.choices[0].message.content.strip()
            parsed = json.loads(result)
            job["score"] = round(parsed["score"], 4)
            job["summary"] = parsed["summary"]
            job["similarity"] = similarity
            job["posted_str"] = f"🕒 Posted: {job.get('posted')}" if job.get("posted") else ""
            scored_jobs.append(job)

        except Exception as e:
            print(f"⚠️ Error processing job: {job.get('title', '')}\n{e}")

    scored_jobs.sort(key=lambda x: x["score"], reverse=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(scored_jobs, f, indent=2)

    print(f"\n✅ Ranked results saved to {output_path}")
    print("\n🏆 Top 3 Matches:\n")
    for job in scored_jobs[:3]:
        print(f"📌 {job['title']} ({job['score']})\n{job['link']}\n{job.get('posted_str', '')}\n{job['summary']}\n")

    return scored_jobs
