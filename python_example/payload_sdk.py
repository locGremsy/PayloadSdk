import ctypes
import time
import threading
from typing import Callable

# Định nghĩa các kiểu dữ liệu từ payloadsdk.h
class T_ConnInfo_Uart(ctypes.Structure):
    _fields_ = [("name", ctypes.c_char_p),
                ("baudrate", ctypes.c_int)]

class T_ConnInfo_UDP(ctypes.Structure):
    _fields_ = [("ip", ctypes.c_char_p),
                ("port", ctypes.c_int)]

class T_ConnInfo(ctypes.Union):
    _fields_ = [("uart", T_ConnInfo_Uart),
                ("udp", T_ConnInfo_UDP)]

class T_ConnInfoStruct(ctypes.Structure):
    _anonymous_ = ("device",)
    _fields_ = [("type", ctypes.c_uint8),
                ("device", T_ConnInfo)]
    
class MavlinkMessageT(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("checksum", ctypes.c_uint16),
        ("magic", ctypes.c_uint8),
        ("len", ctypes.c_uint8),
        ("incompat_flags", ctypes.c_uint8),
        ("compat_flags", ctypes.c_uint8),
        ("seq", ctypes.c_uint8),
        ("sysid", ctypes.c_uint8),
        ("compid", ctypes.c_uint8),
        ("msgid", ctypes.c_uint8 * 3),  # Đổi thành mảng 3 byte thay vì c_uint32
        ("payload64", ctypes.c_uint64 * 33),
        ("ck", ctypes.c_uint8 * 2),
        ("signature", ctypes.c_uint8 * 13),
    ]

# Callback types
PAYLOAD_PARAM_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))
PAYLOAD_STATUS_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
PAYLOAD_STREAMINFO_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))

# Hằng số từ payloadsdk.h
CONTROL_UDP = 1
SDK_VERSION = "3.0.0_build.04022025"
CAMERA_MODE_RECORD = 1  # Ví dụ, cần thêm đầy đủ từ enum
INPUT_MODE_RATE = 2     # Ví dụ, cần thêm đầy đủ từ enum

# Thêm các hằng số từ enum payload_status_event_t
PAYLOAD_CAM_CAPTURE_STATUS = 0
PAYLOAD_CAM_STORAGE_INFO = 1
PAYLOAD_CAM_SETTINGS = 2
PAYLOAD_CAM_PARAMS = 3
PAYLOAD_GB_ATTITUDE = 4
PAYLOAD_GB_PARAMS = 5
PAYLOAD_ACK = 6
PAYLOAD_CAM_INFO = 7
PAYLOAD_CAM_STREAMINFO = 8
PAYLOAD_PARAMS = 9
PAYLOAD_PARAM_EXT_ACK = 10

class PayloadSdkInterface:
    def __init__(self, conn_info: T_ConnInfoStruct = None):
        # Load thư viện động
        self.lib = ctypes.CDLL("./PayloadSdk/build/libs/libPayloadSDK.so")  # Thay đường dẫn nếu cần
        
        # Khởi tạo các hàm từ wrapper
        self._setup_function_prototypes()
        
        # Tạo instance
        if conn_info is None:
            self.obj = self.lib.PayloadSdkInterface_new_default()
        else:
            self.obj = self.lib.PayloadSdkInterface_new(conn_info)
        
        # Lưu callback
        self._param_callback = None
        self._status_callback = None
        self._stream_callback = None

    def _setup_function_prototypes(self):
        # Core functions
        self.lib.PayloadSdkInterface_new.argtypes = [T_ConnInfoStruct]
        self.lib.PayloadSdkInterface_new.restype = ctypes.c_void_p
        self.lib.PayloadSdkInterface_new_default.argtypes = []
        self.lib.PayloadSdkInterface_new_default.restype = ctypes.c_void_p
        self.lib.PayloadSdkInterface_delete.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sdkInitConnection.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sdkInitConnection.restype = ctypes.c_int
        self.lib.PayloadSdkInterface_sdkQuit.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_checkPayloadConnection.argtypes = [ctypes.c_void_p]

        # Callback registration
        self.lib.PayloadSdkInterface_regPayloadParamChanged.argtypes = [ctypes.c_void_p, PAYLOAD_PARAM_CALLBACK_T]
        self.lib.PayloadSdkInterface_regPayloadStatusChanged.argtypes = [ctypes.c_void_p, PAYLOAD_STATUS_CALLBACK_T]
        self.lib.PayloadSdkInterface_regPayloadStreamChanged.argtypes = [ctypes.c_void_p, PAYLOAD_STREAMINFO_CALLBACK_T]

        # Camera functions
        self.lib.PayloadSdkInterface_setPayloadCameraParam.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint8]
        self.lib.PayloadSdkInterface_getPayloadCameraSettingList.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadCameraSettingByID.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.PayloadSdkInterface_getPayloadCameraSettingByIndex.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        self.lib.PayloadSdkInterface_getPayloadStorage.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadCaptureStatus.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadCameraMode.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadCameraInformation.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadCameraStreamingInformation.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_setPayloadCameraMode.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        self.lib.PayloadSdkInterface_setPayloadCameraCaptureImage.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.lib.PayloadSdkInterface_setPayloadCameraStopImage.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_setPayloadCameraRecordVideoStart.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_setPayloadCameraRecordVideoStop.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_setCameraZoom.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
        self.lib.PayloadSdkInterface_setCameraFocus.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]

        # Gimbal functions
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByID.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.PayloadSdkInterface_setPayloadGimbalParamByID.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingList.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByIndex.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibGyro.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibAccel.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibMotor.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalSearchHome.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalAutoTune.argtypes = [ctypes.c_void_p, ctypes.c_bool]
        self.lib.PayloadSdkInterface_setGimbalSpeed.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_uint8]

        # Tracking
        self.lib.PayloadSdkInterface_setPayloadObjectTrackingParams.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float]

        # Thêm hàm getNewMessage
        self.lib.PayloadSdkInterface_getNewMessage.argtypes = [ctypes.c_void_p, ctypes.POINTER(MavlinkMessageT)]
        self.lib.PayloadSdkInterface_getNewMessage.restype = ctypes.c_uint8

    # Core methods
    def sdkInitConnection(self):
        return self.lib.PayloadSdkInterface_sdkInitConnection(self.obj)

    def sdkQuit(self):
        self.lib.PayloadSdkInterface_sdkQuit(self.obj)

    def checkPayloadConnection(self):
        self.lib.PayloadSdkInterface_checkPayloadConnection(self.obj)

    # Callback methods
    def regPayloadParamChanged(self, callback: Callable[[int, str, list], None]):
        self._param_callback = PAYLOAD_PARAM_CALLBACK_T(lambda event, param_char, param_double: 
            callback(event, param_char.decode('utf-8'), [param_double[i] for i in range(2)]))
        self.lib.PayloadSdkInterface_regPayloadParamChanged(self.obj, self._param_callback)

    # def regPayloadStatusChanged(self, callback: Callable[[int, list], None]):
    #     self._status_callback = PAYLOAD_STATUS_CALLBACK_T(lambda event, param: 
    #         callback(event, [param[i] for i in range(ctypes.cast(param, ctypes.POINTER(ctypes.c_double * 10)).contents._length_)]))
    #     self.lib.PayloadSdkInterface_regPayloadStatusChanged(self.obj, self._status_callback)

    def regPayloadStatusChanged(self, callback: Callable[[int, list], None]):
        # Sửa lại để đảm bảo callback không bị garbage collected và nhận đúng số tham số
        self._status_callback = PAYLOAD_STATUS_CALLBACK_T(lambda event, param: 
            callback(event, [param[i] for i in range(3)]))  # Chỉ lấy 3 phần tử: cmd_id, result, progress
        self.lib.PayloadSdkInterface_regPayloadStatusChanged(self.obj, self._status_callback)

    def regPayloadStreamChanged(self, callback: Callable[[int, str, list], None]):
        self._stream_callback = PAYLOAD_STREAMINFO_CALLBACK_T(lambda event, param_char, param_double: 
            callback(event, param_char.decode('utf-8'), [param_double[i] for i in range(2)]))
        self.lib.PayloadSdkInterface_regPayloadStreamChanged(self.obj, self._stream_callback)

    # Camera methods
    def setPayloadCameraParam(self, param_id: str, param_value: int, param_type: int):
        self.lib.PayloadSdkInterface_setPayloadCameraParam(self.obj, param_id.encode('utf-8'), param_value, param_type)

    def getPayloadCameraSettingList(self):
        self.lib.PayloadSdkInterface_getPayloadCameraSettingList(self.obj)

    def getPayloadCameraSettingByID(self, param_id: str):
        self.lib.PayloadSdkInterface_getPayloadCameraSettingByID(self.obj, param_id.encode('utf-8'))

    def getPayloadCameraSettingByIndex(self, idx: int):
        self.lib.PayloadSdkInterface_getPayloadCameraSettingByIndex(self.obj, idx)

    def getPayloadStorage(self):
        self.lib.PayloadSdkInterface_getPayloadStorage(self.obj)

    def getPayloadCaptureStatus(self):
        self.lib.PayloadSdkInterface_getPayloadCaptureStatus(self.obj)

    def getPayloadCameraMode(self):
        self.lib.PayloadSdkInterface_getPayloadCameraMode(self.obj)

    def getPayloadCameraInformation(self):
        self.lib.PayloadSdkInterface_getPayloadCameraInformation(self.obj)

    def getPayloadCameraStreamingInformation(self):
        self.lib.PayloadSdkInterface_getPayloadCameraStreamingInformation(self.obj)

    def setPayloadCameraMode(self, mode: int):
        self.lib.PayloadSdkInterface_setPayloadCameraMode(self.obj, mode)

    def setPayloadCameraCaptureImage(self, param: int = 0):
        self.lib.PayloadSdkInterface_setPayloadCameraCaptureImage(self.obj, param)

    def setPayloadCameraStopImage(self):
        self.lib.PayloadSdkInterface_setPayloadCameraStopImage(self.obj)

    def setPayloadCameraRecordVideoStart(self):
        self.lib.PayloadSdkInterface_setPayloadCameraRecordVideoStart(self.obj)

    def setPayloadCameraRecordVideoStop(self):
        self.lib.PayloadSdkInterface_setPayloadCameraRecordVideoStop(self.obj)

    def setCameraZoom(self, zoom_type: float, zoom_value: float):
        self.lib.PayloadSdkInterface_setCameraZoom(self.obj, zoom_type, zoom_value)

    def setCameraFocus(self, focus_type: float, focus_value: float = 0):
        self.lib.PayloadSdkInterface_setCameraFocus(self.obj, focus_type, focus_value)

    # Gimbal methods
    def getPayloadGimbalSettingByID(self, param_id: str):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByID(self.obj, param_id.encode('utf-8'))

    def setPayloadGimbalParamByID(self, param_id: str, value: float):
        self.lib.PayloadSdkInterface_setPayloadGimbalParamByID(self.obj, param_id.encode('utf-8'), value)

    def getPayloadGimbalSettingList(self):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingList(self.obj)

    def getPayloadGimbalSettingByIndex(self, idx: int):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByIndex(self.obj, idx)

    def sendPayloadGimbalCalibGyro(self):
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibGyro(self.obj)

    def sendPayloadGimbalCalibAccel(self):
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibAccel(self.obj)

    def sendPayloadGimbalCalibMotor(self):
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibMotor(self.obj)

    def sendPayloadGimbalSearchHome(self):
        self.lib.PayloadSdkInterface_sendPayloadGimbalSearchHome(self.obj)

    def sendPayloadGimbalAutoTune(self, status: bool):
        self.lib.PayloadSdkInterface_sendPayloadGimbalAutoTune(self.obj, status)

    def setGimbalSpeed(self, spd_pitch: float, spd_roll: float, spd_yaw: float, mode: int):
        self.lib.PayloadSdkInterface_setGimbalSpeed(self.obj, spd_pitch, spd_roll, spd_yaw, mode)

    # Tracking methods
    def setPayloadObjectTrackingParams(self, cmd: float, pos_x: float = 960, pos_y: float = 540):
        self.lib.PayloadSdkInterface_setPayloadObjectTrackingParams(self.obj, cmd, pos_x, pos_y)

    def payload_recv_handle(self):
        # Giả lập xử lý nhận tin nhắn, trong thực tế cần gọi hàm từ C++ nếu có
        while not self.time_to_exit:
            time.sleep(0.0001)  # Tương đương usleep(100)

    # Thêm hàm getNewMessage
    def getNewMessage(self):
        msg = MavlinkMessageT()
        print("receive_messages", f"Size of MavlinkMessageT: {ctypes.sizeof(MavlinkMessageT)}")
        msg_cnt = self.lib.PayloadSdkInterface_getNewMessage(self.obj, ctypes.pointer(msg))
        return msg_cnt, msg
    
    # def get_msgid(self):
    #     # Đọc 24-bit từ mảng 3 byte (little-endian)
    #     return int.from_bytes(self.msgid, byteorder='little') & 0xFFFFFF

    def __del__(self):
        self.lib.PayloadSdkInterface_delete(self.obj)

# Cấu hình kết nối mặc định
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.251"
s_conn.udp.port = 14566

# Ví dụ sử dụng
if __name__ == "__main__":
    payload = PayloadSdkInterface(s_conn)
    payload.sdkInitConnection()
    payload.setGimbalSpeed(10.0, 0.0, 5.0, INPUT_MODE_RATE)
    time.sleep(2)
    payload.setGimbalSpeed(0.0, 0.0, 0.0, INPUT_MODE_RATE)
    time.sleep(2)
    payload.sdkQuit()