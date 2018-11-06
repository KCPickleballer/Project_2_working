import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
Base1 = declarative_base()

from sqlalchemy import Column, Integer, String, Float


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

City_data = Base.classes.CITY_DATA1
Cities = Base.classes.city_names
#Venue_data = Base.classes.venue_data2
Venue_data = Base.classes.city_venue

# class Venue_data(Base1):
#   __tablename__ = "city_venue"
#   id = Column(Integer, primary_key=True)
#   venue = Column(String)
#   city = Column(String)
#   address = Column(String)
#   state = Column(String)
#   zipcode = Column(String)
#   latitude = Column(Float)
#   longitude = Column(Float)
#   url = Column(String)





#session = Session(db.engine)


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of city names."""
   # print('in names')
    # Use Pandas to perform the sql query
    stmt = db.session.query(Cities).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    #print(df)

    data = {
        "city": df.city_name.tolist()
    }
    
    return jsonify(data)




@app.route("/cities/<city>")
def city(city):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    #     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()
    print('B4 Query')
    stmt = db.session.query(City_data).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    
    city_data = df.loc[df["City"] == city, ["eventname", "Date", "Classification", "Latitude", "Longitude", "City", "venue"]]
    
    city_data["frmtdDate"] = city_data["Date"]

#print('test' , city_data)
    
        
    city_data = city_data.loc[city_data["Date"] < "2019-01-31", ["eventname", "Date", "Classification", "Latitude", "Longitude", "City", "venue"]]
    
        #print ('city2', city_data)
    # Format the data to send as json
    data = {
        "eventname": city_data.eventname.values.tolist(),
        "Date": city_data.Date.tolist(),
        "Classification": city_data.Classification.tolist(),
        "Latitude": city_data.Latitude.values.tolist(),
        "Longitude": city_data.Longitude.values.tolist(),
        "City_name": city_data.City.tolist(),
        "Venue":     city_data.venue.tolist()
        #,        "frmtdDate":  city_data.frmtdDate.tolist()
    }
    #print(data)
    return jsonify(data)


@app.route("/chart/<city>")
def chart(city):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
   
    results = db.session.query(func.count(City_data.Classification), City_data.Classification, City_data.dte_wk).group_by(City_data.dte_wk, City_data.Classification  ).filter(City_data.City== city).filter(City_data.Date < '2019-02-01').all()

    event_cnt = []
    classification = []
    mnthWk = []

    for result in results:
        event_cnt.append(result[0])
        classification.append(result[1])
        mnthWk.append(result[2])

        #print ('city2', city_data)
    # Format the data to send as json
    data = {
        "EventCnt": event_cnt,
        "Classification": classification,       
        "Week":  mnthWk
    }
   # print(data)
    return jsonify(data)

@app.route("/venue/<city>")
def venue(city):
    
    results = db.session.query(func.count(Venue_data.venue), Venue_data.venue, Venue_data.city).group_by(Venue_data.venue, Venue_data.city  ).filter(Venue_data.city== city).all()

    venue_cnt = []
    venue = []
    city = []

    for result in results:
        venue_cnt.append(result[0])
        venue.append(result[1])
        city.append(result[2])

        #print ('city2', city_data)
    # Format the data to send as json
    data = {
        "venue": venue
    }


    
    return jsonify(data)

@app.route("/venueinfo/<venue>")
def venueinfo(venue):

    
    stmt = db.session.query(Venue_data).filter(Venue_data.venue == venue).statement
    df = pd.read_sql_query(stmt, db.session.bind)



    data = {
        "venue": df.venue.tolist(),
        "city":  df.city.tolist(),
        "address": df.address.tolist(),
        "zipcode": df.zipcode.tolist(),
        "latitude": df.latitude.values.tolist(),
        "longitude": df.longitude.values.tolist(),
        "url":     df.url.tolist()
    }
    #print(data)

    return jsonify(data)
   


if __name__ == "__main__":
    app.run()
