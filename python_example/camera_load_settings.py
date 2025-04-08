import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, payload_status_event_t, CONTROL_UDP
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

# Callback function for payload param changes
def onPayloadParamChanged(event: int, param_char: str, param: list):
    if event == payload_status_event_t.PAYLOAD_CAM_PARAMS.value:
        # param[0]: param_index
		# param[1]: value
        print(f" --> Param_id: {param_char}, value: {param[1]:.2f}")

# Callback function for payload status changes
def onPayloadStatusChanged(event: int, param: list):
    if event == payload_status_event_t.PAYLOAD_PARAM_EXT_ACK.value:
        print(f" --> Got ack, result {param[0]:.2f}")

def main():
    global my_payload

    print("Starting LoadPayloadSettings example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!\n")

    # Register callback functions
    my_payload.regPayloadParamChanged(onPayloadParamChanged)
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)

    # Check connection
    my_payload.checkPayloadConnection()

    # Request to read all settings of payload
    my_payload.getPayloadCameraSettingList()

    while True:
        time.sleep(10)  
        break
    
    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()