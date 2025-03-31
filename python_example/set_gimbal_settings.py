import time
from payload_sdk import PayloadSdkInterface, s_conn, PAYLOAD_GB_PARAMS

my_payload = None
STIFF_ROLL_VALUE = 0.0
step_num = 0

def onPayloadParamChanged(event: int, param_char: str, param: list):
    global STIFF_ROLL_VALUE, step_num
    if event == PAYLOAD_GB_PARAMS:
        print(f"--> Gimbal_param: id: {param_char}, index: {param[0]}, value: {param[1]}")
        if param_char == "STIFF_ROLL" and step_num == 0:
            STIFF_ROLL_VALUE = param[1]

def main():
    global my_payload, step_num
    
    print("Starting SetPayloadGimbalSettings example...\n")
    print("This sample will:")
    print(" 1. Download the current value of param STIFF_ROLL")
    print(" 2. Change the value of param STIFF_ROLL to 50")
    print(" 3. Download the value of param STIFF_ROLL to verify the changed")
    print(" 4. Change the value for STIFF_ROLL back to the original")
    print(" 5. Download the value of param STIFF_ROLL to verify the changed\n")
    
    # Tạo đối tượng PayloadSdkInterface
    my_payload = PayloadSdkInterface(s_conn)
    
    # Khởi tạo kết nối
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")
    
    # Đăng ký callback
    my_payload.regPayloadParamChanged(onPayloadParamChanged)
    
    # Kiểm tra kết nối
    my_payload.checkPayloadConnection()
    time.sleep(0.5)
    
    while True:
        if step_num == 0:
            # Bước 1
            my_payload.getPayloadGimbalSettingByID("STIFF_ROLL")
            time.sleep(1)
            step_num = 1
        elif step_num == 1:
            # Bước 2
            my_payload.setPayloadGimbalParamByID("STIFF_ROLL", 50.0)
            time.sleep(1)
            step_num = 2
        elif step_num == 2:
            # Bước 3
            my_payload.getPayloadGimbalSettingByID("STIFF_ROLL")
            time.sleep(1)
            step_num = 3
        elif step_num == 3:
            # Bước 4
            my_payload.setPayloadGimbalParamByID("STIFF_ROLL", STIFF_ROLL_VALUE)
            time.sleep(1)
            step_num = 4
        elif step_num == 4:
            # Bước 5
            my_payload.getPayloadGimbalSettingByID("STIFF_ROLL")
            time.sleep(1)
            step_num = 5
        elif step_num == 5:
            # Bước 6
            my_payload.getPayloadGimbalSettingList()
            time.sleep(1)
            step_num = 6
        else:
            break
    
    print("Done. Exit")
    time.sleep(1)
    
    # Đóng kết nối
    my_payload.sdkQuit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTERMINATING AT USER REQUEST\n")
        if my_payload:
            my_payload.sdkQuit()