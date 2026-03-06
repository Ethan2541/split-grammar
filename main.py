from src import Parser, Polygon2D, SplitGrammar, draw, save_derivation_tree


SEED = 0

if __name__ == "__main__":
    parser = Parser("./knowledge_base", "rules.txt")
    print(parser.parse_terminals())
    for r in parser.parse_rules():
        print(r)

    grammar = SplitGrammar("./knowledge_base", seed=SEED)
    initial_shape = Polygon2D([(0,0), (0,50), (100,50), (100,0)], 
                              label="START", 
                              attrs={"alpha": 0.4, "edgecolor": "black", "facecolor": "none", "linewidth": 2})
    derivation_tree = grammar.derivate(initial_shape)

    leaves_shapes = [leaf.shape for leaf in derivation_tree.leaves]
    draw(leaves_shapes, title="./figures/test_facade.png")

    save_derivation_tree(derivation_tree, title="./figures/test_tree.png")