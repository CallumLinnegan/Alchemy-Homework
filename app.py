from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)
app = Flask(__name__)


#precipitation data
sel5 = [measurement.date, measurement.prcp]
new_query = session.query(*sel5).\
    order_by(measurement.date).all()
df2 = pd.DataFrame(new_query,columns=['date','prcp'])
df2.set_index('date',inplace=True)
date_prcp = df2.to_dict()

#stations data
stat = session.query(measurement.station).\
    group_by(measurement.station).all()
df3 = pd.DataFrame(stat)
station_dict = df3.to_dict()

#tobs data
sel6 = [measurement.date, measurement.tobs]
tmps = session.query(*sel6).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date > '2016-08-23').\
    order_by(measurement.date).all()
tmps1 = pd.DataFrame(tmps)
tmps1 = tmps1.set_index('date')
temps = tmps1.to_dict()
temps

@app.route("/")
def home():
    return (
        f"Home Page<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )

@app.route("/api/v1.0/precipitation")
def prcp():
    print("server received prcp page request")
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    print("server has received stations page request")
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    print("server has received tobs page request")
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start():
    print("server has received start page request")


@app.route("/api/v1.0/<start>/<end>")
def startend():
    print("server has received start-end page request")


if __name__=="__main__":
    app.run(debug=True)