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
