

import os

from time import time
from flask import Flask

app = Flask(__name__)

READY_TIME = time() + 5  # Delay readiness by X seconds

ENV = {}

for key, value in os.environ.items():
    if key.startswith("KUBEDEMO_"):
        ENV[key] = value


@app.route("/app-1")
def root():
    return "Hello World! This is version 3 of the demo. Here are all environment variables that start with \"KUBEDEMO_\": {}.".format(ENV)


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
