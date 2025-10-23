from flask import Flask, request, jsonify
import threading
import queue
import time
import os

app = Flask(__name__)

# Environment variables (for future secure setup)
SIGNAL_TOKEN = os.environ.get("SIGNAL_TOKEN", "replace_with_a_strong_token")
DELTA_API_KEY = os.environ.get("DELTA_API_KEY", "")
DELTA_API_SECRET = os.environ.get("DELTA_API_SECRET", "")

# Queue for signals (thread-safe)
signal_queue = queue.Queue()

@app.route('/')
def home():
    return "✅ Delta Bot Render API Active"

@app.route('/signal', methods=['POST'])
def receive_signal():
    # Token-based authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header.replace("Bearer ", "").strip() != SIGNAL_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Get JSON data
    data = request.get_json()
    if not data or "signal" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    # Add signal to processing queue
    signal_queue.put(data)
    print(f"📥 Enqueued signal: {data}")
    return jsonify({"status": "Signal received", "data": data}), 200


def process_signal(signal_data):
    """This function processes signals (you’ll connect real trading logic later)"""
    signal = signal_data.get("signal")
    meta = signal_data.get("meta", {})
    print(f"📡 Processing signal from queue: {signal} | meta: {meta}")

    # Placeholder for your Delta Exchange logic
    if signal == "BUY":
        print("🚀 Placing BUY order (placeholder logic)...")
        result = {"status": "ok", "detail": "buy-simulated"}
    elif signal == "SELL":
        print("🔻 Placing SELL order (placeholder logic)...")
        result = {"status": "ok", "detail": "sell-simulated"}
    else:
        result = {"status": "error", "detail": "unknown signal"}

    print(f"✅ Signal processed: {result}")
    return result


def background_worker():
    """Background thread that runs forever and processes queued signals"""
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
    # Start background worker thread
    threading.Thread(target=background_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)

