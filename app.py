# Flask app for the issue tracker

from datetime import date, datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
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


# check issue data before saving it
def validate_issue_data(data):
    # these fields must be filled by the user
    required_fields = [
        "title",
        "description",
        "asset_name",
        "issue_type",
        "severity",
        "status",
        "reported_by",
        "assigned_to",
        "due_date"
    ]

    # accepted issue type values
    allowed_issue_types = [
        "Bug",
        "Vulnerability",
        "Security Issue",
        "Configuration Issue"
    ]

    # accepted severity values
    allowed_severities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    # accepted status values
    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    # check if any required field is empty
    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return f"{field} is required"

    # check issue type
    if data["issue_type"] not in allowed_issue_types:
        return "Issue type must be Bug, Vulnerability, Security Issue, or Configuration Issue"

    # check severity
    if data["severity"] not in allowed_severities:
        return "Severity must be Low, Medium, High, or Critical"

    # check status
    if data["status"] not in allowed_statuses:
        return "Status must be Open, In Progress, Resolved, or Closed"

    # check due date format
    try:
        datetime.strptime(data["due_date"], "%Y-%m-%d")
    except ValueError:
        return "Due date must use YYYY-MM-DD format"

    # no validation error
    return None


# copy submitted data into the issue object
def apply_issue_data(issue, data):
    issue.title = data["title"].strip()
    issue.description = data["description"].strip()
    issue.asset_name = data["asset_name"].strip()
    issue.issue_type = data["issue_type"]
    issue.severity = data["severity"]
    issue.status = data["status"]
    issue.reported_by = data["reported_by"].strip()
    issue.assigned_to = data["assigned_to"].strip()
    issue.due_date = data["due_date"]
    issue.resolution_notes = data.get("resolution_notes", "").strip()


# homepage route
# gets all issues from database and sends them to index.html
@app.route("/")
def index():
    issues = Issue.query.order_by(Issue.id.asc()).all()
    return render_template("index.html", issues=issues)


# create issue from the HTML form
@app.route("/issues/create", methods=["POST"])
def web_create_issue():
    # get form data from browser
    data = request.form

    # check the form data before saving
    error = validate_issue_data(data)
    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    # create a new issue and set today's date
    issue = Issue(created_date=date.today().strftime("%Y-%m-%d"))

    # copy form values into the issue object
    apply_issue_data(issue, data)

    # save the new issue into the database
    db.session.add(issue)
    db.session.commit()

    flash("Issue created successfully", "success")
    return redirect(url_for("index"))


# open edit page for one selected issue
@app.route("/issues/<int:issue_id>/edit", methods=["GET"])
def web_edit_issue(issue_id):
    # find the issue using its ID
    issue = Issue.query.get(issue_id)

    # if the issue does not exist, go back to homepage
    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    # send the selected issue to edit.html
    return render_template("edit.html", issue=issue)


# update issue from the edit form
@app.route("/issues/<int:issue_id>/update", methods=["POST"])
def web_update_issue(issue_id):
    # find the existing issue using its ID
    issue = Issue.query.get(issue_id)

    # if issue ID is wrong, return to homepage
    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    # get updated form data from edit.html
    data = request.form

    # validate updated data before saving
    error = validate_issue_data(data)
    if error:
        flash(error, "error")
        return redirect(url_for("web_edit_issue", issue_id=issue_id))

    # copy updated values into the existing issue
    apply_issue_data(issue, data)

    # save updated issue in database
    db.session.commit()

    flash("Issue updated successfully", "success")
    return redirect(url_for("index"))


# delete issue from the issue list
@app.route("/issues/<int:issue_id>/delete", methods=["POST"])
def web_delete_issue(issue_id):
    # find the issue using its ID
    issue = Issue.query.get(issue_id)

    # if issue ID is wrong, return to homepage
    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    # delete the issue from database
    db.session.delete(issue)
    db.session.commit()

    flash("Issue deleted successfully", "success")
    return redirect(url_for("index"))


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