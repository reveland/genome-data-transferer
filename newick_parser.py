from Bio import Phylo
from io import StringIO
import json

def parse_newick(newick_str):
    tree = Phylo.read(StringIO(newick_str), 'newick')

    height = 100
    width = 100
    clades = sorted(list(tree.find_clades()), key=lambda c: tree.clade.distance(c), reverse=True)
    max_x = tree.clade.distance(clades[0])
    number_of_leafs = int(len(clades) / 2)
    nodes = {}
    for i, clade in enumerate(clades):
        if len(clade.clades) == 0:
            y = width
            x = height / number_of_leafs * i
            nodes[clade.name] = {'text':clade.name, 'nodeId':i, 'x':x, 'y':y, 'children': []}
        else:
            y = tree.clade.distance(clade) / max_x * width
            children = list(map(lambda c: nodes[c.name], clade.clades))
            x = children[0]['x'] + (children[1]['x'] - children[0]['x']) / 2
            nodes[clade.name] = {'text':clade.name, 'nodeId':i, 'x':x, 'y':y, 'children': children}
    return nodes['vert0']