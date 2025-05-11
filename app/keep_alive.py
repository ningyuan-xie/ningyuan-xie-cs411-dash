import requests
import time
import threading

def ping_server():
    """Pings the server to prevent cold starts."""
    try:
        response = requests.get('http://0.0.0.0:8050/')
        print(f"Server pinged at {time.ctime()}. Status code: {response.status_code}")
    except Exception as e:
        pass

def start_keep_alive():
    """Runs keep-alive pings every 3 minutes in a background thread."""
    def run_scheduler():
        while True:
            ping_server()
            time.sleep(180)
    
    threading.Thread(target=run_scheduler, daemon=True).start()
    print("Keep-alive scheduler started.") 
