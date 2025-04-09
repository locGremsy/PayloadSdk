import ctypes
import time
from enum import Enum
from typing import Callable
from .payload_define import *
from .mavlink_define import *

# Payload type
PAYLOAD_TYPE = "VIO"

# Control types
CONTROL_UDP = 1
SDK_VERSION = "3.0.0_build.04022025"
CAMERA_MODE_RECORD = 1  
INPUT_MODE_RATE = 2    

# Connection info structures
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

# Param type enum
class param_type(Enum):
    PARAM_TYPE_UINT8 = 1
    PARAM_TYPE_INT8 = 2
    PARAM_TYPE_UINT16 = 3
    PARAM_TYPE_INT16 = 4
    PARAM_TYPE_UINT32 = 5
    PARAM_TYPE_INT32 = 6
    PARAM_TYPE_UINT64 = 7
    PARAM_TYPE_INT64  = 8
    PARAM_TYPE_REAL32 = 9
    PARAM_TYPE_REAL64 = 10

# Payload status event enum
class payload_status_event_t(Enum):
    PAYLOAD_CAM_CAPTURE_STATUS = 0
    PAYLOAD_CAM_STORAGE_INFO = 1
    PAYLOAD_CAM_SETTINGS = 2
    PAYLOAD_CAM_PARAMS = 3
    PAYLOAD_GB_ATTITUDE = 4
    PAYLOAD_GB_PARAMS = 5
    PAYLOAD_ACK = 6
    PAYLOAD_CAM_INFO  = 7
    PAYLOAD_CAM_STREAMINFO = 8
    PAYLOAD_PARAMS = 9
    PAYLOAD_PARAM_EXT_ACK = 10

# Payload param enum
class payload_param_t(Enum):
    PARAM_EO_ZOOM_LEVEL = 0
    PARAM_IR_ZOOM_LEVEL = 1
    PARAM_LRF_RANGE = 2
    PARAM_TRACK_POS_X = 3
    PARAM_TRACK_POS_Y = 4
    PARAM_TRACK_POS_W = 5
    PARAM_TRACK_POS_H = 6
    PARAM_TRACK_STATUS = 7
    PARAM_LRF_OFSET_X = 8
    PARAM_LRF_OFSET_Y = 9
    PARAM_TARGET_COOR_LON = 10
    PARAM_TARGET_COOR_LAT = 11
    PARAM_TARGET_COOR_ALT = 12
    PARAM_PAYLOAD_GPS_LON = 13
    PARAM_PAYLOAD_GPS_LAT = 14
    PARAM_PAYLOAD_GPS_ALT = 15
    PARAM_PAYLOAD_APP_VER_X = 16
    PARAM_PAYLOAD_APP_VER_Y = 17
    PARAM_PAYLOAD_APP_VER_Z = 18
    PARAM_CAM_VIEW_MODE = 19
    PARAM_CAM_REC_SOURCE = 20
    PARAM_CAM_IR_TYPE = 21
    PARAM_CAM_IR_PALETTE_ID = 22
    PARAM_CAM_IR_FFC_MODE = 23
    PARAM_GIMBAL_MODE = 24
    PARAM_COUNT = 25

# Input mode enum
class input_mode_t(Enum):
    INPUT_ANGLE = 1
    INPUT_SPEED = 2

# FFC mode enum
class ffc_mode_t(Enum):
    FFC_MODE_MANUAL = 0
    FFC_MODE_AUTO = 1
    FFC_MODE_END = 2

# Callback types
PAYLOAD_PARAM_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))
PAYLOAD_STATUS_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
PAYLOAD_STREAMINFO_CALLBACK_T = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))

class PayloadSdkInterface:
    def __init__(self, conn_info: T_ConnInfoStruct = None):

        # Load the shared library
        self.lib = ctypes.CDLL("../build/libs/libPayloadSDK.so")
        
        self._setup_function_prototypes()
        
        if conn_info is None:
            self.obj = self.lib.PayloadSdkInterface_new_default()
        else:
            self.obj = self.lib.PayloadSdkInterface_new(conn_info)
        
        self._param_callback = None
        self._status_callback = None
        self._stream_callback = None

    def _setup_function_prototypes(self):

        # Callback registration
        self.lib.PayloadSdkInterface_regPayloadParamChanged.argtypes = [ctypes.c_void_p, PAYLOAD_PARAM_CALLBACK_T]
        self.lib.PayloadSdkInterface_regPayloadStatusChanged.argtypes = [ctypes.c_void_p, PAYLOAD_STATUS_CALLBACK_T]
        self.lib.PayloadSdkInterface_regPayloadStreamChanged.argtypes = [ctypes.c_void_p, PAYLOAD_STREAMINFO_CALLBACK_T]

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
        self.lib.PayloadSdkInterface_setParamRate.argtypes = [ctypes.c_void_p, ctypes.c_uint8, ctypes.c_uint16]
        self.lib.PayloadSdkInterface_setCameraZoom.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
        self.lib.PayloadSdkInterface_setCameraFocus.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]

        # Gimbal functions
        self.lib.PayloadSdkInterface_setPayloadGimbalParamByID.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibGyro.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibAccel.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalCalibMotor.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalSearchHome.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_sendPayloadGimbalAutoTune.argtypes = [ctypes.c_void_p, ctypes.c_bool]
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingList.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByID.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByIndex.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        self.lib.PayloadSdkInterface_setGimbalSpeed.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_uint8]
        
        # FFC functions
        self.lib.PayloadSdkInterface_setPayloadCameraFFCTrigg.argtypes = [ctypes.c_void_p]
        self.lib.PayloadSdkInterface_setPayloadCameraFFCMode.argtypes = [ctypes.c_void_p]

        # GPS and system time functions
        self.lib.PayloadSdkInterface_sendPayloadGPSPosition.argtypes = [ctypes.c_void_p, MavlinkGlobalPositionInt]
        self.lib.PayloadSdkInterface_sendPayloadSystemTime.argtypes = [ctypes.c_void_p, MavlinkSystemTime]
        
        # Tracking functions
        self.lib.PayloadSdkInterface_setPayloadObjectTrackingParams.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float]

        # GetNewMessage function
        self.lib.PayloadSdkInterface_getNewMessage.argtypes = [ctypes.c_void_p, ctypes.POINTER(MavlinkMessageT)]
        self.lib.PayloadSdkInterface_getNewMessage.restype = ctypes.c_uint8

    
    # Callback methods
    def regPayloadParamChanged(self, callback: Callable[[int, str, list], None]):
        self._param_callback = PAYLOAD_PARAM_CALLBACK_T(lambda event, param_char, param_double: 
            callback(event, param_char.decode('utf-8'), [param_double[i] for i in range(2)]))
        self.lib.PayloadSdkInterface_regPayloadParamChanged(self.obj, self._param_callback)

    def regPayloadStatusChanged(self, callback: Callable[[int, list], None]):
        self._status_callback = PAYLOAD_STATUS_CALLBACK_T(lambda event, param: 
            callback(event, [param[i] for i in range(3)])) 
        self.lib.PayloadSdkInterface_regPayloadStatusChanged(self.obj, self._status_callback)

    def regPayloadStreamChanged(self, callback: Callable[[int, str, list], None]):
        self._stream_callback = PAYLOAD_STREAMINFO_CALLBACK_T(lambda event, param_char, param_double: 
            callback(event, param_char.decode('utf-8'), [param_double[i] for i in range(3)]))
        self.lib.PayloadSdkInterface_regPayloadStreamChanged(self.obj, self._stream_callback)

    # Core methods
    def sdkInitConnection(self):
        return self.lib.PayloadSdkInterface_sdkInitConnection(self.obj)

    def sdkQuit(self):
        self.lib.PayloadSdkInterface_sdkQuit(self.obj)

    def checkPayloadConnection(self):
        self.lib.PayloadSdkInterface_checkPayloadConnection(self.obj)

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

    def setParamRate(self, pIndex: int, time_ms: int):
        self.lib.PayloadSdkInterface_setParamRate(self.obj, pIndex, time_ms)

    def setCameraZoom(self, zoom_type: float, zoom_value: float):
        self.lib.PayloadSdkInterface_setCameraZoom(self.obj, zoom_type, zoom_value)

    def setCameraFocus(self, focus_type: float, focus_value: float = 0):
        self.lib.PayloadSdkInterface_setCameraFocus(self.obj, focus_type, focus_value)

    # Gimbal methods
    def setPayloadGimbalParamByID(self, param_id: str, value: float):
        self.lib.PayloadSdkInterface_setPayloadGimbalParamByID(self.obj, param_id.encode('utf-8'), value)

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

    def getPayloadGimbalSettingList(self):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingList(self.obj)

    def getPayloadGimbalSettingByID(self, param_id: str):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByID(self.obj, param_id.encode('utf-8'))

    def getPayloadGimbalSettingByIndex(self, idx: int):
        self.lib.PayloadSdkInterface_getPayloadGimbalSettingByIndex(self.obj, idx)

    def setGimbalSpeed(self, spd_pitch: float, spd_roll: float, spd_yaw: float, mode: int):
        self.lib.PayloadSdkInterface_setGimbalSpeed(self.obj, spd_pitch, spd_roll, spd_yaw, mode)

    # FFC methods
    def setPayloadCameraFFCTrigg(self):
        self.lib.PayloadSdkInterface_setPayloadCameraFFCTrigg(self.obj)   

    def setPayloadCameraFFCMode(self, mode: int):
        self.lib.PayloadSdkInterface_setPayloadCameraFFCMode(self.obj, mode)      

    # GPS and system time methods
    def sendPayloadGPSPosition(self, gps: ctypes.Structure):
        self.lib.PayloadSdkInterface_sendPayloadGPSPosition(self.obj, gps)    

    def sendPayloadSystemTime(self, sys_time: ctypes.Structure):
        self.lib.PayloadSdkInterface_sendPayloadSystemTime(self.obj, sys_time)        

    # Tracking method
    def setPayloadObjectTrackingParams(self, cmd: float, pos_x: float = 960, pos_y: float = 540):
        self.lib.PayloadSdkInterface_setPayloadObjectTrackingParams(self.obj, cmd, pos_x, pos_y)

    # Get new message method
    def getNewMessage(self):
        msg = MavlinkMessageT()
        print("receive_messages", f"Size of MavlinkMessageT: {ctypes.sizeof(MavlinkMessageT)}")
        msg_cnt = self.lib.PayloadSdkInterface_getNewMessage(self.obj, ctypes.pointer(msg))
        return msg_cnt, msg
    
    # Payload receive handle method
    def payload_recv_handle(self):
        while not self.time_to_exit:
            time.sleep(0.0001) 

    def __del__(self):
        self.lib.PayloadSdkInterface_delete(self.obj)