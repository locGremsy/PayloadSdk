import time
import signal
import sys
from enum import Enum
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, payload_status_event_t, CONTROL_UDP
from ..libs.payload_define import *
from ..libs.mavlink_define import *

# Configuration for connection
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.248"  
s_conn.udp.port = 14566           

my_payload = None
time_to_record = 10  
time_to_exit = False

class capture_sequence_t(Enum):
    IDLE = 0
    CHECK_STORAGE = 1
    CHECK_CAPTURE_STATUS = 2
    CHECK_CAMERA_MODE = 3
    CHANGE_CAMERA_MODE = 4
    DO_RECORD_VIDEO = 5
    VIDEO_IN_RECORDING = 6
    STOP_RECORD_VIDEO = 7
    WAIT_RECORD_DONE = 8

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
    global my_capture, time_to_record, time_to_exit
    if event == payload_status_event_t.PAYLOAD_CAM_CAPTURE_STATUS.value:

        # param[0]: image_status
		# param[1]: video_status
		# param[2]: image_count
		# param[3]: recording_time_ms
        
        if my_capture == capture_sequence_t.CHECK_CAPTURE_STATUS.value:
            print(f"Got payload capture status: image_status: {param[0]:.2f}, video_status: {param[1]:.2f}")
            # If video status is idle, do capture
            if param[1] == 0:
                my_capture = capture_sequence_t.CHECK_CAMERA_MODE.value
                print("   ---> Payload is idle, Check camera mode")
            else:
                print("   ---> Payload is busy")
                my_capture = capture_sequence_t.IDLE.value
                
        elif my_capture == capture_sequence_t.WAIT_RECORD_DONE.value:
            if param[1] == 0:
                print("   ---> Payload is completed record video")
                # Can't call sys.exit(0) in callback function.
                time_to_exit = True
            else:
                print("   ---> Payload is busy. Wait...")
    
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
                print("   ---> Payload's storage is not ready")
                my_capture = capture_sequence_t.IDLE.value
    
    elif event == payload_status_event_t.PAYLOAD_CAM_SETTINGS.value:
    
        # param[0]: mode_id
		# param[1]: zoomLevel
		# param[2]: focusLevel
        
        if my_capture == capture_sequence_t.CHECK_CAMERA_MODE.value:
            print(f"Got camera mode: {param[0]:.2f}")
            if param[0] == 1: 
                my_capture = capture_sequence_t.DO_RECORD_VIDEO.value
                print("   ---> Payload in Video mode, do record video")
            else:
                my_capture = capture_sequence_t.CHANGE_CAMERA_MODE.value
                print("   ---> Payload not in Video mode, change camera mode")

def main():
    global my_payload, my_capture, time_to_record, time_to_exit

    print("Starting RecordVideo example...\n")
    signal.signal(signal.SIGINT, quit_handler)
    
    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")
    
    # Register callback function
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)
    
    # Check connection
    my_payload.checkPayloadConnection()
    
    # Set payload to video mode for testing
    my_payload.setPayloadCameraMode(CAMERA_MODE.CAMERA_MODE_VIDEO.value)
    
    # Set record source to IR
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_RECORD_SRC, Payload_Camera_Record_Src.PAYLOAD_CAMERA_RECORD_IR.value, param_type.PARAM_TYPE_UINT32.value)  
    
    while not time_to_exit:

        # Record IR video with payload following this sequence
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
            my_payload.setPayloadCameraMode(CAMERA_MODE.CAMERA_MODE_VIDEO.value)  
            my_capture = capture_sequence_t.CHECK_CAMERA_MODE.value

        elif my_capture == capture_sequence_t.DO_RECORD_VIDEO.value:
            my_payload.setPayloadCameraRecordVideoStart()
            time_to_record = 10
            print(f"Payload is recording video in {time_to_record}s, wait...")
            my_capture = capture_sequence_t.VIDEO_IN_RECORDING.value

        elif my_capture == capture_sequence_t.VIDEO_IN_RECORDING.value:
            time.sleep(0.7) 
            time_to_record -= 1
            print(time_to_record)
            if time_to_record == 0:
                my_capture = capture_sequence_t.STOP_RECORD_VIDEO.value

        elif my_capture == capture_sequence_t.STOP_RECORD_VIDEO.value:
            my_payload.setPayloadCameraRecordVideoStop()
            my_capture = capture_sequence_t.WAIT_RECORD_DONE.value

        elif my_capture == capture_sequence_t.WAIT_RECORD_DONE.value:
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