import flask
import requests
from flask import Flask
from flask import request
from werkzeug.exceptions import HTTPException
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "status": "failed",
    })
    response.content_type = "application/json"
    return response


@app.route("/")
def api_routes():
    """get Covid API routes"""
    response = requests.get("https://api.covid19api.com/")
    return response.json()



@app.route("/status")
def health_check():
    """Return a success status only if the HTTP request is valid"""
    requests.get("https://api.covid19api.com/")
    return {"status": "success"}


@app.route("/summary")
def summary_cases():
    """summary of new and total cases per country updated daily"""
    response = requests.get("https://api.covid19api.com/summary")
    return response.json()


@app.route("/death_peaks_by_month")
def death_peaks():
    """get the death peak in a country in the last 30 days"""
    country = request.args.get("country")
    today = datetime.today()
    d = today - relativedelta(months=1)
    str_d = d.strftime('%Y-%m-%d %I:%M:%S')
    str_today = today.strftime('%Y-%m-%d %I:%M:%S')
    response = requests.get(f"https://api.covid19api.com/country/{country}/status/deaths?from={str_d}&to={str_today}")
    max_cases = max(response.json(), key=lambda x: x['Cases'])
    return {"max_cases": max_cases.get("Cases"), "date": max_cases.get("Date")}


if __name__ == '__main__':
    app.run(port=8080)
