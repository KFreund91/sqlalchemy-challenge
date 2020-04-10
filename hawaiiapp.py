import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///data/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()
#save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#flask setup
app = Flask(__name__)

#time calculations
latestdate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
latestdate = list(np.ravel(latestdate))[0]

latestdate = dt.datetime.strptime(latestdate, '%Y-%m-%d')
latestyear = int(dt.datetime.strftime(latestdate, '%Y'))
latestmonth = int(dt.datetime.strftime(latestdate, '%m'))
latestday = int(dt.datetime.strftime(latestdate, '%d'))

oneyearago = dt.date(latestyear, latestmonth, latestday) - dt.timedelta(days=365)
oneyearago = dt.datetime.strftime(oneyearago, '%Y-%m-%d')

#flask routes

@app.route("/")
def welcome():
    """List all available Hawaii api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > oneyearago)
                      .order_by(Measurement.date)
                      .all())
    
    prcpdata = []
    for result in results:
        prcpdict = {result.date: result.prcp, "Station": result.station}
        prcpdata.append(prcpdict)

    return jsonify(prcpdata)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)