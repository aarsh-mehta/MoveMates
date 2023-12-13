
import bcrypt
import os
from datetime import datetime, date

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from twilio.rest import Client

from helpers import distance_matrix_filter, distance_matrix
from model import User, Trip, UserTrip, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

googlePlaceKey = os.environ['GOOGLE_PLACES_KEY']
twilioSID = os.environ['TWILIO_SID']
twilioAuthKey = os.environ['TWILIO_AUTH_KEY']
twilioNum = os.environ['TWILIO_NUM']
myNum = os.environ['MY_NUM']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

# Flask Upload
UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.context_processor
def inject_user():
    """Pass in user information."""
    user_id = session.get('user_id')

    user_info = User.query.filter(User.user_id == user_id).first()
    return dict(user_info=user_info)


@app.route('/')
def index():
    """Display Homepage."""
    user_id = session.get('user_id')

    user_info = User.query.filter(User.user_id == user_id).first()

    if user_id:
        return render_template('homepage.html', user_info=user_info)
    else:
        return render_template('index.html')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/trips.json')
def trips():
    """Return trips where user is a driver or passenger."""
    user_id = session.get('user_id')

    if user_id:
        # Query all of the trips where the user is the driver
        trips = Trip.query.filter(Trip.user_id == user_id).all()

        trips_dict_list = []
        trips_by_date = {}

        for trip in trips:
            trip_json = trip.to_json()
            trips_dict_list.append(trip_json)

            passengers = (UserTrip.query.filter(UserTrip.trip_id ==
                                                trip_json["tripId"]).all())
            trip_json["passengers"] = ([passenger.to_json()
                                        for passenger in passengers])

        trips_as_passenger = UserTrip.query.filter(UserTrip.user_id ==
                                                   user_id).all()
        trips_pass_dict = [trip.to_json() for trip in trips_as_passenger]

        for trip in trips_pass_dict:
            trips_by_date[trip['dateOfTrip']] = trip

        for trip in trips_dict_list:
            trips_by_date[trip['dateOfTrip']] = trip

        return jsonify({'trips': trips_dict_list,
                        'tripsAsPassenger': trips_pass_dict,
                        'tripsByDate': trips_by_date})
    else:
        flash("Oops! You need to log in.")
        return jsonify({'status': 'You"re not logged in'})