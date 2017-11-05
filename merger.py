from collections import OrderedDict

import pandas as pd

def get_possible_merge_points(g):
    prev_id  = g['id'].values[0]
    prev_adjacency = g['adjacency'].values[0]
    prev_label = g['label'].values[0]
    indexes = []
    adjacencies = []
    for i in range(1, len(g)):
        current_id  = g['id'].values[i]
        current_adjacency = g['adjacency'].values[i]
        current_label = g['label'].values[i]
        if (prev_label == current_label) and (prev_adjacency + 1 == current_adjacency):
            indexes.append([prev_id, current_id])
            adjacencies.append([prev_adjacency, current_adjacency])
        prev_id  = current_id
        prev_adjacency = current_adjacency
        prev_label = current_label
    mergeable = pd.DataFrame(data=[indexes, adjacencies]).T.rename(columns={0: 'indexes', 1:'adjacency'})
    mergeable['adjacency'] = mergeable['adjacency'].map(lambda a: str(a[0]) + ',' + str(a[1]))
    return mergeable
def add_sign(b):
    a = b['adjacency']
    if '-'  not in a:
        a = a.split(',')
        a[0] = '-' + a[0]
        a[1] = '-' + a[1]
        a = a[::-1]
        a = ','.join(a)
        b['indexes'] = b['indexes'][::-1]
        b['adjacency'] = a
    return b
def remove_sign(b):
    a = b['adjacency']
    if '-' in a:
        a = a.replace('-', '')
        a = a.split(',')
        a = a[::-1]
        a = ','.join(a)
        b['indexes'] = b['indexes'][::-1]
        b['adjacency'] = a
    return b
def find_overlaps(t_m, o1_m, o2_m, o3_m):
    res = t_m[t_m['adjacency'].isin(o1_m['adjacency']).values]
    res = res[res['adjacency'].isin(o2_m['adjacency']).values]
    res = res[~res['adjacency'].isin(o3_m['adjacency']).values]
    return res
def remove_signs(m_p):
    return m_p.copy().apply(remove_sign, axis=1)
def add_signs(m_p):
    return m_p.copy().apply(add_sign, axis=1)
def merge(g, result, invert=False):
    sizes = OrderedDict(zip(g['id'], g['size']))
    if invert:
        rang = range(len(result))[::-1]
    else:
        rang = range(len(result))
    for i in rang:
        i1  = result['indexes'].values[i][0]
        i2  = result['indexes'].values[i][1]
        sizes[i2] = sizes[i1] + sizes[i2]
    g['size'] = sizes.values()
    if len(result) == 0:
        indexes_to_remove = []
    else:
        indexes_to_remove = list(map(lambda r: r[0], result['indexes']))
    ids_to_remove = [True] * len(g)
    for i_to_r in indexes_to_remove:
        id_to_r = list(sizes.keys()).index(i_to_r)
        ids_to_remove[id_to_r] = False
    g = g[ids_to_remove]
    return g
def filter_out_signed_adjacencies(adjacencies):
    return adjacencies.map(lambda adjacency: adjacency[0] != '-')
def merge_with(args, s_m_p, ref_r, g1_r, g2_r, ref_m_p, g1_m_p, g2_m_p, ref_m_no_sign, g1_m_no_sign, g2_m_no_sign):
    m1 = ref_m_no_sign.copy() if args[0] == '1' else ref_m_p.copy()
    m2 = g1_m_no_sign.copy() if args[1] == '1' else g1_m_p.copy()
    m3 = g2_m_no_sign.copy() if args[2] == '1' else g2_m_p.copy()
    if args == '000':
        m1 = m1[filter_out_signed_adjacencies(m1['adjacency'])]
        m2 = m2[filter_out_signed_adjacencies(m2['adjacency'])]
        m3 = m3[filter_out_signed_adjacencies(m3['adjacency'])]
    if args == '001':
        m1 = m1[filter_out_signed_adjacencies(m1['adjacency'])]
        m2 = m2[filter_out_signed_adjacencies(m2['adjacency'])]
    if args == '010':
        m1 = m1[filter_out_signed_adjacencies(m1['adjacency'])]
    m1_m_p = find_overlaps(m1, m2, m3, s_m_p)
    m2_m_p = find_overlaps(m2, m1, m3, s_m_p)
    m3_m_p = find_overlaps(m3, m1, m2, s_m_p)
    ref_r = merge(ref_r.copy(), m1_m_p, args[0] == '1')
    g1_r = merge(g1_r.copy(), m2_m_p, args[1] == '1')
    g2_r = merge(g2_r.copy(), m3_m_p, args[2] == '1')
    s_m_p = s_m_p.append(remove_signs(m1_m_p.copy()))
    return [s_m_p, ref_r, g1_r, g2_r]

def merge_genomes(ref, g1, g2):
    ref['size'], g1['size'], g2['size'] = 1, 1, 1
    ref['id'], g1['id'], g2['id'] = range(len(ref)), range(len(g1)), range(len(g2))
    ref_m_p = get_possible_merge_points(ref.copy())
    g1_m_p = get_possible_merge_points(g1.copy())
    g2_m_p = get_possible_merge_points(g2.copy())
    ref_m_no_sign = remove_signs(ref_m_p.copy())
    g1_m_no_sign = remove_signs(g1_m_p.copy())
    g2_m_no_sign = remove_signs(g2_m_p.copy())
    steps = [8, 9, 10, 12, 11, 13, 14, 15]
    s_m_p = pd.DataFrame(columns=['indexes', 'adjacency'])
    for step in steps:
        args = str(bin(step))[-3:]
        s_m_p, ref, g1, g2 = merge_with(args, s_m_p, ref, g1, g2, ref_m_p, g1_m_p, g2_m_p, ref_m_no_sign, g1_m_no_sign, g2_m_no_sign)
    return [ref, g1, g2]
