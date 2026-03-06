from src import SplitGrammar
from src import Parser
from src import Rectangle2D
from src import draw_rectangles, save_derivation_tree


SEED = 0

if __name__ == "__main__":
    root = Rectangle2D(0, 0, 10, 10, attrs={"facecolor": "none", "edgecolor": "black", "linewidth": 2})
    bottom, top = root.split(0.5, "H")
    top_left, top_right = top.split(0.5, "V")
    draw_rectangles([bottom, top_right], title="./figures/test_rectangles.png")

    parser = Parser("./knowledge_base", "rules.txt")
    for r in parser.parse_rules():
        print(r)

    grammar = SplitGrammar("./knowledge_base", seed=SEED)
    initial_shape = Rectangle2D(0, 0, 100, 50, label="START", attrs={"alpha": 0.4, "edgecolor": "black", "facecolor": "none", "linewidth": 2})
    derivation_tree = grammar.derivate(initial_shape)

    rects = [leaf.shape for leaf in derivation_tree.leaves]
    draw_rectangles(rects, title="./figures/test_facade.png")

    save_derivation_tree(derivation_tree, title="./figures/test_tree.png")