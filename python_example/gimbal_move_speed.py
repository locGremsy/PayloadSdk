import time
import signal
import sys
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, payload_status_event_t, input_mode_t, param_type, CONTROL_UDP
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
    if event == payload_status_event_t.PAYLOAD_GB_ATTITUDE.value:
        # param[0]: pitch
        # param[1]: roll
        # param[2]: yaw

        print(f"Pitch: {param[0]:.2f} - Roll: {param[1]:.2f} - Yaw: {param[2]:.2f}")

def main():
    global my_payload

    print("Starting Set gimbal mode example...\n")
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
    time.sleep(0.1)  

    # Set gimbal RC mode
    print("Set gimbal RC mode")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_RC_MODE, Payload_Camera_Rc_Mode.PAYLOAD_CAMERA_RC_MODE_STANDARD.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.1)  

    # Move gimbal yaw to the right 20 deg/s
    print("Move gimbal yaw to the right 20 deg/s, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, 20, input_mode_t.INPUT_SPEED.value)
    time.sleep(5) 

    # Move gimbal yaw to the left 20 deg/s
    print("Move gimbal yaw to the left 20 deg/s, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, -20, input_mode_t.INPUT_SPEED.value)
    time.sleep(5) 

    # Keep gimbal stop
    print("Keep gimbal stop, delay in 5secs")
    my_payload.setGimbalSpeed(0, 0, 0, input_mode_t.INPUT_SPEED.value)
    time.sleep(0.5) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()