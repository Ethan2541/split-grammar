from .shapes import Rectangle2D

from anytree import RenderTree
from anytree.exporter import DotExporter
from typing import List

import matplotlib.pyplot as plt


def save_derivation_tree(tree, title="tree.png"):
    DotExporter(tree).to_picture(title)


def draw_rectangles(
    rectangles: List[Rectangle2D], 
    labels_len: int = 3, 
    color: str = "black", 
    fontsize: int = 8,
    title: str = "rectangular_facade.png"
) -> None:
    
    fig, ax = plt.subplots()
    
    for rectangle in rectangles:
        ax.add_patch(rectangle.get_patch())

        if rectangle.label is not None:
            center_x, center_y = (rectangle.x + rectangle.width/2), (rectangle.y + rectangle.height/2)
            ax.text(center_x, center_y, rectangle.label[:labels_len], color=color, fontsize=fontsize, 
                    ha="center", va='center')
    
    ax.set_xlim(0, max(rectangle.x + rectangle.width for rectangle in rectangles))
    ax.set_ylim(0, max(rectangle.y + rectangle.height for rectangle in rectangles))

    plt.tight_layout()
    plt.savefig(title)