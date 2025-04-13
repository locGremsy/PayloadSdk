#!/bin/bash
# Get root directory (directory containing this script)
ROOT_DIR="$(realpath "$(dirname "$0")")"

# Define paths
WRAPPER_FILE="./wrapper.cpp"
LIBS_DIR="./PayloadSdk/libs"
CMAKELISTS_FILE="$LIBS_DIR/CMakeLists.txt"
PYTHON_EXAMPLE_DIR="./python_example"
PAYLOAD_SDK_FILE="$PYTHON_EXAMPLE_DIR/payload_sdk.py"
PAYLOAD_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/payload_define.py"
MAVLINK_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/mavlink_define.py"
ENUM_BASE_FILE="$PYTHON_EXAMPLE_DIR/enum_base.py"
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

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --payload)
            if [[ -n "$2" && "$2" != --* ]]; then
                PAYLOAD_TYPE="$2"
                shift 2
            else
                echo "Error: Missing value for --payload"
                usage
            fi
            ;;
        --ip)
            if [[ -n "$2" && "$2" != --* ]]; then
                IP_ADDRESS="$2"
                shift 2
            else
                echo "Error: Missing value for --ip"
                usage
            fi
            ;;
        --port)
            if [[ -n "$2" && "$2" != --* ]]; then
                PORT="$2"
                shift 2
            else
                echo "Error: Missing value for --port"
                usage
            fi
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Validate payload type
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

# Default values
DEFAULT_IP="192.168.55.1"
DEFAULT_PORT="14566"

# Handle IP and Port fallback cases
if [ -n "$PORT" ] && [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS="$DEFAULT_IP"
    echo "No IP address provided, using default: $IP_ADDRESS with specified port: $PORT"
fi

if [ -n "$IP_ADDRESS" ] && [ -z "$PORT" ]; then
    PORT="$DEFAULT_PORT"
    echo "No port provided, using default: $PORT with specified IP: $IP_ADDRESS"
fi

if [ -z "$IP_ADDRESS" ] && [ -z "$PORT" ]; then
    IP_ADDRESS="$DEFAULT_IP"
    PORT="$DEFAULT_PORT"
    echo "No IP address or port provided, using defaults: IP=$IP_ADDRESS, Port=$PORT"
fi

echo "Using configuration: Payload=$PAYLOAD_TYPE, IP=$IP_ADDRESS, Port=$PORT"

# Update payloadsdk.h values
PAYLOADSDK_H_FILE="$LIBS_DIR/payloadsdk.h"
echo "Updating udp_ip_target and udp_port_target in $PAYLOADSDK_H_FILE"

if [ -f "$PAYLOADSDK_H_FILE" ]; then
    ESCAPED_IP=$(echo "$IP_ADDRESS" | sed 's/\./\\./g')
    sed -i -E "s/(static char \*udp_ip_target = \(char\*\)\")([^\"]+)(\";)/\1$IP_ADDRESS\3/" "$PAYLOADSDK_H_FILE"
    sed -i -E "s/(static int udp_port_target = )([0-9]+)(;)/\1$PORT\3/" "$PAYLOADSDK_H_FILE"
    echo "Updated udp_ip_target to $IP_ADDRESS and udp_port_target to $PORT in payloadsdk.h"
else
    echo "Error: $PAYLOADSDK_H_FILE not found!"
fi

echo "----------------------------------------------------------------------------------------------------------------------"


# Define destination
PAYLOAD_SDK_DEST="$ROOT_DIR/python_examples/libs/payload_sdk.py"


if [ -f "$PAYLOAD_SDK_DEST" ]; then
    echo "Updating PAYLOAD_TYPE in $PAYLOAD_SDK_DEST to \"$PAYLOAD_TYPE\""
    sed -i -E "s|^(PAYLOAD_TYPE *= *)\"[^\"]+\"|\1\"$PAYLOAD_TYPE\"|" "$PAYLOAD_SDK_DEST"
    echo "Updated PAYLOAD_TYPE successfully to \"$PAYLOAD_TYPE\"."
else
    echo "Error: $PAYLOAD_SDK_DEST not found!"
fi


# Move wrapper.cpp
echo "Checking and moving $WRAPPER_FILE to $LIBS_DIR"

if [ -f "$WRAPPER_FILE" ]; then
    if [ -d "$LIBS_DIR" ]; then
        TARGET_WRAPPER_FILE="$LIBS_DIR/wrapper.cpp"
        if [ -f "$TARGET_WRAPPER_FILE" ]; then
            echo "$TARGET_WRAPPER_FILE already exists. Removing to update"
            rm -f "$TARGET_WRAPPER_FILE"
        fi
        cp "$WRAPPER_FILE" "$LIBS_DIR"
        echo "Moved (or updated) $WRAPPER_FILE to $LIBS_DIR"
    else
        echo "Missing target directory: $LIBS_DIR"
    fi
else
    echo "Missing file: $WRAPPER_FILE"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Comment out example/test subdirectories in CMakeLists
echo "Commenting out test/example entries in $PAYLOAD_CMAKELISTS_FILE"

if [ -f "$PAYLOAD_CMAKELISTS_FILE" ]; then
    sed -i 's/^[[:space:]]*\(add_subdirectory(examples)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(if (VIO)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(add_subdirectory(tests\/demo_project)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(endif(VIO)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(if (GHADRON)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(add_subdirectory(tests\/ghadron_project)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    sed -i 's/^[[:space:]]*\(endif(GHADRON)\)/#\1/' "$PAYLOAD_CMAKELISTS_FILE"
    echo "Commented subdirectories."
else
    echo "Error: $PAYLOAD_CMAKELISTS_FILE does not exist."
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Add wrapper.cpp to SOURCES if not present
echo "Checking and updating wrapper.cpp entry in $CMAKELISTS_FILE"

if [ -f "$CMAKELISTS_FILE" ]; then
    if ! grep -q "wrapper.cpp" "$CMAKELISTS_FILE"; then
        sed -i '/file(GLOB_RECURSE SOURCES/,/^[ \t]*)/s/^[ \t]*)/            ${CMAKE_CURRENT_SOURCE_DIR}\/wrapper.cpp\n            )/' "$CMAKELISTS_FILE"
        echo "Added wrapper.cpp to SOURCES block"
    else
        echo "Skipping: wrapper.cpp already present"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Change STATIC to SHARED
echo "Converting library type from STATIC to SHARED if needed"

if [ -f "$CMAKELISTS_FILE" ]; then
    if grep -q "add_library(\${PROJECT_NAME} STATIC" "$CMAKELISTS_FILE"; then
        sed -i 's/add_library(${PROJECT_NAME} STATIC/add_library(${PROJECT_NAME} SHARED/' "$CMAKELISTS_FILE"
        echo "Changed STATIC to SHARED"
    else
        echo "Already SHARED or not applicable"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Add set_target_properties block
echo "Ensuring set_target_properties block is added"

if [ -f "$CMAKELISTS_FILE" ]; then
    if ! grep -q "set_target_properties(\${PROJECT_NAME} PROPERTIES" "$CMAKELISTS_FILE"; then
        cat <<EOL >> "$CMAKELISTS_FILE"

set_target_properties(\${PROJECT_NAME} PROPERTIES
   CXX_VISIBILITY "default"
   VISIBILITY_INLINES_HIDDEN ON
)
EOL
        echo "Added target properties"
    else
        echo "Target properties already set"
    fi
else
    echo "Error: $CMAKELISTS_FILE not found"
fi

echo "----------------------------------------------------------------------------------------------------------------------"
# Build project
echo "Building project with PAYLOAD_TYPE=$PAYLOAD_TYPE"
cd "$PAYLOAD_SDK_DIR"

if [ ! -d "build" ]; then
    echo "Creating build directory"
    mkdir build
else
    echo "Build directory already exists."
fi

cd build

if [ -f "CMakeCache.txt" ]; then
    echo "Cleaning old CMake cache"
    rm CMakeCache.txt
    rm -rf CMakeFiles
fi

case "$PAYLOAD_TYPE" in
    VIO) cmake -DVIO=1 .. ;;
    ZIO) cmake -DZIO=1 .. ;;
    GHADRON) cmake -DGHADRON=1 .. ;;
esac

make -j6
echo "Build complete."

echo "----------------------------------------------------------------------------------------------------------------------"
# Update shared library path in payload_sdk.py
ABS_LIB_PATH="$ROOT_DIR/PayloadSdk/build/libs/libPayloadSDK.so"

if [ -f "$ABS_LIB_PATH" ]; then
    echo "Shared library built successfully: $ABS_LIB_PATH"

    if [ -f "$PAYLOAD_SDK_DEST" ]; then
        echo "Updating shared library path in payload_sdk.py file"
        sed -i -E "s|^(.*self\.lib = ctypes\.CDLL\()\s*\"[^\"]+\"\s*(\).*)|\1\"$ABS_LIB_PATH\"\2|" "$PAYLOAD_SDK_DEST"
        echo "Shared library path updated"
    else
        echo "Error: $PAYLOAD_SDK_DEST not found."
    fi
else
    echo "Build failed: $ABS_LIB_PATH does not exist!"
    exit 1
fi