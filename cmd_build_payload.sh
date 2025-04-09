#!/bin/bash

# Define paths
WRAPPER_FILE="./wrapper.cpp"
LIBS_DIR="./PayloadSdk/libs"
CMAKELISTS_FILE="$LIBS_DIR/CMakeLists.txt"
PYTHON_EXAMPLE_DIR="./python_example"
PAYLOAD_SDK_FILE="$PYTHON_EXAMPLE_DIR/payload_sdk.py"
PAYLOAD_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/payload_define.py"
MAVLINK_DEFINE_FILE="$PYTHON_EXAMPLE_DIR/mavlink_define.py"
INIT_FILE="$PYTHON_EXAMPLE_DIR/__init__.py"
PAYLOAD_SDK_DIR="./PayloadSdk"
EXAMPLES_DIR="$PAYLOAD_SDK_DIR/examples"
TESTS_DIR="$PAYLOAD_SDK_DIR/tests"
PAYLOAD_CMAKELISTS_FILE="$PAYLOAD_SDK_DIR/CMakeLists.txt"

# Hàm hiển thị hướng dẫn sử dụng
usage() {
    echo "Usage: $0 [--payload <PAYLOAD_TYPE>]"
    echo "  --payload: Specify payload type (VIO, ZIO, or GHADRON)"
    echo "Example: $0 --payload VIO"
    exit 1
}

# Xử lý tham số đầu vào
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --payload)
            PAYLOAD_TYPE="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

# Kiểm tra xem PAYLOAD_TYPE có được cung cấp không
if [ -z "$PAYLOAD_TYPE" ]; then
    echo "Error: Missing --payload argument."
    usage
fi

# Kiểm tra giá trị PAYLOAD_TYPE hợp lệ
case "$PAYLOAD_TYPE" in
    VIO|ZIO|GHADRON)
        echo "Payload type set to: $PAYLOAD_TYPE"
        ;;
    *)
        echo "Error: Invalid PAYLOAD_TYPE. Must be VIO, ZIO, or GHADRON."
        usage
        ;;
esac

# Move payload_sdk.py, payload_define.py, mavlink_define.py, and __init__.py to PayloadSdk/libs
echo "Checking and moving Python files to $LIBS_DIR..."

# Check if PayloadSdk/libs directory exists
if [ -d "$LIBS_DIR" ]; then
    # Check and move payload_sdk.py
    if [ -f "$PAYLOAD_SDK_FILE" ] && [ ! -f "$LIBS_DIR/payload_sdk.py" ]; then
        sudo mv "$PAYLOAD_SDK_FILE" "$LIBS_DIR"
        echo "Moved $PAYLOAD_SDK_FILE to $LIBS_DIR"
    else
        echo "Skipping $PAYLOAD_SDK_FILE (either not found or already moved)"
    fi

    # Check and move payload_define.py
    if [ -f "$PAYLOAD_DEFINE_FILE" ] && [ ! -f "$LIBS_DIR/payload_define.py" ]; then
        sudo mv "$PAYLOAD_DEFINE_FILE" "$LIBS_DIR"
        echo "Moved $PAYLOAD_DEFINE_FILE to $LIBS_DIR"
    else
        echo "Skipping $PAYLOAD_DEFINE_FILE (either not found or already moved)"
    fi

    # Check and move mavlink_define.py
    if [ -f "$MAVLINK_DEFINE_FILE" ] && [ ! -f "$LIBS_DIR/mavlink_define.py" ]; then
        sudo mv "$MAVLINK_DEFINE_FILE" "$LIBS_DIR"
        echo "Moved $MAVLINK_DEFINE_FILE to $LIBS_DIR"
    else
        echo "Skipping $MAVLINK_DEFINE_FILE (either not found or already moved)"
    fi

    # Check and move __init__.py
    if [ -f "$INIT_FILE" ] && [ ! -f "$LIBS_DIR/__init__.py" ]; then
        sudo mv "$INIT_FILE" "$LIBS_DIR"
        echo "Moved $INIT_FILE to $LIBS_DIR"
    else
        echo "Skipping $INIT_FILE (either not found or already moved)"
    fi
else
    echo "Error: $LIBS_DIR does not exist, cannot move Python files."
fi

# Move python_example directory to PayloadSdk
echo "Checking and moving $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR..."
if [ -d "$PYTHON_EXAMPLE_DIR" ] && [ -d "$PAYLOAD_SDK_DIR" ] && [ ! -d "$PAYLOAD_SDK_DIR/python_example" ]; then
    sudo mv "$PYTHON_EXAMPLE_DIR" "$PAYLOAD_SDK_DIR"
    echo "Moved $PYTHON_EXAMPLE_DIR to $PAYLOAD_SDK_DIR"
else
    echo "Skipping $PYTHON_EXAMPLE_DIR (either not found, $PAYLOAD_SDK_DIR missing, or already moved)"
fi

# Move wrapper.cpp to the libs directory
echo "Checking and moving $WRAPPER_FILE to $LIBS_DIR..."
if [ -f "$WRAPPER_FILE" ] && [ ! -f "$LIBS_DIR/wrapper.cpp" ]; then
    sudo mv "$WRAPPER_FILE" "$LIBS_DIR"
    echo "Moved $WRAPPER_FILE to $LIBS_DIR"
else
    echo "Skipping $WRAPPER_FILE (either not found or already moved)"
fi

# Remove examples and tests directories from PayloadSdk
echo "Checking and removing $EXAMPLES_DIR and $TESTS_DIR..."
# Check and remove examples directory
if [ -d "$EXAMPLES_DIR" ]; then
    sudo rm -r "$EXAMPLES_DIR"
    echo "Removed $EXAMPLES_DIR"
else
    echo "Skipping $EXAMPLES_DIR (not found)"
fi

# Check and remove tests directory
if [ -d "$TESTS_DIR" ]; then
    sudo rm -r "$TESTS_DIR"
    echo "Removed $TESTS_DIR"
else
    echo "Skipping $TESTS_DIR (not found)"
fi

# Comment out examples and tests subdirectories in PayloadSdk/CMakeLists.txt
echo "Updating $PAYLOAD_CMAKELISTS_FILE to comment out examples and tests subdirectories..."
if [ -f "$PAYLOAD_CMAKELISTS_FILE" ]; then
    # Comment lines related to examples and tests
    sudo sed -i 's/add_subdirectory(examples)/#add_subdirectory(examples)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/if (VIO)/#if (VIO)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/add_subdirectory(tests\/demo_project)/#add_subdirectory(tests\/demo_project)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/endif(VIO)/#endif(VIO)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/if (GHADRON)/#if (GHADRON)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/add_subdirectory(tests\/ghadron_project)/#add_subdirectory(tests\/ghadron_project)/' "$PAYLOAD_CMAKELISTS_FILE"
    sudo sed -i 's/endif(GHADRON)/#endif(GHADRON)/' "$PAYLOAD_CMAKELISTS_FILE"
    echo "Commented out examples and tests subdirectories in $PAYLOAD_CMAKELISTS_FILE"
else
    echo "Error: $PAYLOAD_CMAKELISTS_FILE does not exist, skipping update."
fi

# Ensure wrapper.cpp is not already in SOURCES block
echo "Checking and updating $CMAKELISTS_FILE for wrapper.cpp in SOURCES..."
if ! grep -q "wrapper.cpp" "$CMAKELISTS_FILE"; then
    # Add wrapper.cpp properly indented into SOURCES block before the closing parenthesis
    sudo sed -i '/file(GLOB_RECURSE SOURCES/,/^[ \t]*)/s/^[ \t]*)/            ${CMAKE_CURRENT_SOURCE_DIR}\/wrapper.cpp\n            )/' "$CMAKELISTS_FILE"
    echo "Added wrapper.cpp to SOURCES block"
else
    echo "Skipping wrapper.cpp addition (already present in SOURCES)"
fi

# Change STATIC to SHARED in add_library if not already changed
echo "Checking and updating $CMAKELISTS_FILE for SHARED library..."
if grep -q "add_library(\${PROJECT_NAME} STATIC" "$CMAKELISTS_FILE"; then
    sudo sed -i 's/add_library(${PROJECT_NAME} STATIC/add_library(${PROJECT_NAME} SHARED/' "$CMAKELISTS_FILE"
    echo "Changed STATIC to SHARED in add_library"
else
    echo "Skipping STATIC to SHARED change (already set to SHARED or not applicable)"
fi

# Add the set_target_properties block at the end if it doesn't exist
echo "Checking and adding set_target_properties to $CMAKELISTS_FILE..."
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

# Build the project
echo "Building the project with PAYLOAD_TYPE=$PAYLOAD_TYPE..."
cd "$PAYLOAD_SDK_DIR"
if [ ! -d "build" ]; then
    mkdir build
fi
cd build

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