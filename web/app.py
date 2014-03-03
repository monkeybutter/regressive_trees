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
    data =  json.loads(request.data)
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

    df = df[var_list]

    df = df.sort([class_var])
    df.index = range(0,len(df))

    data = Data(df, class_var, var_types)

    tree = Tree()

    node = tree.tree_grower(data)

    return Response(tree.tree_to_dict(node, "O"),  mimetype='application/json')

if __name__ == "__main__":
    app.run()