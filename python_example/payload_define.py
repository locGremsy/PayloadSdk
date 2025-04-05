from enum import Enum

PAYLOAD_CAMERA_TRACKING_MODE =                                          "TRACK_MODE"
class Payload_Camera_Tracking_Mode(Enum):
    PAYLOAD_CAMERA_TRACKING_OBJ_TRACKING  =                             0
    PAYLOAD_CAMERA_TRACKING_OBJ_DETECTION =                             1

PAYLOAD_CAMERA_VIDEO_OSD_MODE =                                         "OSD_MODE"
class Payload_Camera_Osd_Mode(Enum):
    PAYLOAD_CAMERA_VIDEO_OSD_MODE_DISABLE =                             0
    PAYLOAD_CAMERA_VIDEO_OSD_MODE_DEBUG   =                             1
    PAYLOAD_CAMERA_VIDEO_OSD_MODE_STATUS  =                             2

PAYLOAD_CAMERA_RC_MODE =                                                "RC_MODE"
class Payload_Camera_Rc_Mode(Enum):
    PAYLOAD_CAMERA_RC_MODE_GREMSY   =                                   0
    PAYLOAD_CAMERA_RC_MODE_STANDARD =                                   1

PAYLOAD_CAMERA_VIDEO_FLIP =                                             "C_V_FLIP"
class Payload_Camera_Video_Flip(Enum):
    PAYLOAD_CAMERA_VIDEO_FLIP_OFF =                                     3
    PAYLOAD_CAMERA_VIDEO_FLIP_ON  =                                     2

PAYLOAD_CAMERA_VIDEO_DEFOG =                                            "C_V_DEFOG"
class Payload_Camera_Video_Defog(Enum):
    PAYLOAD_CAMERA_VIDEO_DEFOG_OFF =                                    0
    PAYLOAD_CAMERA_VIDEO_DEFOG_ON  =                                    1

PAYLOAD_CAMERA_VIDEO_DEFOG_LEVEL =                                      "C_V_DEFOG_LV"
class Payload_Camera_Video_Defog_Level(Enum):
    PAYLOAD_CAMERA_VIDEO_DEFOG_LOWEST =                                 0
    PAYLOAD_CAMERA_VIDEO_DEFOG_LOW    =                                 1
    PAYLOAD_CAMERA_VIDEO_DEFOG_MID    =                                 2
    PAYLOAD_CAMERA_VIDEO_DEFOG_HIGH   =                                 3

PAYLOAD_CAMERA_VIDEO_AUTO_EXPOSURE =                                    "C_V_AE"
class Payload_Camera_Video_Auto_Exposure(Enum):
    PAYLOAD_CAMERA_VIDEO_EXPOSURE_AUTO    =                             0
    PAYLOAD_CAMERA_VIDEO_EXPOSURE_MANUAL  =                             3
    PAYLOAD_CAMERA_VIDEO_EXPOSURE_SHUTTER =                             10
    PAYLOAD_CAMERA_VIDEO_EXPOSURE_IRIS    =                             11
    PAYLOAD_CAMERA_VIDEO_EXPOSURE_BRIGHT  =                             13

PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED =                                    "C_V_SP"
class Payload_Camera_Video_Shutter_Speed(Enum):
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_10   =                         13
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_20   =                         14
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_50   =                         17
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_100  =                         20
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_125  =                         21
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_500  =                         25
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_725  =                         26
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_1000 =                         27
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_1500 =                         28
    PAYLOAD_CAMERA_VIDEO_SHUTTER_SPEED_1_2000 =                         30

# Aperture value can be set from 0 to 25, step 1
PAYLOAD_CAMERA_VIDEO_APERTURE_VALUE =                                   "C_V_IrP"

# Bright value can be set from 0 to 41, step 1a
PAYLOAD_CAMERA_VIDEO_BRIGHT_VALUE =                                     "C_V_BrP"

PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE =                                    "C_V_WB"
class Payload_Camera_Video_White_Balance(Enum):
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_AUTO     =                       0
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_INDOOR   =                       1
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_OUTDOOR  =                       2
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_ONE_PUSH =                       3
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_ATW      =                       4
    PAYLOAD_CAMERA_VIDEO_WHITE_BALANCE_MANUAL   =                       5

PAYLOAD_CAMERA_VIDEO_ZOOM_MODE =                                        "C_V_ZM_MODE"
class Payload_Camera_Video_Zoom_Mode(Enum):
    PAYLOAD_CAMERA_VIDEO_ZOOM_MODE_COMBINE          =                   0
    PAYLOAD_CAMERA_VIDEO_ZOOM_MODE_SUPER_RESOLUTION =                   2

# Zoom super resolution value can be set from 1x to 30x
PAYLOAD_CAMERA_VIDEO_ZOOM_SUPER_RESOLUTION_FACTOR =                     "C_V_ZM_SR_LV"
class Payload_Camera_Video_Zoom_Super_Resolution_Factor(Enum):
    ZOOM_SUPER_RESOLUTION_1X  =                                         0
    ZOOM_SUPER_RESOLUTION_2X  =                                         1
    ZOOM_SUPER_RESOLUTION_4X  =                                         2
    ZOOM_SUPER_RESOLUTION_6X  =                                         3
    ZOOM_SUPER_RESOLUTION_8X  =                                         4
    ZOOM_SUPER_RESOLUTION_10X =                                         5
    ZOOM_SUPER_RESOLUTION_12X =                                         6
    ZOOM_SUPER_RESOLUTION_14X =                                         7
    ZOOM_SUPER_RESOLUTION_16X =                                         8
    ZOOM_SUPER_RESOLUTION_18X =                                         9
    ZOOM_SUPER_RESOLUTION_20X =                                         10
    ZOOM_SUPER_RESOLUTION_22X =                                         11
    ZOOM_SUPER_RESOLUTION_24X =                                         12
    ZOOM_SUPER_RESOLUTION_26X =                                         13
    ZOOM_SUPER_RESOLUTION_28X =                                         14
    ZOOM_SUPER_RESOLUTION_30X =                                         15

# Zoom super resolution value can be set from 1x to 240x
PAYLOAD_CAMERA_VIDEO_ZOOM_COMBINE_FACTOR =                              "C_V_ZM_CB_LV"
class Payload_Camera_Video_Zoom_Combine_Factor(Enum):
    ZOOM_COMBINE_1X   =                                                 0
    ZOOM_COMBINE_10X  =                                                 1
    ZOOM_COMBINE_20X  =                                                 2
    ZOOM_COMBINE_40X  =                                                 3
    ZOOM_COMBINE_80X  =                                                 4
    ZOOM_COMBINE_120X =                                                 5
    ZOOM_COMBINE_240X =                                                 6

PAYLOAD_CAMERA_VIDEO_FOCUS_MODE =                                       "C_V_FM"
class Payload_Camera_Video_Focus_Mode(Enum):
    PAYLOAD_CAMERA_VIDEO_FOCUS_MODE_MANUAL       =                      0
    PAYLOAD_CAMERA_VIDEO_FOCUS_MODE_ZOOM_TRIGGER =                      1
    PAYLOAD_CAMERA_VIDEO_FOCUS_MODE_AUTO_NEAR    =                      2
    PAYLOAD_CAMERA_VIDEO_FOCUS_MODE_AUTO_FAR     =                      3

# Manual focus value can be set from 0 to 61440, step 10
PAYLOAD_CAMERA_VIDEO_FOCUS_VALUE =                                      "C_V_FV"

PAYLOAD_CAMERA_GIMBAL_MODE =                                            "GB_MODE"
class Payload_Camera_Gimbal_Mode(Enum):
    PAYLOAD_CAMERA_GIMBAL_MODE_OFF     =                                0
    PAYLOAD_CAMERA_GIMBAL_MODE_LOCK    =                                1
    PAYLOAD_CAMERA_GIMBAL_MODE_FOLLOW  =                                2
    PAYLOAD_CAMERA_GIMBAL_MODE_MAPPING =                                3
    PAYLOAD_CAMERA_GIMBAL_MODE_RESET   =                                4

PAYLOAD_CAMERA_VIEW_SRC =                                               "C_SOURCE"
class Payload_Camera_View_Src(Enum):
    PAYLOAD_CAMERA_VIEW_EOIR         =                                  0
    PAYLOAD_CAMERA_VIEW_EO           =                                  1
    PAYLOAD_CAMERA_VIEW_IR           =                                  2
    PAYLOAD_CAMERA_VIEW_IREO         =                                  3
    PAYLOAD_CAMERA_VIEW_SYNC         =                                  4
    PAYLOAD_CAMERA_VIEW_SIDE_BY_SIDE =                                  6

PAYLOAD_CAMERA_RECORD_SRC =                                             "C_V_REC"
class Payload_Camera_Record_Src(Enum):
    PAYLOAD_CAMERA_RECORD_BOTH =                                        0
    PAYLOAD_CAMERA_RECORD_EO   =                                        1
    PAYLOAD_CAMERA_RECORD_IR   =                                        2
    PAYLOAD_CAMERA_RECORD_OSD  =                                        5

PAYLOAD_CAMERA_IR_PALETTE =                                             "C_T_PALETTE"
class Payload_Camera_Ir_Palette(Enum):
    PAYLOAD_CAMERA_IR_PALETTE_1  =                                      0     #      F1: WhiteHot         |       G1: WhiteHot
    PAYLOAD_CAMERA_IR_PALETTE_2  =                                      1     #      F1: BlackHot         |       G1: Fulgurite
    PAYLOAD_CAMERA_IR_PALETTE_3  =                                      2     #      F1: Rainbow          |       G1: IronRed
    PAYLOAD_CAMERA_IR_PALETTE_4  =                                      3     #      F1: RainbowHC        |       G1: HotIron
    PAYLOAD_CAMERA_IR_PALETTE_5  =                                      4     #      F1: Ironbow          |       G1: Medical
    PAYLOAD_CAMERA_IR_PALETTE_6  =                                      5     #      F1: Lava             |       G1: Arctic
    PAYLOAD_CAMERA_IR_PALETTE_7  =                                      6     #      F1: Arctic           |       G1: Rainbow1
    PAYLOAD_CAMERA_IR_PALETTE_8  =                                      7     #      F1: Globow           |       G1: Rainbow2
    PAYLOAD_CAMERA_IR_PALETTE_9  =                                      8     #      F1: Gradedfire       |       G1: Tint
    PAYLOAD_CAMERA_IR_PALETTE_10 =                                      9     #      F1: Hottest          |       G1: BlackHot

PAYLOAD_CAMERA_IR_ZOOM_FACTOR =                                         "C_T_ZOOM"
class Payload_Camera_Ir_Zoom_Factor(Enum):
    ZOOM_IR_1X =                                                        0
    ZOOM_IR_2X =                                                        1
    ZOOM_IR_3X =                                                        2
    ZOOM_IR_4X =                                                        3
    ZOOM_IR_5X =                                                        4
    ZOOM_IR_6X =                                                        5
    ZOOM_IR_7X =                                                        6
    ZOOM_IR_8X =                                                        7

class Camera_Zoom_Value(Enum):
    ZOOM_OUT  =                                                         -1
    ZOOM_STOP =                                                         0 
    ZOOM_IN   =                                                         1

class Camera_Focus_Value(Enum):
    FOCUS_OUT  =                                                        -1
    FOCUS_STOP =                                                        0
    FOCUS_IN   =                                                        1
    FOCUS_AUTO =                                                        2

PAYLOAD_CAMERA_VIDEO_ZOOM_FACTOR =                                      "C_V_ZOOM"
class Payload_Camera_Video_Zoom_Factor(Enum):
    ZOOM_EO_1X  =                                                       0
    ZOOM_EO_2X  =                                                       1
    ZOOM_EO_3X  =                                                       2
    ZOOM_EO_4X  =                                                       3
    ZOOM_EO_5X  =                                                       4
    ZOOM_EO_6X  =                                                       5
    ZOOM_EO_7X  =                                                       6
    ZOOM_EO_8X  =                                                       7
    ZOOM_EO_9X  =                                                       8
    ZOOM_EO_10X =                                                       9
    ZOOM_EO_11X =                                                       10
    ZOOM_EO_12X =                                                       11

PAYLOAD_CAMERA_STORAGE =                                                "STORAGE"
class Payload_Camera_Storage(Enum):
    PAYLOAD_CAMERA_STORAGE_INTERNAL =                                   0
    PAYLOAD_CAMERA_STORAGE_SDCARD   =                                   1

PAYLOAD_CAMERA_OBJECT_DETECTION =                                       "DETECTION_EN"
class Payload_Camera_Object_Detection(Enum):
    PAYLOAD_CAMERA_OBJECT_DETECTION_DISABLE =                           0                                        
    PAYLOAD_CAMERA_OBJECT_DETECTION_ENABLE  =                           1                                          

PAYLOAD_CAMERA_IR_ISOTHERMS =                                           "ISOTHERMS_EN"
class Payload_Camera_Ir_Isotherms(Enum):
    PAYLOAD_CAMERA_IR_ISOTHERMS_DISABLE =                               0                                        
    PAYLOAD_CAMERA_IR_ISOTHERMS_ENABLE  =                               1      

PAYLOAD_CAMERA_IR_ISOTHERMS_GAIN =                                      "ISOTHERMS_GAIN"
class Payload_Camera_Ir_Isotherms_Gain(Enum):
    PAYLOAD_CAMERA_IR_ISOTHERMS_HIGH_GAIN =                             0                                        
    PAYLOAD_CAMERA_IR_ISOTHERMS_LOW_GAIN  =                             1   