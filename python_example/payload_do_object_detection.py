import time
import signal
import sys
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, CONTROL_UDP, PAYLOAD_TYPE
from payload_define import *
from mavlink_define import *

# Configuration connect
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.248"
s_conn.udp.port = 14566

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
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Check payload connection
    my_payload.checkPayloadConnection()

    # Set view source
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