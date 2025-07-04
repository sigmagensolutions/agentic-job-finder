import requests

try:
    print("🔍 Sending test request to SerpAPI...")
    response = requests.get("https://serpapi.com/search", timeout=10)
    print(f"✅ Status code: {response.status_code}")
    print(f"📄 Response (first 200 chars):\n{response.text[:200]}")
except requests.exceptions.RequestException as e:
    print("❌ Request failed:")
    print(e)
