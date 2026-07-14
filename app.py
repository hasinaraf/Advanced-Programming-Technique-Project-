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


# Issue table for storing issue and vulnerability records
class Issue(db.Model):
    # unique ID for each issue
    id = db.Column(db.Integer, primary_key=True)

    # issue title
    title = db.Column(db.String(150), nullable=False)

    # issue details
    description = db.Column(db.Text, nullable=False)

    # affected system or asset
    asset_name = db.Column(db.String(120), nullable=False)

    # type of issue
    issue_type = db.Column(db.String(50), nullable=False)

    # issue severity
    severity = db.Column(db.String(20), nullable=False)

    # issue progress status
    status = db.Column(db.String(30), nullable=False)

    # who reported the issue
    reported_by = db.Column(db.String(100), nullable=False)

    # who is assigned to fix it
    assigned_to = db.Column(db.String(100), nullable=False)

    # date the issue was created
    created_date = db.Column(db.String(20), nullable=False)

    # target fix date
    due_date = db.Column(db.String(20), nullable=False)

    # optional notes after fixing
    resolution_notes = db.Column(db.Text, nullable=True)

    # convert issue object into dictionary format for API response
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "asset_name": self.asset_name,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "status": self.status,
            "reported_by": self.reported_by,
            "assigned_to": self.assigned_to,
            "created_date": self.created_date,
            "due_date": self.due_date,
            "resolution_notes": self.resolution_notes or ""
        }


# home route to check if the website is running
@app.route("/")
def index():
    return "SecureFleet Issue Tracker is running"


# API health route to check backend status
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "system_name": "SecureFleet",
        "company": "Lidl Ireland",
        "message": "API is running"
    })


# create database tables if they exist in the code
with app.app_context():
    db.create_all()


# run Flask app
if __name__ == "__main__":
    app.run(debug=True)