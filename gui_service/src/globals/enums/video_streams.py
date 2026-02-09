from enum import Enum


class VideoStreams(Enum):
    video1 = "rtspsrc location=rtsp://admin:Rd123456@10.0.0.10:554 latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true sync=false"
    video2 = "rtspsrc location=rtsp://admin:Rd123456@10.0.0.20:553 latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true sync=false"
    video3 = "rtspsrc location=rtsp://admin:Rd123456@10.0.0.30:552 latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true sync=false"
    video4 = "v4l2src device=/dev/video3 ! videoconvert ! appsink"
