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
    echo "Example: $0 --payload VIO --ip 192.168.12.254 --port 14566"
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
    ESCAPED_IP=$(echo "$IP_ADDRESS" | sudo sed 's/\./\\./g')

    # Chỉ thay phần IP trong chuỗi
    sudo sed -i -E "s/(static char \*udp_ip_target = \(char\*\)\")([^\"]+)(\";)/\1$IP_ADDRESS\3/" "$PAYLOADSDK_H_FILE"

    # Chỉ thay phần số Port
    sudo sed -i -E "s/(static int udp_port_target = )([0-9]+)(;)/\1$PORT\3/" "$PAYLOADSDK_H_FILE"

    echo "Updated udp_ip_target to $IP_ADDRESS and udp_port_target to $PORT in payloadsdk.h"
else
    echo "Error: $PAYLOADSDK_H_FILE not found!"
fi

echo "----------------------------------------------------------------------------------------------------------------------"

echo "Checking and moving Python files to $LIBS_PYTHON_DIR..."

# Tạo thư mục nếu chưa tồn tại
if [ ! -d "$LIBS_PYTHON_DIR" ]; then
    echo "Creating $LIBS_PYTHON_DIR directory..."
    mkdir -p "$LIBS_PYTHON_DIR"
    echo "Setting ownership to current user..."
    chown "$USER":"$(id -gn)" "$LIBS_PYTHON_DIR"
else
    echo "$LIBS_PYTHON_DIR already exists."

    # Nếu thư mục tồn tại nhưng do root sở hữu → cần đổi lại quyền
    OWNER=$(stat -c '%U' "$LIBS_PYTHON_DIR")
    if [ "$OWNER" = "root" ]; then
        echo "Changing ownership from root to $USER..."
        sudo chown "$USER":"$(id -gn)" "$LIBS_PYTHON_DIR"
    fi
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
# # Move python_example directory to PayloadSdk
# echo "Checking and moving $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR..."
# if [ -d "$PYTHON_EXAMPLE_DIR" ] && [ -d "$PAYLOAD_SDK_DIR" ] && [ ! -d "$PAYLOAD_SDK_DIR/python_example" ]; then
#     mv "$PYTHON_EXAMPLE_DIR" "$PAYLOAD_SDK_DIR"
#     echo "Moved $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR"
# else
#     echo "Skipping $PYTHON_EXAMPLE_DIR (either not found, $PAYLOAD_SDK_DIR missing, or already moved)"
# fi

# # Move wrapper.cpp to the libs directory
# echo "Checking and moving $WRAPPER_FILE to $LIBS_DIR..."
# if [ -f "$WRAPPER_FILE" ] && [ ! -f "$LIBS_DIR/wrapper.cpp" ]; then
#     mv "$WRAPPER_FILE" "$LIBS_DIR"
#     echo "Moved $WRAPPER_FILE to $LIBS_DIR"
# else
#     echo "Skipping $WRAPPER_FILE (either not found or already moved)"
# fi

echo "----------------------------------------------------------------------------------------------------------------------"
# # Comment out examples and tests subdirectories in PayloadSdk/CMakeLists.txt
# echo "Updating $PAYLOAD_CMAKELISTS_FILE to comment out examples and tests subdirectories..."
# if [ -f "$PAYLOAD_CMAKELISTS_FILE" ]; then
#     # Comment lines related to examples and tests
#     sed -i 's/add_subdirectory(examples)/#add_subdirectory(examples)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/if (VIO)/#if (VIO)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/add_subdirectory(tests\/demo_project)/#add_subdirectory(tests\/demo_project)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/endif(VIO)/#endif(VIO)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/if (GHADRON)/#if (GHADRON)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/add_subdirectory(tests\/ghadron_project)/#add_subdirectory(tests\/ghadron_project)/' "$PAYLOAD_CMAKELISTS_FILE"
#     sed -i 's/endif(GHADRON)/#endif(GHADRON)/' "$PAYLOAD_CMAKELISTS_FILE"
#     echo "Commented out examples and tests subdirectories in $PAYLOAD_CMAKELISTS_FILE"
# else
#     echo "Error: $PAYLOAD_CMAKELISTS_FILE does not exist, skipping update."
# fi

echo "----------------------------------------------------------------------------------------------------------------------"
# # Ensure wrapper.cpp is not already in SOURCES block
# echo "Checking and updating $CMAKELISTS_FILE for wrapper.cpp in SOURCES..."
# if ! grep -q "wrapper.cpp" "$CMAKELISTS_FILE"; then
#     # Add wrapper.cpp properly indented into SOURCES block before the closing parenthesis
#     sed -i '/file(GLOB_RECURSE SOURCES/,/^[ \t]*)/s/^[ \t]*)/            ${CMAKE_CURRENT_SOURCE_DIR}\/wrapper.cpp\n            )/' "$CMAKELISTS_FILE"
#     echo "Added wrapper.cpp to SOURCES block"
# else
#     echo "Skipping wrapper.cpp addition (already present in SOURCES)"
# fi

echo "----------------------------------------------------------------------------------------------------------------------"
# # Change STATIC to SHARED in add_library if not already changed
# echo "Checking and updating $CMAKELISTS_FILE for SHARED library..."
# if grep -q "add_library(\${PROJECT_NAME} STATIC" "$CMAKELISTS_FILE"; then
#     sed -i 's/add_library(${PROJECT_NAME} STATIC/add_library(${PROJECT_NAME} SHARED/' "$CMAKELISTS_FILE"
#     echo "Changed STATIC to SHARED in add_library"
# else
#     echo "Skipping STATIC to SHARED change (already set to SHARED or not applicable)"
# fi

echo "----------------------------------------------------------------------------------------------------------------------"
# # Add the set_target_properties block at the end if it doesn't exist
# echo "Checking and adding set_target_properties to $CMAKELISTS_FILE..."
# if ! grep -q "set_target_properties(\${PROJECT_NAME} PROPERTIES" "$CMAKELISTS_FILE"; then
#     cat <<EOL >> "$CMAKELISTS_FILE"

# set_target_properties(\${PROJECT_NAME} PROPERTIES
#    CXX_VISIBILITY "default"  # Ensure C++ functions are exported
#    VISIBILITY_INLINES_HIDDEN ON
# )
# EOL
#     echo "Added set_target_properties block"
# else
#     echo "Skipping set_target_properties addition (already present)"
# fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Build the project
echo "Building the project with PAYLOAD_TYPE=$PAYLOAD_TYPE..."
cd "$PAYLOAD_SDK_DIR"

# Kiểm tra thư mục build
if [ ! -d "build" ]; then
    echo "Creating build directory..."
    sudo mkdir build
else
    echo "Build directory already exists."
fi

cd build

# Xóa cache cmake cũ nếu có
if [ -f "CMakeCache.txt" ]; then
    echo "Removing old CMakeCache.txt..."
    sudo rm CMakeCache.txt
    sudo rm -rf CMakeFiles
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

# sudo make -j6

echo "Build complete."
echo "Modifications and build complete."