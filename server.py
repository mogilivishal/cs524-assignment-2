import os
import geopandas as gpd
from shapely.geometry import Polygon
from flask import Flask, request, send_from_directory, safe_join, jsonify
import numpy as np
import json

app = Flask(__name__, static_folder=os.path.abspath('../vis/app/'))
geo_network = None
gdf_network = None

#Applying the route
@app.route('/', methods=['GET'])
def index():
    return serve_static('index.html')
#Applying the root path
@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory(safe_join(app.root_path, 'vis/dist/shadow-maps/'), filename)
#Calling the newtwork using the GET Method
@app.route('/network', methods=['GET'])
def serve_network():
    return geo_network
#Data Processing for Winter summer spring/fall using post method
@app.route('/distribution', methods=['POST'])
def serve_distribution():
    data = request.get_json()
    data = data['dataToCompute']
    Winter = []
    Summer = []
    Fall = []
    Winter = list(data[1])
    Winter.sort()
    Summer = list(data[0])
    Summer.sort()
    Fall = list(data[2])
    Fall.sort()
    ans = [
         {
            "key": 'Winter',
            "q1": np.quantile(Winter, 0.25),
            "median": np.median(Winter),
            "q3":  np.quantile(Winter, 0.75),
            "interQuantileRange":  np.quantile(Winter, 0.75) - np.quantile(Winter, 0.25),
            "min": min(Winter),
            "max": max(Winter),
            "std": np.std(Winter)
        },
        {
            "key": 'Summer',
            "q1": np.quantile(Summer, 0.25),
            "median": np.median(Summer),
            "q3": np.quantile(Summer, 0.75),
            "interQuantileRange": np.quantile(Summer, 0.75) - np.quantile(Summer, 0.25),
            "min": min(Summer),
            "max": max(Summer),
            "std": np.std(Summer)
        },
        {
            "key": 'Fall',
            "q1": np.quantile(Fall, 0.25),
            "median": np.median(Fall),
            "q3": np.quantile(Fall, 0.75),
            "interQuantileRange": np.quantile(Fall, 0.75) - np.quantile(Fall, 0.25),
            "min": min(Fall),
            "max": max(Fall),
            "std": np.std(Fall)
        }]

    return jsonify({'res': ans})
#Loadind the given dataset
def load():
    global gdf_network
    global geo_network
    gdf_network = gpd.read_file('./chicago-street-shadow.geojson')
    geo_network = gdf_network.to_json()


if __name__ == '__main__':
    load()
    app.run(debug=True, host='127.0.0.1', port=8080)