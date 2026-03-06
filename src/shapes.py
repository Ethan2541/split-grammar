from __future__ import annotations
from shapely.geometry import Polygon, LineString
from shapely.ops import split as shapely_split
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.patches as patches


class Polygon2D:
    def __init__(self, 
                 points: List[Tuple[float, float]], 
                 label: Optional[str] = None, 
                 attrs: Dict[str, Any] = None
                 ) -> None:
        
        self.geom = Polygon(points)
        self.label = label
        self.attrs = attrs or {}


    def split(self, 
              r1: Tuple[float, float], 
              r2: Tuple[float, float], 
              labels: Optional[List[str]] = None,
              attrs: Optional[List[Dict[str, Any]]] = None
              ) -> List['Polygon2D']:
        
        p1, p2 = self.ratios_to_coords(r1, r2)
        cutter = LineString([p1, p2])
        sub_shapes = shapely_split(self.geom, cutter)
        
        children = []
        for i, shape in enumerate(sub_shapes.geoms):
            label = labels[i] if labels and i < len(labels) else None
            points = list(shape.exterior.coords)
            child_attrs = attrs[i] if attrs and i < len(attrs) else self.attrs.copy() 
            children.append(Polygon2D(points, label=label, attrs=child_attrs))
            
        return children
    

    def ratios_to_coords(self, r1: float, r2: float):
        min_x, min_y, max_x, max_y = self.geom.bounds
        width = max_x - min_x
        height = max_y - min_y

        p1 = min_x + r1[0] * width, min_y + r1[1] * height
        p2 = min_x + r2[0] * width, min_y + r2[1] * height

        dx, dy = p2[0] - p1[0], p2[1] - p1[1]

        return (p1[0] - 0.1 * dx, p1[1] - 0.1 * dy), (p2[0] + 0.1 * dx, p2[1] + 0.1 * dy)


    def get_patch(self, **kwargs) -> patches.Polygon:
        vertices = list(self.geom.exterior.coords)
        final_attrs = {**self.attrs, **kwargs}
        return patches.Polygon(vertices, **final_attrs)