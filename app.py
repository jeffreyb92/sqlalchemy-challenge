import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/< start > and /api/v1.0/< start >/< end >"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_dates = []
    for date, prcp in results:
        station_dict = {}
        station_dict[date] = prcp
        all_dates.append(station_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station names"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for name, station in results:
        stations_dict = {}
        stations_dict["name"] = name
        stations_dict["station"] = station
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures from the last year"""
    # Query all temperatures
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-17', Measurement.station == 'USC00519281')


    session.close()

# Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for date, temp in results:
        temps_dict = {}
        temps_dict["date"] = date
        temps_dict["tobs"] = temp
        all_temps.append(temps_dict)

    return jsonify(all_temps)   


if __name__ == '__main__':
    app.run(debug=True)

@app.route("api/v1.0/<int:start>")
def start_date(start):

     # Create our session (link) from Python to the DB
    session = Session(engine)

    start_string= str(start)
    start_num = str(start_string[:4]) + "-"  + str(start_string[4:6]) + "-" + str(start_string[6:])

    """Return a list of temperatures from the last year"""
    # Query all temperatures from start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_num).all()

    session.close()


    # Create a dictionary from the row data and append to a list of start_temps
    start_temps = []
    for mini, avg, maxi in results:
        temps_dict = {}
        temps_dict["min"] = mini
        temps_dict["avg"] = avg
        temps_dict["max"] = maxi
        start_temps.append(temps_dict)

    return jsonify(start_temps)

@app.route("api/v1.0/<int:start>/<int:end>")
def startend(start, end):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    start_string= str(start)
    start_date = str(start_string[:4]) + "-"  + str(start_string[4:6]) + "-" + str(start_string[6:])

    end_string= str(end)
    end_date = str(end_string[:4]) + "-"  + str(end_string[4:6]) + "-" + str(end_string[6:])

    """Return a list of temperatures from the last year"""
    # Query all temperatures from start to end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of end_temps
    end_temps = []
    for mini, avg, maxi in results:
        temps_dict = {}
        temps_dict["min"] = mini
        temps_dict["avg"] = avg
        temps_dict["max"] = maxi
        end_temps.append(temps_dict)

    return jsonify(end_temps)