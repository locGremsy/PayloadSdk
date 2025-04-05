#!/bin/bash

# Define paths
WRAPPER_FILE="./wrapper.cpp"
LIBS_DIR="./PayloadSdk/libs"
CMAKELISTS_FILE="$LIBS_DIR/CMakeLists.txt"

# Copy wrapper.cpp to the libs directory
cp "$WRAPPER_FILE" "$LIBS_DIR"

# Ensure wrapper.cpp is not already in SOURCES block
if ! grep -q "wrapper.cpp" "$CMAKELISTS_FILE"; then
    # Add wrapper.cpp properly indented into SOURCES block before the closing parenthesis
    sed -i '/file(GLOB_RECURSE SOURCES/,/^[ \t]*)/s/^[ \t]*)/            ${CMAKE_CURRENT_SOURCE_DIR}\/wrapper.cpp\n            )/' "$CMAKELISTS_FILE"
fi

# Change STATIC to SHARED in add_library
sed -i 's/add_library(${PROJECT_NAME} STATIC/add_library(${PROJECT_NAME} SHARED/' "$CMAKELISTS_FILE"

# Add the set_target_properties block at the end if it doesn't exist
if ! grep -q "set_target_properties(${PROJECT_NAME} PROPERTIES" "$CMAKELISTS_FILE"; then
    cat <<EOL >> "$CMAKELISTS_FILE"

set_target_properties(\${PROJECT_NAME} PROPERTIES
   CXX_VISIBILITY "default"  # Ensure C++ functions are exported
   VISIBILITY_INLINES_HIDDEN ON
)
EOL
fi

echo "Modifications complete."