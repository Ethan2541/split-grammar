from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt


class Rectangle2D(object):
    def __init__(
        self, 
        x: float, 
        y: float, 
        width: float, 
        height: float, 
        label: Optional[str] = None, 
        attrs: Dict[str, Any] = None
    ) -> None:
        
        self.label = label

        self.x, self.y = x, y
        self.width, self.height = width, height

        self.attrs = attrs

    
    def split(
        self, 
        position: float, 
        axis: str, 
        labels: List[Optional[str]] = None, 
        attrs: List[Optional[Dict[str, Any]]] = None
    ) -> Tuple[Rectangle2D, Rectangle2D]:

        labels = labels or [None]*2
        attrs = attrs or [self.attrs.copy() for _ in range(2)]  # Keep parent attributes if unspecified

        if axis == "H":
            boundary_point = position * self.height
            bottom_rectangle = Rectangle2D(self.x, self.y, self.width, boundary_point, 
                                           label=labels[0], attrs=attrs[0])
            top_rectangle = Rectangle2D(self.x, self.y + boundary_point, self.width, self.height - boundary_point, 
                                        label=labels[1], attrs=attrs[1])
            return (bottom_rectangle, top_rectangle)
        
        elif axis == "V":
            boundary_point = position * self.width
            left_rectangle = Rectangle2D(self.x, self.y, boundary_point, self.height, 
                                         label=labels[0], attrs=attrs[0])
            right_rectangle = Rectangle2D(self.x + boundary_point, self.y, self.width - boundary_point, self.height, 
                                          label=labels[1], attrs=attrs[1])
            return (left_rectangle, right_rectangle)

    
    def get_patch(self) -> patches.Rectangle:
        return patches.Rectangle((self.x, self.y), self.width, self.height, **self.attrs)