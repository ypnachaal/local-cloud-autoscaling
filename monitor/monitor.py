def create_gcp_vm():
    print("\n🚀 STEP: Checking if VM already exists...\n")

    check_cmd = """
    gcloud compute instances list --filter="name=autoscale-vm-2" --format="value(name)"
    """

    existing_vm = os.popen(check_cmd).read().strip()

    if existing_vm == "autoscale-vm-2":
        print("✅ VM already exists. Reusing existing VM.\n")
        return

    print("⚡ VM not found. Creating new VM...\n")

    create_cmd = """
    gcloud compute instances create autoscale-vm-2 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server
    """

    result = os.system(create_cmd)

    if result == 0:
        print("✅ VM successfully created on GCP\n")
    else:
        print("❌ Error creating VM\n")
