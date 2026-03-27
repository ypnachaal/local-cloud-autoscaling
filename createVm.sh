cat > createVm.sh << 'EOF'
gcloud compute instances create autoscale-vm-1 \
--zone=us-central1-a \
--machine-type=e2-micro \
--image-family=ubuntu-2204-lts \
--image-project=ubuntu-os-cloud \
--tags=http-server \
--metadata=startup-script='#! /bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install flask
cat <<APP > app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from GCP VM"

app.run(host="0.0.0.0", port=5000)
APP
python3 app.py'
EOF