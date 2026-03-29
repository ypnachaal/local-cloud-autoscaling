import psutil
import time
import os
import multiprocessing

THRESHOLD = 75
VM_NAME = "autoscale-vm-2"
ZONE = "us-central1-a"
VM_CREATED = False


# 🔥 Function to create CPU load
def stress_cpu():
    while True:
        pass


# ⚡ Start CPU stress
def start_stress():
    print("\n⚡ STEP 1: Starting CPU stress...\n")

    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)

    return processes


# 🔍 Check if VM exists
def check_vm_exists():
    cmd = f'gcloud compute instances list --filter="name={VM_NAME}" --format="value(name)"'
    result = os.popen(cmd).read().strip()
    return result == VM_NAME


# 🚀 Create or reuse VM
def create_or_reuse_vm():
    print("\n🚀 STEP 2: Checking VM on GCP...\n")

    if check_vm_exists():
        print("✅ VM already exists. Reusing existing VM.\n")

        # Optional: ensure it's running
        os.system(f"gcloud compute instances start {VM_NAME} --zone={ZONE}")
        return

    print("⚡ VM not found. Creating new VM...\n")

    cmd = f"""
    gcloud compute instances create {VM_NAME} \
    --zone={ZONE} \
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


# 📊 Monitor loop
def monitor():
    global VM_CREATED

    print("\n📊 STEP 2: Monitoring CPU...\n")

    while True:
        cpu = psutil.cpu_percent(interval=2)
        print(f"📊 CPU Usage: {cpu}%")

        if cpu > THRESHOLD and not VM_CREATED:
            print("\n🔥 Threshold exceeded (>75%)")
            print("➡️ Triggering cloud scaling...\n")

            create_or_reuse_vm()
            VM_CREATED = True

        time.sleep(5)


# 🚀 MAIN
if __name__ == "__main__":
    print("\n==============================")
    print("🚀 CLOUD AUTO-SCALING DEMO")
    print("==============================\n")

    stress_processes = start_stress()
    monitor()
