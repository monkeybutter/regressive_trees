# -*- coding: utf-8 -*-
"""
    Flask
    ~~~~~~
    2014 by CSIRO.
"""

from flask import Flask, render_template, Response
import glob
import pandas
import sys
sys.path.append("../")
from tree import *
from data.data import Data

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/datasets")
def datasets():
    paths = glob.glob("static/data/*.csv")

    return Response(json.dumps([path.split('/')[2][:-4] for path in paths]),  mimetype='application/json')


@app.route("/datasets/<name>")
def dataset(name):

    df = pandas.read_csv("static/data/" + name + ".csv")

    desc = {}

    desc["columns"] = df.columns.values.tolist()

    desc["head"] = df.head(10).to_json()

    print type(df.head(10))

    return Response(json.dumps(desc),  mimetype='application/json')


@app.route("/datasets/<name>", methods= ['POST'])
def tree(name):

    df = pandas.read_csv("static/data/weather.csv")

    df = df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]

    class_var = 'windSpeed'
    var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
    df = df.sort([class_var])
    df.index = range(0,len(df))

    data = Data(df, class_var, var_types)

    tree = Tree()
    node = tree.tree_grower(data)

    return Response(tree.tree_to_dict(node, "O"),  mimetype='application/json')

if __name__ == "__main__":
    app.run()