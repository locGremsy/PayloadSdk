import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, payload_status_event_t, CONTROL_UDP, PAYLOAD_TYPE
from ..libs.payload_define import *
from ..libs.mavlink_define import *

# Configuration for connection
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

    # Set view source to EO
    print("Set view source to EO!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_EO.value, param_type.PARAM_TYPE_UINT32.value) 
    time.sleep(1) 
    
    print("Set zoom level to 1x!")
    if PAYLOAD_TYPE == "GHADRON":
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_ZOOM_FACTOR, Payload_Camera_Video_Zoom_Factor.ZOOM_EO_1X.value, param_type.PARAM_TYPE_UINT32.value) 
    elif PAYLOAD_TYPE in ["VIO", "ZIO"]:
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_ZOOM_SUPER_RESOLUTION_FACTOR, Payload_Camera_Video_Zoom_Super_Resolution_Factor.ZOOM_SUPER_RESOLUTION_1X.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(3)
    
    # Zoom step
    print("Zoom In 4 times!")
    for _ in range(4):
        my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_STEP.value, Camera_Zoom_Value.ZOOM_IN.value)    # Zoom in 
        time.sleep(1)  
    
    print("Zoom Out 2 times!")
    for _ in range(2):
        my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_STEP.value, Camera_Zoom_Value.ZOOM_OUT.value)   # Zoom out
        time.sleep(1)   

    # Zoom continuous
    print("Start Zoom In!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_IN.value)   # Zoom in 
    time.sleep(5)   
    
    print("Stop Zoom!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_STOP.value)    # Stop zoom  
    time.sleep(2)   
    
    print("Start Zoom Out!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_OUT.value)     # Zoom out
    time.sleep(7)  
    print("Stop Zoom!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Zoom_Value.ZOOM_STOP.value)    # Stop zoom 
    time.sleep(2)   

    # Zoom range
    print("Zoom Range 50%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 50.0)  # Zoom 50%
    time.sleep(3)  
    
    print("Zoom Range 70%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 70.0)  # Zoom 70%
    time.sleep(3)    
    
    print("Zoom Range 100%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 100.0) # Zoom 100%
    time.sleep(3)   
    
    print("Zoom Range 0%!")
    my_payload.setCameraZoom(CAMERA_ZOOM_TYPE.ZOOM_TYPE_RANGE.value, 0.0)   # Zoom 0%
    time.sleep(5)  
    
    if PAYLOAD_TYPE in ["VIO", "ZIO"]:
        # Focus continuous
        print("Start Focus In!")
        my_payload.setCameraFocus(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Focus_Value.FOCUS_IN.value)   # Focus in
        time.sleep(4)  
        print("Stop Focus!")
        my_payload.setCameraFocus(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Focus_Value.FOCUS_STOP.value)  # Stop focus
        time.sleep(2)   
        
        print("Start Focus Out!")
        my_payload.setCameraFocus(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Focus_Value.FOCUS_OUT.value)   # Focus out
        time.sleep(4)   
        print("Stop Focus!")
        my_payload.setCameraFocus(CAMERA_ZOOM_TYPE.ZOOM_TYPE_CONTINUOUS.value, Camera_Focus_Value.FOCUS_STOP.value)  # Stop focus
        time.sleep(2)   
        
        # Auto focus
        print("Auto Focus!")
        my_payload.setCameraFocus(1)
    
    print("!--------------------!\n")
    
    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()