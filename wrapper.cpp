#include "payloadSdkInterface.h"

/**
 * Callback function typedefs for payload parameter, status, and stream information changes
 **/
typedef void (*payload_param_callback_t)(int event, char *param_char, double *param);
typedef void (*payload_status_callback_t)(int event, double *param);
typedef void (*payload_streamInfo_callback_t)(int event, char *param_char, double *param);

extern "C" void PayloadSdkInterface_regPayloadParamChanged(void *obj, payload_param_callback_t callback)
{
    auto cb = [callback](int event, char *param_char, double *param)
    {
        callback(event, param_char, param);
    };
    ((PayloadSdkInterface *)obj)->regPayloadParamChanged(cb);
}

extern "C" void PayloadSdkInterface_regPayloadStatusChanged(void *obj, payload_status_callback_t callback)
{
    auto cb = [callback](int event, double *param)
    {
        callback(event, param);
    };
    ((PayloadSdkInterface *)obj)->regPayloadStatusChanged(cb);
}

extern "C" void PayloadSdkInterface_regPayloadStreamChanged(void *obj, payload_streamInfo_callback_t callback)
{
    auto cb = [callback](int event, char *param_char, double *param)
    {
        callback(event, param_char, param);
    };
    ((PayloadSdkInterface *)obj)->regPayloadStreamChanged(cb);
}

/**
 * Create a new instance of PayloadSdkInterface
 **/
extern "C" void *PayloadSdkInterface_new(T_ConnInfo conn)
{
    return new PayloadSdkInterface(conn);
}

extern "C" void *PayloadSdkInterface_new_default()
{
    return new PayloadSdkInterface();
}

/**
 * Delete an instance of PayloadSdkInterface
 **/
extern "C" void PayloadSdkInterface_delete(void *obj)
{
    delete (PayloadSdkInterface *)obj;
}

/**
 * Init connection to payload
 **/
extern "C" int PayloadSdkInterface_sdkInitConnection(void *obj)
{
    return ((PayloadSdkInterface *)obj)->sdkInitConnection();
}

/**
 * Interface terminator
 **/
extern "C" void PayloadSdkInterface_sdkQuit(void *obj)
{
    ((PayloadSdkInterface *)obj)->sdkQuit();
}

/**
 * Check Payload connection
 **/
extern "C" void PayloadSdkInterface_checkPayloadConnection(void *obj)
{
    ((PayloadSdkInterface *)obj)->checkPayloadConnection();
}

/**
 * Check new message 
 **/
extern "C" uint8_t PayloadSdkInterface_getNewMessage(void *obj, mavlink_message_t *msg)
{
    uint8_t cnt = ((PayloadSdkInterface *)obj)->getNewMewssage(*msg);
    SDK_LOG("getNewMessage: sizeof(mavlink_message_t)=%zu", sizeof(mavlink_message_t));
    SDK_LOG("getNewMessage: cnt=%d, msgid=%d, sysid=%d, compid=%d, raw=[%02x %02x %02x %02x %02x %02x %02x %02x %02x %02x]",
            cnt, msg->msgid, msg->sysid, msg->compid,
            ((uint8_t *)msg)[0], ((uint8_t *)msg)[1], ((uint8_t *)msg)[2], ((uint8_t *)msg)[3],
            ((uint8_t *)msg)[4], ((uint8_t *)msg)[5], ((uint8_t *)msg)[6], ((uint8_t *)msg)[7],
            ((uint8_t *)msg)[8], ((uint8_t *)msg)[9]);
    return cnt;
}

/**
 * Set payload's camera parameter
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraParam(void *obj, const char *param_id, uint32_t param_value, uint8_t param_type)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraParam((char *)param_id, param_value, param_type);
}

/**
 * Get all payload's settings
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraSettingList(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraSettingList();
}

/**
 * Get payload's setting by id
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraSettingByID(void *obj, const char *param_id)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraSettingByID((char *)param_id);
}

/**
 * Get payload's setting by index
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraSettingByIndex(void *obj, uint8_t idx)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraSettingByIndex(idx);
}

/**
 * Get payload's storage volume
 **/
extern "C" void PayloadSdkInterface_getPayloadStorage(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadStorage();
}

/**
 * Get payload's capture status
 **/
extern "C" void PayloadSdkInterface_getPayloadCaptureStatus(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadCaptureStatus();
}

/**
 * Get payload's camera mode
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraMode(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraMode();
}

/**
 * Get payload's camera information
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraInformation(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraInformation();
}

/**
 * Get payload's camera streaming information
 **/
extern "C" void PayloadSdkInterface_getPayloadCameraStreamingInformation(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadCameraStreamingInformation();
}

/**
 * Get payload's gimbal param
 **/
extern "C" void PayloadSdkInterface_setPayloadGimbalParamByID(void *obj, const char *param_id, float value)
{
    ((PayloadSdkInterface *)obj)->setPayloadGimbalParamByID((char *)param_id, value);
}

/**
 * Send command to trigger gimbal gyro calibration
 **/
extern "C" void PayloadSdkInterface_sendPayloadGimbalCalibGyro(void *obj)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGimbalCalibGyro();
}

/**
 * Send command to trigger gimbal accel calibration
 **/
extern "C" void PayloadSdkInterface_sendPayloadGimbalCalibAccel(void *obj)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGimbalCalibAccel();
}

/**
 * Send command to trigger gimbal motor calibration
 **/
extern "C" void PayloadSdkInterface_sendPayloadGimbalCalibMotor(void *obj)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGimbalCalibMotor();
}

/**
 * Send command to trigger gimbal search home
 **/
extern "C" void PayloadSdkInterface_sendPayloadGimbalSearchHome(void *obj)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGimbalSearchHome();
}

/**
 * Send command to trigger gimbal auto tune
 **/
extern "C" void PayloadSdkInterface_sendPayloadGimbalAutoTune(void *obj, bool status)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGimbalAutoTune(status);
}

/**
 * Get all gimbal's settings
 **/
extern "C" void PayloadSdkInterface_getPayloadGimbalSettingList(void *obj)
{
    ((PayloadSdkInterface *)obj)->getPayloadGimbalSettingList();
}

/**
 * Get specific gimbal param by id string
 **/
extern "C" void PayloadSdkInterface_getPayloadGimbalSettingByID(void *obj, const char *param_id)
{
    ((PayloadSdkInterface *)obj)->getPayloadGimbalSettingByID((char *)param_id);
}

/**
 * Get specific gimbal param by index
 **/
extern "C" void PayloadSdkInterface_getPayloadGimbalSettingByIndex(void *obj, uint8_t idx)
{
    ((PayloadSdkInterface *)obj)->getPayloadGimbalSettingByIndex(idx);
}

/**
 * Set payload's camera mode
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraMode(void *obj, uint8_t mode)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraMode((CAMERA_MODE)mode);
}

/**
 * Set payload's camera capture image
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraCaptureImage(void *obj, int param)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraCaptureImage(param);
}

/**
 * Set payload's camera stop image
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraStopImage(void *obj)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraStopImage();
}

/**
 * Set payload's camera start record video
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraRecordVideoStart(void *obj)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraRecordVideoStart();
}

/**
 * Set payload's camera stop record video
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraRecordVideoStop(void *obj)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraRecordVideoStop();
}

/**
 * Set IR FFC mode
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraFFCMode(void *obj, uint8_t mode)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraFFCMode(ffc_mode_t(mode));
}

/**
 * Set IR FFC trigger
 **/
extern "C" void PayloadSdkInterface_setPayloadCameraFFCTrigg(void *obj)
{
    ((PayloadSdkInterface *)obj)->setPayloadCameraFFCTrigg();
}

/**
 * Set param rate
 **/
extern "C" void PayloadSdkInterface_setParamRate(void *obj, uint8_t pIndex, uint16_t time_ms)
{
    ((PayloadSdkInterface *)obj)->setParamRate(pIndex, time_ms);
}

/*!<@brief: used to rotate gimbal for each axis depend on angular rate or angle mode
 * @para1,2,3 : value for each axis
 * @para4 : Angular rate or angle mode
 * */
extern "C" void PayloadSdkInterface_setGimbalSpeed(void *obj, float spd_pitch, float spd_roll, float spd_yaw, uint8_t mode)
{
    ((PayloadSdkInterface *)obj)->setGimbalSpeed(spd_pitch, spd_roll, spd_yaw, (input_mode_t)mode);
}

/**
 * set camera zoom ZOOM_TYPE_CONTINUOUS
 * (ZOOM_OUT, ZOOM_STOP, ZOOM_IN)
 * */
extern "C" void PayloadSdkInterface_setCameraZoom(void *obj, float zoomType, float zoomValue)
{
    ((PayloadSdkInterface *)obj)->setCameraZoom(zoomType, zoomValue);
}

/**
 * set camera focus
 * (FOCUS_OUT, FOCUS_STOP, FOCUS_IN)
 * */
extern "C" void PayloadSdkInterface_setCameraFocus(void *obj, float focusType, float focusValue)
{
    ((PayloadSdkInterface *)obj)->setCameraFocus(focusType, focusValue);
}

/**
 * send bounding box position for object tracking feature
 **/
extern "C" void PayloadSdkInterface_setPayloadObjectTrackingParams(void *obj, float cmd, float pos_x, float pos_y)
{
    ((PayloadSdkInterface *)obj)->setPayloadObjectTrackingParams(cmd, pos_x, pos_y);
}

/**
 * Send the GPS information to the payload
 **/
extern "C" void PayloadSdkInterface_sendPayloadGPSPosition(void *obj, mavlink_global_position_int_t gps)
{
    ((PayloadSdkInterface *)obj)->sendPayloadGPSPosition(mavlink_global_position_int_t(gps));
}

/**
 * Send the Sytem Time to the payload
 **/
extern "C" void PayloadSdkInterface_sendPayloadSystemTime(void *obj, mavlink_system_time_t sys_time)
{
    ((PayloadSdkInterface *)obj)->sendPayloadSystemTime(mavlink_system_time_t(sys_time));
}