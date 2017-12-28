import json
from pandas.io.json import json_normalize
import requests
from flask import Flask, Response, request
import logging

import merger
import fitter
import to_data
import newick_parser


# LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
# logging.basicConfig(filename='./logs/main.log',
#                    level=logging.INFO,
#                    format=LOG_FORMAT)
# console = logging.StreamHandler()
# # console.setLevel(logging.DEBUG)
# formatter = logging.Formatter(LOG_FORMAT)
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

# logger = logging.getLogger(__name__)

app = Flask(__name__)

baseUrl = 'http://localhost:8080/'

# @app.route('/', methods=['GET'])
# def verify():
#     return "Hello world", 200

# @app.route('/compare', methods=['GET'])
# def compare():
#     headers = {
#         "Content-Type": "application/json"
#     }
#     url = baseUrl + 'getSquares'
#     ref_genome_name = request.args.get('refGenomeName')
#     g1_genome_name = request.args.get('genomeName1')
#     g2_genome_name = request.args.get('genomeName2')
#     logger.info('get genome: %s' % ref_genome_name)
#     ref = json_normalize(json.loads(requests.get(url, params={"genomeName": ref_genome_name}, headers=headers).text))
#     logger.info('received genome: %s with length %d' % (ref_genome_name, len(ref)))
#     logger.info('get genome: %s' % g1_genome_name)
#     g1 = json_normalize(json.loads(requests.get(url, params={"genomeName": g1_genome_name}, headers=headers).text))
#     logger.info('received genome: %s with length %d' % (g1_genome_name, len(g1)))
#     logger.info('get genome: %s' % g2_genome_name)
#     g2 = json_normalize(json.loads(requests.get(url, params={"genomeName": g2_genome_name}, headers=headers).text))
#     logger.info('received genome: %s with length %d' % (g2_genome_name, len(g2)))
#     logger.info('merge genomes')
#     ref_merged, g1_merged, g2_merged = merger.merge_genomes(ref, g1, g2)
#     logger.info('fit genomes')
#     ref_fitter, g1_fitter, g2_fitter = fitter.fit_genomes(ref_merged, g1_merged, g2_merged)
#     logger.info('combinate them')
#     data = to_data.to_data(ref_fitter, g1_fitter, g2_fitter)
#     logger.info('response with data')
#     resp = Response(json.dumps(data))
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route('/tree', methods=['GET'])
# def tree():
#     headers = {
#         "Content-Type": "application/json"
#     }
#     url = baseUrl + 'tree'
#     logger.info('get newick from')
#     newick = requests.get(url, headers=headers).text
#     logger.info('receive newick')
#     data = newick_parser.parse_newick(newick)
#     logger.info('parse newick')
#     resp = Response(json.dumps(data))
#     logger.info('respond')
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

@app.route('/dependency_tree', methods=['GET'])
def dependency_tree():
    related_project = request.args.get('related_project')
    # related_project = 'PRI/prime-hcommodules-modules'
    without_hcm = True

    with open('arp.json', 'r') as infile:
        arp = json.load(infile)
        pom = arp[related_project]

    if(without_hcm):
        remove_hcm(pom)

    newick = json_to_newick(pom, key=lambda d: '#' + str(d['related_project']))

    data = newick_parser.parse_newick(newick)
    
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def json_to_newick(json, key=lambda d: 'id-' + str(d['id']), scion=lambda d: d['dependencies']):
    """Convert json data to newick tree format"""
    if len(scion(json)) == 0:
        return key(json)
    else:
        return '%s(%s)' % (key(json), ','.join(map(lambda d: json_to_newick(d, key, scion), scion(json))))

def remove_hcm(pom):
    if pom['related_project'] == 'PRI/prime-hcommodules-modules':
        pom['dependencies'] = []
    if len(pom['dependencies']) > 0:
        for d in pom['dependencies']:
            remove_hcm(d)

if __name__ == '__main__':
    app.run(debug=False)
