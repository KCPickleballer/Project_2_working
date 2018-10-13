import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/TM_DATA.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
#Samples_Metadata = Base.classes.sample_metadata

City_data = Base.classes.CITY_DATA
Cities = Base.classes.city_names


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of city names."""
    print('in names')
    # Use Pandas to perform the sql query
    stmt = db.session.query(Cities).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    #print(df)

    data = {
        "city": df.city_name.tolist()
    }
    
    #print('data', data)
    # Return a list of cities 
    return jsonify(data)


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata) 


@app.route("/cities/<city>")
def city(city):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    #     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    stmt = db.session.query(City_data).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    print ('in cities', city)
    # Filter the data based on the sample number and
    # only keep rows with values above 1
    city_data = df.loc[df["City"] == city, ["eventname", "Date", "Classification", "Latitude", "Longitude", "City", "venue"]]
    print ('city2', city_data)
    # Format the data to send as json
    data = {
        "eventname": city_data.eventname.values.tolist(),
        "Date": city_data.Date.tolist(),
        "Classification": city_data.Classification.tolist(),
        "Latitude": city_data.Latitude.values.tolist(),
        "Longitude": city_data.Longitude.values.tolist(),
        "City_name": city_data.City.tolist(),
        "Venue":     city_data.venue.tolist()
    }
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
