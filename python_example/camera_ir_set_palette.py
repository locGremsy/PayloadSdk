import time
import signal
import sys
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, param_type, CONTROL_UDP
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
    print("Starting set palette example...")

    # Set view source
    print("Set view source to IR!")
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_IR.value, param_type.PARAM_TYPE_UINT32.value) 
    
    # Set palete
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_1.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: WhiteHot         |       G1: WhiteHot")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_2.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: BlackHot         |       G1: Fulgurite")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_3.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Rainbow         |       G1: IronRed")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_4.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: RainbowHC       |       G1: HotIron")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_5.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Ironbow         |       G1: Medical")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_6.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Lava            |       G1: Arctic")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_7.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Arctic          |       G1: Rainbow1")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_8.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Globow          |       G1: Rainbow2")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_9.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Gradedfire      |       G1: Tint")
    time.sleep(2)

    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_IR_PALETTE, Payload_Camera_Ir_Palette.PAYLOAD_CAMERA_IR_PALETTE_10.value, param_type.PARAM_TYPE_UINT32.value)
    print(" --> SET:      F1: Hottest         |       G1: BlackHot")
    time.sleep(2)

    # Close payload interface
    try:
        my_payload.sdkQuit()
        print("Payload connection closed successfully.")
    except Exception as e:
        print(f"Error while quitting payload: {e}")  

if __name__ == "__main__":
    main()