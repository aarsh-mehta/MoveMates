
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
