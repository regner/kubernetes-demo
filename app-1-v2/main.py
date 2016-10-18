

from time import time
from flask import Flask

app = Flask(__name__)

READY_TIME = time() + 5  # Delay readiness by X seconds


@app.route("/app-1")
def root():
    return "Hello World! This is version 2 of the demo."


@app.route("/liveness")
def liveness():
    return "OK"


@app.route("/readiness")
def readiness():
    if time() >= READY_TIME:
        return "OK"
    else:
        return "Not Ready", 503


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
