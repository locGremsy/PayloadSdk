import time
import signal
import sys
import threading
import random
from enum import Enum
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, payload_status_event_t, payload_param_t, param_type, CONTROL_UDP, PAYLOAD_TYPE
from payload_define import *
from mavlink_define import *

# Configuration connect
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.248"
s_conn.udp.port = 14566

my_payload = None
time_to_exit = False

class tracking_cmd_t(Enum):
    TRACK_IDLE = 0
    TRACK_ACT = 1
    TRACK_LOST = 2

# track status
track_pos_x = 0.0
track_pos_y = 0.0
track_status = 0.0
track_pos_w = 0.0
track_pos_h = 0.0

# Signal handler for quitting
def quit_handler(sig, frame):
    global time_to_exit
    print("\nTERMINATING AT USER REQUEST\n")
    time_to_exit = True
    
    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

    # End program    
    sys.exit(0)

# Callback function for payload status changes
def onPayloadStatusChanged(event: int, param: list):
    global track_pos_x, track_pos_y, track_status, track_pos_w, track_pos_h
    if event == payload_status_event_t.PAYLOAD_PARAMS.value:
        # param[0]: param index
        # param[1]: value

        if param[0] == payload_param_t.PARAM_TRACK_POS_X.value:
            track_pos_x = param[1]

        elif param[0] == payload_param_t.PARAM_TRACK_POS_Y.value:
            track_pos_y = param[1]

        elif param[0] == payload_param_t.PARAM_TRACK_POS_W.value:
            track_pos_w = param[1]

        elif param[0] == payload_param_t.PARAM_TRACK_POS_H.value:
            track_pos_h = param[1]

        elif param[0] == payload_param_t.PARAM_TRACK_STATUS.value:
            track_status = param[1]

        print(f"onPayloadStatusChanged, status: {track_status:.2f}, x: {track_pos_x:.2f}, y: {track_pos_y:.2f}, w: {track_pos_w:.2f}, h: {track_pos_h:.2f}")

# Handle tracking 
def handle_tracking():
    global time_to_exit

    while not time_to_exit:
        # Random tracking bounding box
        random_w = random.randint(20, 1920)     # 1920 + 1 to include 1920
        random_h = random.randint(20, 1080)     # 1080 + 1 to include 1080

        print("Start tracking new object")
        my_payload.setPayloadObjectTrackingParams(tracking_cmd_t.TRACK_ACT.value, random_w, random_h)
        time.sleep(0.2) 

        # Check tracking status
        if track_status:
            print("Object was tracked. Keep this object for 5 seconds...")
            time.sleep(5)  
            # Release object
            my_payload.setPayloadObjectTrackingParams(tracking_cmd_t.TRACK_IDLE.value, random_w, random_h)
            print("Object was released. Wait 3 seconds...")
            time.sleep(3)

        else:
            print("Lost object. Try catch another object")
            my_payload.setPayloadObjectTrackingParams(tracking_cmd_t.TRACK_IDLE.value, random_w, random_h)
            time.sleep(1) 

def all_threads_init():
    tracking_thread = threading.Thread(target=handle_tracking)
    tracking_thread.daemon = True 
    tracking_thread.start()
    print("Thread created\n")

def main():
    global my_payload

    print("Starting Do Object Tracking example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Register callback function
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)

    # Check payload connection
    my_payload.checkPayloadConnection()

    # Init the environment
	# Change view mode to EO
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_EO.value, param_type.PARAM_TYPE_UINT32.value)

    if PAYLOAD_TYPE in ["VIO", "ZIO"]:
        # Change tracking mode to Object tracking
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_TRACKING_MODE, Payload_Camera_Tracking_Mode.PAYLOAD_CAMERA_TRACKING_OBJ_TRACKING.value, param_type.PARAM_TYPE_UINT32.value)

    # Change OSD mode to Status
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_OSD_MODE, Payload_Camera_Osd_Mode.PAYLOAD_CAMERA_VIDEO_OSD_MODE_STATUS.value, param_type.PARAM_TYPE_UINT32.value)

	# Init the status messages rate
	# If you do not want to receive the message anymore, need to set rate to 0
    my_payload.setParamRate(payload_param_t.PARAM_TRACK_POS_X.value, 100)
    my_payload.setParamRate(payload_param_t.PARAM_TRACK_POS_Y.value, 100)
    my_payload.setParamRate(payload_param_t.PARAM_TRACK_POS_W.value, 100)
    my_payload.setParamRate(payload_param_t.PARAM_TRACK_POS_H.value, 100)
    my_payload.setParamRate(payload_param_t.PARAM_TRACK_STATUS.value, 100)

    # Init threads
    all_threads_init()

    # Check payload messages
    while not time_to_exit:
        # Do nothing
        time.sleep(0.001)

if __name__ == "__main__":
    main()