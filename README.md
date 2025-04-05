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

## How to build
- Run script for update wrapper.cpp file to PayloadSDK libs

```shell
chmod +x update_payloadsdk.sh
./update_payloadsdk.sh
```

- Build share lib
<pre>
cd PayloadSdk
mkdir build && cd build

cmake -D<b>payload</b> ../
<i>e.g. cmake -DVIO=1 ../</i>
<i>     cmake -DGHADRON=1 ../</i>
<i>     cmake -DZIO=1 ../</i>

make -j6

</pre>
