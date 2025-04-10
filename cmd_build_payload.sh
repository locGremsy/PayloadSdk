#!/bin/bash

# Define paths
WRAPPER_FILE="./wrapper.cpp"
LIBS_DIR="./PayloadSdk/libs"
LIBS_PYTHON_DIR="./PayloadSdk/libs_python"
CMAKELISTS_FILE="$LIBS_DIR/CMakeLists.txt"
PYTHON_EXAMPLE_DIR="./python_example"
PAYLOAD_SDK_FILE="$PYTHON_EXAMPLE_DIR/payload_sdk.py"
PAYLOAD_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/payload_define.py"
MAVLINK_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/mavlink_define.py"
PAYLOAD_SDK_DIR="./PayloadSdk"
PAYLOAD_CMAKELISTS_FILE="$PAYLOAD_SDK_DIR/CMakeLists.txt"

usage() {
    echo "Usage: $0 [--payload <PAYLOAD_TYPE>] [--ip <IP_ADDRESS>] [--port <PORT>]"
    echo "  --payload: Specify payload type (VIO, ZIO, or GHADRON) - Required"
    echo "  --ip: Specify IP address for control (default: 192.168.55.1)"
    echo "  --port: Specify port for control (default: 14566)"
    echo "Example: $0 --payload VIO --ip 192.168.55.1 --port 14566"
    exit 1
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --payload)
            PAYLOAD_TYPE="$2"
            shift 2
            ;;
        --ip)
            IP_ADDRESS="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

# Kiểm tra và thiết lập giá trị mặc định cho PAYLOAD_TYPE
if [ -z "$PAYLOAD_TYPE" ]; then
    echo "Error: Missing --payload argument (required)."
    usage
fi

case "$PAYLOAD_TYPE" in
    VIO|ZIO|GHADRON)
        echo "Payload type set to: $PAYLOAD_TYPE"
        ;;
    *)
        echo "Error: Invalid PAYLOAD_TYPE. Must be VIO, ZIO, or GHADRON."
        usage
        ;;
esac

# Thiết lập giá trị mặc định cho IP_ADDRESS và PORT
DEFAULT_IP="192.168.55.1"
DEFAULT_PORT="14566"

# Nếu chỉ nhập --port mà không nhập --ip, dùng IP mặc định
if [ -n "$PORT" ] && [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS="$DEFAULT_IP"
    echo "No IP address provided, using default: $IP_ADDRESS with specified port: $PORT"
fi

# Nếu chỉ nhập --ip mà không nhập --port, dùng PORT mặc định
if [ -n "$IP_ADDRESS" ] && [ -z "$PORT" ]; then
    PORT="$DEFAULT_PORT"
    echo "No port provided, using default: $PORT with specified IP: $IP_ADDRESS"
fi

# Nếu không nhập cả hai, dùng cả IP và PORT mặc định
if [ -z "$IP_ADDRESS" ] && [ -z "$PORT" ]; then
    IP_ADDRESS="$DEFAULT_IP"
    PORT="$DEFAULT_PORT"
    echo "No IP address or port provided, using defaults: IP=$IP_ADDRESS, Port=$PORT"
fi

# In thông báo sử dụng Payload, IP và Port
echo "Using configuration: Payload=$PAYLOAD_TYPE, IP=$IP_ADDRESS, Port=$PORT"

PAYLOADSDK_H_FILE="$LIBS_DIR/payloadsdk.h"

echo "Updating udp_ip_target and udp_port_target in $PAYLOADSDK_H_FILE..."

if [ -f "$PAYLOADSDK_H_FILE" ]; then
    # Escape IP for sed (dùng nếu bạn cần dùng trong biểu thức regex)
    ESCAPED_IP=$(echo "$IP_ADDRESS" | sed 's/\./\\./g')

    # Chỉ thay phần IP trong chuỗi
    sed -i -E "s/(static char \*udp_ip_target = \(char\*\)\")([^\"]+)(\";)/\1$IP_ADDRESS\3/" "$PAYLOADSDK_H_FILE"

    # Chỉ thay phần số Port
    sed -i -E "s/(static int udp_port_target = )([0-9]+)(;)/\1$PORT\3/" "$PAYLOADSDK_H_FILE"

    echo "Updated udp_ip_target to $IP_ADDRESS and udp_port_target to $PORT in payloadsdk.h"
else
    echo "Error: $PAYLOADSDK_H_FILE not found!"
fi

echo "----------------------------------------------------------------------------------------------------------------------"

echo "Checking and moving Python files to $LIBS_PYTHON_DIR..."

# Check and create libs_python directory only if it doesn't exist
if [ ! -d "$LIBS_PYTHON_DIR" ]; then
    echo "Creating $LIBS_PYTHON_DIR directory..."
    mkdir "$LIBS_PYTHON_DIR"
else
    echo "$LIBS_PYTHON_DIR already exists."
fi

# Move payload_sdk.py if it exists
if [ -f "$PAYLOAD_SDK_FILE" ]; then
    mv -f "$PAYLOAD_SDK_FILE" "$LIBS_PYTHON_DIR"
    echo "Moved (or updated) $PAYLOAD_SDK_FILE to $LIBS_PYTHON_DIR"
else
    echo "Missing file: $PAYLOAD_SDK_FILE"
fi

# Move payload_define.py if it exists
if [ -f "$PAYLOAD_DEFINE_FILE" ]; then
    mv -f "$PAYLOAD_DEFINE_FILE" "$LIBS_PYTHON_DIR"
    echo "Moved (or updated) $PAYLOAD_DEFINE_FILE to $LIBS_PYTHON_DIR"
else
    echo "Missing file: $PAYLOAD_DEFINE_FILE"
fi

# Move mavlink_define.py if it exists
if [ -f "$MAVLINK_DEFINE_FILE" ]; then
    mv -f "$MAVLINK_DEFINE_FILE" "$LIBS_PYTHON_DIR"
    echo "Moved (or updated) $MAVLINK_DEFINE_FILE to $LIBS_PYTHON_DIR"
else
    echo "Missing file: $MAVLINK_DEFINE_FILE"
fi

echo "----------------------------------------------------------------------------------------------------------------------"

# Move python_example directory to PayloadSdk
echo "Checking and moving $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR..."

if [ -d "$PYTHON_EXAMPLE_DIR" ]; then
    if [ -d "$PAYLOAD_SDK_DIR" ]; then
        TARGET_PYTHON_EXAMPLE_DIR="$PAYLOAD_SDK_DIR/python_example"
        if [ -d "$TARGET_PYTHON_EXAMPLE_DIR" ]; then
            echo "$TARGET_PYTHON_EXAMPLE_DIR already exists. Removing to update..."
            rm -rf "$TARGET_PYTHON_EXAMPLE_DIR"
        fi
        mv "$PYTHON_EXAMPLE_DIR" "$PAYLOAD_SDK_DIR"
        echo "Moved (or updated) $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR"
    else
        echo "Missing target directory: $PAYLOAD_SDK_DIR"
    fi
else
    echo "Missing directory: $PYTHON_EXAMPLE_DIR"
fi

echo "----------------------------------------------------------------------------------------------------------------------"

# Move wrapper.cpp to the libs directory
echo "Checking and moving $WRAPPER_FILE to $LIBS_DIR..."

if [ -f "$WRAPPER_FILE" ]; then
    if [ -d "$LIBS_DIR" ]; then
        TARGET_WRAPPER_FILE="$LIBS_DIR/wrapper.cpp"
        if [ -f "$TARGET_WRAPPER_FILE" ]; then
            echo "$TARGET_WRAPPER_FILE already exists. Removing to update..."
            rm -f "$TARGET_WRAPPER_FILE"
        fi
        mv -f "$WRAPPER_FILE" "$LIBS_DIR"
        echo "Moved (or updated) $WRAPPER_FILE to $LIBS_DIR"
    else
        echo "Missing target directory: $LIBS_DIR"
    fi
else
    echo "Missing file: $WRAPPER_FILE"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Comment out examples and tests subdirectories in PayloadSdk/CMakeLists.txt
echo "Checking and commenting out subdirectories in $PAYLOAD_CMAKELISTS_FILE..."

if [ -f "$PAYLOAD_CMAKELISTS_FILE" ]; then
    # Chỉ comment nếu dòng chưa bị comment
    grep -q "^[^#]*add_subdirectory(examples)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(add_subdirectory(examples)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*if (VIO)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(if (VIO)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*add_subdirectory(tests/demo_project)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(add_subdirectory(tests\/demo_project)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*endif(VIO)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(endif(VIO)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*if (GHADRON)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(if (GHADRON)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*add_subdirectory(tests/ghadron_project)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(add_subdirectory(tests\/ghadron_project)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    grep -q "^[^#]*endif(GHADRON)" "$PAYLOAD_CMAKELISTS_FILE" && \
        sed -i 's/^[[:space:]]*\(endif(GHADRON)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"

    echo "Commented necessary lines in $PAYLOAD_CMAKELISTS_FILE"
else
    echo "Error: $PAYLOAD_CMAKELISTS_FILE does not exist, skipping update."
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Ensure wrapper.cpp is not already in SOURCES block
echo "Checking and updating $CMAKELISTS_FILE for wrapper.cpp in SOURCES..."

if [ -f "$CMAKELISTS_FILE" ]; then
    if ! grep -q "wrapper.cpp" "$CMAKELISTS_FILE"; then
        sed -i '/file(GLOB_RECURSE SOURCES/,/^[ \t]*)/s/^[ \t]*)/            ${CMAKE_CURRENT_SOURCE_DIR}\/wrapper.cpp\n            )/' "$CMAKELISTS_FILE"
        echo "Added wrapper.cpp to SOURCES block"
    else
        echo "Skipping wrapper.cpp addition (already present in SOURCES)"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi


echo "----------------------------------------------------------------------------------------------------------------------"
# Change STATIC to SHARED in add_library if not already changed
echo "Checking and updating $CMAKELISTS_FILE for SHARED library..."

if [ -f "$CMAKELISTS_FILE" ]; then
    if grep -q "add_library(\${PROJECT_NAME} STATIC" "$CMAKELISTS_FILE"; then
        sed -i 's/add_library(${PROJECT_NAME} STATIC/add_library(${PROJECT_NAME} SHARED/' "$CMAKELISTS_FILE"
        echo "Changed STATIC to SHARED in add_library"
    else
        echo "Skipping STATIC to SHARED change (already set to SHARED or not applicable)"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi


echo "----------------------------------------------------------------------------------------------------------------------"
# Add the set_target_properties block at the end if it doesn't exist
echo "Checking and adding set_target_properties to $CMAKELISTS_FILE..."

if [ -f "$CMAKELISTS_FILE" ]; then
    if ! grep -q "set_target_properties(\${PROJECT_NAME} PROPERTIES" "$CMAKELISTS_FILE"; then
        cat <<EOL >> "$CMAKELISTS_FILE"

set_target_properties(\${PROJECT_NAME} PROPERTIES
   CXX_VISIBILITY "default"  # Ensure C++ functions are exported
   VISIBILITY_INLINES_HIDDEN ON
)
EOL
        echo "Added set_target_properties block"
    else
        echo "Skipping set_target_properties addition (already present)"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Build the project
echo "Building the project with PAYLOAD_TYPE=$PAYLOAD_TYPE..."
cd "$PAYLOAD_SDK_DIR"

# Kiểm tra thư mục build
if [ ! -d "build" ]; then
    echo "Creating build directory..."
    mkdir build
else
    echo "Build directory already exists."
fi

cd build

# Xóa cache cmake cũ nếu có
if [ -f "CMakeCache.txt" ]; then
    echo "Removing old CMakeCache.txt..."
    rm CMakeCache.txt
    rm -rf CMakeFiles
fi

# Chạy cmake dựa trên PAYLOAD_TYPE
case "$PAYLOAD_TYPE" in
    VIO)
        cmake -DVIO=1 ..
        ;;
    ZIO)
        cmake -DZIO=1 ..
        ;;
    GHADRON)
        cmake -DGHADRON=1 ..
        ;;
esac

make -j6

echo "Build complete."
echo "Modifications and build complete."