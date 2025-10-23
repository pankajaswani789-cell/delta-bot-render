import requests

# 🔹 Render API URL
url = "https://delta-bot-render.onrender.com/signal"

# 🔹 Data to send (signal + token)
payload = {
    "signal": "BUY",
    "token": "PInu12@@"
}

try:
    response = requests.post(url, json=payload)
    print("Response status:", response.status_code)
    print("Response body:", response.text)
except Exception as e:
    print("❌ Error:", e)
