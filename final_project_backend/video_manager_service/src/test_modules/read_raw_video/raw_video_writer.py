from datetime import datetime
import cv2
import logging
import time
import os
import signal
import sys

from src.globals.consts.logger_messages import LoggerMessages
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.consts.consts_strings import ConstsStrings

class RTSPStreamProcessor:
    def __init__(self, camera_ip, camera_port, output_dir="./videos"):
        self._camera_ip = camera_ip
        self._camera_port = camera_port
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)
        self.rtsp_url = f"rtsp://admin:Rd123456@{self._camera_ip}:{self._camera_port}"
        self.capture = cv2.VideoCapture(self.rtsp_url)
        self._video_fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        self._logger = LoggerFactory.get_logger_manager()
        if not self.capture.isOpened():
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.RTSP_STREAM_NOT_OPEN, level=logging.ERROR) 
            exit()
        self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.frame_width == 0 or self.frame_height == 0:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.INVALID_FRAME_SIZE, level=logging.ERROR) 
            exit()
        self._video_frame_size = (self.frame_width, self.frame_height)
        self._init_writer()
        self.running = True

        # Handle Ctrl+C or SIGTERM gracefully
        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

    def _handle_exit(self, signum, frame):
        self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.EXIT_GRACEFULLY, level=logging.DEBUG) 

        self.running = False

    def start(self):
        self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.START_RTSP_STREAM_CAPTURE, level=logging.DEBUG) 
        while self.running:
            ret, frame = self.capture.read()
            if not ret:

                self._logger.log(ConstsStrings.LOG_NAME_WARNING,
                             LoggerMessages.FAIL_TO_GRAB_FRAME, level=logging.WARNING) 
                break

            if self.out.isOpened():
                self.out.write(frame)
            else:
                self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.VIDEO_WRITER_NOT_OPEN, level=logging.ERROR) 

            # Optional: Display live preview
            # cv2.imshow("RTSP Stream", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # Release resources
        self.capture.release()
        if self.out:
            self.out.release()
        # cv2.destroyAllWindows()
        self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.PIPELINE_STOP_AND_OUTPUT_SAVE, level=logging.DEBUG) 

    def _init_writer(self) -> None:
        self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.INITIALIZE_VIDEO_WRITER, level=logging.DEBUG) 
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(self._output_dir, f"output_{timestamp}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(
            output_file,
            fourcc,
            self._video_fps,
            self._video_frame_size,
        )

if __name__ == "__main__":
    camera_ip = "192.168.1.60"  
    camera_port = "556" 

    processor = RTSPStreamProcessor(camera_ip, camera_port, output_dir="/app/videos")
    processor.start()
