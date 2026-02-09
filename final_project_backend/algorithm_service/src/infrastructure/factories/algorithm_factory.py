from src.infrastructure.interfaces.algorithm.imovement_detection import IMovementDetection
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.models.algorithm.movement_detection import MovementDetection
from src.models.handlers.algorithm_handler import AlgorithmHandler


class AlgorithmFactory:
    """Factory for creating algorithm-related components."""

    @staticmethod
    def create_movement_detection(sensitivity: float = 0.5) -> IMovementDetection:
        """
        Create a movement detection algorithm instance.

        Args:
            sensitivity: Detection sensitivity (0.0 to 1.0)

        Returns:
            Movement detection algorithm instance
        """
        return MovementDetection(sensitivity=sensitivity)

    @staticmethod
    def create_algorithm_handler(movement_detection: IMovementDetection) -> IAlgorithmHandler:
        """
        Create an algorithm handler instance.

        Args:
            movement_detection: Movement detection algorithm instance

        Returns:
            Algorithm handler instance
        """
        return AlgorithmHandler(movement_detection)

    @staticmethod
    def create_all(sensitivity: float = 0.5) -> IAlgorithmHandler:
        """
        Create a complete algorithm handler with movement detection.

        Args:
            sensitivity: Detection sensitivity (0.0 to 1.0)

        Returns:
            Configured algorithm handler instance
        """
        movement_detection = AlgorithmFactory.create_movement_detection(
            sensitivity)
        return AlgorithmFactory.create_algorithm_handler(movement_detection)
