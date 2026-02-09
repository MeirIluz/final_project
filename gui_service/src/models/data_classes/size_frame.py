from dataclasses import dataclass


@dataclass
class SizeFrame:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    width: float
    height: float
