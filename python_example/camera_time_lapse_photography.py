import time
import signal
import sys
from enum import Enum
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs_python.payload_sdk import PayloadSdkInterface, payload_status_event_t, param_type
from libs_python.payload_define import *
from libs_python.mavlink_define import *

my_payload = None
interval = 3  
time_to_capturing = 12 
time_to_exit = False 

class capture_sequence_t(Enum):
    IDLE = 0
    CHECK_STORAGE = 1
    CHECK_CAPTURE_STATUS = 2
    CHECK_CAMERA_MODE = 3
    CHANGE_CAMERA_MODE = 4
    DO_CAPTURE = 5
    IMAGE_IN_CAPTURING = 6
    STOP_CAPTURING_IMAGE = 7


my_capture = capture_sequence_t.CHECK_STORAGE.value

# Signal handler for quitting
def quit_handler(sig, frame):
    global time_to_exit
    print("\nTERMINATING AT USER REQUEST")
    time_to_exit = True

    # Close payload interface
    if my_payload:
        try:
            my_payload.sdkQuit()
        except Exception as e:
            print(f"Error while quitting payload: {e}")
    # End program    
    sys.exit(0)

# Callback function for payload status changes
def onPayloadStatusChanged(event: int, param: list):
    global my_capture, time_to_exit

    if event == payload_status_event_t.PAYLOAD_CAM_CAPTURE_STATUS.value:
        # param[0]: image_status
        # param[1]: video_status
        # param[2]: image_count
        # param[3]: recording_time_ms

        if my_capture == capture_sequence_t.CHECK_CAPTURE_STATUS.value:
            print(f"Got payload capture status: image_status: {param[0]:.2f}, video_status: {param[1]:.2f}")
            
            # If image status is idle, do capture
            if param[0] == 0: 
                my_capture = capture_sequence_t.CHECK_CAMERA_MODE.value
                print("   ---> Payload is idle, Check camera mode")
            else:
                my_capture = capture_sequence_t.IDLE.value
                print("   ---> Payload is busy")

        elif my_capture == capture_sequence_t.STOP_CAPTURING_IMAGE.value:
            if param[0] == 0: 
                my_capture = capture_sequence_t.CHECK_STORAGE.value
                print("   ---> Payload is completed capture image")
                # Can't call sys.exit(0) in callback function.
                time_to_exit = True
            else:
                print("   ---> Payload is busy")

    elif event == payload_status_event_t.PAYLOAD_CAM_STORAGE_INFO.value:
        # param[0]: total_capacity
        # param[1]: used_capacity
        # param[2]: available_capacity
        # param[3]: status

        if my_capture == capture_sequence_t.CHECK_STORAGE.value:
            print(f"Got payload storage info: total: {param[0]:.2f} MB, used: {param[1]:.2f} MB, available: {param[2]:.2f} MB")
            
            # If payload have enough space, check capture status
            if param[2] >= 10.0: 
                my_capture = capture_sequence_t.CHECK_CAPTURE_STATUS.value
                print("   ---> Storage ready, check capture status")
            else:
                my_capture = capture_sequence_t.IDLE.value
                print("   ---> Payload's storage is not ready")

    elif event == payload_status_event_t.PAYLOAD_CAM_SETTINGS.value:
        # param[0]: mode_id
        # param[1]: zoomLevel
        # param[2]: focusLevel

        if my_capture == capture_sequence_t.CHECK_CAMERA_MODE.value:
            print(f"Got camera mode: {param[0]:.2f}")

            if param[0] == CAMERA_MODE.CAMERA_MODE_IMAGE.value:
                my_capture = capture_sequence_t.DO_CAPTURE.value
                print("   ---> Payload in Image mode, do capture image")
            else:
                my_capture = capture_sequence_t.CHANGE_CAMERA_MODE.value
                print("   ---> Payload in Video mode, change camera mode")

def main():
    global my_payload, my_capture, time_to_capturing, time_to_exit

    print("Starting CaptureImage example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface()

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Register callback function
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)

    # Check connection
    my_payload.checkPayloadConnection()

    # Set payload to IMAGE mode for testing
    my_payload.setPayloadCameraMode(CAMERA_MODE.CAMERA_MODE_IMAGE.value)

    # Set record source to IR (or EO)
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_RECORD_SRC, Payload_Camera_Record_Src.PAYLOAD_CAMERA_RECORD_IR.value, param_type.PARAM_TYPE_UINT32.value)

    while not time_to_exit:

        # Capture time-lapse images with payload following this sequence
        if my_capture == capture_sequence_t.IDLE.value:
            # Wait in idle state
            pass  

        elif my_capture == capture_sequence_t.CHECK_STORAGE.value:
            my_payload.getPayloadStorage()

        elif my_capture == capture_sequence_t.CHECK_CAPTURE_STATUS.value:
            my_payload.getPayloadCaptureStatus()

        elif my_capture == capture_sequence_t.CHECK_CAMERA_MODE.value:
            my_payload.getPayloadCameraMode()

        elif my_capture == capture_sequence_t.CHANGE_CAMERA_MODE.value:
            my_payload.setPayloadCameraMode(CAMERA_MODE.CAMERA_MODE_IMAGE.value)
            my_capture = capture_sequence_t.CHECK_CAMERA_MODE.value

        elif my_capture == capture_sequence_t.DO_CAPTURE.value:
            my_payload.setPayloadCameraCaptureImage(interval)
            print(f"Payload is capturing image elapsed time between {interval}s, within {time_to_capturing}s, wait...")
            my_capture = capture_sequence_t.IMAGE_IN_CAPTURING.value

        elif my_capture == capture_sequence_t.IMAGE_IN_CAPTURING.value:
            print("Captured ...")
            time.sleep(interval)  
            time_to_capturing -= interval
            if time_to_capturing <= 0:
                my_capture = capture_sequence_t.STOP_CAPTURING_IMAGE.value

        elif my_capture == capture_sequence_t.STOP_CAPTURING_IMAGE.value:
            my_payload.setPayloadCameraStopImage()
            my_payload.getPayloadCaptureStatus()

        time.sleep(0.3) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
        print("Payload connection closed successfully.")
    except Exception as e:
        print(f"Error while quitting payload: {e}")      

if __name__ == "__main__":
    main()