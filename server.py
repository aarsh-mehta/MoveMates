
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