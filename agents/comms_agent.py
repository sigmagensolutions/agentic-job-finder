# agents/comms_agent.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_ranked_results_email(matches):
    from_email = os.getenv("EMAIL_SENDER")
    to_email = os.getenv("EMAIL_RECIPIENT")
    sendgrid_key = os.getenv("SENDGRID_API_KEY")

    if not from_email or not to_email or not sendgrid_key:
        print("❌ Missing required environment variables.")
        return

    subject = "🎯 Your Top 3 AI/Data Science Job Matches Today"

    if not matches:
        content = "<p>No matches found today.</p>"
    else:
        content_lines = []
        for job in matches[:3]:
            title = job.get("title", "No title")
            link = job.get("link", "#")
            summary = job.get("summary", "")
            posted = job.get("posted", "")

            posted_line = f"🕒 Posted: {posted}<br>" if posted else ""

            line = f"""📌 <b>{title}</b><br>
{posted_line}
<a href="{link}">{link}</a><br>
<i>{summary}</i><br><br>"""
            content_lines.append(line)

        content = "<br>".join(content_lines).strip()

        if not content:
            content = "<p>No valid matches with summaries available.</p>"

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    try:
        sg = SendGridAPIClient(sendgrid_key)
        response = sg.send(message)
        print(f"📬 Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        if hasattr(e, 'body'):
            print(f"📨 SendGrid error body: {e.body}")
