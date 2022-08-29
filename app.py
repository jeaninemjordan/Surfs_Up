# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes so they can be referenced later
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database
session = Session(engine)

# Define the Flask app
app = Flask(__name__)

# Create the welcome route
@app.route("/")

#  Create a function welcome() with a return statement
#  Add the precipitation, stations, tobs, and temp routes into the return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create route for precipitation analysis
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function
# Add the line of code that calculates the date one year ago from the most recent date in the database
# Write a query to get the date and precipitation for the previous year
# Use jsonify() to format our results into a JSON structured file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Create route for stations
@app.route("/api/v1.0/stations")

# Create new function called stations()
# Create a query that will allow us to get all of the stations in our database
# Unravel results into a one-dimensional array: use the function np.ravel(), with results as the parameter then convert unraveled results into a list
# Jsonify list
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create route for temperature observations for previous year
@app.route("/api/v1.0/tobs")

# Create new function called temp_monthly()
# Calculate the date one year ago from the last date in the database
# Query the primary station for all the temperature observations from the previous year
# Unravel the results into a one-dimensional array and convert that array into a list
# Jsonify list & jsonify temps list
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create route to report on the minimum, average, and maximum temperatures - provite start and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a function called stats()
# Add start parameter and an end parameter to stats() function
# Create a query to select the minimum, average, and maximum temperatures from the SQLite database, create a list called sel
# Add an if-not statement, unravel results into one-dimensional array, convert into list and jsonify results
# Note: asterisk in query nedy to sel list indicates there are multiple results for query: min, avg, max temps
# Calculate the temperature minimum, average, and maximum with the start and end dates
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

    








