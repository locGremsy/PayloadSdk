import ctypes
import time
import signal
import sys
import threading
from enum import Enum
from typing import Callable
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, CONTROL_UDP, PAYLOAD_GB_PARAMS, PAYLOAD_CAM_PARAMS, PAYLOAD_ACK

# Định nghĩa các hằng số từ MAVLink (cần giá trị thực tế từ SDK hoặc pymavlink)
MAV_CMD_GIMBAL_REQUEST_AXIS_CALIBRATION = 42503  # Giá trị giả định
MAV_CMD_DO_SET_HOME = 179                      # Giá trị từ MAVLink
MAV_CMD_USER_3 = 300                           # Giá trị giả định
MAV_RESULT_ACCEPTED = 0
MAV_RESULT_IN_PROGRESS = 5

# Cấu hình kết nối mặc định
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.251"
s_conn.udp.port = 14566

# Định nghĩa enum calib_type_t
class CalibType(Enum):
    CALIB_GYRO = 0
    CALIB_ACCEL = 1
    AUTO_TUNE = 2
    CALIB_MOTOR = 3
    SEARCH_HOME = 4

# Biến toàn cục
my_payload = None
is_calibration_running = False
is_exit = False
my_calib = CalibType.CALIB_GYRO
start_time = time.time() * 1000000  # Microseconds để tính timestamp

# Hàm log giống SDK_LOG
def sdk_log(func_name, message):
    elapsed_time = int((time.time() * 1000000) - start_time)
    print(f"[{elapsed_time}] SDK {func_name}(): {message}")

# Hàm xử lý tín hiệu thoát (SIGINT)
def quit_handler(sig, frame):
    print("\nTERMINATING AT USER REQUEST")
    global is_exit
    is_exit = True
    if my_payload:
        my_payload.sdkQuit()
    sys.exit(0)

# Callback xử lý trạng thái
def on_payload_status_changed(event: int, param: list):
    global is_calibration_running, is_exit
    # print("my_calib: ", my_calib)
    if event == PAYLOAD_ACK:
        if len(param) < 3:
            sdk_log("onPayloadStatusChanged", f"Warning: Received param with insufficient length: {param}")
            return
        
        cmd_id, result, progress = param[0], param[1], param[2]
        # sdk_log("onPayloadStatusChanged", f"Got ack from {cmd_id:.0f}, result {result:.0f}, progress: {progress:.0f}")

        if my_calib == CalibType.CALIB_GYRO:
            if cmd_id == MAV_CMD_GIMBAL_REQUEST_AXIS_CALIBRATION:
                if result == MAV_RESULT_ACCEPTED:
                    is_calibration_running = True
                if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                    sdk_log("onPayloadStatusChanged", "The gyro calibration done!")
                    is_exit = True
                elif progress == MAV_RESULT_IN_PROGRESS:
                    is_calibration_running = True
                    sdk_log("onPayloadStatusChanged", "The gyro calibration is processing...")

        elif my_calib == CalibType.CALIB_ACCEL:
            if cmd_id == MAV_CMD_GIMBAL_REQUEST_AXIS_CALIBRATION:
                if result == MAV_RESULT_ACCEPTED:
                    is_calibration_running = True
                if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                    sdk_log("onPayloadStatusChanged", "The accel calibration done!")
                    is_exit = True
                elif progress == MAV_RESULT_IN_PROGRESS:
                    is_calibration_running = True
                    sdk_log("onPayloadStatusChanged", "The accel calibration is processing...")

        elif my_calib == CalibType.CALIB_MOTOR:
            if cmd_id == MAV_CMD_DO_SET_HOME:
                if result == MAV_RESULT_ACCEPTED:
                    is_calibration_running = True
                    time.sleep(1)
                if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                    sdk_log("onPayloadStatusChanged", "The motor calibration done!")
                    is_exit = True
                elif progress == MAV_RESULT_IN_PROGRESS:
                    is_calibration_running = True
                    sdk_log("onPayloadStatusChanged", "The motor calibration is processing...")

        elif my_calib == CalibType.AUTO_TUNE:
            if cmd_id == MAV_CMD_USER_3:
                if result == MAV_RESULT_ACCEPTED:
                    is_calibration_running = True
                    time.sleep(1)
                if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                    sdk_log("onPayloadStatusChanged", "The Auto tune done!")
                    time.sleep(1)
                    is_exit = True
                elif progress == MAV_RESULT_IN_PROGRESS:
                    is_calibration_running = True
                    sdk_log("onPayloadStatusChanged", "The Auto tune is processing...")

        elif my_calib == CalibType.SEARCH_HOME:
            if cmd_id == MAV_CMD_DO_SET_HOME:
                if result == MAV_RESULT_ACCEPTED:
                    is_calibration_running = True
                    time.sleep(1)
                if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                    sdk_log("onPayloadStatusChanged", "The SearchHome done!")
                    is_exit = True
                elif progress == MAV_RESULT_IN_PROGRESS:
                    is_calibration_running = True
                    sdk_log("onPayloadStatusChanged", "The SearchHome is processing...")

# Callback xử lý tham số
def on_payload_param_changed(event: int, param_char: str, param: list):
    if event == PAYLOAD_CAM_PARAMS and len(param) >= 2:
        sdk_log("onPayloadParamChanged", f"--> Payload_param: {param_char}, value: {param[1]:.2f}")
    elif event == PAYLOAD_GB_PARAMS and len(param) >= 2:
        sdk_log("onPayloadParamChanged", f"--> Gimbal_param: index: {param[0]:.0f}, id: {param_char}, value: {param[1]:.0f}")

def main():
    global my_payload, is_calibration_running, is_exit, my_calib

    print("Starting Do Calib gimbal example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Tạo đối tượng PayloadSdkInterface
    my_payload = PayloadSdkInterface(s_conn)
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Đăng ký callback
    my_payload.regPayloadStatusChanged(on_payload_status_changed)
    # my_payload.regPayloadParamChanged(on_payload_param_changed)

    # Kiểm tra kết nối
    my_payload.checkPayloadConnection()

    # Chọn loại calibration
    my_calib = CalibType.CALIB_MOTOR

    # Gửi lệnh calibration
    if my_calib == CalibType.CALIB_GYRO:
        is_calibration_running = False
        my_payload.sendPayloadGimbalCalibGyro()
        sdk_log("main", "Calib gyro command was sent. Waiting for the calibration done...")
    elif my_calib == CalibType.CALIB_ACCEL:
        is_calibration_running = False
        my_payload.sendPayloadGimbalCalibAccel()
        sdk_log("main", "Calib accel command was sent. Waiting for the calibration done...")
    elif my_calib == CalibType.CALIB_MOTOR:
        is_calibration_running = False
        my_payload.sendPayloadGimbalCalibMotor()
        sdk_log("main", "Calib motor command was sent. Waiting for the calibration done...")
    elif my_calib == CalibType.AUTO_TUNE:
        is_calibration_running = False
        my_payload.sendPayloadGimbalAutoTune(True)
        sdk_log("main", "Auto tune command was sent. Waiting for the process done...")
    elif my_calib == CalibType.SEARCH_HOME:
        is_calibration_running = False
        my_payload.sendPayloadGimbalSearchHome()
        sdk_log("main", "Searching Home command was sent. Waiting for the calibration done...")

    # Chờ quá trình calib hoàn tất
    while not is_exit:
        time.sleep(1)  # Tương đương usleep(1000000)

    # Tải tham số để xác minh
    if my_calib == CalibType.CALIB_GYRO:
        sdk_log("main", "Load the Gyro offset values...")
        my_payload.getPayloadGimbalSettingByID("GYROX_OFFSET")
        my_payload.getPayloadGimbalSettingByID("GYROY_OFFSET")
        my_payload.getPayloadGimbalSettingByID("GYROZ_OFFSET")
    elif my_calib == CalibType.CALIB_ACCEL:
        sdk_log("main", "Load the accel offset values...")
        my_payload.getPayloadGimbalSettingByID("ACCELX_OFFSET")
        my_payload.getPayloadGimbalSettingByID("ACCELY_OFFSET")
        my_payload.getPayloadGimbalSettingByID("ACCELZ_OFFSET")
    elif my_calib == CalibType.AUTO_TUNE:
        sdk_log("main", "Waiting for the gimbal rebooted...20s")
        time.sleep(20)  # Tương đương usleep(20000000)
        sdk_log("main", "Load the Stiffness/Holdstrength values...")
        my_payload.getPayloadGimbalSettingByID("STIFF_TILT")
        my_payload.getPayloadGimbalSettingByID("STIFF_ROLL")
        my_payload.getPayloadGimbalSettingByID("STIFF_PAN")
        my_payload.getPayloadGimbalSettingByID("PWR_TILT")
        my_payload.getPayloadGimbalSettingByID("PWR_ROLL")
        my_payload.getPayloadGimbalSettingByID("PWR_PAN")

    time.sleep(1)  # Tương đương usleep(1000000)
    sdk_log("main", "Exit.")

if __name__ == "__main__":
    main()