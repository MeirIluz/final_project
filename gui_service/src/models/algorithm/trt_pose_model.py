import json
import trt_pose.coco
import trt_pose.models
import torch
import torch2trt
from torch2trt import TRTModule

from src.infrastructure.interfaces.algorithm.itrt_pose_model import ITrtPose
from src.globals.consts.consts import Consts
from src.globals.consts.consts_strings import ConstsStrings
from src.models.data_classes.size_frame import SizeFrame
from src.test_modules.debug_print import DEBUG_PRINT


class TrtPose(ITrtPose):
    def __init__(self) -> None:
        with open(ConstsStrings.topology_pose_path, ConstsStrings.open_to_read) as f: human_pose = json.load(f)
        self._model = None
        self._model_trt = None
        self._num_parts = len(human_pose[ConstsStrings.keypoints_key])
        self._num_links = len(human_pose[ConstsStrings.skeleton_key])
        self._optimized_model = ConstsStrings.optimzied_model_path
        self._size_frame = SizeFrame(Consts.model_width_parameter, Consts.model_height_parameter)
        self._topology = trt_pose.coco.coco_category_to_topology(human_pose) 
        
    def execute(self) -> tuple:
        self._load_model()
        engine = self._provide_trt_model()
        return engine, self._topology

    def _prepare_resnet_model(self) -> None:
        # TODO: check this function why the model in line num 30 not in used
        try:
            model_weights = ConstsStrings.model_weights
            self._model = (trt_pose.models.resnet18_baseline_att(self._num_parts, 2 * self._num_links).cuda().eval())
            self._model.load_state_dict(torch.load(model_weights))
        except:
            DEBUG_PRINT("Could not Load Weights")

    def _load_model(self) -> None:
        # TODO: check this function why the model_trt in line num 38 not in used
        try:
            self._model_trt = TRTModule()
            self._model_trt.load_state_dict(torch.load(self._optimized_model))
        except FileNotFoundError:
            self._creating_the_model()

    def _creating_the_model(self) -> None:
        try:
            self._prepare_resnet_model()
            data = torch.zeros((1, 3, self._size_frame.height, self._size_frame.width)).cuda()
            self._model_trt = torch2trt.torch2trt(
                self._model, [data], fp16_mode=True, max_workspace_size=1 << 25
            )
            torch.save(self._model_trt.state_dict(), self._optimized_model)
        except:
            DEBUG_PRINT("Couldnt Create the Model")

    def _provide_trt_model(self) -> None:
        return self._model_trt

