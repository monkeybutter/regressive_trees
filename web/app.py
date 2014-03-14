# -*- coding: utf-8 -*-
"""
    Flask
    ~~~~~~
    2014 by CSIRO.
"""

from flask import Flask, render_template, Response, send_file, make_response, request
import glob
import pandas
import sys
sys.path.append("../")
from tree import *
from data.data import Data
from util import date_to_angle, time_to_angle
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return make_response(open('templates/index.html').read())
    #return send_file('index.html')

@app.route("/datasets")
def datasets():
    paths = glob.glob("static/data/*.csv")

    return Response(json.dumps([path.split('/')[2][:-4] for path in paths]),  mimetype='application/json')


@app.route("/datasets/<name>")
def dataset(name):

    out = {}

    df = pandas.read_csv("static/data/" + name + ".csv")
    desc = []
    variables = df.columns.values.tolist()
    first = True

    for var in variables:
        elem = {}
        elem["var_name"] = var
        elem["circular"] = False
        if first:
            elem["class_var"] = True
            first = False
        else:
            elem["class_var"] = False
        desc.append(elem)

    out["descriptor"] = desc
    out["rows"] = df.shape[0]
    out["head"] = json.loads(df.head(5).to_json())

    return Response(json.dumps(out),  mimetype='application/json')


@app.route("/datasets/<name>", methods= ['POST'])
def tree(name):
    recv = json.loads(request.data)
    data = recv["variables"]
    min_leaf = recv["min_leaf"]
    var_list = []
    var_types = []
    class_var = None
    for var in data:
        var_list.append(var["var_name"])
        if var["circular"]:
            var_types.append('circular')
        else:
            var_types.append('linear')
        if var["class_var"]:
            class_var = var["var_name"]

    df = pandas.read_csv("static/data/" + name + ".csv")

    var_list = ['date', 'time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']
    var_types = ['date', 'time', 'circular', 'linear', 'linear', 'linear', 'linear']

    df = df[var_list]

    #data = Data(df, class_var, var_types, True)

    #tree = Tree()

    #node = tree.tree_grower(data, min_leaf)
    #print tree.tree_to_dict(node, "O")

    #return Response(tree.tree_to_dict(node, "O"),  mimetype='application/json')
    return Response('{"var_limits": [0.0, 5.0, 5.0, 0.0], "var_name": "windDir", "name": "O", "var_type": "circular", "children": [{"value": "0.48", "name": "OL", "members": 14598}, {"var_limits": ["09:54", "19:18", "19:18", "09:54"], "var_name": "time", "name": "OR", "var_type": "time", "children": [{"var_limits": [5.0, 45.0, 45.0, 0.0], "var_name": "windDir", "name": "ORL", "var_type": "circular", "children": [{"var_limits": ["May 16", "Jan 29", "Jan 29", "May 16"], "var_name": "date", "name": "ORLL", "var_type": "date", "children": [{"value": "9.83", "name": "ORLLL", "members": 2997}, {"value": "8.06", "name": "ORLLR", "members": 1002}]}, {"var_limits": [null, 1010.5, 1010.5, null], "var_name": "pressure", "name": "ORLR", "var_type": "linear", "children": [{"value": "10.02", "name": "ORLRL", "members": 1792}, {"var_limits": [45.0, 205.0, 205.0, 0.0], "var_name": "windDir", "name": "ORLRR", "var_type": "circular", "children": [{"value": "5.88", "name": "ORLRRL", "members": 2139}, {"var_limits": ["Jan 16", "Feb 05", "Feb 05", "Jan 16"], "var_name": "date", "name": "ORLRRR", "var_type": "date", "children": [{"value": "10.11", "name": "ORLRRRL", "members": 322}, {"var_limits": [null, 9.5, 9.5, null], "var_name": "dewPoint", "name": "ORLRRRR", "var_type": "linear", "children": [{"value": "8.11", "name": "ORLRRRRL", "members": 2804}, {"value": "6.86", "name": "ORLRRRRR", "members": 984}]}]}]}]}]}, {"var_limits": [5.0, 125.0, 125.0, 0.0], "var_name": "windDir", "name": "ORR", "var_type": "circular", "children": [{"var_limits": [5.0, 35.0, 35.0, 125.0], "var_name": "windDir", "name": "ORRL", "var_type": "circular", "children": [{"value": "5.68", "name": "ORRLL", "members": 2425}, {"value": "3.50", "name": "ORRLR", "members": 2571}]}, {"var_limits": [null, 1014.5, 1014.5, null], "var_name": "pressure", "name": "ORRR", "var_type": "linear", "children": [{"value": "7.86", "name": "ORRRL", "members": 2958}, {"var_limits": ["Feb 25", "Jan 08", "Jan 08", "Feb 25"], "var_name": "date", "name": "ORRRR", "var_type": "date", "children": [{"value": "4.99", "name": "ORRRRL", "members": 2962}, {"value": "6.50", "name": "ORRRRR", "members": 1420}]}]}]}]}]}',  mimetype='application/json')

if __name__ == "__main__":
    #app.run(host='188.226.143.52',port=80)
    app.run()