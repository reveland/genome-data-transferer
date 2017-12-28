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
    with open('ba_pom.json', 'r') as infile:
        ba_pom = json.load(infile)
    newick = json_to_newick(ba_pom)

    data = newick_parser.parse_newick(newick)
    
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def json_to_newick(json, key = lambda d: 'id-' + str(d['id']), scion = lambda d: d['dependencies']):
    """Convert json data to newick tree format"""
    if len(scion(json)) == 0:
        return key(json)
    else:
        return '%s(%s):10.0' % (key(json), ','.join(map(json_to_newick, scion(json))))

if __name__ == '__main__':
    app.run(debug=False)
