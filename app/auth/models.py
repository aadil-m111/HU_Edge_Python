from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# we are creating a class 'USER', to define the schema for the user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # function to create a secure hash password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # check password, function to verify the password enterd for authorisation correct or not.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)