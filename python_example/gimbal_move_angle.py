import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, input_mode_t, param_type, CONTROL_UDP
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

    print("Starting Set gimbal mode example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Check connection
    my_payload.checkPayloadConnection()
    time.sleep(0.1)

    # Set gimbal RC mode to STANDARD 
    print("Set gimbal RC mode")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_RC_MODE, Payload_Camera_Rc_Mode.PAYLOAD_CAMERA_RC_MODE_STANDARD.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.1)  

    # Move gimbal yaw to 90 deg
    print("Move gimbal yaw to 90 deg, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, 90, input_mode_t.INPUT_ANGLE.value)
    time.sleep(5)  

    # Move gimbal yaw to -90 deg
    print("Move gimbal yaw to -90 deg, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, -90, input_mode_t.INPUT_ANGLE.value)
    time.sleep(5)  

    # Move gimbal yaw to 0 deg
    print("Move gimbal yaw to 0 deg, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, 0, input_mode_t.INPUT_ANGLE.value)
    time.sleep(0.5) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()