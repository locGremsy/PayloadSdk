import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, payload_status_event_t, payload_param_t, CONTROL_UDP
from ..libs.payload_define import *
from ..libs.mavlink_define import *

# Configuration for connection
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.248"
s_conn.udp.port = 14566

my_payload = None
time_to_exit = False

# Signal handler for quitting
def quit_handler(sig, frame):
    print("\nTERMINATING AT USER REQUEST")
    global time_to_exit
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

    if event == payload_status_event_t.PAYLOAD_ACK.value:
        print(f" --> Got ack, from command: {param[0]:.0f} - result: {param[1]:.2f}")

    elif event == payload_status_event_t.PAYLOAD_PARAM_EXT_ACK.value:
        print(f" --> Got ext_ack, result {param[0]:.2f}")

    elif event == payload_status_event_t.PAYLOAD_PARAMS.value:
        # param[0]: param index
		# param[1]: value

        if param[0] == payload_param_t.PARAM_EO_ZOOM_LEVEL.value:  
            print(f"Payload EO_ZOOM_LEVEL: {param[1]:.2f}")

        elif param[0] == payload_param_t.PARAM_IR_ZOOM_LEVEL.value:  
            print(f"Payload IR_ZOOM_LEVEL: {param[1]:.2f}")


def main():
    global my_payload, time_to_exit

    print("Starting ConnectPayload example...\n")
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
    
    # Register to receive zoom status updates
    my_payload.setParamRate(payload_param_t.PARAM_EO_ZOOM_LEVEL.value, 1000)  
    my_payload.setParamRate(payload_param_t.PARAM_IR_ZOOM_LEVEL.value, 1000)  
    
    # Set view source to EO/IR
    print("Set view source to EO/IR!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_EOIR.value, param_type.PARAM_TYPE_UINT32.value) 

    # Change EO zoom mode to Super Resolution
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_ZOOM_MODE, Payload_Camera_Video_Zoom_Mode.PAYLOAD_CAMERA_VIDEO_ZOOM_MODE_SUPER_RESOLUTION.value, param_type.PARAM_TYPE_UINT32.value) 

    # Perform zoom operations in a loop
    while not time_to_exit:

        # Zoom EO to 1x
        print("zoom EO to 1x")
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_ZOOM_SUPER_RESOLUTION_FACTOR, Payload_Camera_Video_Zoom_Super_Resolution_Factor.ZOOM_SUPER_RESOLUTION_1X.value, param_type.PARAM_TYPE_UINT32.value)  
        time.sleep(3)
        
        # Zoom EO to 4x
        print("zoom EO to 4x")
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIDEO_ZOOM_SUPER_RESOLUTION_FACTOR, Payload_Camera_Video_Zoom_Super_Resolution_Factor.ZOOM_SUPER_RESOLUTION_4X.value, param_type.PARAM_TYPE_UINT32.value)
        time.sleep(3) 
        
        # Zoom IR to 1x
        print("zoom IR to 1x")
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ZOOM_FACTOR, Payload_Camera_Ir_Zoom_Factor.ZOOM_IR_1X.value, param_type.PARAM_TYPE_UINT32.value) 
        time.sleep(3)  
        
        # Zoom IR to 4x
        print("zoom IR to 4x")
        my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ZOOM_FACTOR, Payload_Camera_Ir_Zoom_Factor.ZOOM_IR_4X.value, param_type.PARAM_TYPE_UINT32.value) 
        time.sleep(3)  
        
        # Short delay to prevent high CPU usage
        time.sleep(0.001)

if __name__ == "__main__":
    main()