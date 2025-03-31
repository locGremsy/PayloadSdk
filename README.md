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
- Install required lib
```
sudo apt-get install libcurl4-openssl-dev libjsoncpp-dev
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

- Open the file PayloadSdk/libs/CMakeLists.txt and replace STATIC with SHARED to switch to building a shared library
```cmake
add_library(${PROJECT_NAME} SHARED ${SOURCES})
```

- Add the following code at the end of the CMakeLists.txt file to configure the target's properties
```cmake
set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_VISIBILITY "default"  # Ensure C++ functions are exported
    VISIBILITY_INLINES_HIDDEN ON
)
```

- Build share lib
<pre>
cp wrapper.cpp PayloadSdk/libs/
cd PayloadSdk
mkdir build && cd build

cmake -D<b>payload</b> ../
<i>e.g. cmake -DVIO=1 ../</i>
<i>     cmake -DGHADRON=1 ../</i>
<i>     cmake -DZIO=1 ../</i>

make -j6

</pre>
