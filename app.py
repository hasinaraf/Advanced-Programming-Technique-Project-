# Flask app for the issue tracker

from flask import Flask, jsonify

# create Flask app
app = Flask(__name__)


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


# run Flask app
if __name__ == "__main__":
    app.run(debug=True)