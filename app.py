from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "you need to install -- flask to run this app"

if __name__ == "__main__":
    app.run(debug=True)