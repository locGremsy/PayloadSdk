# PayloadSdk Python
This repo is officially SDK for all Gremsy's Payloads using Python

## Hardware
- Ubuntu PC (x86_64)
- Jetson platform (aarch64)
- Raspberry Pi
- Qualcomm RB5165

## Software
This branch supported:
- Vio payload: software v2.0.0 or higher
- Zio payload: not supported yet
- GHardron payload: not supported yet
- OrusL payload: software v2.0.0 or higher
- Support Python-version: [3.6, 3.7, 3.8, 3.9]

## Clone the project 
```shell
git clone --recurse-submodules -b develop ssh://git@gitlab.gremsy.vn:2224/ai/tay-cu/payloadsdk_python.git
```

## How to build and run example
- Navigate to the cloned directory and install required packages

```shell
cd payloadsdk_python/
pip3 install -r requirements.txt
```

- Run script file to build the project

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

- Run example
```shell
python3 PayloadSdk/python_example/payload_do_object_detection.cpp
```