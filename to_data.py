from collections import OrderedDict
import itertools

import persister

def sort_g(g):
    g['l'] = g['label'].apply(lambda l: int(l) if l.isdigit() else 1000)
    g = g.sort_values(['l','id'], ascending=[True,True])
    del g['l']
    return g
def get_blocks(ref):
    blocks = []
    for b in ref.iterrows():
        b = b[1]
        blocks.append({"id":b['id'], "referenceChromosomeLabel":str(b['label']), "size":int(b['size'])})
    return blocks
def get_genome(name, genome):
    chs = {}
    for b in genome.itertuples():
        if b.label not in chs.keys():
            chs[b.label] = []
        chs[b.label].append({'id': int(b.id), 'inverted': bool(b.inverted)})
    chs = OrderedDict(sorted(chs.items(), key=lambda l: int(l[0]) if l[0].isdigit() else 1000))
    chs_r = []
    for k in chs.keys():
        chs_r.append({'label':str(k), 'blocks':chs[k]})
    chs_r
    g = {'name': name, 'chromosomes':chs_r}
    return g

def to_data(ref, g1, g2):
    persister.persist(ref, 'fitted', 'ref')
    persister.persist(g1, 'fitted', 'g1')
    persister.persist(g2, 'fitted', 'g2')
    blocks = get_blocks(ref.copy())
    ref_r = get_genome('referenceGenom', ref)
    g1_r = get_genome('genomeName1', g1)
    g2_r = get_genome('genomeName2', g2)
    data = {'blocks': blocks, 'genomes': [ref_r, g1_r, g2_r]}
    return data
