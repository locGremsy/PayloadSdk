import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, CONTROL_UDP
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

def main():
    global my_payload

    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Check connection
    my_payload.checkPayloadConnection()

    # Set view source to IR
    print("Set view source to IR!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_IR.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(1) 

    # Enable IR isotherms with high gain
    print("Enable IR Isotherms with high GAIN, sleep 5s ...")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ISOTHERMS, Payload_Camera_Ir_Isotherms.PAYLOAD_CAMERA_IR_ISOTHERMS_ENABLE.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.1) 
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ISOTHERMS_GAIN, Payload_Camera_Ir_Isotherms_Gain.PAYLOAD_CAMERA_IR_ISOTHERMS_HIGH_GAIN.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5)  

    # Switch to low gain
    print("Switch low GAIN, sleep 5s ...")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ISOTHERMS_GAIN, Payload_Camera_Ir_Isotherms_Gain.PAYLOAD_CAMERA_IR_ISOTHERMS_LOW_GAIN, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(5) 

    # Disable IR Isotherms
    print("Disable IR Isotherms.")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_ISOTHERMS, Payload_Camera_Ir_Isotherms.PAYLOAD_CAMERA_IR_ISOTHERMS_DISABLE, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.1) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
        print("Payload connection closed successfully.")
    except Exception as e:
        print(f"Error while quitting payload: {e}") 

if __name__ == "__main__":
    main()