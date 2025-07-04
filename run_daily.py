# run_daily.py

import subprocess
import datetime

print(f"\n📆 Running job finder - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Run search agent
subprocess.run(["python", "agents/search_agent.py"], check=True)

# Run match agent
subprocess.run(["python", "agents/match_agent.py"], check=True)

# Run comms agent
subprocess.run(["python", "agents/comms_agent.py"], check=True)

print("\n✅ Daily pipeline completed.")
