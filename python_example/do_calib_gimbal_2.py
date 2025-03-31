import ctypes
import time
import signal
import sys
import threading
from enum import Enum
from typing import Callable
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, CONTROL_UDP, PAYLOAD_ACK

# Định nghĩa các hằng số từ MAVLink
MAV_CMD_GIMBAL_REQUEST_AXIS_CALIBRATION = 42503
MAV_CMD_DO_SET_HOME = 179
MAV_CMD_USER_3 = 300
MAV_RESULT_ACCEPTED = 0
MAV_RESULT_IN_PROGRESS = 5
MAVLINK_MSG_ID_COMMAND_ACK = 77

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
start_time = time.time() * 1000000

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
    if event == PAYLOAD_ACK:
        if len(param) < 3:
            sdk_log("onPayloadStatusChanged", f"Warning: Received param with insufficient length: {param}")
            return
        
        cmd_id, result, progress = int(param[0]), int(param[1]), int(param[2])
        sdk_log("onPayloadStatusChanged", f"Got ack from {cmd_id}, result {result}, progress: {progress}")

        if my_calib == CalibType.CALIB_MOTOR and cmd_id == MAV_CMD_DO_SET_HOME:
            if result == MAV_RESULT_ACCEPTED and not is_calibration_running:
                is_calibration_running = True
                sdk_log("onPayloadStatusChanged", "Calibration started")
                time.sleep(1)
            if progress == MAV_RESULT_ACCEPTED and is_calibration_running:
                sdk_log("onPayloadStatusChanged", "The motor calibration done!")
                is_exit = True
            elif progress == MAV_RESULT_IN_PROGRESS:
                sdk_log("onPayloadStatusChanged", "The motor calibration is processing...")
                is_calibration_running = True

# Luồng nhận tin nhắn
def receive_messages():
    global is_exit
    while not is_exit:
        msg_cnt, msg = my_payload.getNewMessage()
        if msg_cnt:
            sdk_log("receive_messages", f"Received message: msgid={msg.msgid}, sysid={msg.sysid}, compid={msg.compid}")
            if msg.msgid == MAVLINK_MSG_ID_COMMAND_ACK:
                # Phân tích payload của COMMAND_ACK
                payload = ctypes.cast(msg.payload64, ctypes.POINTER(ctypes.c_uint8))
                cmd_id = ctypes.c_uint16.from_buffer(payload, 0).value  # 2 bytes
                result = payload[2]  # 1 byte
                progress = payload[3]  # 1 byte
                sdk_log("receive_messages", f"COMMAND_ACK parsed: cmd_id={cmd_id}, result={result}, progress={progress}")
                # Gọi callback thủ công
                on_payload_status_changed(PAYLOAD_ACK, [cmd_id, result, progress])
        # else:
        #     sdk_log("receive_messages", "No message received")
        time.sleep(0.01)  # Giảm thời gian ngủ để tăng tần suất kiểm tra

def main():
    global my_payload, is_calibration_running, is_exit, my_calib

    print("Starting Do Calib gimbal example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Tạo đối tượng PayloadSdkInterface
    my_payload = PayloadSdkInterface(s_conn)
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Đăng ký callback (dù có thể không cần nếu dùng receive_messages)
    my_payload.regPayloadStatusChanged(on_payload_status_changed)

    # Kiểm tra kết nối
    my_payload.checkPayloadConnection()

    # Chạy luồng nhận tin nhắn
    recv_thread = threading.Thread(target=receive_messages, daemon=True)
    recv_thread.start()

    # Chọn loại calibration
    my_calib = CalibType.CALIB_MOTOR

    # Gửi lệnh calibration
    if my_calib == CalibType.CALIB_MOTOR:
        is_calibration_running = False
        my_payload.sendPayloadGimbalCalibMotor()
        sdk_log("main", "Calib motor command was sent. Waiting for the calibration done...")

    # Chờ quá trình calib hoàn tất
    while not is_exit:
        time.sleep(1)

    time.sleep(1)
    sdk_log("main", "Exit.")

if __name__ == "__main__":
    main()