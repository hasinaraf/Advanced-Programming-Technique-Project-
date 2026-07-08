from flask import Flask, jsonify, request
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


@app.route("/api/assets", methods=["POST"])
def create_asset():
    data = request.get_json()

    asset = Asset(
        asset_name=data["asset_name"],
        asset_type=data["asset_type"],
        department=data["department"],
        criticality=data["criticality"]
    )

    db.session.add(asset)
    db.session.commit()

    return jsonify({
        "message": "Asset created successfully",
        "asset": asset.to_dict()
    }), 201


@app.route("/api/assets", methods=["GET"])
def get_assets():
    assets = Asset.query.all()

    return jsonify({
        "asset_count": len(assets),
        "assets": [asset.to_dict() for asset in assets]
    }), 200


@app.route("/api/assets/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    asset = Asset.query.get(asset_id)

    if asset is None:
        return jsonify({"error": "Asset not found"}), 404

    return jsonify(asset.to_dict()), 200


@app.route("/api/assets/<int:asset_id>", methods=["PUT"])
def update_asset(asset_id):
    asset = Asset.query.get(asset_id)

    if asset is None:
        return jsonify({"error": "Asset not found"}), 404

    data = request.get_json()

    asset.asset_name = data["asset_name"]
    asset.asset_type = data["asset_type"]
    asset.department = data["department"]
    asset.criticality = data["criticality"]

    db.session.commit()

    return jsonify({
        "message": "Asset updated successfully",
        "asset": asset.to_dict()
    }), 200


@app.route("/api/assets/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)

    if asset is None:
        return jsonify({"error": "Asset not found"}), 404

    db.session.delete(asset)
    db.session.commit()

    return jsonify({
        "message": "Asset deleted successfully"
    }), 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)