from flask import Flask, request, jsonify
import threading
import queue
import time
import os

app = Flask(__name__)

# Environment variables
SIGNAL_TOKEN = os.environ.get("SIGNAL_TOKEN", "PInu12@@")
DELTA_API_KEY = os.environ.get("DELTA_API_KEY", "bvmFpGf4f6o9jYplg7icacIbhEt637")
DELTA_API_SECRET = os.environ.get("DELTA_API_SECRET", "g5bn7Wa0x5zQu6kaaEpQbHXDh2nHYnKGAd2GgCEeQYdo1NcHwbQggLPBaZwT")

# Queue for signals
signal_queue = queue.Queue()

@app.route('/')
def home():
    return "✅ Delta Bot Render API Active"

@app.route('/signal', methods=['POST'])
def receive_signal():
    data = request.get_json()
    token = data.get("token") if data else None

    # Debug print (visible in Render logs)
    print(f"DEBUG: Received token={token} | Expected SIGNAL_TOKEN={SIGNAL_TOKEN}")

    if token != SIGNAL_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    if not data or "signal" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    signal_queue.put(data)
    print(f"📥 Enqueued signal: {data}")
    return jsonify({"status": "Signal received", "data": data}), 200


def process_signal(signal_data):
    """Trading logic placeholder"""
    signal = signal_data.get("signal")
    print(f"📡 Processing signal: {signal}")

    if signal == "BUY":
        print("🚀 Simulating BUY order on Delta Exchange...")
    elif signal == "SELL":
        print("🔻 Simulating SELL order on Delta Exchange...")
    else:
        print("⚠️ Unknown signal received.")


def background_worker():
    """Background thread for processing signals"""
    while True:
        try:
            if not signal_queue.empty():
                data = signal_queue.get()
                process_signal(data)
            else:
                print("🕒 Waiting for Termux signals...")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Worker error: {e}")
            time.sleep(10)


if __name__ == '__main__':
    threading.Thread(target=background_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
