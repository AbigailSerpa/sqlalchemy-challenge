# Import the dependencies.

# %matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt
import os

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Step 1: Initialize the Flask app
app = Flask(__name__)

#################################################
# Database Setup

# Check if the database file exists
print(os.path.exists("Resources/hawaii.sqlite"))  # Should return True if the file exists

# Create the engine to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes

# Step 2: Define the homepage route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

# Step 3: Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the database
    session = Session(engine)

    # Calculate the date 12 months ago from the most recent date in the database
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query to get the date and precipitation for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Convert the query results to a dictionary (date as the key and prcp as the value)
    precipitation_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Step 4: Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

   