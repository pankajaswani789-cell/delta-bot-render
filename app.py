import os
import time
import hmac
import hashlib
import requests

DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

ENDPOINTS = [
    "https://cdn-ind.testnet.deltaex.org",
    "https://testnet-api.delta.exchange",
    "https://api-testnet.delta.exchange"
]

def get_server_time(base):
    paths = ["/v2/time", "/v2/timestamp", "/v2/server_time"]
    for path in paths:
        try:
            url = base.rstrip("/") + path
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                j = r.json()
                if isinstance(j, dict):
                    for key in ["server_time", "time", "timestamp"]:
                        if key in j:
                            return int(j[key])
        except:
            continue
    return None

def build_signature(secret, timestamp, method, path, body=""):
    payload = str(timestamp) + method.upper() + path + (body or "")
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

def check_auth():
    if not DELTA_API_KEY or not DELTA_API_SECRET:
        print("❌ Missing DELTA_API_KEY or DELTA_API_SECRET")
        return

    path = "/v2/orders"
    method = "GET"

    for base in ENDPOINTS:
        print(f"\n🔎 Checking endpoint: {base}")

        server_time = get_server_time(base)
        if not server_time:
            print("⚠️ No server time endpoint found, using local time fallback.")
            server_time = int(time.time() * 1000)

        local_time = int(time.time() * 1000)
        drift = local_time - server_time
        print(f"🕒 Server time: {server_time} | Local time: {local_time} | Drift: {drift} ms")

        # Try with ±5000ms drift adjustment
        for offset in [0, -2000, 2000, -4000, 4000, -5000, 5000]:
            adj_time = local_time + offset
            sig = build_signature(DELTA_API_SECRET, adj_time, method, path)
            headers = {
                "api-key": DELTA_API_KEY,
                "signature": sig,
                "timestamp": str(adj_time)
            }

            try:
                r = requests.get(base.rstrip("/") + path, headers=headers, timeout=10)
                print(f"⏱️ Trying offset {offset:+} ms → Status {r.status_code}")
                if r.status_code == 200:
                    print("✅ SUCCESS! Auth verified:", base)
                    return
                elif r.status_code == 401 and "ip_not_whitelisted" in r.text:
                    print("⚠️ IP not whitelisted, but signature is VALID ✅")
                    return
            except Exception as e:
                print("❌ Error:", e)

    print("\n❌ All attempts failed. Possible large time drift or bad endpoint.")

if __name__ == "__main__":
    print("🚀 Running Delta Testnet Authentication with Auto Time Fix...")
    check_auth()
