import psutil
import time
import os

THRESHOLD = 75
VM_CREATED = False

def create_gcp_vm():
    print("🚀 Creating VM on GCP...")

    os.system("""
    gcloud compute instances create autoscale-vm-1 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server
    """)

while True:
    cpu = psutil.cpu_percent(interval=2)
    print(f"CPU Usage: {cpu}%")

    if cpu > THRESHOLD and not VM_CREATED:
        print("🔥 Threshold exceeded! Triggering auto-scale...")
        create_gcp_vm()
        VM_CREATED = True

    time.sleep(5)
