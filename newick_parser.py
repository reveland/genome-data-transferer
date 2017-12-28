from Bio import Phylo
from io import StringIO
import json


def get_number_of_leafs(c):
    return 1 if len(c.clades) == 0 else sum(map(get_number_of_leafs, c.clades))

def add_clade(clade, y, neighbors_leafs_left):
    global nodes
    
    nof = get_number_of_leafs(clade)
    x = neighbors_leafs_left + (nof - 1) / 2
    x*=5

    i=0
    name = clade.name
    while(clade.name in nodes):
        clade.name = ('' if i == 0 else str(i)) + name
        i+=1
    nodes[clade.name] = {'text':clade.name, 'x':x, 'y':y }

    leafs_left = neighbors_leafs_left

    shift_size = 7
    shifts = 0
    for c in clade.clades:
        add_clade(c, y + 10, leafs_left)
        nol = get_number_of_leafs(c)
        leafs_left += nol
        if nol < 4:
            y += shift_size
            shifts += 1
        if shifts > 10:
            y -= shifts * shift_size
            shifts = 0

def parse_newick(newick_str):
    global nodes
    
    nodes = {}
    # newick_str = 'a(b(c,d,e,f,c,t,y,u,s,d),g(h,j))'
    tree = Phylo.read(StringIO(newick_str), 'newick')
    add_clade(tree.clade, 0, 0)

    clades = list(tree.find_clades())
    for i, clade in enumerate(clades):
        children = list(map(lambda c: nodes[c.name], clade.clades))
        nodes[clade.name]['children'] = children

    return nodes[tree.clade.name]


# print(parse_newick('a(b(d:10,e),c)'))
# print(parse_newick('a(b(d:10,e),c)'))

# tree = Phylo.read(StringIO('a(b(d:10,e:10):10,c:10):10'), 'newick')
# print(get_number_of_leafs(tree.clade))

