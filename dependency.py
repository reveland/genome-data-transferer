import simplejson as json

with open('data/arp.json', 'r') as infile:
    arp = json.load(infile)

def get_dependent_poms(pom, dept=0):
    pom['dependencies'] = []
    if pom['related_project'] in ['COP/bookingapp', 'COP/bookingchangeapp', 'COP/bookingmanagementapp']:
        return pom
    for rp in arp:
        if pom['related_project'] in map(lambda d: d['related_project'], arp[rp]['dependencies']):
        	if rp not in ['COP/bookingchangeapp', 'COP/bookingmanagementapp']:
        		pom['dependencies'].append(rp)
    pom['dependencies'] = list(map(lambda rp: get_dependent_poms(arp[rp].copy(), dept+1), pom['dependencies']))
    return pom

def remove_hcm(pom):
    if pom['related_project'] == 'PRI/prime-hcommodules-modules':
        pom['dependencies'] = []
    if len(pom['dependencies']) > 0:
        for d in pom['dependencies']:
            remove_hcm(d)

def json_to_newick(json, key=lambda d: 'id-' + str(d['id']), scion=lambda d: d['dependencies']):
    """Convert json data to newick tree format"""
    if len(scion(json)) == 0:
        return key(json)
    else:
        return '%s(%s)' % (key(json), ','.join(map(lambda d: json_to_newick(d, key, scion), scion(json))))