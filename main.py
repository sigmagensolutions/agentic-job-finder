# main.py

import os
import json
from agents.search_agent import generate_boolean_query_from_resume, search_jobs
from agents.match_agent import rank_jobs
from agents.comms_agent import send_ranked_results_email

os.makedirs("outputs", exist_ok=True)


def main():
    print("🚀 Job Finder Workflow Starting...")

    # 1. Load resume and generate Boolean search query
    resume_path = "data/resumes/example_resume.docx"
    query = generate_boolean_query_from_resume(resume_path)

    # 2. Perform search
    raw_results = search_jobs(query)

    # 3. Save raw results
    os.makedirs("data/job_results", exist_ok=True)
    raw_path = "data/job_results/boolean_search_results.json"
    with open(raw_path, "w") as f:
        json.dump(raw_results, f, indent=2)
    print(f"\n📄 Saved raw search results to {raw_path}")

    # 4. Rank jobs
    output_path = "outputs/ranked_jobs.json"
    ranked_results = rank_jobs(resume_path, raw_results, output_path)

    ranked_path = "data/job_results/ranked_matches.json"
    with open(ranked_path, "w") as f:
        json.dump(ranked_results, f, indent=2)
    print(f"\n📄 Saved ranked results to {ranked_path}")

    # 5. Email top matches
    top_matches = ranked_results[:3]
    send_ranked_results_email(top_matches)

    print("\n✅ Workflow complete.")

if __name__ == "__main__":
    main()
