import torch
import cv2
import PIL.Image
import numpy as np
from typing import Any
import torchvision.transforms as transforms
from trt_pose.parse_objects import ParseObjects

from src.infrastructure.interfaces.algorithm.itrt_pose_model import ITrtPose
from src.globals.consts.consts import Consts
from src.infrastructure.interfaces.algorithm.ipose_estimation import IPoseEstimation
from src.models.data_classes.size_frame import SizeFrame
from src.test_modules.debug_print import DEBUG_PRINT


class PoseEstimation(IPoseEstimation):
    def __init__(self, trt_model: ITrtPose) -> None:
        try:
            self._engine, self._topology = trt_model.execute()
        except:
            DEBUG_PRINT("Failed To Create Engine And Topology For Pose")
        self._cmap = None
        self._paf = None
        self._counts = None
        self._objects = None
        self._peaks = None
        self._data = None
        # self._parse_objects = None
        self._draw_objects = None
        self._frame = None
        self._frame_copy = None
        self._size_frame = SizeFrame(Consts.model_width_parameter, Consts.model_height_parameter)        
        self._parse_objects = ParseObjects(self._topology)
        self._mean = torch.Tensor([0.485, 0.456, 0.406]).cuda() # Dont put in const !
        self._std = torch.Tensor([0.229, 0.224, 0.225]).cuda() # Dont put in const !

    def get_topology(self) -> np.ndarray:
        return self._topology
 
    def execute(self, frame: np.ndarray) -> tuple:
        self._frame = frame
        self._frame_copy = frame
        self._data = self._preprocess()
        self._process()
        self._post_process()
        return self._counts, self._objects, self._peaks
       
    def _preprocess(self) -> Any:
        resize_frame = cv2.resize(self._frame, (self._size_frame.width, self._size_frame.height))
        color_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
        pil_frame = PIL.Image.fromarray(color_frame)
        tensor_frame = transforms.functional.to_tensor(pil_frame).cuda()
        tensor_frame.sub_(self._mean[:, None, None]).div_(self._std[:, None, None])
        return tensor_frame[None, ...]

    def _process(self) -> None:
        self._cmap, self._paf = self._engine(self._data)
        self._cmap, self._paf = self._cmap.detach().cpu(), self._paf.detach().cpu()

    def _post_process(self) -> None:
        self._counts, self._objects, self._peaks = self._parse_objects(
            self._cmap, self._paf
        )
