import psutil
import time
import os
import multiprocessing

THRESHOLD = 75
SETUP_DONE = False


# 🔥 CPU Stress
def stress_cpu():
    while True:
        pass


def start_stress():
    print("\n⚡ Step 1: Starting CPU stress...")
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)
    return processes


# 🚀 Step 2: Create Instance Template
def create_template():
    print("\n📦 Step 2: Creating Instance Template...")

    os.system("""
    gcloud compute instance-templates create my-template \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --metadata=startup-script='#! /bin/bash
    sudo apt update
    sudo apt install -y python3-pip
    pip3 install flask
    cat <<EOF > app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Auto Scaling VM"

app.run(host="0.0.0.0", port=5000)
EOF
    python3 app.py'
    """)


# 🚀 Step 3: Create MIG
def create_mig():
    print("\n🖥️ Step 3: Creating Managed Instance Group...")

    os.system("""
    gcloud compute instance-groups managed create my-mig \
    --base-instance-name autoscale-vm \
    --size=1 \
    --template=my-template \
    --zone=us-central1-a
    """)


# 🚀 Step 4: Enable Autoscaling
def enable_autoscaling():
    print("\n📈 Step 4: Enabling Autoscaling (CPU > 75%)...")

    os.system("""
    gcloud compute instance-groups managed set-autoscaling my-mig \
    --zone=us-central1-a \
    --max-num-replicas=3 \
    --target-cpu-utilization=0.75 \
    --cool-down-period=60
    """)


# 🔍 Step 5: Monitor MIG
def monitor_mig():
    print("\n🔍 Monitoring instance group...")
    os.system("""
    gcloud compute instance-groups managed list-instances my-mig \
    --zone=us-central1-a
    """)


# MAIN
if __name__ == "__main__":

    print("\n🚀 CLOUD AUTO-SCALING DEMO STARTED\n")

    # Step 1: Start stress
    stress_processes = start_stress()


    while True:
        cpu = psutil.cpu_percent(interval=2)
        print(f"\n📊 CPU Usage: {cpu}%")

        # Run setup once
        if not SETUP_DONE:
            create_template()
            create_mig()
            enable_autoscaling()
            SETUP_DONE = True

        # Show scaling trigger
        if cpu > THRESHOLD:
            print("\n🔥 CPU Threshold Exceeded (>75%)")
            print("➡️ Autoscaler will increase instances in GCP\n")

        # Monitor MIG status
        monitor_mig()

        time.sleep(10)
