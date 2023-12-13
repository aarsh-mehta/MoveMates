
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
    @app.route('/register', methods=["POST"])
def register_user():
    """Register user."""
    email = request.form['email']
    password = request.form['password']

    b = password.encode("utf-8")

    # When registering, this hashes password
    hashed_pw = bcrypt.hashpw(b, bcrypt.gensalt())

    new_user = User(email=email,
                    password=hashed_pw.decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    flash('Registration completed--log in now')
    return redirect('/')


@app.route('/login', methods=["POST"])
def log_user_in():
    """Log the user in."""
    email = request.form['email']
    password = request.form['password']

    user_by_email = User.query.filter(User.email == email).first()

    # If email is not found in db
    if user_by_email is None:
        flash('Oops! You need to register first.')
    # If email is found in db
    elif user_by_email is not None:
        user_id = user_by_email.user_id
        user_password = user_by_email.password

        is_password_match = (bcrypt.checkpw(password.encode("utf-8"),
                                            user_password.encode("utf-8")))

        # Verify password is correct
        if is_password_match is False:
            flash("Incorrect password.")

        elif email == user_by_email.email and is_password_match:
            session['user_id'] = user_id
            flash('Logged in successfully')

    return redirect('/')


@app.route('/add-ride')
def add_trip():
    """Add ride to the rides table."""
    user_id = session.get('user_id')

    if user_id:
        return render_template('add_ride.html', key=googlePlaceKey)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/')


@app.route('/add-ride', methods=["POST"])
def add_trip_process():
    """Add a trip to the database."""
    trip_date = request.form['date']
    trip_time = request.form['time']
    trip_origin = request.form['origin']
    trip_destination = request.form['destination']
    max_passengers = request.form['max_passengers']
    trip_cost = request.form['cost']
    willing_to_stop = request.form['newleg'] in ('True')
    user_id = session.get('user_id')
    '''distance_meters, display_distance = (distance_matrix.distance_matrix(
                                         trip_origin,
                                         trip_destination))
    ''' 
    new_trip = Trip(date_of_trip=trip_date,
                    time=trip_time,
                    max_passengers=max_passengers,
                    origin=trip_origin,
                    destination=trip_destination,
                    willing_to_stop=willing_to_stop,
                    trip_cost=trip_cost,
                    user_id=user_id,
                    distance_meters=5000,
                    display_distance=10,
                    is_active=True)

    db.session.add(new_trip)
    db.session.commit()

    return redirect('/')
