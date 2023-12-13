
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):  # pragma: no cover

    __tablename__ = "users"

    # Log-in information
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(649), nullable=True)

    # Profile information
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    user_gender = db.Column(db.String(20), nullable=True)
    user_bio = db.Column(db.String(160), nullable=True)
    user_profile_img = db.Column(db.String(250), nullable=True)
    user_social_media = db.Column(db.String(3000), nullable=True)
    phone_number = db.Column(db.Numeric(12), nullable=True)

    def to_json(self):  # pragma: no cover
        """Serialize data."""
        return {'user_id': self.user_id,
                'email': self.email,
                'password': self.password,
                'fname': self.fname,
                'lname': self.lname,
                'userGender': self.user_gender,
                'userBio': self.user_bio,
                'userProfileImg': self.user_profile_img,
                'userSocialMedia': self.user_social_media}
