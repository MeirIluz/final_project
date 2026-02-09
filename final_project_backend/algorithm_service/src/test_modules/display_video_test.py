import cv2
import numpy as np
from src.globals.consts.consts import Consts


class DisplayVideoTest:
    def __init__(self, window_name: str = "Video Display"):
        self._window_name = window_name
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL)

    def close(self):
        cv2.destroyWindow(self._window_name)

    def concat_and_show_frames(self, posed_frames) -> int:
        frames = []
        for frame in posed_frames:
            if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                resized_frame = cv2.resize(
                    frame,
                    (Consts.ALGO_FRAME_WIDTH,
                     Consts.ALGO_FRAME_HEIGHT),
                )
            else:
                resized_frame = np.zeros(
                    (
                        Consts.ALGO_FRAME_HEIGHT,
                        Consts.ALGO_FRAME_WIDTH,
                        Consts.RGB_NUM_OF_COLORS,
                    ),
                    dtype=np.uint8,
                )
            frames.append(resized_frame)

        if not frames:
            return
        first_shape = frames[0].shape
        first_dtype = frames[0].dtype
        valid_frames = [
            f for f in frames if f.shape == first_shape and f.dtype == first_dtype
        ]

        if valid_frames:
            combined_frame = cv2.hconcat(valid_frames)
        else:
            combined_frame = np.zeros(
                (
                    Consts.ALGO_FRAME_HEIGHT,
                    Consts.ALGO_FRAME_WIDTH * len(frames),
                    Consts.RGB_NUM_OF_COLORS,
                ),
                dtype=np.uint8,
            )

        cv2.imshow(self._window_name, combined_frame)
