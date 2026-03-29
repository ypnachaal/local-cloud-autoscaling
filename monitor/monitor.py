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
    print("\n🚀 STEP: Creating VM on GCP...\n")

    cmd = """
    gcloud compute instances create autoscale-vm-2 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server
    """

    result = os.system(cmd)

    if result == 0:
        print("✅ VM successfully created on GCP\n")
    else:
        print("❌ Error creating VM\n")


# 🔥 Start stress automatically
def start_stress():
    print("⚡ STEP: Starting CPU stress...\n")

    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)

    return processes


# 📊 Monitor loop
def monitor():
    global VM_CREATED

    while True:
        cpu = psutil.cpu_percent(interval=2)
        print(f"📊 CPU Usage: {cpu}%")

        if cpu > THRESHOLD and not VM_CREATED:
            print("\n🔥 Threshold exceeded (>75%)")
            print("➡️ Triggering cloud scaling...\n")

            create_gcp_vm()
            VM_CREATED = True

        time.sleep(5)


# MAIN
if __name__ == "__main__":
    print("\n🚀 AUTO-SCALING DEMO STARTED\n")

    stress_processes = start_stress()
    monitor()
