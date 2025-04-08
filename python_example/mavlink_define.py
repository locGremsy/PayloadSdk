from enum import Enum
import ctypes

# MAVLink message structures
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
        ("msgid", ctypes.c_uint8 * 3), 
        ("payload64", ctypes.c_uint64 * 33),
        ("ck", ctypes.c_uint8 * 2),
        ("signature", ctypes.c_uint8 * 13),
    ]

# MAVLink global position structure
class MavlinkGlobalPositionInt(ctypes.Structure):
    _fields_ = [
        ("time_boot_ms", ctypes.c_uint32), 
        ("lat", ctypes.c_int32),           
        ("lon", ctypes.c_int32),           
        ("alt", ctypes.c_int32),           
        ("relative_alt", ctypes.c_int32),  
        ("vx", ctypes.c_int16),           
        ("vy", ctypes.c_int16),            
        ("vz", ctypes.c_int16),           
        ("hdg", ctypes.c_uint16),     
    ]   

# MAVLink system time structure
class MavlinkSystemTime(ctypes.Structure):
    _fields_ = [
        ("time_unix_usec", ctypes.c_uint64),  
        ("time_boot_ms", ctypes.c_uint32),  
    ]

class CAMERA_ZOOM_TYPE(Enum):
   ZOOM_TYPE_STEP            =                                             0 
   ZOOM_TYPE_CONTINUOUS      =                                             1 
   ZOOM_TYPE_RANGE           =                                             2 
   ZOOM_TYPE_FOCAL_LENGTH    =                                             3
   ZOOM_TYPE_HORIZONTAL_FOV  =                                             4 
   CAMERA_ZOOM_TYPE_ENUM_END =                                             5

class CAMERA_MODE(Enum):
   CAMERA_MODE_IMAGE        =                                              0
   CAMERA_MODE_VIDEO        =                                              1
   CAMERA_MODE_IMAGE_SURVEY =                                              2
   CAMERA_MODE_ENUM_END     =                                              3

class CAMERA_CAP_FLAGS(Enum):
   CAMERA_CAP_FLAGS_CAPTURE_VIDEO                   =                      1
   CAMERA_CAP_FLAGS_CAPTURE_IMAGE                   =                      2
   CAMERA_CAP_FLAGS_HAS_MODES                       =                      4
   CAMERA_CAP_FLAGS_CAN_CAPTURE_IMAGE_IN_VIDEO_MODE =                      8
   CAMERA_CAP_FLAGS_CAN_CAPTURE_VIDEO_IN_IMAGE_MODE =                      16
   CAMERA_CAP_FLAGS_HAS_IMAGE_SURVEY_MODE           =                      32
   CAMERA_CAP_FLAGS_HAS_BASIC_ZOOM                  =                      64
   CAMERA_CAP_FLAGS_HAS_BASIC_FOCUS                 =                      128
   CAMERA_CAP_FLAGS_HAS_VIDEO_STREAM                =                      256
   CAMERA_CAP_FLAGS_HAS_TRACKING_POINT              =                      512
   CAMERA_CAP_FLAGS_HAS_TRACKING_RECTANGLE          =                      1024
   CAMERA_CAP_FLAGS_HAS_TRACKING_GEO_STATUS         =                      2048
   CAMERA_CAP_FLAGS_HAS_THERMAL_RANGE               =                      4096
   CAMERA_CAP_FLAGS_ENUM_END                        =                      4097

class VIDEO_STREAM_TYPE(Enum):
   VIDEO_STREAM_TYPE_RTSP     =                                            0
   VIDEO_STREAM_TYPE_RTPUDP   =                                            1
   VIDEO_STREAM_TYPE_TCP_MPEG =                                            2
   VIDEO_STREAM_TYPE_MPEG_TS  =                                            3
   VIDEO_STREAM_TYPE_ENUM_END =                                            4 