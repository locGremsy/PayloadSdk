import time
import signal
import sys
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, payload_status_event_t, CONTROL_UDP
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
    if my_payload:
        try:
            my_payload.sdkQuit()
        except Exception as e:
            print(f"Error while quitting payload: {e}")
    # End program    
    sys.exit(0)

# Callback function for payload status changes
def onPayloadStatusChanged(event: int, param: list):
    if event == payload_status_event_t.PAYLOAD_ACK.value:
        print(f" --> Got ack, from command: {param[0]:.0f} - result: {param[1]:.2f}")

def main():
    global my_payload

    print("Starting CaptureImage example...\n")
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

    # Set view source
    print("Set view source to IR!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_IR.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(1) 

    # Set zoom level
    print("Set zoom level to 1x!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ZOOM_FACTOR, Payload_Camera_Ir_Zoom_Factor.ZOOM_IR_1X.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(3) 

    # Zoom step
    print("Zoom In 4 times!")
    for _ in range(4):
        my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_STEP.value, Camera_Zoom_Value.ZOOM_IN.value)  # Zoom in
        time.sleep(1)

    print("Zoom Out 2 times!")
    for _ in range(2):
        my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_STEP.value, Camera_Zoom_Value.ZOOM_OUT.value)  # Zoom out
        time.sleep(1)

    # Zoom continuous
    print("Start Zoom In!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_IN.value) # Zoom in
    time.sleep(5)  

    print("Stop Zoom!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_STOP.value)  # Stop zoom
    time.sleep(2)  

    print("Start Zoom Out!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_OUT.value)  # Zoom out
    time.sleep(7)  

    print("Stop Zoom!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_STOP.value)  # Stop zoom
    time.sleep(2)

    # Zoom range
    print("Zoom Range 50%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 50.0) # Zoom 50%
    time.sleep(3) 

    print("Zoom Range 70%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 70.0)  # Zoom 70%
    time.sleep(3)

    print("Zoom Range 100%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 100.0) # Zoom 100%
    time.sleep(3)
    
    print("Zoom Range 0%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 0.0) # Zoom 0%
    time.sleep(5)
    print("!--------------------!")

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()