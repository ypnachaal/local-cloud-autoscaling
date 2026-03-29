gcloud compute instances create autoscale-vm-1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server \
  --metadata-from-file startup-script=createVm.sh
