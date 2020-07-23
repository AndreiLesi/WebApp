from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e850c5fe6a0cf3d65da4dcc8b652adc8'
db_uri = "postgresql://postgres:postgres123@db/tests_db"
# db_uri = "postgresql://postgres:postgres123@localhost/tests_db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("flask.config.Config")
db = SQLAlchemy(app)


class dbData(db.Model):
    """
    Defines the shape of the table in the database. It is used to query it
    """
    __tablename__ = "tests"

    request_id = db.Column(db.Integer, primary_key=True)
    requested_by = db.Column(db.String(20))
    created_at = db.Column(db.String())
    env_id = db.Column(db.Integer)
    test_path = db.Column(db.String(40))
    status = db.Column(db.String(20))
    details = db.Column(db.String())


# WARNING: routes import must be below app import to avoid circular importing !
# Should be under this comment!
from tester_webapp import routes
