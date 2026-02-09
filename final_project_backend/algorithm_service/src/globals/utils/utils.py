import os
import time
from typing import Any, Deque, Tuple
from src.globals.consts.consts_strings import ConstsStrings
import warnings


class Utils:

    @staticmethod
    def calculate_fps(frame_times: Deque[float], frame_count: int, start_time: float) -> Tuple[float, float]:
        elapsed_time = time.time() - start_time
        real_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        if len(frame_times) > 1:
            avg_fps = len(
                frame_times) / (frame_times[-1] - frame_times[0]) if len(frame_times) > 1 else real_fps
        else:
            avg_fps = real_fps
        return real_fps, avg_fps

    @staticmethod
    def get_bool_env_var(env_var_name: str) -> bool:
        """
        Reads and validates a boolean-like value from the environment.
        Returns: Python boolean True or False.
        Accepts flexible inputs, but warns on non-standard values.
        """
        raw_value = os.getenv(env_var_name, "")
        value = raw_value.strip().lower()

        true_values = {"true", "1", "yes", "on", "t", "y"}
        false_values = {"false", "0", "no", "off", "f", "n"}

        if value in true_values:
            if value != "true":
                warnings.warn(
                    f"{env_var_name} is set to '{raw_value}', which is accepted but non-standard. "
                    f"Use 'true' or 'false' to avoid confusion."
                )
            return True

        elif value in false_values:
            if value != "false":
                warnings.warn(
                    f"{env_var_name} is set to '{raw_value}', which is accepted but non-standard. "
                    f"Use 'true' or 'false' to avoid confusion."
                )
            return False

        else:
            raise ValueError(
                f"Invalid value for {env_var_name}: '{raw_value}'. "
                f"Expected a boolean-like string such as 'true' or 'false'."
            )
