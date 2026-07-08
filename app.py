from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# SQLite database configuration for the SecureFleet API
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securefleet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(120), nullable=False)
    asset_type = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    criticality = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "department": self.department,
            "criticality": self.criticality
        }


@app.route("/")
def home():
    return jsonify({
        "system_name": "SecureFleet",
        "company": "GoCar Ireland",
        "message": "Issue and Vulnerability Tracking API is running",
        "project_note": "This is an academic prototype using simulated data only.",
        "database": "SQLite database configured successfully",
        "api_version": "1.0"
    })


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)