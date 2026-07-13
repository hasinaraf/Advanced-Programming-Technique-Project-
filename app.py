# Flask app for the issue tracker

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# create Flask app
app = Flask(__name__)

# secret key is needed for Flask messages later
app.secret_key = "securefleet-development-key"

# enable CORS for API access
CORS(app)

# configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securefleet_nojs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create database object
db = SQLAlchemy(app)

# home route to check if the website is running
@app.route("/")
def index():
    return "SecureFleet Issue Tracker is running"


# API route to check backend status
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "system_name": "SecureFleet",
        "company": "GoCar Ireland",
        "message": "API is running"
    })

# create database tables if they exist in the code
with app.app_context():
    db.create_all()


# run Flask app
if __name__ == "__main__":
    app.run(debug=True)