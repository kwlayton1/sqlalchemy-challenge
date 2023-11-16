# Import the dependencies.
from datetime import datetime
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func

# #################################################
# # Database Setup
# #################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("Resources/hawaii.sqlite", echo=False)

# # reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# # # Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# # # Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date here e.g. 2016-08-23<br/>"
        f"/api/v1.0/start date here e.g. 2016-08-23/end date here e.g.2017-01-01<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results from your precipitation 
    analysis (i.e. retrieve only the last 12 months of data)
    to a dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary."""
    
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>='2016-08-23').all()

    return { d:p for d,p in results }



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

# Return a JSON list of stations from the dataset.
    results = session.query(station.station,station.name).all()

    return {id:loc for id,loc in results}


@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for #the previous year of data.
    # Return a JSON list of temperature observations for the previous year.
    
    results = session.query(measurement.date,measurement.tobs).filter((measurement.station=='USC00519281')&(measurement.date>='2016-08-23')).all()

    return {d:t for d,t in results}


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    ### "Return a JSON list of the minimum temperature, the average temperature and the #maximum temperature for a specified start. For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.### 
    
    # Query minimum, average, and maximum temperatures for dates greater than or equal to the start date
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    results = session.query(*sel).filter(measurement.date >= start).all()

    # Close the session
    session.close()

    # Create a dictionary to hold the results
    start_date_temps = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return (start_date_temps)

          
     ###Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range. For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive. ###


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Query minimum, average, and maximum temperatures for the specified date range
    sel = [
        func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)
    ]
    results = session.query(*sel).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).\
        all()

    # Close the session
    session.close()

    # Create a dictionary to hold the results
    start_end_temps = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return (start_end_temps)
