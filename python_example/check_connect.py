import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, CONTROL_UDP
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

def main():
    global my_payload, time_to_exit

    print("Starting ConnectPayload example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Check connection
    my_payload.checkPayloadConnection()

    # Keep program running to maintain connection
    while not time_to_exit:
        # Short delay to prevent high CPU usage
        time.sleep(0.001)

if __name__ == "__main__":
    main()