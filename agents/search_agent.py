# agents/search_agent.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os
import json
import requests
from dotenv import load_dotenv
from utils.keywords import extract_text_from_docx, extract_keywords

load_dotenv()

def generate_boolean_query_from_resume(resume_path):
    print("📄 Reading resume to generate Boolean query...")
    text = extract_text_from_docx(resume_path)
    titles, skills = extract_keywords(text)

    titles = [f'"{t}"' for t in titles if len(t.split()) <= 6][:5]
    skills = [f'"{s}"' for s in skills if len(s.split()) <= 3][:5]
    modifiers = ['"hiring"', '"careers"', '"apply now"']

    query = f"({' OR '.join(titles + skills)}) AND (job OR apply OR opening OR hiring OR opportunity) -site:linkedin.com"
    print(f"\n🔍 Generated Boolean query:\n{query}")
    return query

def search_jobs(query):
    api_key = os.getenv("SERPAPI_KEY")
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 10,
        "gl": "us",
        "hl": "en"
    }

    response = requests.get("https://serpapi.com/search", params=params)
    print("\n📄 Full SerpAPI response:")
    print(json.dumps(response.json(), indent=2))  # Debug print

    results = response.json().get("organic_results", [])

    filtered_results = []
    for r in results:
        url = r.get("link", "").lower()
        title = r.get("title", "").lower()

        # Include if it looks like a job post
        allowlist = [
            "myworkdayjobs.com", "oraclecloud.com/hcmui", "greenhouse.io", "boards.greenhouse.io",
            "lever.co", "/careers/", "/job/", "/apply/", "jobs.", "/opportunities/"
        ]
        is_job = any(x in url for x in allowlist)

        # Avoid news or directories
        blocklist = [
            ".gov", ".mil", "x.com", "/news", "/people", "/about", "in-the-news", "linkedin.com", "indeed.com/q-"
        ]
        is_bad = any(x in url for x in blocklist)

        # Add if it passes the filter
        if is_job and not is_bad:
            filtered_results.append({
                "title": r.get("title", "[No Title]"),
                "link": r.get("link", "#"),
                "snippet": r.get("snippet", "")
            })

    return filtered_results

if __name__ == "__main__":
    resume_path = "data/resumes/example_resume.docx"
    query = generate_boolean_query_from_resume(resume_path)
    results = search_jobs(query)

    print(f"\n🔎 Found {len(results)} job listings:")
    for job in results:
        print(f"\n📌 {job['title']}\n{job['link']}\n{job['snippet']}")

    os.makedirs("data/job_results", exist_ok=True)
    with open("data/job_results/boolean_search_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Results saved to data/job_results/boolean_search_results.json")
