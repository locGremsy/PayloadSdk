import time
import signal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs_python.payload_sdk import PayloadSdkInterface, param_type
from libs_python.payload_define import *
from libs_python.mavlink_define import *

my_payload = None

# Signal handler for quitting
def quit_handler(sig, frame):
    print("\nTERMINATING AT USER REQUEST")

    # Close payload interface
    if my_payload:
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

    # Check connection
    my_payload.checkPayloadConnection()

    # Set gimbal to LOCK mode
    print("Gimbal set LOCK mode, delay in 5 secs")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_GIMBAL_MODE, Payload_Camera_Gimbal_Mode.PAYLOAD_CAMERA_GIMBAL_MODE_LOCK.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5) 

    # Set gimbal to FOLLOW mode
    print("Gimbal set FOLLOW mode, delay in 5 secs")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_GIMBAL_MODE, Payload_Camera_Gimbal_Mode.PAYLOAD_CAMERA_GIMBAL_MODE_FOLLOW.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5)

    # Set gimbal to MAPPING mode
    print("Gimbal set MAPPING mode, delay in 5 secs")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_GIMBAL_MODE, Payload_Camera_Gimbal_Mode.PAYLOAD_CAMERA_GIMBAL_MODE_MAPPING.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5)

    # Set gimbal to OFF mode
    print("Gimbal set OFF mode, delay in 5 secs")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_GIMBAL_MODE, Payload_Camera_Gimbal_Mode.PAYLOAD_CAMERA_GIMBAL_MODE_OFF.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5)

    # Set gimbal to RESET mode
    print("Gimbal set RESET mode, delay in 5 secs")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_GIMBAL_MODE, Payload_Camera_Gimbal_Mode.PAYLOAD_CAMERA_GIMBAL_MODE_RESET.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5)

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()