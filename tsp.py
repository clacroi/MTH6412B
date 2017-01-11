# coding: utf-8

from flask import Flask, render_template, make_response, request
from flask_googlemaps import Map, GoogleMaps
import json

from tsp_config import api_key
from my_tsp import get_visit_order
from tsp_helper import GeoPoint

app = Flask(__name__, template_folder="templates")

# you can set key as config
GoogleMaps(app, key=api_key)


@app.route('/')
def fullmap():
    """Display main web page."""
    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:80%;"
            "width:100%;"
            "bottom:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=45.5017,
        lng=-73.5673,
        zoom=12,
        markers=[],
    )
    return render_template('example_fullmap.html', fullmap=fullmap)


@app.route('/get_order', methods=['GET', 'POST'])
def get_order():
    """Return the order of visit of nodes.

    Node informations are in lats[] and lngs[] arrays of the GET request.
    """
    lats = map(float, json.loads(request.args.get('lats')))
    lngs = map(float, json.loads(request.args.get('lngs')))
    nMarks = len(lats)
    geoPoints = [GeoPoint(lats[i], lngs[i]) for i in range(nMarks)]
    order = get_visit_order(geoPoints)
    resp = make_response(json.dumps(order))
    resp.headers['Content-Type'] = "application/json"
    return resp


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
