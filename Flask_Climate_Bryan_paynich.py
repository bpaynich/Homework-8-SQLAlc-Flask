# University of Arizona Data Bootcamp
# Bryan Paynich
# Flask - Climate Homework
# 02/16/2019

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all measurements
    results = session.query(Measurement.date, Measurement.prcp, Measurement.station).\
    order_by(Measurement.date).all()

    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["station"] = measurement.station
        measurement_dict["prcp"] = measurement.prcp
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).\
    order_by(Station.station).all()

    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["longitude"] = station.longitude
        station_dict["latitude"] = station.latitude
        station_dict["elevation"] = station.elevation
        station_dict["name"] = station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).all()
    all_tobs = []
    for tobs_info in results:
        tobs_dict = {}
        tobs_dict["date"] = tobs_info.date
        tobs_dict["tobs"]  = tobs_info.tobs
        tobs_dict["station"]  = tobs_info.station
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start_date/<start_date>")
def averages(start_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()[0]

    averages_dict = {}
    averages_dict["min"] = results[0]
    averages_dict["max"]  = results[1]
    averages_dict["average"]  = results[2]

    return jsonify(averages_dict)

@app.route("/api/v1.0/<start>/<end>")
def averages_se(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()[0]
    averages_se_dict = {}
    averages_se_dict["min"] = results[0]
    averages_se_dict["max"]  = results[1]
    averages_se_dict["average"]  = results[2]

    return jsonify(averages_se_dict)

if __name__ == '__main__':
    app.run(debug=True)
