import time
import signal
import sys
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, MavlinkGlobalPositionInt, CONTROL_UDP
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
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

    # End program    
    sys.exit(0)

def main():
    global my_payload

    print("Starting SendGPS example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Check connection
    my_payload.checkPayloadConnection()

    msg_cnt = 0
    boot_time_ms = 0


    while True:

        # Create GPS data
        gps = MavlinkGlobalPositionInt()
        gps.time_boot_ms = boot_time_ms
        boot_time_ms += 100               # Need to add boot_time_ms of your system here
        gps.lat = int(40.730610 * 1e7)    # The location of NewYork city
        gps.lon = int(-73.935242 * 1e7)   
        gps.alt = int(50 * 1e3)           
        gps.relative_alt = 0              
        gps.vx = 0                        # Don't use
        gps.vy = 0                        # Don't use
        gps.vz = 0                        # Don't use
        gps.hdg = 90                      # The heading of GPS

        # Send GPS data
        my_payload.sendPayloadGPSPosition(gps)
        print(f"Send GPS data to payload: {msg_cnt}")
        msg_cnt += 1

        time.sleep(0.1)

if __name__ == "__main__":
    main()