# Flask app for the issue tracker

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# create Flask app
app = Flask(__name__)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

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