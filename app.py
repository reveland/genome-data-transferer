import json
from pandas.io.json import json_normalize
import requests
from flask import Flask, Response

import merger
import fitter
import to_data

app = Flask(__name__)

baseUrl = 'http://localhost:8080/'

@app.route('/', methods=['GET'])
def verify():
    return "Hello world", 200

@app.route('/compare', methods=['GET'])
def compare():
    headers = {
        "Content-Type": "application/json"
    }
    ref = json_normalize(json.loads(requests.get(baseUrl + 'getSquares', params={"genomeName": 'hg1'}, headers=headers).text))
    g1 = json_normalize(json.loads(requests.get(baseUrl + 'getSquares', params={"genomeName": 'mm'}, headers=headers).text))
    g2 = json_normalize(json.loads(requests.get(baseUrl + 'getSquares', params={"genomeName": 'rn'}, headers=headers).text))
    ref_merged, g1_merged, g2_merged = merger.merge_genomes(ref, g1, g2)
    ref_fitter, g1_fitter, g2_fitter = fitter.fit_genomes(ref_merged, g1_merged, g2_merged)
    data = to_data.to_data(ref_fitter, g1_fitter, g2_fitter)

    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
