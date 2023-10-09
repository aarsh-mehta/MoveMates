"""Utility file to seed user and trip information."""

from sqlalchemy import func
from model import connect_to_db, db, User, Trip  # Import User and Trip models
from server import app
from random import choice
from sqlalchemy import text

def set_val_user_id():
    """Set value for the next user_id after seeding database."""
    with app.app_context():
        # Get the Max user_id in the database
        result = db.session.query(func.max(User.user_id)).one()

        max_id = int(result[0]) if result[0] is not None else 0

        # Set the value for the next user_id to be max_id + 1
        query = text("SELECT setval('users_user_id_seq', :new_id)")
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

def set_val_trip_id():
    """Set value for the next trip_id after seeding db."""
    with app.app_context():
        result = db.session.query(func.max(Trip.trip_id)).one()
        max_id = int(result[0]) if result[0] is not None else 0

        query = text("SELECT setval('trips_trip_id_seq', :new_id)")
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()
        
if __name__ == "__main__":
    with app.app_context():
        connect_to_db(app)

        # In case tables haven't been created, create them
        db.create_all()

        # Call functions to set values for user_id and trip_id sequences
        set_val_user_id()
        set_val_trip_id()
