

import os

from time import time
from flask import Flask

app = Flask(__name__)

READY_TIME = time() + 5  # Delay readiness by X seconds


def get_env_vars():
    env_vars = {}

    for key, value in os.environ.items():
        if key.startswith("KUBEDEMO_"):
            env_vars[key] = value

    return env_vars


@app.route("/app-4")
def root():
    env_vars = get_env_vars()
    return "Hello World! This is version 1 of the env listing demo. Here are all environment variables that start with \"KUBEDEMO_\": {}.".format(env_vars)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
