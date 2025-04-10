import time
import signal
import sys
import threading
from enum import Enum
import os
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs_python.payload_sdk import PayloadSdkInterface, payload_status_event_t, param_type
from libs_python.payload_define import *
from libs_python.mavlink_define import *

my_payload = None
time_to_exit = False
stream_uri = ""
is_rtsp_stream = False
video_thread = None

class get_stream_sequence_t(Enum):
    IDLE = 0
    CHECK_CAMERA_INFO = 1
    CHECK_STREAMING_URI = 2
    START_PIPELINE = 3
    PIPELINE_RUNNING = 4

my_job = get_stream_sequence_t.CHECK_CAMERA_INFO.value

def quit_handler(sig, frame):
    global time_to_exit
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
    if event == payload_status_event_t.PAYLOAD_CAM_INFO.value:
        if int(param[0]) & CAMERA_CAP_FLAGS.CAMERA_CAP_FLAGS_HAS_VIDEO_STREAM.value:
            print("   ---> Got payload has streaming video, Check streaming URI")
            my_job = get_stream_sequence_t.CHECK_STREAMING_URI.value
        else:
            print("   ---> Payload has no streaming video")
            my_job = get_stream_sequence_t.IDLE.value

def onPayloadStreamChanged(event: int, param_char: str, param_double: list):
    global my_job, stream_uri, is_rtsp_stream
    if event == payload_status_event_t.PAYLOAD_CAM_STREAMINFO.value:
        print("   ---> Got streaming information:")
        print(f"   ---> Streaming type: {param_double[0]:.2f}")
        print(f"   ---> Streaming uri: {param_char}")
        if my_job == get_stream_sequence_t.CHECK_STREAMING_URI.value:
            my_job = get_stream_sequence_t.START_PIPELINE.value
            is_rtsp_stream = (param_double[0] == VIDEO_STREAM_TYPE.VIDEO_STREAM_TYPE_RTSP.value)
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
    global my_payload, my_job
    print("Starting GetStreaming example...")
    signal.signal(signal.SIGINT, quit_handler)

    my_payload = PayloadSdkInterface()
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)
    my_payload.regPayloadStreamChanged(onPayloadStreamChanged)
    my_payload.checkPayloadConnection()
    my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_VIEW_SRC, Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_IREO.value, param_type.PARAM_TYPE_UINT32.value)
    time.sleep(0.5)

    while not time_to_exit:
        if my_job == get_stream_sequence_t.IDLE.value:
            print("Program exit.")
            try:
                my_payload.sdkQuit()
            except Exception as e:
                print(f"Error while quitting payload: {e}")
            sys.exit(0)
        elif my_job == get_stream_sequence_t.CHECK_CAMERA_INFO.value:
            print("Send request to read camera's information")
            my_payload.getPayloadCameraInformation()
        elif my_job == get_stream_sequence_t.CHECK_STREAMING_URI.value:
            my_payload.getPayloadCameraStreamingInformation()
        elif my_job == get_stream_sequence_t.START_PIPELINE.value:
            opencv_start()
            my_job = get_stream_sequence_t.PIPELINE_RUNNING.value
        elif my_job == get_stream_sequence_t.PIPELINE_RUNNING.value:
            while not time_to_exit:
                time.sleep(1)
        time.sleep(1.5)

if __name__ == "__main__":
    main()