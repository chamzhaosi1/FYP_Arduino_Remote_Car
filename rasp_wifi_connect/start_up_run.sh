#!/bin/bash

# Change directory to the root directory of your Flask application
cd /home/engineer/romo_v2/romo_web/rasp_wifi_connect

# Activate the virtual environment
source /usr/local/bin/venv/bin/activate 

# Set the FLASK_APP environment variable to the name of your Flask application module
export FLASK_APP=app

# Run the Flask application with the development server
flask run --host=0.0.0.0 --port=5000
# flask run