import psutil
import time
import os
import multiprocessing

THRESHOLD = 75
ZONE = "us-central1-a"
MIG_NAME = "my-mig"
TEMPLATE_NAME = "my-template"
SETUP_DONE = False


# LOCAL CPU STRESS
def stress_cpu():
    while True:
        pass


def start_stress():
    print("\nSTEP 1: Starting LOCAL CPU stress...\n")

    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)

    return processes


# CREATE INSTANCE TEMPLATE
def create_template():
    print("STEP 2: Creating instance template...\n")

    os.system(f"""
    gcloud compute instance-templates create {TEMPLATE_NAME} \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud
    """)


# CREATE MIG
def create_mig():
    print("STEP 3: Creating managed instance group...\n")

    os.system(f"""
    gcloud compute instance-groups managed create {MIG_NAME} \
    --base-instance-name autoscale-vm \
    --size=1 \
    --template={TEMPLATE_NAME} \
    --zone={ZONE}
    """)


# ENABLE AUTOSCALING
def enable_autoscaling():
    print("STEP 4: Enabling autoscaling...\n")

    os.system(f"""
    gcloud compute instance-groups managed set-autoscaling {MIG_NAME} \
    --zone={ZONE} \
    --max-num-replicas=3 \
    --target-cpu-utilization=0.75 \
    --cool-down-period=60
    """)


# APPLY STRESS ON GCP INSTANCE
def stress_gcp():
    print("\nSTEP 5: Applying stress on GCP instance...\n")

    # Get first instance name
    instance = os.popen(f"""
    gcloud compute instance-groups managed list-instances {MIG_NAME} \
    --zone={ZONE} \
    --format="value(instance)"
    """).read().strip().split("\n")[0]

    os.system(f"""
    gcloud compute ssh {instance} --zone={ZONE} --command="
    sudo apt update -y &&
    sudo apt install -y stress &&
    stress --cpu 2 --timeout 120
    "
    """)


# MONITOR MIG SIZE
def monitor_mig():
    print("\nChecking instance count in MIG...\n")

    os.system(f"""
    gcloud compute instance-groups managed list-instances {MIG_NAME} \
    --zone={ZONE}
    """)


# MAIN MONITOR LOOP
def monitor():
    global SETUP_DONE

    print("\nSTEP 2: Monitoring CPU...\n")

    while True:
        cpu = psutil.cpu_percent(interval=2)
        print(f"CPU Usage: {cpu}%")

        # Run setup once
        if not SETUP_DONE:
            create_template()
            create_mig()
            enable_autoscaling()
            SETUP_DONE = True

        if cpu > THRESHOLD:
            print("\nThreshold exceeded (>75%)")
            print("Triggering GCP autoscaling\n")

            stress_gcp()

        monitor_mig()

        time.sleep(10)


# MAIN
if __name__ == "__main__":
    print("\n==============================")
    print("CLOUD AUTO-SCALING DEMO")
    print("==============================\n")

    start_stress()
    monitor()
