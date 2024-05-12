from typing import Any
from typing import Dict
from typing import List
from typing import Union

from constants import FONT
from constants import NATIVE_SURF
from constants import pg


class DebugDraw:
    def __init__(self):
        self.layers: List[List[Any]] = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]

    def add(self, obj: Dict[str, Union[int, str]]):
        layer = obj["layer"]
        self.layers[layer].append(obj)

    def draw(self):
        for layer in self.layers:
            for obj in layer:
                if obj["type"] == "text":
                    FONT.render_to(
                        NATIVE_SURF,
                        (obj["x"], obj["y"]),
                        obj["text"],
                        "white",
                        "black",
                    )

                elif obj["type"] == "rect":
                    pg.draw.rect(
                        NATIVE_SURF,
                        obj["color"],
                        obj["rect"],
                        obj["width"],
                    )

                elif obj["type"] == "line":
                    pg.draw.line(
                        NATIVE_SURF,
                        obj["color"],
                        obj["start"],
                        obj["end"],
                        obj["width"],
                    )

                elif obj["type"] == "circle":
                    pg.draw.circle(
                        NATIVE_SURF,
                        obj["color"],
                        obj["center"],
                        obj["radius"],
                    )

                elif obj["type"] == "surf":
                    NATIVE_SURF.blit(
                        obj["surf"],
                        (obj["x"], obj["y"]),
                    )

        self.layers = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]