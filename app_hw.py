import numpy as np 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and precipitation"""
    sel = [Measurement.date, Measurement.prcp]

    prcp_12mo = session.query(*sel).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    results = []
    for x in prcp_12mo:
        prcp_dict = {}
        prcp_dict["date"] = x.date
        prcp_dict["prcp"] = x.prcp
        results.append(prcp_dict)
    
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    sel = [Measurement.date, Measurement.tobs]

    tobs_12mo = session.query(*sel).\
    filter(Measurement.date >='2016-08-23').\
    order_by(Measurement.date).all()

    all_tobs = list(np.ravel(tobs_12mo))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def date_start(start):
    """Fetch tmin, tavg, and tmax for dates >= start date"""
    sel = [Measurement.date, 
    func.min(Measurement.tobs),
    func.avg(Measurement.tobs),
    func.max(Measurement.tobs)]

    tobs_forever = session.query(*sel).\
    filter(Measurement.date >= start).all()

    return jsonify(tobs_forever)


