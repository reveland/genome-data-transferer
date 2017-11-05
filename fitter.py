def set_inverted(g):
    g['inverted'] = g['adjacency'] < 0
    g['adjacency'] = abs(g['adjacency'])
    return g
def fit(b, ref):
    b['id'] = int(ref.loc[ref['adjacency'] == b['adjacency'], 'id'])
    return b
def fit_genomes(ref, g1, g2):
    ref['id'] = range(len(ref))
    g1['id'] = range(len(g1))
    g2['id'] = range(len(g2))
    ref = set_inverted(ref.copy())
    g1 = set_inverted(g1.copy())
    g2 = set_inverted(g2.copy())
    ref_fitted = ref.apply(lambda a: fit(a, ref), axis=1)
    g1_fitted = g1.apply(lambda a: fit(a, ref), axis=1)
    g2_fitted = g2.apply(lambda a: fit(a, ref), axis=1)
    return [ref_fitted, g1_fitted, g2_fitted]
