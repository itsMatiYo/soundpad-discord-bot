from flask import Flask

app = Flask(__name__)
"""Added flask so the app does not get into idle mode in heroku."""


@app.route("/")
def index():
    return "Hello Chad!"


if __name__ == "__main__":
    app.run()
