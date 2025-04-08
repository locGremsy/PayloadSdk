import time
import signal
import sys
from ..libs.payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, payload_status_event_t, payload_param_t, CONTROL_UDP, PAYLOAD_TYPE
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
    global time_to_exit
    print("\nTERMINATING AT USER REQUEST")
    time_to_exit = True

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

    elif event == payload_status_event_t.PAYLOAD_PARAMS.value:
        # param[0]: param index
        # param[1]: value

        if param[0] == payload_param_t.PARAM_EO_ZOOM_LEVEL.value:
            print(f"Payload EO_ZOOM_LEVEL: {param[1]:.2f}")

        elif param[0] == payload_param_t.PARAM_IR_ZOOM_LEVEL.value:
            print(f"Payload IR_ZOOM_LEVEL: {param[1]:.2f}")

        elif PAYLOAD_TYPE == "VIO":
            if param[0] == payload_param_t.PARAM_LRF_RANGE.value:
                print(f"Payload LRF_RANGE: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_LRF_OFSET_X.value:
                print(f"Payload PARAM_LRF_OFSET_X: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_LRF_OFSET_Y.value:
                print(f"Payload PARAM_LRF_OFSET_Y: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_TARGET_COOR_LON.value:
                print(f"Payload PARAM_TARGET_COOR_LON: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_TARGET_COOR_LAT.value:
                print(f"Payload PARAM_TARGET_COOR_LAT: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_TARGET_COOR_ALT.value:
                print(f"Payload PARAM_TARGET_COOR_ALT: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_CAM_VIEW_MODE.value:
                print(f"Payload PARAM_CAM_VIEW_MODE: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_CAM_REC_SOURCE.value:
                print(f"Payload PARAM_CAM_REC_SOURCE: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_CAM_IR_TYPE.value:
                print(f"Payload PARAM_CAM_IR_TYPE: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_CAM_IR_PALETTE_ID.value:
                print(f"Payload PARAM_CAM_IR_PALETTE_ID: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_GIMBAL_MODE.value:
                print(f"Payload PARAM_GIMBAL_MODE: {param[1]:.2f}")

            elif param[0] == payload_param_t.PARAM_PAYLOAD_GPS_LON.value:
                print(f"Payload PARAM_PAYLOAD_GPS_LON: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_PAYLOAD_GPS_LAT.value:
                print(f"Payload PARAM_PAYLOAD_GPS_LAT: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_PAYLOAD_GPS_ALT.value:
                print(f"Payload PARAM_PAYLOAD_GPS_ALT: {param[1]:.6f}")

            elif param[0] == payload_param_t.PARAM_CAM_IR_FFC_MODE.value:
                print(f"Payload PARAM_CAM_IR_FFC_MODE: {param[1]:.2f}")

def main():
    global my_payload

    print("Starting Set gimbal mode example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Register callback function
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)

    # Check connection
    my_payload.checkPayloadConnection()

    my_payload.setParamRate(payload_param_t.PARAM_EO_ZOOM_LEVEL.value, 1000)
    my_payload.setParamRate(payload_param_t.PARAM_IR_ZOOM_LEVEL.value, 1000)

    if PAYLOAD_TYPE == "VIO":
        my_payload.setParamRate(payload_param_t.PARAM_LRF_RANGE.value, 100)
        my_payload.setParamRate(payload_param_t.PARAM_LRF_OFSET_X.value, 100)
        my_payload.setParamRate(payload_param_t.PARAM_LRF_OFSET_Y.value, 100)

        my_payload.setParamRate(payload_param_t.PARAM_TARGET_COOR_LON.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_TARGET_COOR_LAT.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_TARGET_COOR_ALT.value, 1000)

        my_payload.setParamRate(payload_param_t.PARAM_CAM_VIEW_MODE.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_CAM_REC_SOURCE.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_CAM_IR_TYPE.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_CAM_IR_PALETTE_ID.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_GIMBAL_MODE.value, 1000)

        my_payload.setParamRate(payload_param_t.PARAM_PAYLOAD_GPS_LON.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_PAYLOAD_GPS_LAT.value, 1000)
        my_payload.setParamRate(payload_param_t.PARAM_PAYLOAD_GPS_ALT.value, 1000)

        my_payload.setParamRate(payload_param_t.PARAM_CAM_IR_FFC_MODE.value, 1000)

    while not time_to_exit:
        time.sleep(0.01) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()