# pi-iot

Simple code to read sensor data and send to Azure IoT Hub

## Instructions

1. SSH into your Raspberry PI
1. `git clone https://github.com/adestr/pi-iot`
1. `cd pi-iot`
1. `chmod u+x setup.sh`
1. `./setup.sh`
1. `python app.py '<IoT Hub Connection String>'`

You'll need to make sure you're set up to build on your Pi, and you'll need to create a device in Azure IoT Hub; these should be pretty straightforward.
