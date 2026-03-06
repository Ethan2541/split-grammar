from .shapes import Polygon2D

from anytree import Node
from anytree.exporter import DotExporter
from shapely.ops import unary_union
from typing import List

import matplotlib.pyplot as plt


def save_derivation_tree(tree, title: str = "tree.png") -> None:
    def get_node_attributes(node: Node) -> str:
        attrs = {
            'shape': '"box"' if not node.children else '"ellipse"',
            'fillcolor': '"#b7c3a7"' if not node.children else '"#f6f3ea"',
        }
        return ", ".join([f'{k}={v}' for k, v in attrs.items()])

    options = [
        'graph [dpi=300, nodesep="1.0", ranksep="1.5", splines=ortho]',
        'node [fontname="Helvetica", fontsize=14, margin=0.2, style="filled"]'
    ]
    
    DotExporter(
                tree,
                nodeattrfunc=get_node_attributes,
                edgeattrfunc=lambda node, child: 'dir=none, color="#757575"',
                options=options
               ).to_picture(title)


def draw(shapes: List[Polygon2D], 
         labels_len: int = 3, 
         color: str = "black", 
         fontsize: int = 8,
         title: str = "facade.png"
         ) -> None:
      
    fig, ax = plt.subplots()
    
    for shape in shapes:
        ax.add_patch(shape.get_patch())

        if shape.label is not None:
            center_point = shape.geom.centroid
            center_x, center_y = (center_point.x, center_point.y)
            ax.text(center_x, center_y, shape.label[:labels_len], color=color, fontsize=fontsize, 
                    ha="center", va='center')
    
    total_bounds = unary_union([s.geom for s in shapes]).bounds
    ax.set_xlim(total_bounds[0], total_bounds[2])
    ax.set_ylim(total_bounds[1], total_bounds[3])

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(title)