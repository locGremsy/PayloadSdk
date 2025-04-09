import time
import signal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs_python.payload_sdk import PayloadSdkInterface, param_type, PAYLOAD_TYPE
from libs_python.payload_define import *
from libs_python.mavlink_define import *

my_payload = None

# Signal handler for quitting
def quit_handler(sig, frame):
    print("\nTERMINATING AT USER REQUEST")

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

    # End program    
    sys.exit(0)

def main():
    global my_payload

    print("Starting Set gimbal mode example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface()

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Check payload connection
    my_payload.checkPayloadConnection()

    # Set view source to EO
    print("Set view source to EO!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_EO.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.5)  

    # Enable object detection
    print("Enable object detection, delay in 5 secs")
    if PAYLOAD_TYPE in ["VIO", "ZIO"]:
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_TRACKING_MODE, Payload_Camera_Tracking_Mode.PAYLOAD_CAMERA_TRACKING_OBJ_DETECTION.value, param_type.PARAM_TYPE_UINT32.value)
    elif PAYLOAD_TYPE == "GHADRON":
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_OBJECT_DETECTION, Payload_Camera_Object_Detection.PAYLOAD_CAMERA_OBJECT_DETECTION_ENABLE.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5) 

    # Disable object detection
    print("Disable object detection. Exit!")
    if PAYLOAD_TYPE in ["VIO", "ZIO"]:
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_TRACKING_MODE, Payload_Camera_Tracking_Mode.PAYLOAD_CAMERA_TRACKING_OBJ_TRACKING.value, param_type.PARAM_TYPE_UINT32.value)
    elif PAYLOAD_TYPE == "GHADRON":
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_OBJECT_DETECTION, Payload_Camera_Object_Detection.PAYLOAD_CAMERA_OBJECT_DETECTION_DISABLE.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.5)  

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()