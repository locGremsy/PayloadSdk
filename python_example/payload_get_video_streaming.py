import time
import signal
import sys
import threading
from enum import Enum
from payload_sdk import PayloadSdkInterface, T_ConnInfoStruct, payload_status_event_t, param_type, CONTROL_UDP
from payload_define import *
from mavlink_define import *
import pretty_errors

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Configuration connect
s_conn = T_ConnInfoStruct()
s_conn.type = CONTROL_UDP
s_conn.udp.ip = b"192.168.12.248"
s_conn.udp.port = 14566

my_payload = None
time_to_exit = False
stream_uri = ""
is_rtsp_stream = False
video_thread = None
main_pipeline = None
loop = None

class get_stream_sequence_t(Enum):
    IDLE = 0
    CHECK_CAMERA_INFO = 1
    CHECK_STREAMING_URI = 2
    START_PIPELINE = 3
    PIPELINE_RUNNING = 4

my_job = get_stream_sequence_t.IDLE.value
time_to_view = 10

# Signal handler for quitting
def quit_handler(sig, frame):
    global time_to_exit
    print("\nTERMINATING AT USER REQUEST\n")
    time_to_exit = True

    # Close payload interface
    if my_payload:
        try:
            my_payload.sdkQuit()
            gstreamer_terminate()
        except Exception as e:
            print(f"Error while quitting payload: {e}")

    sys.exit(0)

# Callback function for payload status changes
def onPayloadStatusChanged(event: int, param: list):
    global my_job
    if event == payload_status_event_t.PAYLOAD_CAM_INFO.value:
        if int(param[0]) & CAMERA_CAP_FLAGS.CAMERA_CAP_FLAGS_HAS_VIDEO_STREAM.value:
            print("   ---> Got payload has streaming video, Check streaming URI")
            my_job = get_stream_sequence_t.CHECK_STREAMING_URI.value
        else:
            print("   ---> Payload has no streaming video")
            print("It looks like your video streaming setting was DISABLE Auto Connection")
            print("Please enter the Web server and switch Auto Connection to ENABLE. Then try again.")
            my_job = get_stream_sequence_t.IDLE.value

# Callback function for payload stream changes
def onPayloadStreamChanged(event: int, param_char: str, param_double: list):
    global my_job, stream_uri, is_rtsp_stream
    if event == payload_status_event_t.PAYLOAD_CAM_STREAMINFO.value:
        print("   ---> Got streaming information:")
        print(f"   ---> Streaming type: {param_double[0]:.2f}")
        print(f"   ---> Streaming resolution_v: {param_double[1]:.2f}")
        print(f"   ---> Streaming resolution_h: {param_double[2]:.2f}")
        print(f"   ---> Streaming uri: {param_char}")

        if my_job == get_stream_sequence_t.CHECK_STREAMING_URI.value:
            my_job = get_stream_sequence_t.START_PIPELINE.value
            is_rtsp_stream = (param_double[0] == VIDEO_STREAM_TYPE.VIDEO_STREAM_TYPE_RTSP.value)
            stream_uri = param_char

def run_video_stream():
    global time_to_exit, stream_uri, main_pipeline, loop

    if not is_rtsp_stream or not stream_uri:
        print("No RTSP stream available")
        return

    # Initialize GStreamer
    Gst.init(None)

    # GStreamer pipeline
    gst_pipeline = f"rtspsrc location={stream_uri} latency=0 ! decodebin ! videoconvert ! autovideosink sync=false async=false"
    print(f"Starting GStreamer pipeline: {gst_pipeline}")

    # Create pipeline
    main_pipeline = Gst.parse_launch(gst_pipeline)
    if not main_pipeline:
        print("Failed to create pipeline")
        return

    # Start playing
    main_pipeline.set_state(Gst.State.PLAYING)

    # Create main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except Exception as e:
        print(f"Error in GStreamer loop: {e}")

    # Cleanup when loop exits
    main_pipeline.set_state(Gst.State.NULL)

# Pipeline handle to show video
def gstreamer_start():
    global video_thread
    video_thread = threading.Thread(target=run_video_stream)
    video_thread.daemon = True
    video_thread.start()
    print("GStreamer thread created\n")

# Pipeline handle to stop video
def gstreamer_terminate():
    global time_to_exit, main_pipeline, loop
    print("Exit GStreamer")
    time_to_exit = True
    if loop:
        loop.quit()
    if main_pipeline:
        main_pipeline.set_state(Gst.State.NULL)
    if video_thread and video_thread.is_alive():
        video_thread.join()

def main():
    global my_payload, my_job

    print("Starting GetStreaming example...")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface(s_conn)

    # Init payload
    my_payload.sdkInitConnection()
    print("Waiting for payload signal!")

    # Register callback function
    my_payload.regPayloadStatusChanged(onPayloadStatusChanged)
    my_payload.regPayloadStreamChanged(onPayloadStreamChanged)

    # Check connection
    my_payload.checkPayloadConnection()

    # Set view source
    my_payload.setPayloadCameraParam(
        PAYLOAD_CAMERA_VIEW_SRC,
        Payload_Camera_View_Src.PAYLOAD_CAMERA_VIEW_IREO.value,
        param_type.PARAM_TYPE_UINT32.value
    )
    time.sleep(0.5)

    my_job = get_stream_sequence_t.CHECK_CAMERA_INFO.value

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
            gstreamer_start()
            my_job = get_stream_sequence_t.PIPELINE_RUNNING.value

        elif my_job == get_stream_sequence_t.PIPELINE_RUNNING.value:
            while not time_to_exit:
                time.sleep(1)

        time.sleep(1.5)

if __name__ == "__main__":
    main()