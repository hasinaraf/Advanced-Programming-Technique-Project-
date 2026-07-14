# SecureLidl Issue and Vulnerability Tracking System

## Project Overview

SecureLidl is a basic issue and vulnerability tracking system developed for **Lidl Ireland** as part of the Advanced Programming Technique CA project.

The purpose of this system is to allow a company to record, view, update, and delete IT issues or security vulnerabilities. The project uses a Python Flask backend, an SQLite database, and a simple HTML/CSS frontend.

This is an academic prototype and uses simulated data only. It does not represent real Lidl Ireland systems, vulnerabilities, or internal information.

---

## Selected Company

The selected company for this project is:

**Lidl Ireland**

Lidl Ireland was selected because it is a large retail organisation that may depend on different digital systems such as customer applications, staff systems, inventory platforms, payment systems, and internal administration tools. These systems can be used as example assets in an issue and vulnerability tracking system.

---

## Project Aim

The aim of this project is to create a simple issue and vulnerability tracking system using an API-based backend written in Python.

The system allows users to:

- Add new issue or vulnerability records
- View saved records
- Edit existing records
- Delete records
- Access issue data through JSON API endpoints

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| Flask-SQLAlchemy | Database connection and ORM |
| Flask-CORS | API access support |
| SQLite | Local database |
| HTML | Frontend page structure |
| CSS | Frontend styling |
| Git and GitHub | Version control and project submission |

---

## Project Structure

```text
Advanced Programming Technique Project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── edit.html
│
└── static/
    └── style.css