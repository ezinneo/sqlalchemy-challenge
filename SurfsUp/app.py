# Import the dependencies.


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################

from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import func

# Create a Flask app
app = Flask(__name__)

# Define the home route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data for the last 12 months<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the last 12 months<br/>"
        f"/api/v1.0/start_date - Temperature statistics from start date to latest data<br/>"
        f"/api/v1.0/start_date/end_date - Temperature statistics between start and end dates<br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the last date in the data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_datetime = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_datetime - dt.timedelta(days=365)
    
    # Query to retrieve the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query to retrieve the list of stations
    station_list = session.query(Station.station).all()
    
    # Convert the results to a list
    stations_data = [station[0] for station in station_list]
    
    return jsonify(stations_data)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year ago from the last date in the data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_datetime = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_datetime - dt.timedelta(days=365)
    
    # Query to retrieve the temperature observations for the most active station in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the results to a list of dictionaries
    temperature_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    
    return jsonify(temperature_data)

# Define the start date route
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Query to calculate temperature statistics for dates greater than or equal to the start date
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # Convert the results to a dictionary
    stats_data = {
        "start_date": start,
        "temperature_min": temperature_stats[0][0],
        "temperature_avg": temperature_stats[0][1],
        "temperature_max": temperature_stats[0][2]
    }
    
    return jsonify(stats_data)

# Define the start and end date route
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    # Query to calculate temperature statistics for dates between start and end dates
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    # Convert the results to a dictionary
    stats_data = {
        "start_date": start,
        "end_date": end,
        "temperature_min": temperature_stats[0][0],
        "temperature
