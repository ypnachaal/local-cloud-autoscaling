import psutil
import time
import os

THRESHOLD = 75

def trigger_cloud():
    print("Threshold exceeded! Triggering cloud scaling...")
    os.system("bash deploy_to_cloud.sh")

while True:
    cpu = psutil.cpu_percent(interval=2)
    mem = psutil.virtual_memory().percent

    print(f"CPU: {cpu}%, Memory: {mem}%")

    if cpu > THRESHOLD or mem > THRESHOLD:
        trigger_cloud()
        break

    time.sleep(5)
