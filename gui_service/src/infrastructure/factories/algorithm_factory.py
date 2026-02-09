from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.models.algorithm.depth_estimation import DepthEstimation
from src.infrastructure.interfaces.algorithm.ipose_estimation import IPoseEstimation
from src.infrastructure.interfaces.algorithm.itrt_pose_model import ITrtPose
from src.models.algorithm.pose_estimation import PoseEstimation
from src.models.algorithm.trt_pose_model import TrtPose


class AlgorithmFactory: 
    @staticmethod
    def create_trt_pose_model() -> ITrtPose:
        return TrtPose()

    @staticmethod
    def create_pose_estimation(trt_pose_model: ITrtPose) -> IPoseEstimation:
        return PoseEstimation(trt_pose_model)

    @staticmethod
    def create_depth_estimation(pose_estimation_instance: IPoseEstimation) -> IDepthEstimation:
        return DepthEstimation(pose_estimation_instance)

    @staticmethod
    def create_all() -> None:
        trt_pose_model = AlgorithmFactory.create_trt_pose_model()
        pose_estimation = AlgorithmFactory.create_pose_estimation(trt_pose_model)
        depth_estimation = AlgorithmFactory.create_depth_estimation(pose_estimation)
        return trt_pose_model, pose_estimation, depth_estimation
