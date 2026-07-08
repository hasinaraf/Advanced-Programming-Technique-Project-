from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "system_name": "SecureFleet",
        "company": "GoCar Ireland",
        "message": "Issue and Vulnerability Tracking API is running",
        "project_note": "This is an academic prototype using simulated data only."
    })


if __name__ == "__main__":
    app.run(debug=True)