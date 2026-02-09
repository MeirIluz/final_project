import cv2
from typing import Any
# cv2.startWindowThread()

from src.globals.consts.consts import Consts
from src.infrastructure.interfaces.handlers.ishared_memory_pipeline_handler import ISharedMemoryPipelineHandler
from src.test_modules.debug_print import DEBUG_PRINT


class SharedMemoryPipelineHandler(ISharedMemoryPipelineHandler):
    def __init__(self, camera_name: str) -> None:
        self._camera_name = camera_name
        # self._to_read_pipeline = (
        #     f"shmsrc socket-path=/dev/shm/{self._camera_name}/input ! video/x-raw,"
        #     "format=I420,width=640,height=480,framerate=30/1 ! videoconvert ! appsink"
        # )
        self._test_pipeline = (
            "videotestsrc pattern=ball ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! videoconvert ! appsink"
        )
        # cap = cv2.VideoCapture(self._to_read_pipeline, cv2.CAP_GSTREAMER)
        self._cap = cv2.VideoCapture(self._test_pipeline, cv2.CAP_GSTREAMER)
        if not self._cap.isOpened():
            DEBUG_PRINT("Error: Could not open shared memory video socket.")
            return None

        # self._to_write_pipeline = (
        #     f"appsrc ! videoconvert ! video/x-raw,format=I420,width=640,height=480 "
        #     f"! shmsink socket-path=/dev/shm/{self._camera_name}/output wait-for-connection=false"
        # )
        # self._init_writer()

    def read_frame(self) -> Any:
        ret, frame = self._cap.read()
        # self._cap.release()
        # cv2.imshow("frame", frame)
        return frame if ret else None

    def write_frame(self, frame: Any) -> None:
        if self._writer.isOpened():
            self._writer.write(frame)
        else:
            DEBUG_PRINT("Error: Closed pipeline, cannot write frame.")

    # def _init_writer(self) -> None:
    #     self._writer = cv2.VideoWriter(
    #         self._to_write_pipeline,
    #         cv2.CAP_GSTREAMER,
    #         Consts.video_fourcc,
    #         Consts.video_fps,
    #         Consts.video_frame_size,
    #     )
