import time
import signal
import sys
import threading
from enum import Enum
import os
import cv2

from libs.payload_sdk import PayloadSdkInterface, payload_status_event_t, param_type, get_stream_sequence_t
from libs.payload_define import *
from libs.mavlink_define import *

my_payload = None
time_to_exit = False
stream_uri = ""
is_rtsp_stream = False
video_thread = None

my_job = get_stream_sequence_t.CHECK_CAMERA_INFO

def quit_handler(sig, frame):
    global my_payload, time_to_exit
    print("\nTERMINATING AT USER REQUEST\n")
    time_to_exit = True
    if my_payload:
        try:
            my_payload.sdkQuit()
            opencv_terminate()
        except Exception as e:
            print(f"Error while quitting payload: {e}")
    sys.exit(0)

def onPayloadStatusChanged(event: int, param: list):
    global my_job
    if payload_status_event_t(event) == payload_status_event_t.PAYLOAD_CAM_INFO:
        if int(param[0]) & int(camera_cap_flags.CAMERA_CAP_FLAGS_HAS_VIDEO_STREAM):
            print("   ---> Got payload has streaming video, Check streaming URI")
            my_job = get_stream_sequence_t.CHECK_STREAMING_URI
        else:
            print("   ---> Payload has no streaming video")
            my_job = get_stream_sequence_t.IDLE

def onPayloadStreamChanged(event: int, param_char: str, param_double: list):
    global my_job, stream_uri, is_rtsp_stream
    if payload_status_event_t(event) == payload_status_event_t.PAYLOAD_CAM_STREAMINFO:
        print("   ---> Got streaming information:")
        print(f"   ---> Streaming type: {param_double[0]:.2f}")
        print(f"   ---> Streaming uri: {param_char}")
        if my_job == get_stream_sequence_t.CHECK_STREAMING_URI:
            my_job = get_stream_sequence_t.START_PIPELINE
            is_rtsp_stream = (video_stream_type(param_double[0]) == video_stream_type.VIDEO_STREAM_TYPE_RTSP)
            stream_uri = param_char

def run_video_stream():
    global time_to_exit, stream_uri
    if not is_rtsp_stream or not stream_uri:
        print("No RTSP stream available")
        return

    cap = cv2.VideoCapture(stream_uri, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Could not open RTSP stream")
        return

    print(f"Starting OpenCV stream: {stream_uri}")
    while not time_to_exit:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        cv2.imshow("RTSP Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

def opencv_start():
    global video_thread
    video_thread = threading.Thread(target=run_video_stream)
    video_thread.daemon = True
    video_thread.start()
    print("OpenCV thread created\n")

def opencv_terminate():
    global time_to_exit, video_thread
    print("Exit OpenCV")
    time_to_exit = True
    if video_thread and video_thread.is_alive():
        video_thread.join()

def main():
    global my_payload, my_job, time_to_exit
    print("Starting GetStreaming example...")
    signal.signal(signal.SIGINT, quit_handler)

    my_payload = PayloadSdkInterface()
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)
    my_payload.regPayloadStreamChanged(onPayloadStreamChanged)
    my_payload.checkPayloadConnection()
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, payload_camera_view_src.PAYLOAD_CAMERA_VIEW_IREO, param_type.PARAM_TYPE_UINT32)
    time.sleep(0.5)

    while not time_to_exit:
        if my_job == get_stream_sequence_t.IDLE:
            print("Program exit.")
            try:
                my_payload.sdkQuit()
            except Exception as e:
                print(f"Error while quitting payload: {e}")
            sys.exit(0)
        elif my_job == get_stream_sequence_t.CHECK_CAMERA_INFO:
            print("Send request to read camera's information")
            my_payload.getPayloadCameraInformation()
        elif my_job == get_stream_sequence_t.CHECK_STREAMING_URI:
            my_payload.getPayloadCameraStreamingInformation()
        elif my_job == get_stream_sequence_t.START_PIPELINE:
            opencv_start()
            my_job = get_stream_sequence_t.PIPELINE_RUNNING
        elif my_job == get_stream_sequence_t.PIPELINE_RUNNING:
            while not time_to_exit:
                time.sleep(1)
        time.sleep(1.5)

if __name__ == "__main__":
    main()