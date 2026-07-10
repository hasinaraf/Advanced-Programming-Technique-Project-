# SecureFleet Phase 1: Basic CRUD issue and vulnerability tracker

from datetime import date, datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "securefleet-development-key"
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securefleet_nojs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    asset_name = db.Column(db.String(120), nullable=False)
    issue_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    reported_by = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    resolution_notes = db.Column(db.Text, nullable=True)

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


def validate_issue_data(data):
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

    allowed_issue_types = [
        "Bug",
        "Vulnerability",
        "Security Issue",
        "Configuration Issue"
    ]

    allowed_severities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return f"{field} is required"

    if data["issue_type"] not in allowed_issue_types:
        return "Issue type must be Bug, Vulnerability, Security Issue, or Configuration Issue"

    if data["severity"] not in allowed_severities:
        return "Severity must be Low, Medium, High, or Critical"

    if data["status"] not in allowed_statuses:
        return "Status must be Open, In Progress, Resolved, or Closed"

    try:
        datetime.strptime(data["due_date"], "%Y-%m-%d")
    except ValueError:
        return "Due date must use YYYY-MM-DD format"

    return None


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


@app.route("/")
def index():
    issues = Issue.query.order_by(Issue.id.asc()).all()
    return render_template("index.html", issues=issues)


@app.route("/issues/create", methods=["POST"])
def web_create_issue():
    data = request.form

    error = validate_issue_data(data)
    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    issue = Issue(created_date=date.today().strftime("%Y-%m-%d"))
    apply_issue_data(issue, data)

    db.session.add(issue)
    db.session.commit()

    flash("Issue created successfully", "success")
    return redirect(url_for("index"))


@app.route("/issues/<int:issue_id>/edit", methods=["GET"])
def web_edit_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    return render_template("edit.html", issue=issue)


@app.route("/issues/<int:issue_id>/update", methods=["POST"])
def web_update_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    data = request.form

    error = validate_issue_data(data)
    if error:
        flash(error, "error")
        return redirect(url_for("web_edit_issue", issue_id=issue_id))

    apply_issue_data(issue, data)
    db.session.commit()

    flash("Issue updated successfully", "success")
    return redirect(url_for("index"))


@app.route("/issues/<int:issue_id>/delete", methods=["POST"])
def web_delete_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        flash("Issue not found", "error")
        return redirect(url_for("index"))

    db.session.delete(issue)
    db.session.commit()

    flash("Issue deleted successfully", "success")
    return redirect(url_for("index"))


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "system_name": "SecureFleet",
        "company": "GoCar Ireland",
        "message": "Basic CRUD API is running",
        "project_note": "Academic prototype using simulated data only"
    }), 200


@app.route("/api/issues", methods=["GET"])
def api_get_issues():
    issues = Issue.query.order_by(Issue.id.asc()).all()

    return jsonify({
        "issue_count": len(issues),
        "issues": [issue.to_dict() for issue in issues]
    }), 200


@app.route("/api/issues/<int:issue_id>", methods=["GET"])
def api_get_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        return jsonify({"error": "Issue not found"}), 404

    return jsonify(issue.to_dict()), 200


@app.route("/api/issues", methods=["POST"])
def api_create_issue():
    data = request.get_json(silent=True) or {}

    error = validate_issue_data(data)
    if error:
        return jsonify({"error": error}), 400

    issue = Issue(created_date=date.today().strftime("%Y-%m-%d"))
    apply_issue_data(issue, data)

    db.session.add(issue)
    db.session.commit()

    return jsonify({
        "message": "Issue created successfully",
        "issue": issue.to_dict()
    }), 201


@app.route("/api/issues/<int:issue_id>", methods=["PUT"])
def api_update_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        return jsonify({"error": "Issue not found"}), 404

    data = request.get_json(silent=True) or {}

    error = validate_issue_data(data)
    if error:
        return jsonify({"error": error}), 400

    apply_issue_data(issue, data)
    db.session.commit()

    return jsonify({
        "message": "Issue updated successfully",
        "issue": issue.to_dict()
    }), 200


@app.route("/api/issues/<int:issue_id>", methods=["DELETE"])
def api_delete_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if issue is None:
        return jsonify({"error": "Issue not found"}), 404

    db.session.delete(issue)
    db.session.commit()

    return jsonify({"message": "Issue deleted successfully"}), 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)