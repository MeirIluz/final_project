from dataclasses import dataclass


@dataclass
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    x: float
    y: float
