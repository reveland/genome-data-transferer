import simplejson as json
from flask import Flask, Response, request

import newick_parser
import dependency

app = Flask(__name__)

@app.route('/dependency_tree', methods=['GET'])
def dependency_tree():
    related_project = request.args.get('related_project')
    without_hcm = True if related_project != 'PRI/prime-hcommodules-modules' else False

    with open('data/arp.json', 'r') as infile:
        arp = json.load(infile)
        pom = arp[related_project]

    if(without_hcm):
        dependency.remove_hcm(pom)

    newick = dependency.json_to_newick(pom, key=lambda d: '#' + str(d['related_project']) + '#' + str(d['short_name']))

    data = newick_parser.parse_newick(newick)
    
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/inverz_tree', methods=['GET'])
def inverz_tree():
    related_project = request.args.get('related_project')

    with open('data/arp.json', 'r') as infile:
        arp = json.load(infile)

    pom = arp[related_project]
    pom = dependency.get_dependent_poms(pom.copy())

    newick = dependency.json_to_newick(pom, key=lambda d: '#' + str(d['related_project']) + '#' + str(d['short_name']))

    data = newick_parser.parse_newick(newick)
    
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get_pom', methods=['GET'])
def get_pom():
    related_project = request.args.get('related_project')

    with open('data/arp.json', 'r') as infile:
        arp = json.load(infile)

    pom = arp[related_project]
    pom['dependencies'] = []
    
    resp = Response(json.dumps(pom))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run()
