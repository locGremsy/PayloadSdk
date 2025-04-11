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

## Clone the project 
```
git clone --recurse-submodules -b develop ssh://git@gitlab.gremsy.vn:2224/ai/tay-cu/payloadsdk_python.git
```

## How to build and run example
- Run script for build project

```shell
chmod +x cmd_build_payload.sh
./cmd_build_payload.sh
```

- Run example
```shell
python3 PayloadSdk/python_example/payload_do_object_detection.cpp
```