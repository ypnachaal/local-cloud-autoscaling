import psutil
import time
import os
import multiprocessing

THRESHOLD = 75
VM_CREATED = False


# 🔥 Function to create CPU load
def stress_cpu():
    while True:
        pass


# 🚀 Function to create GCP VM
def create_gcp_vm():
    print("🚀 Creating VM on GCP...")

    os.system("""
    gcloud compute instances create autoscale-vm-2 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server
    """)


# 🔥 Start stress automatically
def start_stress():
    print("⚡ Starting CPU stress...")
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)
    return processes


# MAIN
if __name__ == "__main__":
    stress_processes = start_stress()

    while True:
        cpu = psutil.cpu_percent(interval=2)
        print(f"CPU Usage: {cpu}%")

        if cpu > THRESHOLD and not VM_CREATED:
            print("🔥 Threshold exceeded! Triggering auto-scale...")
            create_gcp_vm()
            VM_CREATED = True

        time.sleep(5)
