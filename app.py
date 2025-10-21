import time
import requests
import os

BASE_URL = "https://cdn-ind.testnet.deltaex.org"

print("✅ Bot is running...")

try:
    r = requests.get(BASE_URL + "/v2/public/time")
    print("Fetched server_time:", r.json().get("result", {}).get("server_time"))
except Exception as e:
    print("Time fetch error:", e)

while True:
    print("Working... (replace this with your bot code)")
    time.sleep(20)
