# Import the dependencies.
# Import necessary libraries
import sqlalchemy
import flask
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
metadata = MetaData()
metadata.reflect(bind=engine)

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB

app = Flask(__name__)
#################################################
# Flask Setup
#################################################

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query dates and temperature observations of the most-active station for the previous year of data
    tobs_data = session.query(measurement.date, measurement.tobs)\
        .filter(and_(measurement.station == most_active_station_id, measurement.date >= one_year_ago, measurement.date <= most_recent_date))\
        .all()

    # Convert the query results to a list of dictionaries
    tobs_list = [{'Date': date, 'Temperature': tobs} for date, tobs in tobs_data]

    # Return the JSON list of temperature observations
    return jsonify(tobs_list)

# Define the start date route
@app.route("/api/v1.0/<start_date>")
def start_date_stats(start_date):
    # Query TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start_date)\
        .all()

    # Convert the query results to a dictionary
    stats_dict = {
        'Min Temperature': stats[0][0],
        'Avg Temperature': stats[0][1],
        'Max Temperature': stats[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(stats_dict)

# Define the start date and end date route
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date_stats(start_date, end_date):
    # Query TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(and_(measurement.date >= start_date, measurement.date <= end_date))\
        .all()

    # Convert the query results to a dictionary
    stats_dict = {
        'Min Temperature': stats[0][0],
        'Avg Temperature': stats[0][1],
        'Max Temperature': stats[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(stats_dict)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)



#################################################
# Flask Routes
#################################################
