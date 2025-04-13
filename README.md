# PayloadSdk Python
This repo is officially SDK for all Gremsy's Payloads using Python.

## Hardware
- Ubuntu PC (x86_64)
- Jetson platform (aarch64)
- Raspberry Pi
- Qualcomm RB5165

## Software
This branch supports:
- Vio payload: Software v2.0.0 or higher
- Zio payload: not supported yet
- GHardron payload: not supported yet
- OrusL payload: Software v2.0.0 or higher
- Supported Python versions: 3.6, 3.7, 3.8, 3.9, 3.11

## Clone the project 
```shell
git clone --recurse-submodules -b python_sdk_v3 git@github.com:Gremsy/PayloadSdk.git
```

## Install required libraries
After cloning the submodule PayloadSdk C++, install the required libraries:

```shell
sudo apt-get install libcurl4-openssl-dev libjsoncpp-dev
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

## Setup Environment
You can set up the environment using either `conda` or `virtualenv`.

### Using Conda
```shell
conda create -n payloadsdk_env python=3.8
conda activate payloadsdk_env
pip install -r requirements.txt
```

### Using Virtualenv
```shell
python3 -m venv payloadsdk_env
source payloadsdk_env/bin/activate
pip install -r requirements.txt
```

## How to build and run example
- Navigate to the cloned directory and install required packages:

```shell
cd payloadsdk_python/
pip3 install -r requirements.txt
```

- Run the script file to build the project:

```bash
chmod +x cmd_build_payload.sh
./cmd_build_payload.sh --payload VIO --ip 192.168.55.1 --port 14566
```

**Usage:**

```text
./cmd_build_payload.sh [--payload <PAYLOAD_TYPE>] [--ip <IP_ADDRESS>] [--port <PORT>]
  --payload: Specify payload type (VIO, ZIO, or GHADRON) - Required
  --ip: Specify IP address for control (default: 192.168.55.1)
  --port: Specify port for control (default: 14566)

Example: 
  ./cmd_build_payload.sh --payload VIO --ip 192.168.55.1 --port 14566
```

> **Note:** The default IP address `192.168.55.1` is used when connecting via physical USB Type-C. If using an internet connection, replace it with the appropriate IP address assigned by your network.

- Run the example:
```shell
python3 python_example/payload_do_object_detection.py
```
